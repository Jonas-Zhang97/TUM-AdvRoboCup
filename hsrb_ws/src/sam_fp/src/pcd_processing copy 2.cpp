#include "pcd_processing/pcd_processing.h"



// Constructor for base class
// pcd_processing_base::pcd_processing_base(const std::string &topic, const std::string &frame)
//     : pointcloud_topic(topic), base_frame(frame), is_cloud_updated(false), centroid_published_(false) {
// }

// Initialize method for base class
bool pcd_processing_base::initialize(ros::NodeHandle &nh) {
    point_cloud_sub_ = nh.subscribe(pointcloud_topic, 1, &pcd_processing_base::cloudCallback, this);
    masks_sub_ = nh.subscribe("/sam_mask", 1, &pcd_processing_base::masksCallback, this);
    objects_cloud_pub_ = nh.advertise<sensor_msgs::PointCloud2>("/objects_cloud", 1);
    object_centers_pub_ = nh.advertise<project_msgs::LabeledCentroid>("/labeled_objects", 1);

    raw_cloud_.reset(new pcl::PointCloud<pcl::PointXYZRGB>);
    preprocessed_cloud_.reset(new pcl::PointCloud<pcl::PointXYZRGB>);
    objects_cloud_.reset(new pcl::PointCloud<pcl::PointXYZRGB>);
    latest_maskID_msg_.reset(new masks_msgs::maskID);

    centroid_published_ = false;
    return true;
}

// Update method for base class
void pcd_processing_base::update(const ros::Time &time) {
    if (is_cloud_updated && !centroid_published_) {// && !centroid_published_
        if (!raw_cloud_preprocessing(raw_cloud_, preprocessed_cloud_)) {
            ROS_ERROR("Raw cloud preprocessing failed!");
            return;
        }

        if (!cut_point_cloud(preprocessed_cloud_, processed_masks_, objects_cloud_)) {
            ROS_ERROR("Cutting point cloud failed!");
            return;
        };

        pcl::toROSMsg(*objects_cloud_, cloudmsg_);
        objects_cloud_pub_.publish(cloudmsg_);

        project_msgs::LabeledCentroid centroid = calculateCentroid(objects_cloud_, cloudmsg_.header);
        object_centers_pub_.publish(centroid);

        centroid_published_ = true;
        is_cloud_updated = false;
    }
}

bool pcd_processing_base::raw_cloud_preprocessing(CloudPtr &input, CloudPtr &output) {
    // Modify if further preprocessing needed
    // Note: Since the point cloud segmentation is pixel-wise, preprocessing may cause lack of points.
    *output = *input;
    return true;
}

bool pcd_processing_base::cut_point_cloud(CloudPtr &input, const std::vector<singlemask> &masks, CloudPtr &objects) {
    // Implement the logic to cut the point cloud using masks
    *objects = *input;
    objects->points.clear();

    for (const auto& mask : masks) {
        int min_x = mask.bbox[0];
        int min_y = mask.bbox[1];
        int width = mask.bbox[2];
        int height = mask.bbox[3];

        for (int i = min_y; i < min_y + height; ++i) {
            for (int j = min_x; j < min_x + width; ++j) {
                if (mask.segmentation(i, j) == 1) {
                    int index = i * input->width + j;
                    if (index < input->points.size()) {
                        objects->points.push_back(input->points[index]);
                    }
                }
            }
        }
    }
    objects->width = objects->points.size();
    objects->height = 1;
    objects->is_dense = false;
    return true;
}

void pcd_processing_base::cloudCallback(const sensor_msgs::PointCloud2ConstPtr &msg) {
    is_cloud_updated = true;
    pcl::fromROSMsg(*msg, *raw_cloud_);
}

void pcd_processing_base::masksCallback(const masks_msgs::maskID::Ptr &msg) {
    processed_masks_ = maskID_msg_processing(msg);
}

project_msgs::LabeledCentroid pcd_processing_base::calculateCentroid(const CloudPtr &cloud, const std_msgs::Header &header) {
    geometry_msgs::PointStamped centroid;
    project_msgs::LabeledCentroid labeled_centroid;
    centroid.header = header;

    if (cloud->points.empty()) {
        labeled_centroid.pose.pose.position = centroid.point;
        labeled_centroid.label = 0;
        return labeled_centroid;
    }

    Eigen::Vector4f centroid_eigen;
    pcl::compute3DCentroid(*cloud, centroid_eigen);

    centroid.point.x = centroid_eigen[0];
    centroid.point.y = centroid_eigen[1];
    centroid.point.z = centroid_eigen[2];

    std::string target_frame = "odom";
    try {
        geometry_msgs::PointStamped transformed_centroid;
        tf_listener_.waitForTransform(target_frame, centroid.header.frame_id, ros::Time(0), ros::Duration(3.0));
        tf_listener_.transformPoint(target_frame, centroid, transformed_centroid);

        labeled_centroid.pose.pose.position = transformed_centroid.point;
        labeled_centroid.label = 1;
        return labeled_centroid;
    } catch (tf::TransformException &ex) {
        ROS_WARN("Failed to transform centroid: %s", ex.what());
        labeled_centroid.pose.pose.position = centroid.point;
        labeled_centroid.label = 0;
        return labeled_centroid;
    }
}

int pcd_processing_base::countOnes(const Eigen::Matrix<int64_t, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> &matrix) {
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

std::vector<pcd_processing_base::singlemask> pcd_processing_base::maskID_msg_processing(const masks_msgs::maskID::Ptr& maskID) {
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

    auto compareArea = [](const singlemask& a, const singlemask& b) {
        return a.area < b.area;
    };
    std::sort(masks.begin(), masks.end(), compareArea);
    if (masks.size() > 5) {
        masks.erase(masks.end() - 5, masks.end());
    }
    return masks;
}

// Derived class implementation
pcd_processing::pcd_processing(const std::string &topic, const std::string &frame)
    : pcd_processing_base(topic, frame), action_name_("calculate_centroid") {
}

bool pcd_processing::initialize(ros::NodeHandle &nh) {
    if (!pcd_processing_base::initialize(nh)) {
        return false;
    }
    as_ = std::make_shared<CentroidActionServer>(nh, action_name_, boost::bind(&pcd_processing::executeCB, this, _1), false);
    as_->start();
    return true;
}

void pcd_processing::executeCB(const project_msgs::CalculateCentroidGoalConstPtr &goal) {
    geometry_msgs::Point centroid = calculateCentroidAction(goal->point_cloud);

    project_msgs::CalculateCentroidFeedback feedback;
    feedback.current_estimate = centroid;
    as_->publishFeedback(feedback);

    project_msgs::CalculateCentroidResult result;
    result.centroid = centroid;
    as_->setSucceeded(result);
}

geometry_msgs::Point pcd_processing::calculateCentroidAction(const sensor_msgs::PointCloud2 &point_cloud) {
    CloudPtr cloud(new Cloud);
    pcl::fromROSMsg(point_cloud, *cloud);

    geometry_msgs::Point centroid;

    if (cloud->points.empty()) {
        ROS_WARN("The point cloud is empty, cannot calculate centroid.");
        return centroid;
    }

    Eigen::Vector4f centroid_eigen;
    pcl::compute3DCentroid(*cloud, centroid_eigen);

    centroid.x = centroid_eigen[0];
    centroid.y = centroid_eigen[1];
    centroid.z = centroid_eigen[2];

    std::string target_frame = "odom";
    try {
        geometry_msgs::PointStamped centroid_stamped;
        centroid_stamped.header = point_cloud.header;
        centroid_stamped.point = centroid;

        geometry_msgs::PointStamped transformed_centroid_stamped;
        tf_listener_.waitForTransform(target_frame, centroid_stamped.header.frame_id, ros::Time(0), ros::Duration(3.0));
        tf_listener_.transformPoint(target_frame, centroid_stamped, transformed_centroid_stamped);

        centroid = transformed_centroid_stamped.point;
        return centroid;
    } catch (tf::TransformException &ex) {
        ROS_WARN("Failed to transform centroid: %s", ex.what());
        return centroid;  // Return the untransformed centroid
    }
}
