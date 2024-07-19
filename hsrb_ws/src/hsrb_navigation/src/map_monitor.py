#!/usr/bin/env python

import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np
import subprocess

class MapMonitor:
    def __init__(self):
        rospy.init_node('map_monitor', anonymous=True)
        self.map_subscriber = rospy.Subscriber('/map', OccupancyGrid, self.map_callback)
        self.map_data = None

    def map_callback(self, data):
        self.map_data = data

    def is_map_complete(self):
        if self.map_data is None:
            return False
        
        # Convert the occupancy grid to a numpy array
        map_array = np.array(self.map_data.data)
        
        # Check the number of unknown cells (value -1) in the map
        unknown_cells = np.sum(map_array == -1)
        
        # Check the percentage of known cells (values 0 or 100)
        total_cells = map_array.size
        known_cells = total_cells - unknown_cells
        known_percentage = (known_cells / total_cells) * 100
        
        rospy.loginfo(f"Known cells: {known_cells}/{total_cells} ({known_percentage:.2f}%)")
        
        # Assume the map is complete if more than 80% of the cells are known
        return known_percentage > 80

if __name__ == '__main__':
    monitor = MapMonitor()
    rate = rospy.Rate(1)  # Check once per second
    
    while not rospy.is_shutdown():
        if monitor.is_map_complete():
            rospy.loginfo("Map is complete!")
            # Save the map
            rospy.loginfo("Saving map...")
            subprocess.call(["rosrun", "map_server", "map_saver", "-f", "/workspaces/ROBCUP_Tutorial/ad_workspace/src/hsrb_navigation/map"])
            rospy.loginfo("Map has been saved successfully.")
            break
        rate.sleep()
