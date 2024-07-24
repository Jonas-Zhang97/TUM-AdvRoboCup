import rospy
from ultralytics_ros.msg import YoloResult
from std_msgs.msg import String, Bool
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import numpy as np
import rospkg
import os
import json

config_path = os.path.join(rospkg.RosPack().get_path('env_detection'), 'config')
ids_to_cls_file = os.path.join(config_path, 'ids_to_cls.json')
with open(ids_to_cls_file, 'r') as f:
  ids_to_cls = json.load(f)
print(ids_to_cls)

class DepSeg:
  def init(self):
    self.has_det = False
    self.has_command = False
    self.has_target = False
    
    self.bridge = CvBridge()
    self.cv2_dep = None

    self.det_ids = set()

    self.cls = []

    self.dep_sub = rospy.Subscriber('/hsrb/head_rgbd_sensor/depth_registered/image', Image, self.dep_callback)
    self.yolores_sub = rospy.Subscriber('/yolo_result', YoloResult, self.res_callback)

  def update(self):
    if self.has_det and self.has_command and self.has_target:

  def ids_to_cls(self):
    for id in self.det_ids:
      self.cls.append(ids_to_cls[str(id)])

  def dep_callback(self, msg):
    self.cv2_dep = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
    pass

  def res_callback(self, msg):
    ids = []
    # Do something with the data
    for detection in msg.detections.detections:
      for result in detection.results:
        ids.append(result.id)
    self.det_ids = set(ids)
    self.has_det = True

if __name__ == "__main__":
  rospy.init_node("depth_segmentation")
