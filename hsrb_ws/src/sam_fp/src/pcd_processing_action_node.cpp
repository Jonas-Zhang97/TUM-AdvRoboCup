#include "pcd_processing/pcd_processing.h"

int main(int argc, char **argv) {
    ros::init(argc, argv, "pcd_processing_action_node");
    ros::NodeHandle nh;

    pcd_processing pcd_processing_obj;
    if (!pcd_processing_obj.initialize(nh)) {
        ROS_ERROR("Failed to initialize the pcd_processing object!");
        return -1;
    }

    ros::Rate loop_rate(30);
    while (ros::ok()) {
        pcd_processing_obj.update(ros::Time::now());
        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}
