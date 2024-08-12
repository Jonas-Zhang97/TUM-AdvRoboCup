#include <pick_place/place.h>

bool Place::init()
{
  place_target_topic_ =  "/place_pose";
  // place_done_topic_ = "/place_done";

  place_target_sub_ = nh_.subscribe(place_target_topic_, 1, &Place::poseCallback, this);

  // place_done_pub_ = nh_.advertise<std_msgs::Bool>(place_done_topic_, 1);
  gripper_pub_ = nh_.advertise<tmc_control_msgs::GripperApplyEffortActionGoal>("/hsrb/gripper_controller/apply_force/goal", 10);
  // problem_pub_ = nh_.advertise<std_msgs::Bool>("/problem_solved", 1);

  command_ = false;
  place_done_.data = true;

  arm_home_value_ = {0.0, 0.0, -1.57, -1.57, 0.0, 0.0};

  gripper_close_value_.joint_names.resize(1);
  gripper_close_value_.joint_names[0] = "hand_motor_joint";

  gripper_close_value_.points.resize(1);
  gripper_close_value_.points[0].positions.resize(1);
  gripper_close_value_.points[0].positions[0] = 0.0174;
  gripper_close_value_.points[0].time_from_start = ros::Duration(1.0);

  ref_frame_ = "odom";

  whole_body_grp.setPlannerId("RRTConnectkConfigDefault");
  whole_body_grp.setPlanningTime(10.0);
  whole_body_grp.setMaxAccelerationScalingFactor(0.1);
  whole_body_grp.setMaxVelocityScalingFactor(0.1);
  whole_body_grp.allowReplanning(true);
  whole_body_grp.setNumPlanningAttempts(10);

  ROS_INFO_STREAM("Place Node Initialized!");

  return true;
}

void Place::update()
{
  if (command_)
  {
    ros::Duration(2.0).sleep();
    place();
    
    // place_done_pub_.publish(place_done_);
    // problem_pub_.publish(place_done_);
    nh_.setParam("/place_done", true);

    // Clear all collision objects in the planning scene
    std::vector<std::string> object_names;
    object_names = PSI_.getKnownObjectNames();
    ROS_INFO_STREAM("Number of collision objects in the scene: " << object_names.size());
    PSI_.removeCollisionObjects(object_names);
    object_names.clear();

    command_ = false;
  }
}

void Place::place()
{
  computeTargetOrientation();
  prePlaceApproach();
  toPlacePose();
  openGripper();
  postPlaceRetreat();
  closeGripper();
  homing();
}

void Place::computeTargetOrientation()
{
  ROS_INFO_STREAM("Target position in computeTO: " << target_position_.x << " " << target_position_.y << " " << target_position_.z);
  geometry_msgs::Point current_base_position;
  current_base_position = whole_body_grp.getCurrentPose("base_link").pose.position;
  geometry_msgs::Vector3 vec;
  vec.x = target_position_.x - current_base_position.x;
  vec.y = target_position_.y - current_base_position.y;
  vec.z = target_position_.z - current_base_position.z;

  target_orientation_ = atan2(vec.y, vec.x);

  ROS_INFO_STREAM("Target orientation: " << target_orientation_);
}

void Place::prePlaceApproach()
{
  ROS_INFO_STREAM("target position in pre-place approach: " << target_position_.x << " " << target_position_.y << " " << target_position_.z);
  geometry_msgs::PoseStamped pre_approach_pose;
  pre_approach_pose.header.frame_id = ref_frame_;
  pre_approach_pose.pose.position = target_position_;
  ROS_INFO_STREAM("pre_approach_pose position before: " << pre_approach_pose.pose.position.x << " " << pre_approach_pose.pose.position.y << " " << pre_approach_pose.pose.position.z);
  pre_approach_pose.pose.position.x -= 0.18 * cos(target_orientation_);
  pre_approach_pose.pose.position.y -= 0.18 * sin(target_orientation_);
  pre_approach_pose.pose.position.z += 0.1;

  tf2::Quaternion quaternion;
  quaternion.setRPY(-1.57, -1.57, target_orientation_ - 1.57);
  pre_approach_pose.pose.orientation = tf2::toMsg(quaternion);

  ROS_INFO_STREAM("Pre-place pose: \n" << pre_approach_pose);

  std::vector<moveit_msgs::CollisionObject> collision_object;
  collision_object.resize(1);
  collision_object[0].header.frame_id = ref_frame_;
  collision_object[0].id = "collision_object";

  geometry_msgs::Pose box_pose;
  box_pose.orientation = pre_approach_pose.pose.orientation;
  box_pose.position = target_position_;
  // Ensure z position is non-negative
  if (box_pose.position.z > 0.1) {
      box_pose.position.z -= 0.1;
  } else {
      box_pose.position.z = 0; // Set to zero if subtracting 0.1 would make it negative
  }
  box_pose.position.z /= 2;
  box_pose.position.x = target_position_.x;
  box_pose.position.y = target_position_.y;

  ROS_INFO_STREAM("Box pose: \n" << box_pose);
  shape_msgs::SolidPrimitive primitive;
  primitive.type = primitive.BOX;
  primitive.dimensions.resize(3);
  primitive.dimensions[primitive.BOX_Z] = 0.26;
  primitive.dimensions[primitive.BOX_Y] = 5;
  primitive.dimensions[primitive.BOX_X] = box_pose.position.z * 2;

  collision_object[0].primitives.push_back(primitive);
  collision_object[0].primitive_poses.push_back(box_pose);
  collision_object[0].operation = collision_object[0].ADD;

  PSI_.addCollisionObjects(collision_object);

  whole_body_grp.setPoseTarget(pre_approach_pose);
  bool succ = (whole_body_grp.plan(whole_body_plan_) == moveit_msgs::MoveItErrorCodes::SUCCESS);

  if (!succ)
  {
    ROS_INFO_STREAM("Planning failed");
  }

  whole_body_grp.move();

  ROS_INFO_STREAM("Pre-place goal reached");
}

void Place::toPlacePose()
{
  geometry_msgs::Pose place_pose;
  place_pose.position = target_position_;
  place_pose.position.x -= 0.03 * cos(target_orientation_);
  place_pose.position.y -= 0.03 * sin(target_orientation_);

  tf2::Quaternion quaternion;
  quaternion.setRPY(-1.57, -1.57, target_orientation_ - 1.57);
  place_pose.orientation = tf2::toMsg(quaternion);

  std::vector<geometry_msgs::Pose> waypoints;
  waypoints.push_back(place_pose);

  ROS_INFO_STREAM("Place pose: \n" << place_pose);
  moveit_msgs::RobotTrajectory trajectory;

  double eef_step = 0.01;  // Resolution of the Cartesian path
  double jump_threshold = 0.0;  // No jump threshold

  double fraction = whole_body_grp.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);

  whole_body_grp.execute(trajectory);
}

void Place::openGripper()
{
  tmc_control_msgs::GripperApplyEffortActionGoal open_goal;
  open_goal.goal.effort = -0.2;
  open_goal.goal.do_control_stop = true;
  gripper_pub_.publish(open_goal);
  ros::Duration(0.5).sleep();
}

void Place::postPlaceRetreat()
{
  geometry_msgs::Pose post_place_pose_1;
  post_place_pose_1.position = target_position_;
  post_place_pose_1.position.x -= 0.03 * cos(target_orientation_);
  post_place_pose_1.position.y -= 0.03 * sin(target_orientation_);
  post_place_pose_1.position.z += 0.1;

  tf2::Quaternion quaternion;
  quaternion.setRPY(-1.57, -1.57, target_orientation_ - 1.57);
  post_place_pose_1.orientation = tf2::toMsg(quaternion);

  geometry_msgs::Pose post_place_pose_2;
  post_place_pose_2.position = target_position_;
  post_place_pose_2.position.x -= 0.2 * cos(target_orientation_);
  post_place_pose_2.position.y -= 0.2 * sin(target_orientation_);
  post_place_pose_2.position.z += 0.1;

  post_place_pose_2.orientation = tf2::toMsg(quaternion);

  std::vector<geometry_msgs::Pose> waypoints;
  waypoints.push_back(post_place_pose_1);
  waypoints.push_back(post_place_pose_2);

  moveit_msgs::RobotTrajectory trajectory;

  double eef_step = 0.01;  // Resolution of the Cartesian path
  double jump_threshold = 0.0;  // No jump threshold

  double fraction = whole_body_grp.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);

  whole_body_grp.execute(trajectory);
}

void Place::closeGripper()
{
  tmc_control_msgs::GripperApplyEffortActionGoal close_goal;
  close_goal.goal.effort = 0.2;
  close_goal.goal.do_control_stop = true;
  gripper_pub_.publish(close_goal);
  ros::Duration(0.5).sleep();
}

void Place::homing()
{
  arm_grp.setJointValueTarget(arm_home_value_);
  arm_grp.plan(arm_plan_);
  arm_grp.move();

  ROS_INFO_STREAM("homed");
}

void Place::poseCallback(const geometry_msgs::PoseStamped::ConstPtr &msg)
{
  // Copy the received message to place_pose
  geometry_msgs::PoseStamped place_pose;
  place_pose = *msg;

  // Create a TransformListener to listen for transforms
  tf2_ros::Buffer tfBuffer;
  tf2_ros::TransformListener tfListener(tfBuffer);

  try
  {
    // Look up the transform from "map" to "odom" frame
    geometry_msgs::TransformStamped map_to_odom;
    map_to_odom = tfBuffer.lookupTransform("odom", "map", ros::Time(0), ros::Duration(3.0));

    // Transform the place_pose from "map" frame to "odom" frame
    tf2::doTransform(place_pose, place_pose, map_to_odom);

    // Set the target position to the transformed pose's position
    target_position_ = place_pose.pose.position;

    // Log the received command and position
    ROS_INFO_STREAM("Command received, position: " << target_position_);

    command_ = true;
  }
  catch (tf2::TransformException &ex)
  {
    ROS_ERROR("%s", ex.what());
  }
}