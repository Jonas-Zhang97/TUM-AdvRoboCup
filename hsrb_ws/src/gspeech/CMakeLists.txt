cmake_minimum_required(VERSION 3.0.2)
project(gspeech)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

# You can add any executables or libraries here using the add_executable() and add_library() commands.
# For example:
# add_executable(your_executable src/your_source_file.cpp)
# target_link_libraries(your_executable ${catkin_LIBRARIES})
catkin_install_python(PROGRAMS src/gspeech.py
DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS src/gspeech_new.py
DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)