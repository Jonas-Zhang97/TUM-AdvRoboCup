import rospy
import smach
import subprocess

from dataclasses import dataclass, field

from typing import List


"""
Middle Flexible States:
Navigation/ Look For/ Pick/ Place/Listen/ Audio Output/ 
Read from config in the future

Fixed States:
Start/ End/ Emergency Stop/ 

Listen: when the speech is recognized, 
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

