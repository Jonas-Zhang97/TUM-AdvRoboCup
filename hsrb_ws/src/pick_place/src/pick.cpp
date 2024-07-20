#include <pick_place/pick.h>

bool Pick::init()
{
  // Topic definitions
  pick_target_topic_ =  "/labeled_objects";
  pick_done_topic_ = "/pick_done";

  // Subscribers and publishers
  pick_target_sub_ = nh_.subscribe(pick_target_topic_, 1, &Pick::poseCallback, this);

  gripper_pub_ = nh_.advertise<trajectory_msgs::JointTrajectory>("/gripper_controller/command", 1);
  pick_done_pub_ = nh_.advertise<std_msgs::Bool>(pick_done_topic_, 1);

  // Initialize flags
  command_ = false;
  pick_done_.data = true;
  
  // Pre-defined poses
  transport_value_ = {0.0, 0.0, 0.0, -1.57, 0.0, 0.0};
  gripper_close_value_.joint_names.resize(1);
  gripper_close_value_.joint_names[0] = "hand_motor_joint";

  gripper_close_value_.points.resize(1);
  gripper_close_value_.points[0].positions.resize(1);
  gripper_close_value_.points[0].positions[0] = 0.0174;
  gripper_close_value_.points[0].time_from_start = ros::Duration(1.0);
  
  // Set values for MoveIt
  ref_frame_ = "odom";

  whole_body_grp.setPlannerId("RRTConnectkConfigDefault");
  whole_body_grp.setPlanningTime(30.0);
  whole_body_grp.setMaxAccelerationScalingFactor(0.1);
  whole_body_grp.setMaxVelocityScalingFactor(0.1);
  whole_body_grp.allowReplanning(true);
  whole_body_grp.setNumPlanningAttempts(10);
  // whole_body_grp.setEndEffectorLink("hand_camera_frame");
  const std::string end_effector_link = whole_body_grp.getEndEffectorLink();

  // Initialize HSRB
  // openGripper();
  ROS_INFO_STREAM("Pick Node Initialized!");
  return true;
}

void Pick::update()
{
  if (command_)
  {
    // Wait for 2 sec to update the planning scene
    ros::Duration(2.0).sleep();

    // reset the joint value
    
    // Perform pick
    pick();

    // Publish msgs that are needed
    pick_done_pub_.publish(pick_done_);

    // Clear all collision objects in the planning scene
    object_names_ = PSI_.getKnownObjectNames();

    ROS_INFO_STREAM("Number of collision objects in the scene: " << object_names_.size());
    
    PSI_.removeCollisionObjects(object_names_);
    object_names_.clear();

    command_ = false;
  }
}

void Pick::pick()
{
  computeTargetOrientation();
  prePickApproach();
  openGripper();
  toPickPose();
  postPickRetreat();
  toTransportPose();

  /* legacy */
  // openGripper();
  // prePickApproach();
  // toPickPose();
  // closeGripper();
  // postPickRetreat();
  // toTransportPose();
}

void Pick::computeTargetOrientation()
{
  geometry_msgs::Point current_base_position;
  current_base_position = whole_body_grp.getCurrentPose("base_link").pose.position;
  geometry_msgs::Vector3 vec;
  vec.x = target_position_.x - current_base_position.x;
  vec.y = target_position_.y - current_base_position.y;
  vec.z = target_position_.z - current_base_position.z;

  target_orientation_ = atan2(vec.y, vec.x);
}

void Pick::prePickApproach()
{
  /* 
    A pre approach for the robot, will be followe by a straight line motion to the pick pose
  */
  
  // define pre-approach pose
  geometry_msgs::PoseStamped pre_approach_pose;
  pre_approach_pose.header.frame_id = ref_frame_;
  pre_approach_pose.pose.position.x = target_position_.x - 0.18 * cos(target_orientation_);
  pre_approach_pose.pose.position.y = target_position_.y - 0.18 * sin(target_orientation_);
  pre_approach_pose.pose.position.z = target_position_.z;

  tf2::Quaternion quaternion;
  quaternion.setRPY(-1.57, -1.57, target_orientation_ - 1.57);

  pre_approach_pose.pose.orientation = tf2::toMsg(quaternion);

  ROS_INFO_STREAM("Pre-approach pose: \n" << pre_approach_pose.pose);

  whole_body_grp.setPoseTarget(pre_approach_pose);
  bool succ = (whole_body_grp.plan(body_plan_) == moveit_msgs::MoveItErrorCodes::SUCCESS);

  if (!succ)
  {
    ROS_INFO_STREAM("Planning failed");
  }

  whole_body_grp.move();
  ROS_INFO_STREAM("Pre-pick goal reached");
}
// 
void Pick::openGripper()     // TODO: Implement this
{
//   std::vector<double> open_value = {-0.043};        // NOTE: set to default for testing
//   gripper_group.setJointValueTarget(open_value);
//   gripper_group.plan(gripper_plan_);
//   gripper_group.move();
//   ROS_INFO_STREAM("Gripper opened");
}
// 
void Pick::toPickPose()
{
  geometry_msgs::Pose pick_pose;
  pick_pose.position.x = target_position_.x - 0.03 * cos(target_orientation_);
  pick_pose.position.y = target_position_.y - 0.03 * sin(target_orientation_);
  pick_pose.position.z = target_position_.z;

  tf2::Quaternion quaternion;
  quaternion.setRPY(-1.57, -1.57, target_orientation_ - 1.57);
  pick_pose.orientation = tf2::toMsg(quaternion);
  ROS_INFO_STREAM("Pick pose: " << pick_pose);

  std::vector<geometry_msgs::Pose> waypoints;
  waypoints.push_back(pick_pose);

  moveit_msgs::RobotTrajectory trajectory;

  double eef_step = 0.01;  // Resolution of the Cartesian path
  double jump_threshold = 0.0;  // No jump threshold

  double fraction = whole_body_grp.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);

  ROS_INFO_STREAM("Straight line generation rate = " << fraction);

  whole_body_grp.execute(trajectory);

  ROS_INFO_STREAM("Arrived at: " << pick_pose.position);
}
// 
// void Pick::closeGripper()
// {
//   gripper_pub_.publish(gripper_close_value_);
//   ros::Duration(1.0).sleep();
// }
//
// 
void Pick::postPickRetreat()
{
  geometry_msgs::Pose post_pick_pose_1;
  post_pick_pose_1.position.x = target_position_.x - 0.03 * cos(target_orientation_);
  post_pick_pose_1.position.y = target_position_.y - 0.03 * sin(target_orientation_);
  post_pick_pose_1.position.z = target_position_.z + 0.1;

  geometry_msgs::Pose post_pick_pose_2;
  post_pick_pose_2.position.x = target_position_.x - 0.21 * cos(target_orientation_);
  post_pick_pose_2.position.y = target_position_.y - 0.21 * sin(target_orientation_);
  post_pick_pose_2.position.z = target_position_.z + 0.1;

  tf2::Quaternion quaternion;
  quaternion.setRPY(-1.57, -1.57, target_orientation_ - 1.57);
  post_pick_pose_1.orientation = tf2::toMsg(quaternion);
  post_pick_pose_2.orientation = tf2::toMsg(quaternion);

  std::vector<geometry_msgs::Pose> waypoints;
  waypoints.push_back(post_pick_pose_1);
  waypoints.push_back(post_pick_pose_2);

  moveit_msgs::RobotTrajectory trajectory;

  double eef_step = 0.01;  // Resolution of the Cartesian path
  double jump_threshold = 0.0;  // No jump threshold

  double fraction = whole_body_grp.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);

  whole_body_grp.execute(trajectory);

  ROS_INFO_STREAM("Retreated");
}

void Pick::toTransportPose()
{
  arm_grp.setJointValueTarget(transport_value_);
  arm_grp.plan(arm_plan_);
  arm_grp.move();

  ROS_INFO_STREAM("Ready to go");
}


void Pick::poseCallback(const project_msgs::LabeledCentroid::ConstPtr &msg)
{
  labeled_centroid_ = *msg;

  command_ = true;

  object_label_ = msg->label;

  target_position_ = msg->pose.pose.position;

  // pre_approach_pose_.header.frame_id = ref_frame_;
  // pre_approach_pose_.pose.position = msg->pose.pose.position;

  // pre_approach_pose_.pose.position.x -= 0.415;    // Length of the gripper = 0.215
  // pre_approach_pose_.pose.position.z += 0.02;

  // tf2::Quaternion quaternion;
  // quaternion.setRPY(3.14, 1.57, 0.0);

  // pre_approach_pose_.pose.orientation = tf2::toMsg(quaternion);
  
  ROS_INFO_STREAM("Command received, position: " << target_position_);
}