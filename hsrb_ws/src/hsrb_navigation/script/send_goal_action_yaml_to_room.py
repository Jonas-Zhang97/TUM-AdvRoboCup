#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2018 Toyota Motor Corporation

import math
import yaml

import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import rospy
from tf import transformations

from tmc_msgs.msg import RoomIdentifier

from std_msgs.msg import String
from actionlib_msgs.msg import GoalStatus

import sys

def load_goals(filename):
    with open(filename, 'r') as file:
        try:
            goals = yaml.safe_load(file)
            return goals['goals']
        except yaml.YAMLError as exc:
            print(exc)
            return []

def get_goal_by_name(goals, room_name):
    for goal in goals:
        if goal['name'] == room_name:
            return goal
    return None

if __name__ == '__main__':
    try:
        rospy.init_node('send_goal', anonymous=True)
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()

        room_identifier_publisher = rospy.Publisher('room_identifier', RoomIdentifier, queue_size=10)
        navigation_status_publisher = rospy.Publisher('navigation_status', String, queue_size=10)

        goals_file = rospy.get_param('~goals_file')
        room_name = rospy.get_param('~room_name')

        goals = load_goals(goals_file)
        goal_data = get_goal_by_name(goals, room_name)

        if not goal_data:
            rospy.logerr(f"Goal for room {room_name} not found.")
            navigation_status_publisher.publish("failed")
        else:
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
            state = client.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo(f"Goal {goal_data['name']} reached successfully.")
                room_identifier_msg = RoomIdentifier()
                room_identifier_msg.name = goal_data['name']
                room_identifier_publisher.publish(room_identifier_msg)
                navigation_status_publisher.publish("reached")
                sys.exit(0) 
            else:
                rospy.logwarn(f"Failed to reach goal {goal_data['name']}.")
                navigation_status_publisher.publish("failed")
                sys.exit(1)

    except rospy.ROSInterruptException:
        sys.exit(1)