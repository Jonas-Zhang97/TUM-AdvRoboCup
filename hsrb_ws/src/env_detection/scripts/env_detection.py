import rospy
from ultralytics_ros.msg import YoloResult
import json
import os
import rospkg
from std_msgs.msg import String
from std_msgs.msg import Bool
from tmc_msgs.msg import RoomIdentifier


config_path = os.path.join(rospkg.RosPack().get_path('env_detection'), 'config')

ids_to_cls_file = os.path.join(config_path, 'ids_to_cls.json')
with open(ids_to_cls_file, 'r') as f:
  ids_to_cls = json.load(f)
print(ids_to_cls)

obj_to_loc_file = os.path.join(config_path, 'obj_to_loc.json')
with open(obj_to_loc_file, 'r') as f:
  obj_to_loc = json.load(f)

loc_to_obj_file = os.path.join(config_path, 'loc_to_obj.json')
with open(loc_to_obj_file, 'r') as f:
  loc_to_obj = json.load(f)


class EnvDetection:
  def init(self):
    self.ids = set()
    self.room_name = None
    self.has_boxes = False
    self.has_room_name = False
    self.has_command = False
    self.bbox_sub = rospy.Subscriber('/yolo_result', YoloResult, self.bbox_callback)
    self.room_sub = rospy.Subscriber('/room_identifier', RoomIdentifier, self.room_callback)
    self.command_sub = rospy.Subscriber('/env_detection_command', Bool, self.command_callback)
    self.string_pub = rospy.Publisher('/env_detection_error_str', String, queue_size=1)
    self.error_pub = rospy.Publisher('/env_detection_error', Bool, queue_size=1)

  def update(self):
    if self.has_boxes and self.has_room_name and self.has_command:
      print("now in ", self.room_name)
      self.varification()
      self.has_command = False
  
  def varification(self):
    # Convert set to list
    ids = list(self.ids)
    # Convert ids to classes
    classes = [ids_to_cls[str(id)] for id in ids]
    for cls in classes:
      print("now processing", cls)
      if cls in obj_to_loc.keys():
        loc = obj_to_loc[cls]
        print("it should be in", loc)
        if loc is not None and self.room_name not in loc:
          print(f'{cls} is in incorrect location: {self.room_name}, which should be in {loc[0]} \n ------')
          self.error_pub.publish(False)
          rospy.set_param('/env_detection/detection_done', True)
          self.string_pub.publish(f'{cls} is in incorrect location: {self.room_name}, which should be in {loc[0]}')
          rospy.set_param('~should_place', loc[0])
          rospy.set_param('~error_obj', cls)
        else:
          print(f'{cls} is in correct location: {self.room_name} \n ------')
          rospy.set_param('/env_detection/detection_done', True)
          # self.error_pub.publish(False)
    # Convert classes to locations

  def bbox_callback(self, yolores):
    ids = []
    # Do something with the data
    for detection in yolores.detections.detections:
      for result in detection.results:
        ids.append(result.id)
    self.ids = set(ids)
    self.has_boxes = True
    # print(self.classes)

  def room_callback(self, room):
    # Do something with the data
    self.room_name = room.name
    print(room.name)
    self.has_room_name = True

  def command_callback(self, command):
    self.has_command = command.data

if __name__ == '__main__':
  rospy.init_node('env_detection')
  env_detection = EnvDetection()
  env_detection.init()
  while not rospy.is_shutdown():
    env_detection.update()
    rospy.Rate(1).sleep()
  rospy.spin()