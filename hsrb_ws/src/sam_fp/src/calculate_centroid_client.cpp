#include <ros/ros.h>
#include <actionlib/client/simple_action_client.h>
#include <project_msgs/CalculateCentroidAction.h>
#include <sensor_msgs/PointCloud2.h>
#include <sensor_msgs/point_cloud2_iterator.h> 

int main(int argc, char **argv) {
  ros::init(argc, argv, "calculate_centroid_client");

  // 创建一个动作客户端，"calculate_centroid"是动作名
  actionlib::SimpleActionClient<project_msgs::CalculateCentroidAction> ac("calculate_centroid", true);

  ROS_INFO("Waiting for action server to start...");
  ac.waitForServer();  // 等待动作服务器启动

  ROS_INFO("Action server started, sending goal.");
  project_msgs::CalculateCentroidGoal goal;
  
  // 填充目标点云数据
  sensor_msgs::PointCloud2 point_cloud;
  point_cloud.header.frame_id = "base_link";
  point_cloud.height = 1;
  point_cloud.width = 5;
  point_cloud.is_dense = true;

  // 示例点云数据
  for (int i = 0; i < 5; ++i) {
    sensor_msgs::PointCloud2Modifier pcd_modifier(point_cloud);
    pcd_modifier.setPointCloud2FieldsByString(2, "xyz", "rgb");
    point_cloud.data.resize(point_cloud.row_step * point_cloud.height);
    sensor_msgs::PointCloud2Iterator<float> iter_x(point_cloud, "x");
    sensor_msgs::PointCloud2Iterator<float> iter_y(point_cloud, "y");
    sensor_msgs::PointCloud2Iterator<float> iter_z(point_cloud, "z");
    for (size_t i = 0; i < point_cloud.width; ++i) {
      *iter_x = i;
      *iter_y = i * 0.1;
      *iter_z = i * 0.01;
      ++iter_x; ++iter_y; ++iter_z;
    }
  }

  goal.point_cloud = point_cloud;
  ac.sendGoal(goal);  // 发送目标

  bool finished_before_timeout = ac.waitForResult(ros::Duration(30.0));

  if (finished_before_timeout) {
    actionlib::SimpleClientGoalState state = ac.getState();
    ROS_INFO("Action finished: %s", state.toString().c_str());
    project_msgs::CalculateCentroidResultConstPtr result = ac.getResult();
    ROS_INFO("Centroid: [x: %f, y: %f, z: %f]", result->centroid.x, result->centroid.y, result->centroid.z);
  } else {
    ROS_INFO("Action did not finish before the time out.");
  }

  return 0;
}
