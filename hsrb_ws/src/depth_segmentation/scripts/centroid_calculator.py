import rospy
from sensor_msgs.msg import PointCloud2
from project_msgs.msg import LabeledCentroid
import ros_numpy
import numpy as np
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import PointStamped

class CentroidCalculator:
    def __init__(self):
        self.pc_sub = rospy.Subscriber('/objects_cloud', PointCloud2, self.pc_callback)
        self.labeled_centroid_pub = rospy.Publisher('/labeled_objects', LabeledCentroid, queue_size=1)
        self.centroid_pub = rospy.Publisher('/centroid_objects', PointStamped, queue_size=1)
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        rospy.loginfo("CentroidCalculator initialized")

    def pc_callback(self, msg):
        rospy.loginfo("PointCloud2 message received")
        # Convert PointCloud2 to numpy array
        try:
            pc_data = ros_numpy.point_cloud2.pointcloud2_to_array(msg)
            rospy.loginfo("PointCloud2 converted to numpy array")
        except Exception as e:
            rospy.logerr("Failed to convert PointCloud2 to numpy array: %s", e)
            return
        
        # Extract x, y, z coordinates
        try:
            points = np.zeros((pc_data.shape[0], 3), dtype=np.float32)
            points[:, 0] = pc_data['x']
            points[:, 1] = pc_data['y']
            points[:, 2] = pc_data['z']
            rospy.loginfo("Extracted x, y, z coordinates")
        except Exception as e:
            rospy.logerr("Failed to extract coordinates: %s", e)
            return

        # Calculate centroid
        try:
            centroid = np.mean(points, axis=0)
            rospy.loginfo("Centroid calculated: (%f, %f, %f)", centroid[0], centroid[1], centroid[2])
        except Exception as e:
            rospy.logerr("Failed to calculate centroid: %s", e)
            return
        
        # Create PointStamped message
        try:
            centroid_msg = PointStamped()
            centroid_msg.header.stamp = rospy.Time(0)  # Use latest available transform
            centroid_msg.header.frame_id = msg.header.frame_id
            centroid_msg.point.x = centroid[0]
            centroid_msg.point.y = centroid[1]
            centroid_msg.point.z = centroid[2]
            rospy.loginfo("PointStamped message created")
        except Exception as e:
            rospy.logerr("Failed to create PointStamped message: %s", e)
            return
        
        # Transform centroid to target frame
        target_frame = "odom"
        try:
            transform = self.tf_buffer.lookup_transform(target_frame, centroid_msg.header.frame_id, rospy.Time(0), rospy.Duration(3.0))
            transformed_centroid = tf2_geometry_msgs.do_transform_point(centroid_msg, transform)
            rospy.loginfo("Centroid transformed to frame: %s", target_frame)
            
            # Create LabeledCentroid message
            labeled_centroid = LabeledCentroid()
            labeled_centroid.pose.header.stamp = rospy.Time.now()
            labeled_centroid.pose.header.frame_id = target_frame
            labeled_centroid.pose.pose.position = transformed_centroid.point
            labeled_centroid.label = 1
            
            # Publish transformed PointStamped
            transformed_centroid.header.stamp = rospy.Time.now()
            transformed_centroid.header.frame_id = target_frame
            self.centroid_pub.publish(transformed_centroid)
            rospy.loginfo("Transformed centroid published to /centroid_objects")
        except tf2_ros.TransformException as ex:
            rospy.logwarn("Failed to transform centroid: %s", ex)
            labeled_centroid = LabeledCentroid()
            labeled_centroid.header.stamp = rospy.Time.now()
            labeled_centroid.header.frame_id = msg.header.frame_id
            labeled_centroid.pose.pose.position = centroid_msg.point
            labeled_centroid.label = 0
            
            # Publish original PointStamped
            centroid_msg.header.stamp = rospy.Time.now()
            self.centroid_pub.publish(centroid_msg)
            rospy.loginfo("Original centroid published to /centroid_objects")
        
        # Publish labeled centroid
        self.labeled_centroid_pub.publish(labeled_centroid)
        rospy.loginfo("Labeled centroid published to /labeled_objects")

if __name__ == "__main__":
    rospy.init_node('centroid_calculator')
    calculator = CentroidCalculator()
    rospy.spin()
