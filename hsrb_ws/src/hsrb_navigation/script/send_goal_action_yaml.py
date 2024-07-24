#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2018 Toyota Motor Corporation

import math
import yaml

import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import rospy
from tf import transformations

def load_goals(filename):
    with open(filename, 'r') as file:
        try:
            goals = yaml.safe_load(file)
            return goals['goals']
        except yaml.YAMLError as exc:
            print(exc)
            return []

if __name__ == '__main__':

    try:
        rospy.init_node('send_goal', anonymous=True)
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()

        goals_file = rospy.get_param('~goals_file')  
        goals = load_goals(goals_file)


        for goal_data in goals:
            rospy.loginfo(f"Sending goal: {goal_data['name']}")
            goal = MoveBaseGoal()
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.header.frame_id = "map"
            goal.target_pose.pose.position.x = goal_data['position']['x']
            goal.target_pose.pose.position.y = goal_data['position']['y']

            q = transformations.quaternion_from_euler(
                goal_data['orientation']['roll'],
                goal_data['orientation']['pitch'],
                goal_data['orientation']['yaw']
            )
            goal.target_pose.pose.orientation.x = q[0]
            goal.target_pose.pose.orientation.y = q[1]
            goal.target_pose.pose.orientation.z = q[2]
            goal.target_pose.pose.orientation.w = q[3]

            print(goal)
            client.send_goal(goal)

            finished = client.wait_for_result()
            if finished:
                rospy.loginfo(f"Goal {goal_data['name']} reached successfully.")
            else:
                rospy.logwarn(f"Failed to reach goal {goal_data['name']}.")

    except rospy.ROSInterruptException:
        pass
