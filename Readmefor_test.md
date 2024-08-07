开机，先开机器人的红钮，然后是释放遥控器的红钮，然后会从黄色变成蓝色。如果有问题那么就直接都按，然后先开机器人的红钮，然后是释放遥控器的红钮。




### Navigation
sudo apt-get install ros-noetic-dwa-local-planner

Terminal #1
$ hsrb_mode
$ rosnode kill /pose_integrator（这步只要按过按钮后就必须重运行）

and open launch file
$ roslaunch hsrb_navigation hsrb_nav_ics.launch map_file:=/workspaces/cup/hsrb_ws/src/hsrb_navigation/map/map.yaml
（这两个指令永远不用关）
（每次launch 只需要一次2D Pose Estimate）
需要任意移动,可以在调好launch后 直接使用2D Nav Goal

Terminal #2
$ hsrb_mode
$ rviz -d $(rospack find hsrb_navigation)/rviz/mapping.rviz
（这两个指令永远不用关）

Terminal #3 
$ hsrb_mode
$ roslaunch hsrb_navigation send_goal.launch room_name:=goal1
（这个指令已经通过sm，调用，除非需要单独调试）

### Reference
## rqt
$ rqt
Next, choose Robot Tools > Robot Steering from Plugins found in the rqt menubar.
Set the movement velocity topic /hsrb/command_velocity into the text box.


### Task_planner

已经封装成roslaunch文件, is_first_time 默认是True
这在个launch 可以直接在sm中被调用

$ roslaunch task_planner task_planner.launch instruction:="grab the bottle at A and move to B and move to D and move to C and release the bottle at C" is_first_time:=True
$ roslaunch task_planner task_planner.launch instruction:="grab a bottle at storage and move to me and release the bottle"

## Prepare
pip install spacy
python3 -m spacy download en_core_web_sm


## Debug
export XDG_RUNTIME_DIR=/tmp/runtime-$USER
mkdir -p $XDG_RUNTIME_DIR
chmod 0700 $XDG_RUNTIME_DIR



 










$ hsrb_mode
$ rosnode kill /pose_integrator

$ rviz -d $(rospack find hsrb_rosnav_config)/launch/hsrb.rviz

rosrun rviz rviz  -d `rospack find hsrb_common_launch`/config/hsrb_display_full_hsrb.rviz

$ roslaunch hsrb_navigation hsrb_nav_ics.launch map_file:=/workspaces/adv_robocup/hsrb_ws/src/hsrb_navigation/map/map.yaml
roslaunch hsrb_navigation hsrb_nav_ics.launch map_file:=/home/athome24-3/cup/hsrb_ws/src/hsrb_navigation/map/map.yaml

可以使用 tf_echo 命令直接查看机器人在 /map 坐标系下的位置和姿态
rosrun tf tf_echo /map /base_link


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


###############################################################
Map creation

Terminal #1
$ hsrb_mode
$ rosnode kill /pose_integrator
$ rviz -d $(rospack find hsrb_rosnav_config)/launch/hsrb.rviz


Terminal #2
$ hsrb_mode
$ roslaunch hsrb_mapping hector.launch

Terminal #3
$ rqt
Next, choose Robot Tools > Robot Steering from Plugins found in the rqt menubar.

Terminal #4
Saving a map
$ rosrun map_server map_saver

