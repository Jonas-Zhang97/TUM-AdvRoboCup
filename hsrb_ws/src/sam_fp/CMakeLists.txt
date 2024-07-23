cmake_minimum_required(VERSION 3.0.2)
project(sam_fp)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
  pcl_ros
  pcl_conversions
  actionlib
  actionlib_msgs
  project_msgs
  masks_msgs
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs sensor_msgs geometry_msgs pcl_ros pcl_conversions actionlib actionlib_msgs project_msgs masks_msgs
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(pcd_processing_node src/pcd_processing_node.cpp src/pcd_processing.cpp)
target_link_libraries(pcd_processing_node ${catkin_LIBRARIES})
add_dependencies(pcd_processing_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

add_executable(pcd_processing_action_node src/pcd_processing_action_node.cpp src/pcd_processing.cpp)
target_link_libraries(pcd_processing_action_node ${catkin_LIBRARIES})
add_dependencies(pcd_processing_action_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
