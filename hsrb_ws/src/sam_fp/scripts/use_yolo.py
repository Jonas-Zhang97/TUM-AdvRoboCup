#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image as SensorImage
from cv_bridge import CvBridge
from masks_msgs.msg import maskID, singlemask
import cv2
import numpy as np
import torch
from ultralytics import YOLO

class YoloV8Ros:
    def __init__(self):
        rospy.init_node('yolov8_ros', anonymous=True)
        self.image_topic = rospy.get_param('image_topic', '/hsrb/head_rgbd_sensor/rgb/image_raw')
        self.pub = rospy.Publisher('/sam_mask', maskID, queue_size=1000)
        self.sub = rospy.Subscriber(self.image_topic, SensorImage, self.callback)
        self.mask_pub = rospy.Publisher('/mask_img', SensorImage, queue_size=1000)
        self.bridge = CvBridge()

        self.model = YOLO('yolov8n.pt')  # Load YOLOv8 model, you can change this to your specific model
        
        rospy.loginfo('Node has been started.')

    def callback(self, rosimage: SensorImage):
        cv_image = self.rosimg2cv(rosimage)
        masks = self.yolov8_inference(cv_image)
        exported_masks = self.maskprocessing(masks)
        self.Pub_mask(exported_masks)
        self.publish_image(cv_image, masks)

    def rosimg2cv(self, image):
        cv_image = self.bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
        return cv_image

    def yolov8_inference(self, image):
        results = self.model(image)
        masks = []
        for result in results:
            for box in result.boxes:
                # Check if the detected class is 'bottle' (class ID for 'bottle' might differ based on your model training)
                if box.cls == 39:  # Assuming class ID 39 is 'bottle'
                    bbox = box.xyxy[0].cpu().numpy().astype(int)
                    mask = {
                        'bbox': bbox,
                        'confidence': box.conf.cpu().numpy(),
                        'class': box.cls.cpu().numpy(),
                    }
                    masks.append(mask)
        return masks

    def maskprocessing(self, masks):
        mask_list = []
        for idx, mask in enumerate(masks):
            singlemask_msg = singlemask()
            bbox = mask['bbox']
            singlemask_msg.maskid = idx
            singlemask_msg.shape = [int(bbox[3] - bbox[1]), int(bbox[2] - bbox[0])]
            singlemask_msg.segmentation = []  # YOLOv8 does not provide segmentation mask directly
            singlemask_msg.area = int((bbox[2] - bbox[0]) * (bbox[3] - bbox[1]))
            singlemask_msg.bbox = bbox.tolist()
            singlemask_msg.predicted_iou = float(mask['confidence'])
            singlemask_msg.point_coords = []  # Not available in YOLOv8
            singlemask_msg.stability_score = 0.0  # Not available in YOLOv8
            singlemask_msg.crop_box = bbox.tolist()
            mask_list.append(singlemask_msg)
        mask_list_msg = maskID()
        mask_list_msg.maskID = mask_list
        return mask_list_msg

    def Pub_mask(self, mask):
        self.pub.publish(mask)

    def publish_image(self, image, masks):
        for mask in masks:
            bbox = mask['bbox']
            cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
        ros_image = self.bridge.cv2_to_imgmsg(image, encoding="bgr8")
        self.mask_pub.publish(ros_image)

if __name__ == '__main__':
    yolo_v8_ros = YoloV8Ros()
    rospy.spin()
