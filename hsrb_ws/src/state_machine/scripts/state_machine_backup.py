# import rospy
# import smach
# import subprocess
# import smach_ros
# import smach_viewer
#
# from dataclasses import dataclass, field
# from std_msgs.msg import String, Bool
#
# from typing import List
#
# """
# Two Modes:
# Patrol inspection
# Serve
#
#
#
# Middle Flexible States:
# Navigation/ Look For/ Pick/ Place/Listen + Analyze/ Audio Output/ Follow
# Read from config in the future
#
# Fixed States:
#
# Start/ End/ Emergency Stop/ waitForNewCmd
#
# Start: always at the beginning
# End: always at the end
#
# Listen and Analyze  can be combined into one state
#
# Listen: when the speech is recognized,
# waitForNewCmd: include a position initialization
#
# Patrol inspection(MODE): check the environment and recover the environment
#
# -----------------------------------------------------------------------------------------------------------------------
# |      Previous State             |             Current State                |                 Next State              |
# -----------------------------------------------------------------------------------------------------------------------
# |         None                    |                 Start                    |                 Nav or Listen           |
# -----------------------------------------------------------------------------------------------------------------------
# |         Start or Audio Output  |                 Listen  + Analyze         |               Look For or Audio Output  |
# -----------------------------------------------------------------------------------------------------------------------
# |         Start or Pick           |                 Nav                    |Look For (object or pose or count) or Place|
# -----------------------------------------------------------------------------------------------------------------------
# |         Nav                     |                 Look For                  |        Pick or Listen or Place or Nav  |
# -----------------------------------------------------------------------------------------------------------------------
# |         Look For                |                 Pick                       |                     Nav               |
# -----------------------------------------------------------------------------------------------------------------------
# |         Nav                    |                 Place                      |                     End            `   |
# -----------------------------------------------------------------------------------------------------------------------
# |         Start or Nav             |      Listen + Analyze                     |                Audio Output           |
# -----------------------------------------------------------------------------------------------------------------------
# |         Listen + Analyze          |             Audio Output                 |                  Nav                  |
# -----------------------------------------------------------------------------------------------------------------------
# |         Nav                   |     Count(may be considered as Look for)   |                  Nav                  |
# -----------------------------------------------------------------------------------------------------------------------
# |Count(may be considered as Look for)|               Nav                      |                 Audio Output           |
# -----------------------------------------------------------------------------------------------------------------------
# |         Nav                     |                 Audio Output               |                  End                  |
# -----------------------------------------------------------------------------------------------------------------------
# |           Audio Output             |              Follow                     |                  End                   |
# -----------------------------------------------------------------------------------------------------------------------
# |     Place or Follow or Audio out |                 End                      |                  End                   |
# -----------------------------------------------------------------------------------------------------------------------
# """
#
#
# # class stateDescription:
# @dataclass
# class stateDescription:
#     """
#     struct stateDescription{
#         string stateName;
#         list<string> preRequisite;
#         list<string> postRequisite;
#         }
#     """
#     stateName: str
#     preRequisite: List[str] = field(default_factory=list)
#     postRequisite: List[str] = field(default_factory=list)
#
# ## TODO: count(YOLO), Look For(Waving hands), Follow
# # TODO: read from config file
# start = stateDescription("start",
#                          ["None"],
#                          ["Nav", "Listen"])
# Nav = stateDescription("Nav",
#                        ["Start", "Pick", "Look For", "Audio Output", "Count"],
#                        ["Look For", "Place", "Audio Output"])
# LookFor = stateDescription("Look For",
#                            ["Nav"],
#                            ["Pick", "Listen", "Place", "Nav"])
# Pick = stateDescription("Pick",
#                         ["Look For"],
#                         ["Nav"])
# Place = stateDescription("Place",
#                          ["Nav", "Look For"],
#                          ["End"])
# Listen = stateDescription("Listen",
#                           ["Start", "Audio Output"],
#                           ["Look For", "Audio Output"])
# AudioOutput = stateDescription("Audio Output",
#                                ["Listen", "Nav", "Look For"],  # look for person
#                                ["Nav", "End"])
# Follow = stateDescription("Follow",
#                           ["Audio Output"],
#                           ["End"])
# End = stateDescription("End",
#                        ["Place", "Follow", "Audio Output"],
#                        ["None"])
#
#
# # class for generating states
# class stateMachineGenerator(smach.State):
#     """
#      Constructor for the state machine generator
#      :param pre_requisite: list of pre_requisite states for state matching
#      :param post_requisite: list of post_requisite states for state matching
#      """
#
#     def __init__(self, state_description):
#         self.lpreRequsite = ['a'] #state_description.preRequisite
#         self.lpostRequsite = ['b'] # state_description.preRequisite
#         smach.State.__init__(self, outcomes=['succeeded', 'failed'])
#
#     def check_pre_requisite(self):
#
#         return
#
#     def execute(self):
#         command = ["ros run", "pkg", "node.py"]
#         process = subprocess.call(command)
#         if process == 0:
#             return 'succeeded'
#         else:
#             return 'failed'
#
#
# # Define start state
# class startState(smach.State):  # TODO: Consider open door as start signal
#     def __init__(self):
#         smach.State.__init__(self, outcomes=['succeeded', 'failed'])
#         self.sD = stateDescription("startState",
#                                    ["None"],
#                                    ["NextState"])  # TODO: decide the next states
#
#     def execute(self):
#         command = ["ros run", "pkg", "node.py"]
#         process = subprocess.call(command)
#         if process == 0:
#             return 'succeeded'
#         else:
#             return 'failed'
#
#
# # Define end state
# class endState(smach.State):
#     def __init__(self):
#         smach.State.__init__(self, outcomes=['succeeded', 'failed'])
#         self.sD = stateDescription("endState",
#                                    ["PreviousState"],  #TODO: decide the previous state
#                                    ["None"])
#
#     def execute(self):
#         command = ["ros run", "pkg", "node.py"]
#         process = subprocess.call(command)
#         if process == 0:
#             return 'succeeded'
#         else:
#             return 'failed'
#
#
# class EmergencyStop(smach.State):
#     def __init__(self):
#         smach.State.__init__(self, outcomes=['stopped'])
#
#     def execute(self, userdata):
#         rospy.loginfo("Emergency Stop Activated!")
#         return 'stopped'
#
#
# # TODO: use get param to get the state list, where the state list is from GPT
# # stateList = rospy.get_param('stateList')
#
#
# def stateOdering(stateList):  #TODO
#     """
#     Function to order the states in a state machine
#     :param stateList: list of stateDescriptions
#     :return: list of ordered stateDescriptions
#     """
#     stateList_ordered = []
#     return stateList_ordered
#
#
# # Define a function to check for speech recognition results
# def speech_cb(userdata, msg):
#     return msg.data != ""
#
#
# # Define a function to check for waving hands
# def wave_cb(userdata, msg):
#     return msg.data
#
#
# def problem_detected_cb(userdata, msg):
#     return msg.data
#
#
# def problem_solved_cb(userdata, msg):
#     return msg.data
#
# def emergency_cb(userdata, msg):
#     return not msg.data  # Trigger emergency stop when msg.data is True
#
#
# def main():
#     rospy.init_node('state_machine')
#     sm = smach.StateMachine(outcomes=['overall succeeded', 'overall failed', 'emergency_stopped'])
#     # create state descriptions
#     sD_A = stateDescription("stateA",
#                             ["a", "b", "c"],
#                             ["d", "e", "f"])
#     sD_B = stateDescription("stateB",
#                             ["a", "b", "c"],
#                             ["d", "e", "f"])
#     sD_C = stateDescription("stateC",
#                             ["a", "b", "c"],
#                             ["d", "e", "f"])
#     sD_D = stateDescription("stateD",
#                             ["a", "b", "c"],
#                             ["d", "e", "f"])
#     sD_E = stateDescription("stateE",
#                             ["a", "b", "c"],
#                             ["d", "e", "f"])
#
#     # create instances of stateMachineGenerator
#     STATE_A = stateMachineGenerator(sD_A)
#     STATE_B = stateMachineGenerator(sD_B)
#     STATE_C = stateMachineGenerator(sD_C)
#     STATE_D = stateMachineGenerator(sD_D)
#     STATE_E = stateMachineGenerator(sD_E)
#
#     state_list = [sD_A, sD_B, sD_C, sD_D, sD_E]
#     # Create the top level state machine
#     with sm:
#         # Patrol inspection mode
#         patrol_sm = smach.StateMachine(outcomes=['patrol_sm_done'])
#         with patrol_sm:
#             """
#             nav -> look for(check the environment) -> once find different -> pick -> nav -> place
#             """
#             regular_routine = smach.StateMachine(outcomes=['regular_routine_done'])
#
#
#             with regular_routine:
#                 smach.StateMachine.add('Nav1', STATE_A,  # TODO: change to the real state
#                                        transitions={'succeeded': 'LookFor'})
#                 smach.StateMachine.add('LookFor', STATE_B,  # TODO: change to the real state
#                                        transitions={'succeeded': 'Pick'})
#                 smach.StateMachine.add('Pick', STATE_C,  # TODO: change to the real state
#                                        transitions={'succeeded': 'Nav2'})
#                 smach.StateMachine.add('Nav2', STATE_D,  # TODO: change to the real state
#                                        transitions={'succeeded': 'Place'})
#                 smach.StateMachine.add('Place', STATE_E,  # TODO: change to the real state
#                                        transitions={'succeeded': 'regular_routine_done'})
#
#             # Problem handling branch
#             problem_handling = smach.StateMachine(outcomes=['problem_handling_done'])
#
#             with problem_handling:
#                 smach.StateMachine.add('Nav3', STATE_A,  # TODO: change to the real state
#                                        transitions={'succeeded': 'Pick'})
#                 smach.StateMachine.add('Pick', STATE_B,  # TODO: change to the real state
#                                        transitions={'succeeded': 'Nav4'})
#                 smach.StateMachine.add('Nav4', STATE_C,  # TODO: change to the real state
#                                        transitions={'succeeded': 'Place'})
#                 smach.StateMachine.add('Place', STATE_D,  # TODO: change to the real state
#                                        transitions={'succeeded': 'problem_handling_done'})
#
#             # Concurrence container to manage regular routine and problem detection
#             patrol_con = smach.Concurrence(outcomes=['regular_done', 'problem_detected'],
#                                            default_outcome='regular_done',
#                                            outcome_map={
#                                                'problem_detected': {'MONITOR_PROBLEM': 'invalid'},
#                                                'regular_done': {'MONITOR_PROBLEM': 'valid',
#                                                                 'REGULAR_ROUTINE': 'regular_routine_done'}
#                                            }
#                                            )
#             with patrol_con:
#                 smach.Concurrence.add('REGULAR_ROUTINE', regular_routine)
#                 smach.Concurrence.add('MONITOR_PROBLEM',
#                                       smach_ros.MonitorState('/problem_detection_topic', Bool, problem_detected_cb)) # TODO: set the publisher in lookfor, true false
#
#             smach.StateMachine.add('PATROL_CON', patrol_con,
#                                    transitions={'regular_done': 'patrol_sm_done', 'problem_detected': 'PROBLEM_HANDLING'})
#             smach.StateMachine.add('PROBLEM_HANDLING', problem_handling,
#                                    transitions={'problem_handling_done': 'PATROL_CON'})
#
#
#         # Serve Mode
#         serve_sm = smach.StateMachine(outcomes=['serve_sm_done'])
#         with serve_sm:
#             """
#             listen or look for(waving hands) -> nav -> listen -> audio output -> nav -> pick or follow -> nav -> place -> end
#             """
#             smach.StateMachine.add('Nav5', STATE_A,  # TODO: change to the real state
#                                    transitions={'succeeded': 'Pick'})
#             smach.StateMachine.add('Pick', STATE_B,  # TODO: change to the real state
#                                    transitions={'succeeded': 'Nav6'})
#             smach.StateMachine.add('Nav6', STATE_C,  # TODO: change to the real state
#                                    transitions={'succeeded': 'Place'})
#             smach.StateMachine.add('Place', STATE_D,  # TODO: change to the real state
#                                    transitions={'succeeded': 'done'})
#
#             # for sub-states
#             # TODO: change the state above in to the format below
#             state_list_ordered = stateOdering(state_list)
#             for state in state_list_ordered:
#                 smach.StateMachine.add(state.stateName, stateMachineGenerator(state),
#                                        transitions={'succeeded': 'succeeded',
#                                                     'failed': 'failed'})
#
#         # Create a Concurrence container for parallel execution
#         con = smach.Concurrence(outcomes=['patrol', 'serve'],
#                                 default_outcome='patrol',
#                                 outcome_map={
#                                     'serve': {
#                                         'MONITOR_SPEECH': 'invalid',
#                                         'MONITOR_WAVE': 'invalid',
#                                         'PROBLEM_DETECTED': 'invalid',
#                                         'PROBLEM_SOLVED': 'valid'
#                                     },
#                                     'patrol': {
#                                         'MONITOR_SPEECH': 'valid',
#                                         'MONITOR_WAVE': 'valid',
#                                         'PROBLEM_DETECTED': 'valid',
#                                         'PROBLEM_SOLVED': 'invalid'
#                                     }
#                                 }
#                                 )
#         with con:
#             smach.Concurrence.add('MONITOR_SPEECH',
#                                   smach_ros.MonitorState('/speech_recognition_topic',
#                                                          String,
#                                                          speech_cb))
#             smach.Concurrence.add('MONITOR_WAVE',
#                                   smach_ros.MonitorState('/waving_hand_topic',
#                                                          Bool,
#                                                          wave_cb))
#             smach.Concurrence.add('PROBLEM_DETECTED',
#                                   smach_ros.MonitorState('/problem_detected_topic',
#                                                          Bool,
#                                                          problem_detected_cb))
#             smach.Concurrence.add('PROBLEM_SOLVED',
#                                   smach_ros.MonitorState('/problem_solved_topic',
#                                                          Bool,
#                                                          problem_solved_cb))
#
#         # Main state machine
#         smach.StateMachine.add('CHECK_MODE', con,
#                                transitions={'patrol': 'PATROL_INSPECTION',
#                                             'serve': 'SERVE'})
#         smach.StateMachine.add('PATROL_INSPECTION', patrol_sm,
#                                transitions={'patrol_sm_done': 'CHECK_MODE'})
#         smach.StateMachine.add('SERVE', serve_sm,
#                                transitions={'serve_sm_done': 'CHECK_MODE'})
#         # Adding the emergency stop monitor to the top level state machine
#         monitor_emergency_stop = smach_ros.MonitorState('/emergency_stop_topic', Bool, lambda ud, msg: False)
#         smach.StateMachine.add('MONITOR_EMERGENCY_STOP', monitor_emergency_stop,
#                                transitions={'invalid': 'EMERGENCY_STOP', 'valid': 'CHECK_MODE'})
#
#     # Create and start the introspection server
#     sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
#     sis.start()
#
#     outcome = sm.execute()
#     rospy.spin()
#     if outcome == 'overall succeeded':
#         print("Overall succeeded")
#     else:
#         print("Overall failed")
#
#
# if __name__ == "__main__":
#     main()
#     # stateA = stateDescription("stateA",
#     #                           ["a", "b", "c"],
#     #                           ["d", "e", "f"])
#     # print('stateA', stateA)
#     # print('stateA.stateName', stateA.stateName)
#     # print('stateA.preRequisite', stateA.preRequisite)
#     # print('stateA.postRequisite', stateA.postRequisite)
#
#     # stateB = stateDescription("stateB",
#     #                           ["a", "b", "c"],
#     #                           ["d", "e", "f"])
#
#     # test = [stateA, stateB]
#     # print('test', test)
#     # print('test[0]', test[0])
#     # print('test[1]', test[1])
# """
# valid Outcome:
#
# The valid outcome is returned when the callback function evaluates to True.
# This means the condition being monitored is not triggering an emergency stop or error condition,
# and the state machine should continue with its normal operation.
#
#
# invalid Outcome:
#
# The invalid outcome is returned when the callback function evaluates to False.
# This indicates that the monitored condition has been met (e.g., an emergency stop signal has been received),
# and the state machine should transition to handle this condition (e.g., stop the machine).
# """
import numpy as np
############################################################################################################
##test code from GPT
############################################################################################################
import rospy
import smach
import subprocess
import smach_ros
import smach_viewer
from dataclasses import dataclass, field
from std_msgs.msg import String, Bool
from typing import List
import yaml
import rospkg
import os
from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_from_euler


"""
Command example:
There is a person at the workroom, their request is:
	grasp a bottle from the storage and bring it to me

"""



# Define state description
@dataclass
class stateDescription:
    stateName: str
    preRequisite: List[str] = field(default_factory=list)
    postRequisite: List[str] = field(default_factory=list)

# State descriptions
Start = stateDescription("Start",
                         ["None"],
                         ["Nav", "Listen"])

Nav = stateDescription("Nav",
                       ["Pick", "Audio Output", "Look For", "Look For wh"],
                       ["Look For", "Place", "Audio Output"])

LookFor_wh = stateDescription("Look For wh",
                           ["Start"],
                           ["Nav","Listen"])

# LookFor = stateDescription("Look For",
#                            ["Nav"],
#                            ["Pick", "Place", "Nav"])

Pick = stateDescription("Pick",
                        ["Look For"],
                        ["Nav"])

Place = stateDescription("Place",
                         ["Nav", "Look For"],
                         ["End"])

Listen = stateDescription("Listen",
                          ["Start", "Audio Output"],
                          ["Look For", "Audio Output"])

AudioOutput = stateDescription("Audio Output",
                               ["Listen", "Nav", "Look For"],
                               ["Nav", "End"])


# Follow = stateDescription("Follow",
#                           ["Audio Output"],
#                           ["End"])

End = stateDescription("End",
                       ["Place", "Audio Output"],   # remove follow for now
                       ["None"])



# State machine generator class
class stateMachineGenerator(smach.State):
    def __init__(self, state_description):
        self.lpreRequsite = state_description.preRequisite
        self.lpostRequsite = state_description.postRequisite
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])

    def execute(self, userdata):
        command = ["rosrun", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'

# Start state
class startState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])
        self.sD = stateDescription("startState", ["None"], ["NextState"])


    def execute(self, userdata):
        command = ["rosrun", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'

class StartServe(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])


    def execute(self, userdata):
        rospy.loginfo("Start Serve")
        return 'succeeded'


class NavState_patrol(smach.State): # Done # for patral
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted'])
        self.room_name = ['goal1', 'kitchen', 'workroom', 'storage']

    def execute(self, userdata):
        rospy.logwarn(monitor_problem)
        if self.preempt_requested():
            print("state Nav is being preempted!!!")
            self.service_preempt()
            return 'preempted'
        current_room_name = self.room_name[0]
        self.room_name.remove(current_room_name)
        self.room_name.append(current_room_name)
        command = ["roslaunch", "hsrb_navigation", "send_goal.launch", f"room_name:={current_room_name}"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'


class NavState_error_handling(smach.State):  # TODO
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])
        self.room_name = item_place

    def execute(self, userdata):
        command = ["roslaunch", "hsrb_navigation", "send_goal.launch", f"room_name:={self.room_name}"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'


class NavServe(smach.State): # Done
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])
        self.room_name = ['storage', 'workroom']

    def execute(self, userdata):
        rospy.logwarn(monitor_problem)

        current_room_name = self.room_name[0]
        self.room_name.remove(current_room_name)
        self.room_name.append(current_room_name)
        command = ["roslaunch", "hsrb_navigation", "send_goal.launch", f"room_name:={current_room_name}"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'

class LookFor_patrol_State(smach.State): # patrol  # FIXME
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted'])
        self.bool = None
    def execute(self, userdata):
        if self.preempt_requested():
            print("state LookFor is being preempted!!!")
            self.service_preempt()
            return 'preempted'
        if monitor_problem: # FIXME
            return 'failed'
        env_detection_pub.publish(True)
        while self.bool is None:
            self.bool = env_detection_error_cb
        if self.bool:  # No problem publish true
            return 'succeeded'
        else:  # Problem detected publish false
            return 'failed'



class Look_and_Pick_State(smach.State): # find, segment, pick # Done
    def __init__(self, item_name):
        smach.State.__init__(self, outcomes=['succeeded'])
        self.item_name = item_name  # string
        global pick_done
        pick_done = None
    def execute(self, userdata):
        grasp_target_name_pub.publish(self.item_name)
        while pick_done is None:
            rospy.loginfo("Waiting for pick node to finish")
            pass # wait the signal from pick node
        if pick_done == True:  # No problem publish true
            return 'succeeded'
        if pick_done == False:  # Problem detected publish false
            return 'failed'

class PickServe(smach.State): # find, segment, pick # Done
    def __init__(self, item_name):
        smach.State.__init__(self, outcomes=['succeeded'])
        self.item_name = item_name  # string
        global pick_done
        pick_done = False
    def execute(self, userdata):
        grasp_target_name_pub.publish(self.item_name)
        while not pick_done :
            rospy.loginfo("Waiting for pick node to finish")
            pass # wait the signal from pick node
        if pick_done == True:  # No problem publish true
            return 'succeeded'
        if pick_done == False:  # Problem detected publish false
            return 'failed'

class PlaceState(smach.State): # done
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])
        global place_done
        place_done = None
        euler = np.array([0, 0, 30])
        quaternion = quaternion_from_euler(euler[0], euler[1], euler[2])
        self.place_pose = PoseStamped()
        self.place_pose.pose.position.x = 3.9
        self.place_pose.pose.position.y = 1.48
        self.place_pose.pose.position.z = 0.8
        self.place_pose.pose.orientation.x = quaternion[0]
        self.place_pose.pose.orientation.y = quaternion[1]
        self.place_pose.pose.orientation.z = quaternion[2]
        self.place_pose.pose.orientation.w = quaternion[3]


    def execute(self, userdata):
        place_pose_pub.publish(self.place_pose)

        while place_done is None:
            pass # wait the signal from pick node
        if place_done == True:  # No problem publish true
            return 'succeeded'
        if place_done == False:  # Problem detected publish false
            return 'failed'

class PlaceServe(smach.State): # done
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])
        global place_done
        place_done = None
        euler = np.array([0, 0, 30])
        quaternion = quaternion_from_euler(euler[0], euler[1], euler[2])
        self.place_pose = PoseStamped()
        self.place_pose.pose.position.x = 3.9
        self.place_pose.pose.position.y = 1.48
        self.place_pose.pose.position.z = 0.8
        self.place_pose.pose.orientation.x = quaternion[0]
        self.place_pose.pose.orientation.y = quaternion[1]
        self.place_pose.pose.orientation.z = quaternion[2]
        self.place_pose.pose.orientation.w = quaternion[3]


    def execute(self, userdata):
        place_pose_pub.publish(self.place_pose)

        while place_done is None:
            pass # wait the signal from pick node
        if place_done == True:  # No problem publish true
            return 'succeeded'
        if place_done == False:  # Problem detected publish false
            return 'failed'


class ListenState(smach.State):  # Done
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])
        self.sr_result = ''
    def execute(self, userdata):

        self.sr_result = speech_cb
        if self.sr_result != '':
            return 'succeeded'
        else:
            return 'failed'

class AudioState(smach.State): # TODO
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])

    def execute(self, userdata):
        command = ["rosrun", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'


# End state
class endState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])
        self.sD = stateDescription("endState", ["PreviousState"], ["None"])

    def execute(self, userdata):
        command = ["rosrun", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'

class EndServe(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])


    def execute(self, userdata):
        rospy.loginfo("End Serve")
        return 'succeeded'

class errorState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])

    def execute(self, userdata):
        rospy.loginfo("Error state!")
        return 'succeeded'
# Emergency stop state
class EmergencyStop(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['stopped'])

    def execute(self, userdata):
        rospy.loginfo("Emergency Stop Activated!")
        return 'stopped'

# Patrol state
class PatrolState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])

    def execute(self, userdata):
        """
        Includes all the states for patrol inspection and run in a loop
        Example waypoints: [room1, room2, room3, room4]
        The robot will navigate to each room and perform the inspection
        Only contains normal routine, no problem handling
        If a problem is detected, the robot will stop the patrol and handle the problem
        """
        command = ["rosrun", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'

# Callback functions
def speech_cb(userdata,msg):
    return msg.data

def wave_cb(userdata, msg):
    return msg.data

def problem_detected_cb(userdata,msg):
    return msg.data

def problem_solved_cb(userdata,msg):
    problem_solved = msg.data
    return problem_solved

def emergency_cb(userdata,msg):
    return not msg.data  # Trigger emergency stop when msg.data is True

def env_detection_error_cb(userdata, msg):
    monitor_problem = msg.data
    rospy.logwarn(monitor_problem)
    if monitor_problem:
        problem_solved = False
    return monitor_problem

def speech_cb(userdata, msg):
    return msg.data

def pick_done_cb(msg):
    pick_done = msg.data
    return pick_done

def place_done_cb(userdata,msg):
    place_done = msg.data
    return place_done

def env_detection_error_string_cb(userdata,msg):
    item_place = msg.data
    return item_place

# def gpt_response_cb(msg):
#     global states_list, main_executed
#     if not main_executed:
#         # Step 1: Extract the list part of the string
#         list_part = msg.data.split('=')[1].strip()
#
#         # Step 2: Remove the square brackets
#         list_part = list_part.strip('[]')
#
#         # Step 3: Split the string into individual elements
#         elements = list_part.split(',')
#
#         # Step 4: Strip any extra whitespace from each element
#         states_list = [element.strip() for element in elements]
#         rospy.loginfo("State list: %s", states_list)
#         main()
#     return states_list


def patrol_con_child_term_cb(outcome_map):
    """
    called after a child state has finished.
    A State Machine Container is also a child state!

        @type child_termination_cb: callable
        @param child_termination_cb: This callback gives the user the ability
        to force the concurrence to preempt running states given the
        termination of some other set of states. This is useful when using
        a concurrence as a monitor container.

        This callback is called each time a child state terminates. It is
        passed a single argument, a dictionary mapping child state labels
        onto their outcomes. If a state has not yet terminated, it's dict
        value will be None.

        This function can return three things:
         - False: continue blocking on the termination of all other states
         - True: Preempt all other states
         - list of state labels: Preempt only the specified states

        If you just want the first termination to cause the other children
        to terminate, the callback (lamda so: True) will always return True.
    """
    print("patrol_con_child_term_cb")
    if outcome_map['REGULAR_ROUTINE'] == 'regular_routine_done':
        print("patrol_con_child_term_cb: regular_routine_done")
        return True # preempt other states, jump out of the concurrence
    elif outcome_map['MONITOR_PROBLEM'] == 'problem_detected':
        print("patrol_con_child_term_cb: problem_detected")
        return True # preempt other states, jump out of the concurrence
    else:
        print("patrol_con_child_term_cb: continue blocking")
        return False

def patrol_con_out_cb(outcome_map):
    """
        @type outcome_cb: callable
        @param outcome_cb: If the outcome policy needs to be more complicated
        than just a conjunction of state outcomes, the user can supply
        a callback for specifying the outcome of the container.

        This callback is called only once all child states have terminated,
        and it is passed the dictionary mapping state labels onto their
        respective outcomes.

        If the callback returns a string, it will treated as the outcome of
        the container.

        If the callback returns None, the concurrence will first check the
        outcome_map, and if no outcome in the outcome_map is satisfied, it
        will return the default outcome.

        NOTE: This callback should be a function ONLY of the outcomes of
        the child states. It should not access any other resources.
    """
    print("patrol_con_out_cb")
    if outcome_map['REGULAR_ROUTINE'] == 'regular_routine_done':
        print("patrol_con_out_cb: regular_routine_done")
        return 'regular_done'
    elif outcome_map['MONITOR_PROBLEM'] == 'valid':
        print("patrol_con_out_cb: problem_detected")
        return 'problem_detected'
    else:
        print("patrol_con_out_cb: regular_done")
        return 'regular_done'
# Main function
def main():


    # Create the top-level state machine
    sm = smach.StateMachine(outcomes=['overall_succeeded', 'overall_failed', 'emergency_stopped'])

    # Create state descriptions
    sD_A = stateDescription("stateA", ["a", "b", "c"], ["d", "e", "f"])
    sD_B = stateDescription("stateB", ["a", "b", "c"], ["d", "e", "f"])
    sD_C = stateDescription("stateC", ["a", "b", "c"], ["d", "e", "f"])
    sD_D = stateDescription("stateD", ["a", "b", "c"], ["d", "e", "f"])
    sD_E = stateDescription("stateE", ["a", "b", "c"], ["d", "e", "f"])

    # Create instances of stateMachineGenerator
    STATE_A = stateMachineGenerator(sD_A)
    STATE_B = stateMachineGenerator(sD_B)
    STATE_C = stateMachineGenerator(sD_C)
    STATE_D = stateMachineGenerator(sD_D)
    STATE_E = stateMachineGenerator(sD_E)

    Nav = NavState_patrol()
    Nav_serve = NavServe()
    LookFor_patrol = LookFor_patrol_State()
    Pick = Look_and_Pick_State('bottle')
    Place = PlaceState()
    Listen = ListenState()
    Audio = AudioState()
    Nav_er = NavState_error_handling()
    error_state = errorState()


    # for serve mode:
    #
    # states = ["Start", "Pick", "Nav", "Place", "End"]
    # classes = {
    #     "Start": StartServe,
    #     "Pick": PickServe,
    #     "Nav": NavServe,
    #     "Place": PlaceServe,
    #     "End": EndServe
    # }
    #
    # instances = {}
    #
    # for state in states:
    #     class_name = f"{state}Serve"
    #     instance_name = f"{state.lower()}_serve_instance"
    #     instances[instance_name] = classes[state]()
    #
    # # Now `instances` dictionary contains all the created instances
    # print(instances)





    with sm:
        # Patrol inspection mode
        patrol_sm = smach.StateMachine(outcomes=['patrol_sm_done'])
        with patrol_sm:

            # Regular routine state machine container
            regular_routine = smach.StateMachine(outcomes=['regular_routine_done', 'problem_detected'])
            with regular_routine:
                smach.StateMachine.add('Nav1', Nav,
                                       transitions={'succeeded': 'LookFor_patrol1', 'preempted': 'problem_detected'})
                smach.StateMachine.add('LookFor_patrol1', LookFor_patrol,
                                       transitions={'succeeded': 'Nav2', 'preempted': 'problem_detected'})
                smach.StateMachine.add('Nav2', Nav,
                                       transitions={'succeeded': 'LookFor_patrol2', 'preempted': 'problem_detected'})
                smach.StateMachine.add('LookFor_patrol2', LookFor_patrol,
                                       transitions={'succeeded': 'Nav3', 'preempted': 'problem_detected'})
                smach.StateMachine.add('Nav3', Nav,
                                       transitions={'succeeded': 'LookFor_patrol3', 'preempted': 'problem_detected'})
                smach.StateMachine.add('LookFor_patrol3', LookFor_patrol,
                                       transitions={'succeeded': 'Nav4', 'preempted': 'error_state'})
                smach.StateMachine.add('Nav4', Nav,
                                       transitions={'succeeded': 'LookFor_patrol4','preempted': 'problem_detected'})
                smach.StateMachine.add('LookFor_patrol4', LookFor_patrol,
                                       transitions={'succeeded': 'regular_routine_done','preempted': 'problem_detected'})

            patrol_con = smach.Concurrence(outcomes=['regular_done', 'problem_detected'],
                                           default_outcome='regular_done',
                                           child_termination_cb=patrol_con_child_term_cb,
                                           outcome_cb=patrol_con_out_cb)
            with patrol_con:
                smach.Concurrence.add('REGULAR_ROUTINE', regular_routine)
                smach.Concurrence.add('MONITOR_PROBLEM',
                                      smach_ros.MonitorState('/env_detection_error', Bool, env_detection_error_cb))

            # Problem handling state machine container
            problem_handling = smach.StateMachine(outcomes=['problem_handling_done'])
            with problem_handling:
                smach.StateMachine.add('Pick', Pick,
                                       transitions={'succeeded': 'Nav4'})
                smach.StateMachine.add('Nav4', Nav_er,
                                       transitions={'succeeded': 'Place'})
                smach.StateMachine.add('Place', Place,
                                       transitions={'succeeded': 'problem_handling_done'})

            smach.StateMachine.add('PATROL_CON', patrol_con,
                                   transitions={'regular_done': 'patrol_sm_done', 'problem_detected': 'PROBLEM_HANDLING'})
            smach.StateMachine.add('PROBLEM_HANDLING', problem_handling,
                                   transitions={'problem_handling_done': 'PATROL_CON'})
###
        # Serve Mode
        serve_sm = smach.StateMachine(outcomes=['serve_sm_done'])
        with serve_sm:
            smach.StateMachine.add('Nav_serve1', Nav_serve, transitions={'succeeded': 'Pick'})
            smach.StateMachine.add('Pick', Pick, transitions={'succeeded': 'Nav_serve2'})
            smach.StateMachine.add('Nav_serve2', Nav_serve, transitions={'succeeded': 'Place'})
            smach.StateMachine.add('Place', Place, transitions={'succeeded': 'serve_sm_done'})

        # Create a Concurrence container for continuous emergency stop monitoring
        monitor_con = smach.Concurrence(outcomes=['emergency', 'normal'],
                                        default_outcome='normal',
                                        outcome_map={
                                            'emergency': {'EMERGENCY_MONITOR': 'invalid'},
                                            'normal': {'EMERGENCY_MONITOR': 'valid'}
                                        })

        with monitor_con:
            smach.Concurrence.add('EMERGENCY_MONITOR',
                                  smach_ros.MonitorState('/emergency_stop_topic', Bool, emergency_cb))

            main_sm = smach.StateMachine(outcomes=['overall_succeeded', 'overall_failed'])
            # Create a Concurrence container for parallel execution
            con = smach.Concurrence(outcomes=['patrol', 'serve'],
                                    default_outcome='patrol',
                                    outcome_map={
                                        'serve': {
                                            'MONITOR_SPEECH': 'valid',
                                            'MONITOR_WAVE': 'valid',
                                            # 'MONITOR_PROBLEM': 'invalid',
                                            # 'PROBLEM_SOLVED': 'valid'
                                        },
                                        'patrol': {
                                            'MONITOR_SPEECH': 'invalid',
                                            'MONITOR_WAVE': 'invalid',
                                            # 'MONITOR_PROBLEM': 'valid',
                                            # 'PROBLEM_SOLVED': 'invalid'
                                        }
                                    }
                                    )
            with con:
                smach.Concurrence.add('MONITOR_SPEECH',
                                      smach_ros.MonitorState('/speech_recognition_bool',
                                                             Bool,
                                                             speech_cb))
                smach.Concurrence.add('MONITOR_WAVE',
                                      smach_ros.MonitorState('/waving_hand_bool',
                                                             Bool,
                                                             wave_cb))
                # smach.Concurrence.add('MONITOR_PROBLEM',
                #                       smach_ros.MonitorState('/env_detection_error',
                #                                              Bool,
                #                                              problem_detected_cb))
                # smach.Concurrence.add('PROBLEM_SOLVED',
                #                       smach_ros.MonitorState('/problem_solved',
                #                                              Bool,
                #                                              problem_solved_cb))  # place done means problem solved
            with main_sm:
                smach.StateMachine.add('CHECK_MODE', con, transitions={'patrol': 'PATROL_INSPECTION', 'serve': 'SERVE'})
                smach.StateMachine.add('PATROL_INSPECTION', patrol_sm, transitions={'patrol_sm_done': 'CHECK_MODE'})
                smach.StateMachine.add('SERVE', serve_sm, transitions={'serve_sm_done': 'CHECK_MODE'})

            smach.Concurrence.add('MAIN_SM', main_sm)

        smach.StateMachine.add('MONITOR_CON', monitor_con, transitions={'emergency': 'EMERGENCY_STOP', 'normal': 'overall_succeeded'})
        smach.StateMachine.add('EMERGENCY_STOP', EmergencyStop(), transitions={'stopped': 'emergency_stopped'})

    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    outcome = sm.execute()
    rospy.loginfo('execute')
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node('state_machine')
    rospy.set_param('/need_help', False)
    env_detection_pub = rospy.Publisher('/env_detection_command', Bool, queue_size=10)
    # env_detection_error_sub = rospy.Subscriber('/env_detection_error', Bool, env_detection_error_cb)
    # pub the place that the item should be placed
    env_detection_error_string = rospy.Subscriber('/env_detection_error_string', String, env_detection_error_string_cb)
    listen_sub = rospy.Subscriber('/gspeech/speech', String, speech_cb)
    gpt_response_sub = rospy.Subscriber('/openai/response', String, gpt_response_cb)
    grasp_target_name_pub = rospy.Publisher('/grasp_target_name', String, queue_size=10)
    pick_done_sub = rospy.Subscriber('/pick_done', Bool, pick_done_cb)
    place_pose_pub = rospy.Publisher('/place_pos',PoseStamped, queue_size=10)
    place_done_sub = rospy.Subscriber('/place_done', Bool, place_done_cb)
    problem_solved_sub = rospy.Subscriber('/problem_solved', Bool, problem_solved_cb)



    main()
    # rospy.loginfo("Waiting for GPT response...")
    rospy.spin()


"""
# error detected
rostopic pub -1 /env_detection_error std_msgs/Bool 'False' 

rostopic pub -1 /emergency_stop std_msgs/Bool 'False'

# when the person needs help
rosparam set /need_help 'True' && rostopic pub -1 /need_help_monitor std_msgs/Bool 'False'  

# transfer the item 
rosparam set /tasks '[['look_for', 'None'], ['Listen', 'None'], ['AudioOutput', 'None'], ['move', 'storage'], ['grab', 'bottle'], ['move', 'my_location'], ['release', 'bottle']]'


"""
