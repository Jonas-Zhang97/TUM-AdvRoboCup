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
     *(Note: These commands should remain active throughout the session. Launch requires a single 2D Pose Estimate each time. For navigation, you can use "2D Nav Goal" after the launch is set up.)*

3. **Terminal #2**:
   - Switch to HSRB mode:
     ```bash
     hsrb_mode
     ```
   - Start RViz with the specific configuration:
     ```bash
     rviz -d $(rospack find hsrb_navigation)/rviz/mapping.rviz
     ```
     *(Note: These commands should remain active throughout the session.)*

4. **Terminal #3**:
   - Switch to HSRB mode:
     ```bash
     hsrb_mode
     ```
   - Launch the goal-sending node:
     ```bash
     roslaunch hsrb_navigation send_goal.launch room_name:=goal1
     ```
     *(Note: This command is integrated into the state machine. Use it independently only for debugging.)*

   Alternatively, you can use the following commands:
   - To send goal messages using a YAML file:
     ```bash
     rosrun hsrb_navigation send_goal_message_yaml.py
     ```
   - To send goal actions using a YAML file:
     ```bash
     rosrun hsrb_navigation send_goal_action_yaml.py
     ```

5. **Check Robot's Position and Orientation**:
   - You can use the `tf_echo` command to view the robot's position and orientation in the `/map` coordinate frame:
     ```bash
     rosrun tf tf_echo /map /base_link
     ```

---

### Map Creation

1. **Terminal #1**:
   - Switch to HSRB mode:
     ```bash
     hsrb_mode
     ```
   - Kill the pose integrator node:
     ```bash
     rosnode kill /pose_integrator
     ```
   - Start RViz with the appropriate configuration:
     ```bash
     rviz -d $(rospack find hsrb_rosnav_config)/launch/hsrb.rviz
     ```

2. **Terminal #2**:
   - Switch to HSRB mode:
     ```bash
     hsrb_mode
     ```
   - Launch the mapping node:
     ```bash
     roslaunch hsrb_mapping hector.launch
     ```

3. **Terminal #3**:
   - Launch rqt:
     ```bash
     rqt
     ```
   - In the rqt menubar, select `Robot Tools > Robot Steering` from Plugins.

4. **Terminal #4**:
   - Save the map:
     ```bash
     rosrun map_server map_saver
     ```

---

### Using rqt

1. **Launch rqt**:
   ```bash
   rqt
   ```
2. **Select Robot Steering**:
   - Navigate to `Robot Tools > Robot Steering` from the Plugins menu.
3. **Set Velocity Topic**:
   - Set the movement velocity topic to `/hsrb/command_velocity` in the provided text box.

