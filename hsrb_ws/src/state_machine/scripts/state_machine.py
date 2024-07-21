import rospy
import smach
import subprocess
import smach_ros
import smach_viewer

from dataclasses import dataclass, field
from std_msgs.msg import String, Bool

from typing import List

"""
Two Modes:
Patrol inspection
Serve



Middle Flexible States:
Navigation/ Look For/ Pick/ Place/Listen + Analyze/ Audio Output/ Follow
Read from config in the future

Fixed States:

Start/ End/ Emergency Stop/ waitForNewCmd

Start: always at the beginning
End: always at the end

Listen and Analyze  can be combined into one state

Listen: when the speech is recognized, 
waitForNewCmd: include a position initialization

Patrol inspection(MODE): check the environment and recover the environment

-----------------------------------------------------------------------------------------------------------------------
|      Previous State             |             Current State                |                 Next State              |
-----------------------------------------------------------------------------------------------------------------------
|         None                    |                 Start                    |                 Nav or Listen           |
-----------------------------------------------------------------------------------------------------------------------
|         Start or Audio Output  |                 Listen  + Analyze         |               Look For or Audio Output  |
-----------------------------------------------------------------------------------------------------------------------
|         Start or Pick           |                 Nav                    |Look For (object or pose or count) or Place|
-----------------------------------------------------------------------------------------------------------------------
|         Nav                     |                 Look For                  |        Pick or Listen or Place or Nav  |
-----------------------------------------------------------------------------------------------------------------------
|         Look For                |                 Pick                       |                     Nav               |
-----------------------------------------------------------------------------------------------------------------------
|         Nav                    |                 Place                      |                     End            `   |
-----------------------------------------------------------------------------------------------------------------------
|         Start or Nav             |      Listen + Analyze                     |                Audio Output           |
-----------------------------------------------------------------------------------------------------------------------
|         Listen + Analyze          |             Audio Output                 |                  Nav                  |
-----------------------------------------------------------------------------------------------------------------------
|         Nav                   |     Count(may be considered as Look for)   |                  Nav                  |
-----------------------------------------------------------------------------------------------------------------------
|Count(may be considered as Look for)|               Nav                      |                 Audio Output           |
-----------------------------------------------------------------------------------------------------------------------
|         Nav                     |                 Audio Output               |                  End                  |
-----------------------------------------------------------------------------------------------------------------------
|           Audio Output             |              Follow                     |                  End                   |
-----------------------------------------------------------------------------------------------------------------------
|     Place or Follow or Audio out |                 End                      |                  End                   |
-----------------------------------------------------------------------------------------------------------------------
"""


# class stateDescription:
@dataclass
class stateDescription:
    """
    struct stateDescription{
        string stateName;
        list<string> preRequisite;
        list<string> postRequisite;
        }
    """
    stateName: str
    preRequisite: List[str] = field(default_factory=list)
    postRequisite: List[str] = field(default_factory=list)


# TODO: read from config file
start = stateDescription("start",
                         ["None"],
                         ["Nav", "Listen"])
Nav = stateDescription("Nav",
                       ["Start", "Pick", "Look For", "Audio Output", "Count"],
                       ["Look For", "Place", "Audio Output"])
LookFor = stateDescription("Look For",
                           ["Nav"],
                           ["Pick", "Listen", "Place", "Nav"])
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
                               ["Listen", "Nav", "Look For"],  # look for person
                               ["Nav", "End"])
Follow = stateDescription("Follow",
                          ["Audio Output"],
                          ["End"])
End = stateDescription("End",
                       ["Place", "Follow", "Audio Output"],
                       ["None"])


# class for generating states
class stateMachineGenerator(smach.State):
    """
     Constructor for the state machine generator
     :param pre_requisite: list of pre_requisite states for state matching
     :param post_requisite: list of post_requisite states for state matching
     """

    def __init__(self, state_description):
        self.lpreRequsite = state_description.preRequisite
        self.lpostRequsite = state_description.preRequisite
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])

    def check_pre_requisite(self):

        return

    def execute(self):
        command = ["ros run", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'


# Define start state
class startState(smach.State):  # TODO: Consider open door as start signal
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])
        self.sD = stateDescription("startState",
                                   ["None"],
                                   ["NextState"])  # TODO: decide the next states

    def execute(self):
        command = ["ros run", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'


# Define end state
class endState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])
        self.sD = stateDescription("endState",
                                   ["PreviousState"],  #TODO: decide the previous state
                                   ["None"])

    def execute(self):
        command = ["ros run", "pkg", "node.py"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'


# TODO: use get param to get the state list, where the state list is from GPT
stateList = rospy.get_param('stateList')


def stateOdering(stateList):
    """
    Function to order the states in a state machine
    :param stateList: list of stateDescriptions
    :return: list of ordered stateDescriptions
    """
    stateList_ordered = []
    return stateList_ordered


# Define a function to check for speech recognition results
def speech_cb(userdata, msg):
    return msg.data != ""


# Define a function to check for waving hands
def wave_cb(userdata, msg):
    return msg.data


def problem_detected_cb(userdata, msg):
    return msg.data


def problem_solved_cb(userdata, msg):
    return msg.data


def main():
    rospy.init_node('state_machine')
    sm = smach.StateMachine(outcomes=['overall succeeded', 'overall failed'])
    # create state descriptions
    sD_A = stateDescription("stateA",
                            ["a", "b", "c"],
                            ["d", "e", "f"])
    sD_B = stateDescription("stateB",
                            ["a", "b", "c"],
                            ["d", "e", "f"])
    sD_C = stateDescription("stateC",
                            ["a", "b", "c"],
                            ["d", "e", "f"])
    sD_D = stateDescription("stateD",
                            ["a", "b", "c"],
                            ["d", "e", "f"])
    sD_E = stateDescription("stateE",
                            ["a", "b", "c"],
                            ["d", "e", "f"])

    # create instances of stateMachineGenerator
    STATE_A = stateMachineGenerator(sD_A)
    STATE_B = stateMachineGenerator(sD_B)
    STATE_C = stateMachineGenerator(sD_C)
    STATE_D = stateMachineGenerator(sD_D)
    STATE_E = stateMachineGenerator(sD_E)

    state_list = [sD_A, sD_B, sD_C, sD_D, sD_E]
    # Create the top level state machine
    with sm:
        # Patrol inspection mode
        patrol_sm = smach.StateMachine(outcomes=['done'])
        with patrol_sm:
            """
            nav -> look for(check the environment) -> once find different -> pick -> nav -> place
            """
            regular_routine = smach.Sequence(outcomes=['done'],  # FIXME: sequence? Normal?
                                             connecter_outcome='done')

            with regular_routine:
                smach.Sequence.add('Nav', STATE_A)  # TODO: change to the real state
                smach.Sequence.add('Look For', STATE_B)
                smach.Sequence.add('Pick', STATE_C)
                smach.Sequence.add('Nav', STATE_D)
                smach.Sequence.add('Place', STATE_E)

            # Problem handling branch
            problem_handling = smach.StateMachine(outcomes=['done'])

            with problem_handling:
                smach.StateMachine.add('Nav', STATE_A,  # TODO: change to the real state
                                       transitions={'done': 'Pick'})
                smach.StateMachine.add('Pick', STATE_B,  # TODO: change to the real state
                                       transitions={'done': 'Nav'})
                smach.StateMachine.add('Nav', STATE_C,  # TODO: change to the real state
                                       transitions={'done': 'Place'})
                smach.StateMachine.add('Place', STATE_D,  # TODO: change to the real state
                                       transitions={'done': 'done'})

            # Concurrence container to manage regular routine and problem detection
            patrol_con = smach.Concurrence(outcomes=['regular_done', 'problem_detected'],
                                           default_outcome='regular_done',
                                           outcome_map={
                                               'problem_detected': {'MONITOR_PROBLEM': 'invalid'},
                                               'regular_done': {'MONITOR_PROBLEM': 'valid'}
                                           }
                                           )
            with patrol_con:
                smach.Concurrence.add('REGULAR_ROUTINE', regular_routine)
                smach.Concurrence.add('MONITOR_PROBLEM',
                                      smach_ros.MonitorState('/problem_detection_topic', Bool, problem_detected_cb))

            smach.StateMachine.add('PATROL_CON', patrol_con,
                                   transitions={'regular_done': 'done', 'problem_detected': 'PROBLEM_HANDLING'})
            smach.StateMachine.add('PROBLEM_HANDLING', problem_handling,
                                   transitions={'done': 'PATROL_CON'})

        # Serve Mode
        serve_sm = smach.StateMachine(outcomes=['done'])
        with serve_sm:
            """
            listen or look for(waving hands) -> nav -> listen -> audio output -> nav -> pick or follow -> nav -> place -> end
            """
            smach.StateMachine.add('Nav', STATE_A,  # TODO: change to the real state
                                   transitions={'done': 'Pick'})
            smach.StateMachine.add('Pick', STATE_B,  # TODO: change to the real state
                                   transitions={'done': 'Nav'})
            smach.StateMachine.add('Nav', STATE_C,  # TODO: change to the real state
                                   transitions={'done': 'Place'})
            smach.StateMachine.add('Place', STATE_D,  # TODO: change to the real state
                                   transitions={'done': 'done'})

            # for sub-states
            # TODO: change the state above in to the format below
            state_list_ordered = stateOdering(state_list)
            for state in state_list_ordered:
                smach.StateMachine.add(state.stateName, stateMachineGenerator(state),
                                       transitions={'succeeded': 'succeeded',
                                                    'failed': 'failed'})

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

        # Main state machine
        smach.StateMachine.add('CHECK_MODE', con,
                               transitions={'patrol': 'PATROL_INSPECTION',
                                            'serve': 'SERVE'})
        smach.StateMachine.add('PATROL_INSPECTION', patrol_sm,
                               transitions={'done': 'CHECK_MODE'})
        smach.StateMachine.add('SERVE', serve_sm,
                               transitions={'done': 'CHECK_MODE'})

    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    outcome = sm.execute()
    rospy.spin()
    if outcome == 'overall succeeded':
        print("Overall succeeded")
    else:
        print("Overall failed")


if __name__ == "__main__":
    stateA = stateDescription("stateA",
                              ["a", "b", "c"],
                              ["d", "e", "f"])
    print('stateA', stateA)
    print('stateA.stateName', stateA.stateName)
    print('stateA.preRequisite', stateA.preRequisite)
    print('stateA.postRequisite', stateA.postRequisite)

    stateB = stateDescription("stateB",
                              ["a", "b", "c"],
                              ["d", "e", "f"])

    test = [stateA, stateB]
    print('test', test)
    print('test[0]', test[0])
    print('test[1]', test[1])
