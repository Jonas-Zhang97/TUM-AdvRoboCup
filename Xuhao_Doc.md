### Navigation Setup

1. **Install DWA Local Planner**:
   ```bash
   sudo apt-get install ros-noetic-dwa-local-planner
   ```

2. **Terminal #1**:
   - Switch to HSRB mode:
     ```bash
     hsrb_mode
     ```
   - Kill the pose integrator node:
     ```bash
     rosnode kill /pose_integrator
     ```
   - Launch the navigation:
     ```bash
     roslaunch hsrb_navigation hsrb_nav_ics.launch map_file:=/hsrb_ws/src/hsrb_navigation/map/map.yaml
     ```
     *(Note: These two commands should remain running throughout. Launch only requires a single 2D Pose Estimate each time. For navigation, you can use the "2D Nav Goal" after the launch is set up.)*

3. **Terminal #2**:
   - Switch to HSRB mode:
     ```bash
     hsrb_mode
     ```
   - Start RViz with the specific configuration:
     ```bash
     rviz -d $(rospack find hsrb_navigation)/rviz/mapping.rviz
     ```
     *(Note: These two commands should remain running throughout.)*

4. **Terminal #3**:
   - Switch to HSRB mode:
     ```bash
     hsrb_mode
     ```
   - Launch the goal-sending node:
     ```bash
     roslaunch hsrb_navigation send_goal.launch room_name:=goal1
     ```
     *(Note: This command is already integrated into the state machine. It should only be used independently for debugging.)*

### Reference

#### Using rqt

1. Launch rqt:
   ```bash
   rqt
   ```
2. Navigate to `Robot Tools > Robot Steering` from the Plugins menu.
3. Set the movement velocity topic to `/hsrb/command_velocity` in the provided text box.

### Task Planner

- The task planner has been encapsulated into a ROS launch file. By default, `is_first_time` is set to `True`, and this launch can be invoked directly within the state machine.

   Example usage:
   ```bash
   roslaunch task_planner task_planner.launch instruction:="grab the bottle at A and move to B and move to D and move to C and release the bottle at C" is_first_time:=True
   ```

   For subsequent tasks:
   ```bash
   roslaunch task_planner task_planner.launch instruction:="grab a bottle at storage and move to me and release the bottle"
   ```

- Required `.json` and `.png` files are located at:
  ```
  hsrb_ws/src/task_planner/scripts
  ```

### Preparation

1. **Install spaCy**:
   ```bash
   pip install spacy
   python3 -m spacy download en_core_web_sm
   ```

### Debugging

1. **Set up runtime directory**:
   ```bash
   export XDG_RUNTIME_DIR=/tmp/runtime-$USER
   mkdir -p $XDG_RUNTIME_DIR
   chmod 0700 $XDG_RUNTIME_DIR
   ```

### Text-to-Speech (TTS)

1. **Install dependencies**:
   ```bash
   pip install gtts
   sudo apt-get install ros-noetic-tmc-msgs
   sudo apt-get install mpg321
   ```

2. **Run TTS**:
   ```bash
   rosrun gtts_tts gtts_tts_rosrun.py _sentence:="This is a test sentence" _language:="en"
   ```

---
