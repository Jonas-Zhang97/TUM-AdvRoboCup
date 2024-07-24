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


# Global variables
states_list = None
main_executed = False
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

LookFor = stateDescription("Look For",
                           ["Nav"],
                           ["Pick", "Place", "Nav"])

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

class NavState(smach.State): # TODO
    def __init__(self, room_name):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])
        self.room_name = room_name

    def execute(self, userdata):
        command = ["roslaunch", "hsrb_navigation", "send_goal.launch", f"room_name:={self.room_name}"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'

class LookForState(smach.State): # patrol # Done
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])

    def execute(self, userdata):
        env_detection_pub.publish(True)
        bool = env_detection_error_cb
        if bool:  # No problem publish true
            return 'succeeded'
        else:  # Problem detected publish false
            return 'failed'

class PickState(smach.State): # call SAM # TODO
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])

    def execute(self, userdata):
        command = ["rosrun", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'

class PlaceState(smach.State): # TODO
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])

    def execute(self, userdata):
        command = ["rosrun", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'


class ListenState(smach.State):  # Done
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])
        self.sr_result = ''
    def execute(self, userdata):

        self.sr_result = speech_cb
        if self.sr_result != '':
            return 'succeeded'
        else:
            return 'failed'

class AudioState(smach.State): # TODO
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])

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
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])
        self.sD = stateDescription("endState", ["PreviousState"], ["None"])

    def execute(self, userdata):
        command = ["rosrun", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'

# Emergency stop state
class EmergencyStop(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['stopped'])

    def execute(self, userdata):
        rospy.loginfo("Emergency Stop Activated!")
        return 'stopped'

# Callback functions
def speech_cb(userdata, msg):
    return msg.data != ""

def wave_cb(msg):
    return msg.data

def problem_detected_cb(msg):
    return msg.data

def problem_solved_cb(msg):
    return msg.data

def emergency_cb(msg):
    return not msg.data  # Trigger emergency stop when msg.data is True

def env_detection_error_cb(msg):
    return msg.data

def speech_cb(msg):
    return msg.data

def gpt_response_cb(msg):
    global states_list, main_executed
    if not main_executed:
        # Step 1: Extract the list part of the string
        list_part = msg.data.split('=')[1].strip()

        # Step 2: Remove the square brackets
        list_part = list_part.strip('[]')

        # Step 3: Split the string into individual elements
        elements = list_part.split(',')

        # Step 4: Strip any extra whitespace from each element
        states_list = [element.strip() for element in elements]
        rospy.loginfo("State list: %s", states_list)
        main()
    return states_list
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


    with sm:
        # Patrol inspection mode
        patrol_sm = smach.StateMachine(outcomes=['patrol_sm_done'])
        with patrol_sm:
            regular_routine = smach.StateMachine(outcomes=['regular_routine_done'])
            with regular_routine:
                smach.StateMachine.add('Nav1', STATE_A, transitions={'succeeded': 'LookFor'})
                smach.StateMachine.add('LookFor', STATE_B, transitions={'succeeded': 'Pick'})
                smach.StateMachine.add('Pick', STATE_C, transitions={'succeeded': 'Nav2'})
                smach.StateMachine.add('Nav2', STATE_D, transitions={'succeeded': 'Place'})
                smach.StateMachine.add('Place', STATE_E, transitions={'succeeded': 'regular_routine_done'})

            problem_handling = smach.StateMachine(outcomes=['problem_handling_done'])
            with problem_handling:
                smach.StateMachine.add('Nav3', STATE_A, transitions={'succeeded': 'Pick'})
                smach.StateMachine.add('Pick', STATE_B, transitions={'succeeded': 'Nav4'})
                smach.StateMachine.add('Nav4', STATE_C, transitions={'succeeded': 'Place'})
                smach.StateMachine.add('Place', STATE_D, transitions={'succeeded': 'problem_handling_done'})

            patrol_con = smach.Concurrence(outcomes=['regular_done', 'problem_detected'],
                                           default_outcome='regular_done',
                                           outcome_map={
                                               'problem_detected': {'MONITOR_PROBLEM': 'invalid'},
                                               'regular_done': {'MONITOR_PROBLEM': 'valid', 'REGULAR_ROUTINE': 'regular_routine_done'}
                                           })
            with patrol_con:
                smach.Concurrence.add('REGULAR_ROUTINE', regular_routine)
                smach.Concurrence.add('MONITOR_PROBLEM', smach_ros.MonitorState('/env_detection_error', Bool, env_detection_error_cb))

            smach.StateMachine.add('PATROL_CON', patrol_con, transitions={'regular_done': 'patrol_sm_done', 'problem_detected': 'PROBLEM_HANDLING'})
            smach.StateMachine.add('PROBLEM_HANDLING', problem_handling, transitions={'problem_handling_done': 'PATROL_CON'})

        # Serve Mode
        serve_sm = smach.StateMachine(outcomes=['serve_sm_done'])
        with serve_sm:
            smach.StateMachine.add('Nav5', STATE_A, transitions={'succeeded': 'Pick'})
            smach.StateMachine.add('Pick', STATE_B, transitions={'succeeded': 'Nav6'})
            smach.StateMachine.add('Nav6', STATE_C, transitions={'succeeded': 'Place'})
            smach.StateMachine.add('Place', STATE_D, transitions={'succeeded': 'serve_sm_done'})

            # state_list_ordered = stateOrdering(state_list)
            # for state in state_list_ordered:
            #     smach.StateMachine.add(state.stateName, stateMachineGenerator(state), transitions={'succeeded': 'succeeded', 'failed': 'failed'})

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
                                            'MONITOR_SPEECH': 'invalid',
                                            'MONITOR_WAVE': 'invalid',
                                            'PROBLEM_DETECTED': 'invalid',
                                            'PROBLEM_SOLVED': 'valid'
                                        },
                                        'patrol': {
                                            'MONITOR_SPEECH': 'valid',
                                            'MONITOR_WAVE': 'valid',
                                            'PROBLEM_DETECTED': 'valid',
                                            'PROBLEM_SOLVED': 'invalid'
                                        }
                                    }
                                    )
            with con:
                smach.Concurrence.add('MONITOR_SPEECH',
                                      smach_ros.MonitorState('/speech_recognition_topic',
                                                             String,
                                                             speech_cb))
                smach.Concurrence.add('MONITOR_WAVE',
                                      smach_ros.MonitorState('/waving_hand_topic',
                                                             Bool,
                                                             wave_cb))
                smach.Concurrence.add('PROBLEM_DETECTED',
                                      smach_ros.MonitorState('/problem_detected_topic',
                                                             Bool,
                                                             problem_detected_cb))
                smach.Concurrence.add('PROBLEM_SOLVED',
                                      smach_ros.MonitorState('/problem_solved_topic',
                                                             Bool,
                                                             problem_solved_cb))
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
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node('state_machine')

    env_detection_pub = rospy.Publisher('/env_detection_command', Bool, queue_size=10)
    env_detection_error_sub = rospy.Subscriber('/env_detection_error', Bool, env_detection_error_cb)
    listen_sub = rospy.Subscriber('/gspeech/speech', String, speech_cb)
    gpt_response_sub = rospy.Subscriber('/openai/response', String, gpt_response_cb)

    rospy.loginfo("Waiting for GPT response...")
    rospy.spin()

