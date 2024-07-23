cmake_minimum_required(VERSION 3.0.2)
project(project_msgs)

find_package(catkin REQUIRED COMPONENTS
  actionlib_msgs
  geometry_msgs
  message_generation
  roscpp
  rospy
  sensor_msgs
  std_msgs
)

## Add message files
add_message_files(
  FILES
  LabeledCentroid.msg
  CollisionGeometry.msg
)

## Add action files
add_action_files(
  DIRECTORY action
  FILES
  CalculateCentroid.action
)

## Generate messages and services
generate_messages(
  DEPENDENCIES
  actionlib_msgs
  geometry_msgs
  sensor_msgs
  std_msgs
)

## Declare catkin package
catkin_package(
  CATKIN_DEPENDS
  actionlib_msgs
  geometry_msgs
  message_runtime
  roscpp
  rospy
  sensor_msgs
  std_msgs
)

## Include directories
include_directories(
  ${catkin_INCLUDE_DIRS}
)
