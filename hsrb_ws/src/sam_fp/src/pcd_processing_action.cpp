#include "pcd_processing/pcd_processing.h"

void pcd_processing::executeCB(const project_msgs::CalculateCentroidGoalConstPtr &goal) {
    // Start calculating centroid
    geometry_msgs::Point centroid = calculateCentroidAction(goal->point_cloud);

    // Publish feedback
    project_msgs::CalculateCentroidFeedback feedback;
    feedback.current_estimate = centroid;
    as_->publishFeedback(feedback);

    // Publish result
    project_msgs::CalculateCentroidResult result;
    result.centroid = centroid;
    as_->setSucceeded(result);
}

// Method to calculate centroid
geometry_msgs::Point pcd_processing::calculateCentroidAction(const sensor_msgs::PointCloud2 &point_cloud) {
    cloudPtr cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    pcl::fromROSMsg(point_cloud, *cloud);

    geometry_msgs::Point centroid;

    if (cloud->points.empty()) {
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
        return centroid;
    }
}
