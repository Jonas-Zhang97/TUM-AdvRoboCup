import numpy as np
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



#######################################################################################################################
# States declaration
#######################################################################################################################

# Create Serve State:
class ServeState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted'])
        self.first_speak = True

    def task_planner(self, task):
        if task[0]== 'look_for': # TODO
            rospy.loginfo('look for state')
            rospy.sleep(3)
            return 'substate_succeeded'
            pass
        elif task[0] == 'Listen':
            rospy.loginfo('Listen state')
            rospy.sleep(3)
            speech_received = rospy.get_param('/gspeech/speech_received')
            while not speech_received:
                rospy.loginfo('Waiting for speech')
                speech_received = rospy.get_param('/gspeech/speech_received')
            if speech_received:
                rospy.set_param('/gspeech/speech_received', False)
                return 'substate_succeeded'

        elif task[0] == 'AudioOutput': #TODO in subprocess call format
            rospy.loginfo('AudioOutput state')
            rospy.sleep(3)
            command  = ["rosrun", "gtts_tts", "gtts_tts_node.py", "text:=Hello"]
            process = subprocess.call(command)
            rospy.sleep(3)
            return 'substate_succeeded'
            pass

        elif task[0] == 'move':
            current_room_name = task[1]
            rospy.loginfo('move state')
            rospy.sleep(3)
            # TODO set the nav location dictionary which located in hsrb_navigation/config/goals.yaml
            command = ["roslaunch", "hsrb_navigation", "send_goal.launch", f"room_name:={current_room_name}"]
            process = subprocess.call(command)
            if process == 0:
                return 'substate_succeeded'
            else:
                return 'substate_failed'


        elif task[0] == 'grab':
            rospy.loginfo('grab state')
            info_flag = False
            rospy.sleep(3)
            rospy.set_param('/pick_done', False) # init the pick done flag
            pick_done_ = rospy.get_param('/pick_done')
            item_name = task[1]
            grasp_target_name_pub.publish(item_name)
            while not pick_done_:
                if not info_flag:
                    rospy.loginfo("Waiting for pick node to finish")
                    info_flag = True
                pick_done_ = rospy.get_param('/pick_done')
            if pick_done_:  # No problem publish true
                return 'substate_succeeded'



        elif task[0] == 'release':
            rospy.loginfo('release state')
            rospy.sleep(3)
            info_flag = False
            rospy.set_param('/place_done', False)
            place_done_ = rospy.get_param('/place_done')
            # TODO set the place location and orientation
            euler = np.array([0, 0, 30])
            quaternion = quaternion_from_euler(euler[0], euler[1], euler[2])
            place_pose = PoseStamped()
            place_pose.pose.position.x = 3.9
            place_pose.pose.position.y = 1.48
            place_pose.pose.position.z = 0.8
            place_pose.pose.orientation.x = quaternion[0]
            place_pose.pose.orientation.y = quaternion[1]
            place_pose.pose.orientation.z = quaternion[2]
            place_pose.pose.orientation.w = quaternion[3]
            place_pose_pub.publish(place_pose)
            while not place_done_:
                if not info_flag:
                    rospy.loginfo("Waiting for place node to finish")
                    info_flag = True
                place_done_ = rospy.get_param('/place_done')
            if place_done_:  # No problem publish true
                return 'substate_succeeded'

    def execute(self, userdata):
        rospy.loginfo("Executing Serve State")
        tasks = rospy.get_param('/tasks')
        while tasks != []:
            if self.preempt_requested():
                print ("state serve is being preempted!!!")
                self.service_preempt()
                return 'preempted'
            result = self.task_planner(tasks.pop(0))
            if result == 'substate_succeeded':
                continue
            # else:
            #     return 'preempted'
        return 'succeeded'


# Create State for patrol:
class NavState_patrol(smach.State): # Done # for patral
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted'])
        self.room_name = ['goal1', 'kitchen', 'workroom', 'storage']

    def execute(self, userdata):
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
        smach.State.__init__(self, outcomes=['succeeded', 'preempted'])


    def execute(self, userdata):
        if self.preempt_requested():
            print("state Nav_er is being preempted!!!")
            self.service_preempt()
            return 'preempted'
        item_place = rospy.get_param('/env_detection/should_place')  # FIXME set the rosparam in the env_detection node
        command = ["roslaunch", "hsrb_navigation", "send_goal.launch", f"room_name:={item_place}"]
        process = subprocess.call(command)
        if process == 0:
            return 'succeeded'
        else:
            return 'failed'



class LookFor_State_patrol(smach.State): # patrol  # FIXME
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted'])
        self.bool = None
    def execute(self, userdata):
        if self.preempt_requested():
            print("state LookFor is being preempted!!!")
            self.service_preempt()
            return 'preempted'
        info_flag = False
        rospy.set_param('/env_detection/detection_done', False)  # init the error flag
        env_detection_pub.publish(True)  # start the env detection
        if_detection_done = rospy.get_param('/env_detection/detection_done')
        while not if_detection_done:
            if not info_flag:
                rospy.loginfo("Waiting for env detection")
                info_flag = True
            if_detection_done = rospy.get_param('/env_detection/detection_done')

        if if_detection_done:
            return 'succeeded'




class Look_and_Pick_State_patrol(smach.State): # find, segment, pick # Done
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted'])

    def execute(self, userdata):
        if self.preempt_requested():
            print("state Pick is being preempted!!!")
            self.service_preempt()
            return 'preempted'

        item_name = rospy.get_param('/env_detection/error_obj')

        rospy.loginfo('Pick_patrol')
        info_flag = False
        rospy.sleep(3)
        rospy.set_param('/pick_done', False)  # init the pick done flag
        pick_done_ = rospy.get_param('/pick_done')
        grasp_target_name_pub.publish(item_name)
        while not pick_done_:
            if not info_flag:
                rospy.loginfo("Waiting for pick node to finish")
                info_flag = True
            pick_done_ = rospy.get_param('/pick_done')
        if pick_done_:  # No problem publish true
            return 'succeeded'


class PlaceState_patrol(smach.State): # done
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


class chooseMode(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['patrol', 'serve', 'preempted'])

    def execute(self, userdata):
        rospy.loginfo("Choose mode")
        if self.preempt_requested():
            print("state foo is being preempted!!!")
            self.service_preempt()
            return 'preempted'
        need_help = rospy.get_param('/need_help')
        if need_help:
            rospy.set_param('/need_help', False) # Reset the need_help flag
            return 'serve'
        else:
            return 'patrol'


#######################################################################################################################
# Callback functions
#######################################################################################################################
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
    return msg.data




def place_done_cb(userdata,msg):
    place_done = msg.data
    return place_done


def env_detection_error_string_cb(msg):  # FIXME msg is string? name?
    result = msg.data
    rospy.loginfo('AudioOutput')
    rospy.sleep(3)
    command = ["rosrun", "gtts_tts", "gtts_tts_node.py", f"text:={result}"]
    process = subprocess.call(command)
    rospy.sleep(3)
    # FIXME for tts
    return result


def need_help_monitor_cb(userdata, msg):
    return msg.data


def emergency_stop_cb(userdata, msg):
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
    elif outcome_map['MONITOR_PROBLEM'] == 'invalid':
        print("patrol_con_child_term_cb: problem_detected")
        return True # preempt other states, jump out of the concurrence
    elif outcome_map['NEED_HELP'] == 'invalid':
        print("patrol_con_out_cb: need_help")
        return True  # preempt other states, jump out of the concurrence
    else:
        print("patrol_con_child_term_cb: any other situation, also preempt")
        return True

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
    elif outcome_map['NEED_HELP'] == 'invalid':
        print("patrol_con_out_cb: need_help")
        return 'regular_done'
    elif outcome_map['MONITOR_PROBLEM'] == 'invalid':
        print("patrol_con_out_cb: problem_detected")
        return 'problem_detected'
    else:
        print("patrol_con_out_cb: patrol_preempted")
        return 'patrol_con_preempted'

def emergency_con_child_term_cb(outcome_map):
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
    print("emergency_con_child_term_cb")
    if outcome_map['MAIN_SM'] == 'overall_succeeded':
        print("emergency_con_child_term_cb: overall_succeeded")
        return True  # preempt other states, jump out of the concurrence
    elif outcome_map['MAIN_SM'] == 'overall_preempted':
        print("emergency_con_child_term_cb: overall_preempted")
        return True
    elif outcome_map['EMERGENCY_STOP'] == 'invalid':
        print('emergency_con_child_term_cb: emergency')
        return True  # preempt other states, jump out of the concurrence
    else:
        print("patrol_con_child_term_cb: any other situation, also preempt")
        return True

def emergency_con_out_cb(outcome_map):
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
    print("emergency_con_out_cb")
    if outcome_map['MAIN_SM'] == 'overall_succeeded':
        print("emergency_con_out_cb: overall_succeeded")
        return 'normal'
    elif outcome_map['MAIN_SM'] == 'overall_preempted':
        print("emergency_con_out_cb: overall_preempted")
        return 'emergency'
    elif outcome_map['EMERGENCY_STOP'] == 'invalid':
        print('emergency_con_out_cb: emergency')
        return 'emergency'
    else:
        print("emergency_con_out_cb: regular_done")
        return 'normal'
# Main function
def main():



    Nav = NavState_patrol()

    LookFor_patrol = LookFor_State_patrol()
    Pick = Look_and_Pick_State_patrol()
    Place = PlaceState_patrol()

    Nav_er = NavState_error_handling()
    error_state = errorState()
    CHOOSEMODE = chooseMode()
    serve_state = ServeState()

    # Create the top-level state machine
    sm = smach.StateMachine(outcomes=['overall_succeeded', 'overall_failed', 'emergency_stopped'])

    with sm:
        # Patrol inspection mode
        patrol_sm = smach.StateMachine(outcomes=['patrol_sm_done', 'patrol_sm_preempted'])
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
                                       transitions={'succeeded': 'Nav4', 'preempted': 'problem_detected'})
                smach.StateMachine.add('Nav4', Nav,
                                       transitions={'succeeded': 'LookFor_patrol4', 'preempted': 'problem_detected'})
                smach.StateMachine.add('LookFor_patrol4', LookFor_patrol,
                                       transitions={'succeeded': 'regular_routine_done',
                                                    'preempted': 'problem_detected'})

            patrol_con = smach.Concurrence(outcomes=['regular_done', 'problem_detected', 'patrol_con_preempted'],
                                           default_outcome='regular_done',
                                           child_termination_cb=patrol_con_child_term_cb,
                                           outcome_cb=patrol_con_out_cb)
            with patrol_con:
                smach.Concurrence.add('REGULAR_ROUTINE', regular_routine)
                smach.Concurrence.add('MONITOR_PROBLEM',
                                      smach_ros.MonitorState('/env_detection_error', Bool, env_detection_error_cb))
                smach.Concurrence.add('NEED_HELP',
                                      smach_ros.MonitorState('/need_help_monitor', Bool, need_help_monitor_cb))
            # Problem handling state machine container
            problem_handling = smach.StateMachine(outcomes=['problem_handling_done', 'problem_handling_preempted'])
            with problem_handling:
                smach.StateMachine.add('Pick', Pick,
                                       transitions={'succeeded': 'Nav4', 'preempted': 'problem_handling_preempted'})
                smach.StateMachine.add('Nav4', Nav_er,
                                       transitions={'succeeded': 'Place', 'preempted': 'problem_handling_preempted'})
                smach.StateMachine.add('Place', Place,
                                       transitions={'succeeded': 'problem_handling_done',
                                                    'preempted': 'problem_handling_preempted'})

            smach.StateMachine.add('PATROL_CON', patrol_con,
                                   transitions={'regular_done': 'patrol_sm_done',
                                                'problem_detected': 'PROBLEM_HANDLING',
                                                'patrol_con_preempted': 'patrol_sm_preempted'})
            smach.StateMachine.add('PROBLEM_HANDLING', problem_handling,
                                   transitions={'problem_handling_done': 'PATROL_CON',
                                                'problem_handling_preempted': 'patrol_sm_preempted'})

        ###
        # Serve Mode
        serve_sm = smach.StateMachine(outcomes=['serve_sm_done', 'serve_sm_preempted'])
        with serve_sm:
            smach.StateMachine.add('SERVE_STATE', serve_state,
                                   transitions={'succeeded': 'serve_sm_done', 'preempted': 'serve_sm_preempted'})

        main_sm = smach.StateMachine(outcomes=['overall_succeeded', 'overall_preempted'])

        with main_sm:
            smach.StateMachine.add('CHOOSE_MODE', CHOOSEMODE,
                                   transitions={'patrol': 'PATROL_INSPECTION', 'serve': 'SERVE',
                                                'preempted': 'overall_preempted'})
            smach.StateMachine.add('PATROL_INSPECTION', patrol_sm, transitions={'patrol_sm_done': 'CHOOSE_MODE',
                                                                                'patrol_sm_preempted': 'overall_preempted'})
            smach.StateMachine.add('SERVE', serve_sm, transitions={'serve_sm_done': 'CHOOSE_MODE',
                                                                   'serve_sm_preempted': 'overall_preempted'})

        emergency_con = smach.Concurrence(outcomes=['emergency', 'normal'],
                                          default_outcome='normal',
                                          child_termination_cb=emergency_con_child_term_cb,
                                          outcome_cb=emergency_con_out_cb)

        with emergency_con:
            smach.Concurrence.add('MAIN_SM', main_sm)
            smach.Concurrence.add('EMERGENCY_STOP', smach_ros.MonitorState('/emergency_stop', Bool,
                                                                           emergency_stop_cb))

        smach.StateMachine.add('EMERGENCY_CON', emergency_con,
                               transitions={'emergency': 'RESET', 'normal': 'overall_succeeded'})
        smach.StateMachine.add('RESET', EmergencyStop(), transitions={'succeeded': 'EMERGENCY_CON'})

    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    outcome = sm.execute()
    rospy.loginfo('execute')
    rospy.spin()


if __name__ == "__main__":
    rospy.init_node('state_machine')
    rospy.set_param('/need_help', False)
    env_detection_pub = rospy.Publisher('/env_detection_command', Bool, queue_size=10) # start the detection
    # env_detection_error_sub = rospy.Subscriber('/env_detection_error', Bool, env_detection_error_cb)
    # pub the place that the item should be placed
    env_detection_error_string = rospy.Subscriber('/env_detection_error_string', String, env_detection_error_string_cb)
    listen_sub = rospy.Subscriber('/gspeech/speech', String, speech_cb)
    gpt_response_sub = rospy.Subscriber('/openai/response', String, gpt_response_cb)
    grasp_target_name_pub = rospy.Publisher('/grasp_target_name', String, queue_size=10)
    place_pose_pub = rospy.Publisher('/place_pos',PoseStamped, queue_size=10)

    # problem_solved_sub = rospy.Subscriber('/problem_solved', Bool, problem_solved_cb)  ?



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
