import rospy
from ultralytics_ros.msg import YoloResult
from std_msgs.msg import String, Bool
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import numpy as np

class DepSeg:
  def init(self):
    self.bridge = CvBridge()
    self.cv2_dep = None
    self.dep_sub = rospy.Subscriber('/hsrb/head_rgbd_sensor/depth_registered/image', Image, self.dep_callback)

  def dep_callback(self, msg):
    self.cv2_dep = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
    pass