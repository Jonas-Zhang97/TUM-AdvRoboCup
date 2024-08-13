
### Text-to-Speech (TTS) Setup

1. **Install Dependencies**:
   ```bash
   pip install gtts
   sudo apt-get install ros-<ros_distro>-tmc-msgs
   sudo apt-get install ros-noetic-tmc-msgs
   sudo apt-get install mpg321
   ```

2. **Run the TTS Node**:
   ```bash
   rosrun gtts_tts gtts_tts_node.py
   ```

3. **Publish a TTS Message**:
   ```bash
   rostopic pub /talk_request tmc_msgs/Voice "interrupting: false
   queueing: false
   language: 1
   sentence: 'Hello, this is a test message from HSR robot.'"
   ```

4. **Launch the TTS with a Custom Sentence**:
   ```bash
   roslaunch gtts_tts gtts_tts.launch sentence:="This is a test sentence" language:="en"
   ```
