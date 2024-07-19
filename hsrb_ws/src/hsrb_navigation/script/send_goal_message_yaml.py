#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2018 Toyota Motor Corporation

from geometry_msgs.msg import PoseStamped
import rospy

if __name__ == '__main__':

    rospy.init_node('send_goal_message', anonymous=True)
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)

    # wait for /clock for simulation
    rospy.sleep(1)

    msg = PoseStamped()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = "map"
    msg.pose.position.x = -0.169
    msg.pose.position.y =  0.605
    msg.pose.orientation.w = 0.525

    print(msg)
    pub.publish(msg)
