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

需要的.json 和 .png 都在hsrb_ws/src/task_planner/scripts 

## Prepare
pip install spacy
python3 -m spacy download en_core_web_sm


## Debug
export XDG_RUNTIME_DIR=/tmp/runtime-$USER
mkdir -p $XDG_RUNTIME_DIR
chmod 0700 $XDG_RUNTIME_DIR

## tts
pip install gtts
sudo apt-get install ros-noetic-tmc-msgs

sudo apt-get install mpg321

rosrun gtts_tts gtts_tts_rosrun.py _sentence:="This is a test sentence" _language:="en"

