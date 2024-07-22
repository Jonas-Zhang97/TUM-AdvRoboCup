pip install gtts
sudo apt-get install ros-<ros_distro>-tmc-msgs

rosrun gtts_tts gtts_tts_node.py

rostopic pub /talk_request tmc_msgs/Voice "interrupting: false
queueing: false
language: 1
sentence: 'Hello, this is a test message from HSR robot.'"
