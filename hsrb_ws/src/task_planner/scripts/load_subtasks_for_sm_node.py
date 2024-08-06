#!/usr/bin/env python3

import rospy
import json
import os
import time

def load_sub_tasks(filename):
    if not os.path.exists(filename):
        rospy.logerr(f"File {filename} does not exist.")
        return []
    rospy.loginfo(f"Loading sub tasks from {filename}")
    with open(filename, 'r') as file:
        sub_tasks = json.load(file)
    return sub_tasks

def save_actions_and_adverbials(sub_tasks, filename):
    actions_and_adverbials = []

    for task in sub_tasks:
        action, *params = task
        if action == 'move':
            adverbial = params[1]
        elif action in ('grab', 'release'):
            adverbial = params[0]
        else:
            adverbial = None
        action_adverbial_pair = [action, adverbial]
        actions_and_adverbials.append(action_adverbial_pair)

    rospy.loginfo(f"Saving actions and adverbials to {filename}")
    with open(filename, 'w') as file:
        json.dump(actions_and_adverbials, file, indent=4)
    rospy.loginfo(f"Actions and adverbials saved to {filename}")

def wait_for_flag(flag_path, timeout=60):
    start_time = time.time()
    while not os.path.exists(flag_path):
        if time.time() - start_time > timeout:
            rospy.logerr(f"Timeout while waiting for flag file: {flag_path}")
            return False
        time.sleep(1)
    return True

def load_subtasks_for_sm_node():
    rospy.init_node('load_subtasks_for_sm_node', anonymous=True)
    sub_tasks_filepath = rospy.get_param('~sub_tasks_filepath', "/workspaces/cup/hsrb_ws/src/task_planner/scripts/sub_tasks.json")
    actions_and_adverbials_filepath = rospy.get_param('~actions_and_adverbials_filepath', "/workspaces/cup/hsrb_ws/src/task_planner/scripts/actions_and_adverbials.json")
    flag_path = "/tmp/task_planner_done.flag"

    rospy.loginfo(f"Sub tasks filepath: {sub_tasks_filepath}")
    rospy.loginfo(f"Actions and adverbials filepath: {actions_and_adverbials_filepath}")

    # Wait for the flag file created by task_planner_node
    if wait_for_flag(flag_path):
        sub_tasks = load_sub_tasks(sub_tasks_filepath)
        if sub_tasks:
            save_actions_and_adverbials(sub_tasks, actions_and_adverbials_filepath)
    else:
        rospy.logerr("Flag file not found. Exiting.")
    
    rospy.spin()

if __name__ == "__main__":
    load_subtasks_for_sm_node()
