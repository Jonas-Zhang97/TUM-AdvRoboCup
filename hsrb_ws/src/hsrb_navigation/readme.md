###Navigation
sudo apt-get install ros-noetic-dwa-local-planner


$ hsrb_mode
$ rosnode kill /pose_integrator

$ rviz -d $(rospack find hsrb_rosnav_config)/launch/hsrb.rviz

rosrun rviz rviz  -d `rospack find hsrb_common_launch`/config/hsrb_display_full_hsrb.rviz

$ roslaunch hsrb_navigation hsrb_nav_ics.launch map_file:=/workspaces/adv_robocup/hsrb_ws/src/hsrb_navigation/map/map.yaml

rosrun tf tf_echo /map /base_link
可以使用 tf_echo 命令直接查看机器人在 /map 坐标系下的位置和姿态
##  Initialization of odometry
roslaunch hsrb_navigation amcl.launch
rosservice call /amcl/global_localization "{}"
rosservice list | grep /amcl
rosrun rqt_reconfigure rqt_reconfigure
sudo apt-get install ros-noetic-laser-scan-matcher



$ roslaunch hsrb_navigation hsrb_nav_ics.launch map_file:=/workspaces/cup/hsrb_ws/src/hsrb_navigation/map/map.yaml

$ rviz -d $(rospack find hsrb_navigation)/rviz/mapping.rviz



rosrun hsrb_navigation send_goal_message_yaml.py
rosrun hsrb_navigation send_goal_action_yaml.py
$ roslaunch hsrb_navigation send_goal.launch


$ rostopic echo move_base_simple/goal
###################################################################################
sudo apt-get install ros-noetic-moveit

sudo apt-get install ros-noetic-gmapping ros-noetic-map-server ros-noetic-amcl ros-noetic-move-base


chmod +x 
##Navigation

roslaunch hsrb_bringup minimal.launch ##不用开启，是不是自动开启了

roslaunch hsrb_navigation slam_gmapping.launch
rosrun rviz rviz

### 一键建图

roslaunch hsrb_navigation mapping.launch

rosrun map_server map_saver -f ~/map


roslaunch hsrb_navigation mapping_with_rviz.launch


##诊断

SLAM节点依赖于激光雷达数据。如果没有正确的激光雷达数据输入，SLAM节点不会生成地图。


rosrun tf view_frames
evince frames.pdf

roswtf

你的问题可能是由于机器人在移动过程中没有足够的环境信息或者激光雷达数据无法有效覆盖整个地图，导致地图更新停滞



