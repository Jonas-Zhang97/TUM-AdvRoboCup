import rospy
import smach
import subprocess

from dataclasses import dataclass, field

from typing import List


"""
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
                            [ "Audio Output"],
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
    def __init__(self,state_description):
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
class startState(smach.State):# TODO: Consider open door as start signal
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'failed'])
        self.sD = stateDescription("startState",
                                   ["None"],
                                   ["NextState"]) # TODO: decide the next states

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
                                   ["PreviousState"], #TODO: decide the previous state
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

    with sm:
        state_list_ordered = stateOdering(state_list)
        for state in state_list_ordered:
            smach.StateMachine.add(state.stateName, stateMachineGenerator(state),
                                   transitions={'succeeded': 'succeeded',
                                                'failed': 'failed'})

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
    print('stateA',stateA)
    print('stateA.stateName',stateA.stateName)
    print('stateA.preRequisite',stateA.preRequisite)
    print('stateA.postRequisite',stateA.postRequisite)

    stateB = stateDescription("stateB",
                              ["a", "b", "c"],
                                ["d", "e", "f"])


    test = [stateA, stateB]
    print('test',test)
    print('test[0]',test[0])
    print('test[1]',test[1])

