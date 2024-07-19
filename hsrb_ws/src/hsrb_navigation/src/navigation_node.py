#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def move_forward():
    rospy.init_node('hsrb_navigation', anonymous=True)
    velocity_publisher = rospy.Publisher('/hsrb/command_velocity', Twist, queue_size=10)
    vel_msg = Twist()
    
    vel_msg.linear.x = 0.01  # 向前移动速度
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    
    rate = rospy.Rate(10)  # 10 Hz
    
    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        move_forward()
    except rospy.ROSInterruptException:
        pass
