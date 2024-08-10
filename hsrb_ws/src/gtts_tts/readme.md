pip install gtts
sudo apt-get install ros-<ros_distro>-tmc-msgs
sudo apt-get install ros-noetic-tmc-msgs
sudo apt-get install mpg321

rosrun gtts_tts gtts_tts_node.py

rostopic pub /talk_request tmc_msgs/Voice "interrupting: false
queueing: false
language: 1
sentence: 'Hello, this is a test message from HSR robot.'"


roslaunch gtts_tts gtts_tts.launch sentence:="This is a test sentence" language:="en"

try_subprocess.py  有用调用模板
