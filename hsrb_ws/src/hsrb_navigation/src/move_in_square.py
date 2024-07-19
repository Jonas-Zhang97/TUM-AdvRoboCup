#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def move_in_complex_pattern():
    rospy.init_node('hsrb_mapping', anonymous=True)
    velocity_publisher = rospy.Publisher('/hsrb/command_velocity', Twist, queue_size=10)
    rate = rospy.Rate(10)

    vel_msg = Twist()
    
    linear_speed = 0.1
    angular_speed = 0.5
    
    # Complex movement pattern
    for _ in range(4):
        # Move forward
        vel_msg.linear.x = linear_speed
        vel_msg.angular.z = 0
        t0 = rospy.Time.now().to_sec()
        while (rospy.Time.now().to_sec() - t0) < 10:
            velocity_publisher.publish(vel_msg)
            rate.sleep()
        
        # Turn 90 degrees
        vel_msg.linear.x = 0
        vel_msg.angular.z = angular_speed
        t0 = rospy.Time.now().to_sec()
        while (rospy.Time.now().to_sec() - t0) < 3.14 / 2 / angular_speed:
            velocity_publisher.publish(vel_msg)
            rate.sleep()
    
    for _ in range(4):
        # Move forward
        vel_msg.linear.x = linear_speed
        vel_msg.angular.z = 0
        t0 = rospy.Time.now().to_sec()
        while (rospy.Time.now().to_sec() - t0) < 10:
            velocity_publisher.publish(vel_msg)
            rate.sleep()
        
        # Turn -90 degrees
        vel_msg.linear.x = 0
        vel_msg.angular.z = -angular_speed
        t0 = rospy.Time.now().to_sec()
        while (rospy.Time.now().to_sec() - t0) < 3.14 / 2 / angular_speed:
            velocity_publisher.publish(vel_msg)
            rate.sleep()
    
    # Stop the robot
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        move_in_complex_pattern()
    except rospy.ROSInterruptException:
        pass
