cmake_minimum_required(VERSION 3.0.2)
project(sam_fp)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
  sensor_msgs
  actionlib_msgs
  project_msgs
  masks_msgs
  tf
  actionlib
)

find_package(OpenCV REQUIRED)
find_package(PCL 1.7 REQUIRED)  # 添加 PCL 依赖

catkin_package(
  CATKIN_DEPENDS 
    geometry_msgs 
    roscpp
    rospy 
    std_msgs 
    message_runtime
    project_msgs
    masks_msgs
    tf
    actionlib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  ${PCL_INCLUDE_DIRS}  # 添加 PCL 包含目录
  ${CMAKE_CURRENT_SOURCE_DIR}/include
)

link_directories(${PCL_LIBRARY_DIRS})  # 添加 PCL 库目录
add_definitions(${PCL_DEFINITIONS})

add_executable(pcd_processing_node src/pcd_processing_node.cpp src/pcd_processing.cpp)
add_executable(pcd_processing_action_node src/pcd_processing_action_node.cpp src/pcd_processing.cpp)

target_link_libraries(pcd_processing_node
  ${catkin_LIBRARIES}
  ${OpenCV_LIBRARIES}
  ${PCL_LIBRARIES}  # 链接 PCL 库

)

target_link_libraries(pcd_processing_action_node
  ${catkin_LIBRARIES}
  ${OpenCV_LIBRARIES}
  ${PCL_LIBRARIES}  # 链接 PCL 库

)
