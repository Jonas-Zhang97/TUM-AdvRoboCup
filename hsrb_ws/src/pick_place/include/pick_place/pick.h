#ifndef PICK_H
#define PICK_H

#include <ros/ros.h>

#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <std_msgs/Bool.h>
#include <project_msgs/LabeledCentroid.h>
#include <moveit_msgs/CollisionObject.h>

#include <tmc_control_msgs/GripperApplyEffortActionGoal.h>

class Pick
{
  private:
    moveit::planning_interface::MoveGroupInterface whole_body_grp;
    moveit::planning_interface::MoveGroupInterface arm_grp;
    moveit::planning_interface::MoveGroupInterface gripper_grp;
    moveit::planning_interface::MoveGroupInterface head_grp;

  public:
    Pick():whole_body_grp("whole_body"), arm_grp("arm"), gripper_grp("gripper"), head_grp("head") {};

  public:
    bool init();
    void update();

  /* Robot Motion */
  public:
    void pick();
  
  private:
    void computeTargetOrientation();
    void moveHead();
    void prePickApproach();
    void openGripper();
    void toPickPose();
    void closeGripper();
    void higherTorso();
    void postPickRetreat();
    void toTransportPose();
    bool checkPick();

  private:
    void setWorkspace();

  /* ROS Communication */
  public:
    ros::NodeHandle nh_;

  private:
    ros::Subscriber pick_target_sub_;   // where is the target object, store this in a local variable

    ros::Publisher gripper_pub_;
    ros::Publisher pick_done_pub_;

  private:
    std::string pick_target_topic_;

    std::string pick_done_topic_;

    std::vector<double> gripper_open_value_;

  private:
    void poseCallback(const project_msgs::LabeledCentroid::ConstPtr &msg);
    int object_label_;

  /* Local Variables */
  private:
    // for ROS
    bool command_;
    std_msgs::Bool pick_done_;

    project_msgs::LabeledCentroid labeled_centroid_;

    // some assistance vars
    std::string ref_frame_;
    geometry_msgs::Point target_position_;
    double target_orientation_;
    std::vector<double> transport_value_;
    geometry_msgs::Pose retreat_pose_;

  /* MoveIt */
  private:
    moveit::planning_interface::MoveGroupInterface::Plan body_plan_;
    moveit::planning_interface::MoveGroupInterface::Plan arm_plan_;
    moveit::planning_interface::MoveGroupInterface::Plan gripper_plan_;
    moveit::planning_interface::PlanningSceneInterface PSI_;
    std::vector<std::string> object_names_;

};

#endif