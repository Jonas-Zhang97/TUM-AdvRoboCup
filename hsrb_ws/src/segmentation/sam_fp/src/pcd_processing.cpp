#include "pcd_processing/pcd_processing.h" 


// Initialize method
bool pcd_processing::initialize(ros::NodeHandle &nh) {
    // ROS_INFO_STREAM(pcd_processing::pointcloud_topic);

    // Initialize ROS subscribers, publishers, and other members
    point_cloud_sub_ = nh.subscribe(pointcloud_topic, 1, &pcd_processing::cloudCallback, this);
    masks_sub_ = nh.subscribe("/sam_mask", 1, &pcd_processing::masksCallback, this);
    objects_cloud_pub_ = nh.advertise<sensor_msgs::PointCloud2>("/objects_cloud", 1);

    object_centers_pub_ = nh.advertise<geometry_msgs::PointStamped>("/object_centers", 1);

    // Initialize pointers
    raw_cloud_.reset(new cloud);
    preprocessed_cloud_.reset(new cloud);
    objects_cloud_.reset(new cloud);
    latest_maskID_msg_.reset(new masks_msgs::maskID);
    return true; // Return true if initialization is successful
}

// Update method
void pcd_processing::update(const ros::Time &time) {
    // Update the pcd_processing object

    if (is_cloud_updated) {
        // Preprocess the raw cloud
        if(!raw_cloud_preprocessing(raw_cloud_, preprocessed_cloud_)) {
            ROS_ERROR("Raw cloud preprocessing failed!");
            return;
        }

        // Cut the preprocessed cloud //TODO: pass the argument
        if(!cut_point_cloud(preprocessed_cloud_, processed_masks_, objects_cloud_)){
            ROS_ERROR("Cutting point cloud failed!");
            return;
        };

        // Publish the objects cloud
        pcl::toROSMsg(*objects_cloud_, cloudmsg_);
        ROS_INFO_STREAM("raw_cloud_:");
        ROS_INFO_STREAM(*raw_cloud_);
        ROS_INFO_STREAM("objects_cloud_:");
        ROS_INFO_STREAM(*objects_cloud_);
        objects_cloud_pub_.publish(cloudmsg_);

        // Calculate and publish the centroid of the objects cloud
        geometry_msgs::PointStamped centroid = calculateCentroid(objects_cloud_, cloudmsg_.header);
        object_centers_pub_.publish(centroid);

        // Reset the flag
        is_cloud_updated = false;
    }
}

// Calculate centroid method
geometry_msgs::PointStamped pcd_processing::calculateCentroid(const cloudPtr &cloud, const std_msgs::Header &header) {
    geometry_msgs::PointStamped centroid;
    centroid.header = header;

    if (cloud->points.empty()) {
        ROS_WARN("The point cloud is empty, cannot calculate centroid.");
        return centroid;
    }

    Eigen::Vector4f centroid_eigen;
    pcl::compute3DCentroid(*cloud, centroid_eigen);

    centroid.point.x = centroid_eigen[0];
    centroid.point.y = centroid_eigen[1];
    centroid.point.z = centroid_eigen[2];

    // 转换质心到目标坐标框架
    std::string target_frame = "odom"; // 目标坐标框架，例如机器人底座坐标框架
    try {
        geometry_msgs::PointStamped transformed_centroid;
        tf_listener_.waitForTransform(target_frame, centroid.header.frame_id, ros::Time(0), ros::Duration(3.0));
        tf_listener_.transformPoint(target_frame, centroid, transformed_centroid);
        return transformed_centroid;
    } catch (tf::TransformException &ex) {
        ROS_WARN("Failed to transform centroid: %s", ex.what());
        return centroid; // 返回未转换的质心
    }
    // return centroid;
}

// Raw cloud preprocessing
bool pcd_processing::raw_cloud_preprocessing(cloudPtr &input, cloudPtr &output) {

    // Modify if further preprocessing needed
    // Note: Since the point cloud segmentation is pixel-wise, preprocessing may cause lack of points.

    *output = *input;




    return true; // Return true on success
}

// Cut point cloud
bool pcd_processing::cut_point_cloud(cloudPtr &input, const std::vector<singlemask> &masks, cloudPtr &objects) {
    // Implement the logic to cut the point cloud using masks
    // Point Cloud frame_id: xtion_rgb_optical_frame
    // image_raw frame_id: xtion_rgb_optical_frame
    // masks frame_id: xtion_rgb_optical_frame

    // Clear the output cloud
    *objects = *input;
    objects->points.clear();

    // Iterate over each mask
    for (const auto& mask : masks) {

        // Find the bounding box of the mask
        int min_x = mask.bbox[0];
        int min_y = mask.bbox[1];
        int width = mask.bbox[2];
        int height = mask.bbox[3];

        int number_of_ones = pcd_processing::countOnes(mask.segmentation);
        ROS_INFO_STREAM("number_of_ones:");
        ROS_INFO_STREAM(number_of_ones);

        // Iterate over the points in the bounding box
        for (int i = min_y; i < min_y + height; ++i) {
            for (int j = min_x; j < min_x + width; ++j) {
                // Check if the mask includes this point
                if (mask.segmentation(i, j) == 1) {
                    // Calculate the index in the point cloud
                    int index = i * input->width + j;
                    if (index < input->points.size()) {
                        // Add the point to the output cloud
                        objects->points.push_back(input->points[index]);
                    }
                }
            }
        }
    }
    objects->width = objects->points.size();
    objects->height = 1;  // Setting height to 1 implies the cloud is unorganized
    objects->is_dense = false;  // Set to false if there might be NaN or invalid points

    return true;
}


// Cloud callback
void pcd_processing::cloudCallback(const sensor_msgs::PointCloud2ConstPtr &msg) {

    is_cloud_updated = true;

    pcl::fromROSMsg(*msg, *raw_cloud_);

}

// Masks callback
void pcd_processing::masksCallback(const masks_msgs::maskID::Ptr &msg) {
    // process new recieved masks
    processed_masks_ = maskID_msg_processing(msg);

}


std::vector<pcd_processing::singlemask> pcd_processing::maskID_msg_processing(const masks_msgs::maskID::Ptr& maskID) {
    ROS_INFO("mask_msg_preprocessing is triggered.");

    std::vector<singlemask> masks;
    for (const auto& singlemask_msg : maskID->maskID) {
        singlemask mask;
        mask.segmentation = Eigen::Map<const Eigen::Matrix<int64_t, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>>(
            singlemask_msg.segmentation.data(), 
            singlemask_msg.shape[0], 
            singlemask_msg.shape[1]);
        mask.area = singlemask_msg.area;
        mask.bbox = singlemask_msg.bbox;
        mask.predicted_iou = singlemask_msg.predicted_iou;
        mask.point_coords = Eigen::Map<const Eigen::Matrix<float, Eigen::Dynamic, 2, Eigen::RowMajor>>(
            singlemask_msg.point_coords.data(), 
            singlemask_msg.point_coords.size() / 2, 
            2);
        mask.stability_score = singlemask_msg.stability_score;
        mask.crop_box = singlemask_msg.crop_box;

        masks.push_back(mask);



    }

    ROS_INFO_STREAM("length of masks before erase:");
    ROS_INFO_STREAM(masks.size());

    // Sort the masks by area
    auto compareArea = [](const singlemask& a, const singlemask& b) {
        return a.area < b.area;
    };
    std::sort(masks.begin(), masks.end(), compareArea);
    // Erase the masks with the largest area (the background mask)
    if(masks.size() > 5) {
        masks.erase(masks.end() - 5, masks.end());
    }

    return masks;

}

int pcd_processing::countOnes(const Eigen::Matrix<int64_t, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> &matrix) {
    int count = 0;
    for (int i = 0; i < matrix.rows(); i++) {
        for (int j = 0; j < matrix.cols(); j++) {
            if (matrix(i, j) == 1) {
                count++;
            }
        }
    }
    return count;
}


