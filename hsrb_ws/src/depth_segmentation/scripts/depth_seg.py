import rospy
from ultralytics_ros.msg import YoloResult
from std_msgs.msg import String, Bool
from sensor_msgs.msg import Image, PointCloud2, CameraInfo
import cv2
from cv_bridge import CvBridge
import numpy as np
import rospkg
import os
import json
import ros_numpy
import math

config_path = os.path.join(rospkg.RosPack().get_path('env_detection'), 'config')
ids_to_cls_file = os.path.join(config_path, 'ids_to_cls.json')
with open(ids_to_cls_file, 'r') as f:
  ids_to_cls = json.load(f)
print(ids_to_cls)

class DepSeg:
  def init(self):
    self.has_det = False
    self.has_command = False
    self.has_info = False
    
    self.bridge = CvBridge()
    self.cv2_dep = None

    self.det_ids = []
    self.target_name = None
    self.cls = []
    self.target_idx = None
    self.K = None
    self.frame_id = None
    self.encoding = None

    self.dep_sub = rospy.Subscriber('/hsrb/head_rgbd_sensor/depth_registered/image', Image, self.dep_callback)
    self.yolores_sub = rospy.Subscriber('/yolo_result', YoloResult, self.res_callback)
    self.command_sub = rospy.Subscriber('/grasp_target_name', String, self.command_callback)
    self.cam_info_sub = rospy.Subscriber('/hsrb/head_rgbd_sensor/depth_registered/camera_info', CameraInfo, self.cam_info_callback)

    self.dep_pub = rospy.Publisher('/target_depth_map', Image, queue_size=10)
    self.pc_pub = rospy.Publisher('/objects_cloud', PointCloud2, queue_size=10)

  def update(self):
    if self.has_det and self.has_command and self.has_info:
      self.has_det = False
      self.has_command = False
      print("update")
      
      self.name_to_cloud()

      self.cls = []
      self.target_name = None
      self.target_idx = None

  def ids_to_cls(self):
    for id in self.det_ids:
      self.cls.append(ids_to_cls[str(id)])

  def name_to_cloud(self):
    # map the target name to the target id
    target_id = [id_t for id_t, target_name in ids_to_cls.items() if target_name == self.target_name]

    if len(target_id) == 0:
      rospy.logwarn("Target not found")
    else:
      target_id = target_id[0]
      rospy.loginfo(target_id)
      target_idx = self.det_ids.index(int(target_id))
      print(target_idx)
      target_mask = self.masks[target_idx]
      self.dep_pub.publish(target_mask)
      # convert mask to cv2
      target_mask_cv2 = self.bridge.imgmsg_to_cv2(target_mask, desired_encoding='passthrough')
      target_dep = self.cv2_dep * target_mask_cv2    # size: 480x640
      target_dep_msg = self.bridge.cv2_to_imgmsg(target_dep, encoding='passthrough')
      self.dep_pub.publish(target_dep_msg)
      # convert depth to point cloud
      target_cloud = []
      for i in range(480):
        for j in range(640):
          if target_mask_cv2[i, j] != 0 and not math.isnan(target_dep[i, j]):
            Z = target_dep[i, j]/225
            X = (j - self.K[0, 2]) * Z / self.K[0, 0]
            Y = (i - self.K[1, 2]) * Z / self.K[1, 1]
            target_cloud.append([X, Y, Z])
      
      # TODO: Convert target_cloud to PointCloud2
      if target_cloud is None:
        raise ValueError("target_cloud is not initialized")
      
      target_cloud_np = np.zeros(len(target_cloud), dtype=[
        ('x', np.float32),
        ('y', np.float32),
        ('z', np.float32),
      ])
      target_cloud = np.array(target_cloud)
      target_cloud_np['x'] = target_cloud[:, 0]
      target_cloud_np['y'] = target_cloud[:, 1]
      target_cloud_np['z'] = target_cloud[:, 2]

      target_cloud_msg = PointCloud2()
      target_cloud_msg = ros_numpy.point_cloud2.array_to_pointcloud2(target_cloud_np, rospy.Time.now(), self.frame_id)
      self.pc_pub.publish(target_cloud_msg)

  ############## callbacks ################


  def dep_callback(self, msg):
    self.cv2_dep = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
    self.encoding = msg.encoding
    # print(self.encoding)
    pass

  def res_callback(self, msg):
    ids = []
    # Do something with the data
    for detection in msg.detections.detections:
      for result in detection.results:
        ids.append(result.id)
    self.det_ids = ids

    self.masks = msg.masks
    self.has_det = True

  def command_callback(self, msg):
    self.target_name = msg.data
    self.has_command = True
    pass

  def cam_info_callback(self, msg):
    self.K = np.array(msg.K).reshape((3, 3))
    self.frame_id = msg.header.frame_id
    self.has_info = True
    pass

if __name__ == "__main__":
  rospy.init_node("depth_segmentation")
  depseg = DepSeg()
  depseg.init()
  rate = rospy.Rate(10)
  while not rospy.is_shutdown():
    depseg.update()
    rate.sleep()
