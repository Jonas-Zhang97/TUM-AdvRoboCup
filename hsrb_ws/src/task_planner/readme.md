### Task Planner

- The Task Planner is encapsulated into a ROS launch file. By default, `is_first_time` is set to `True`, and this launch can be invoked directly within the state machine.

   **Example usage**:
   ```bash
   roslaunch task_planner task_planner.launch instruction:="grab the bottle at A and move to B and move to D and move to C and release the bottle at C" is_first_time:=True
   ```

   **For subsequent tasks**:
   ```bash
   roslaunch task_planner task_planner.launch instruction:="grab a bottle at storage and move to me and release the bottle"
   ```

- **Important Notes**:
  - This Task Planner does not include synonym recognition functionality; its primary purpose is to sequence tasks.
  - The three main keywords used are `grab`, `move`, and `release`.
  - When a grab task is directly specified, the system implicitly understands that the robot should first navigate to the location before attempting the grab.
  - Be sure to avoid spaces before the closing quotation mark at the end of the instruction, for example, `"xxx yyy"`.

- Required `.json` and `.png` files are located in:
  ```
  hsrb_ws/src/task_planner/scripts
  ```

---

### Preparation

1. **Install spaCy**:
   ```bash
   pip install spacy
   python3 -m spacy download en_core_web_sm
   ```

---

### Debugging

1. **Set up runtime directory**:
   ```bash
   export XDG_RUNTIME_DIR=/tmp/runtime-$USER
   mkdir -p $XDG_RUNTIME_DIR
   chmod 0700 $XDG_RUNTIME_DIR
   ```
