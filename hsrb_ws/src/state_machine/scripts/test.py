import rospy
import smach
import smach_ros

from std_msgs.msg import Bool


"""
One Container, one monitor state in the concurrence container
rostopic pub -1 /sm_reset std_msgs/Bool 'False'
"""
class setup(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['setup_done'])
    def execute(self, userdata):
        rospy.sleep(3.5)
        return 'setup_done'

class foo(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['foo_succeeded', 'preempted'])
    def execute(self, userdata):
        for idx in range(5):
            if self.preempt_requested():
                print ("state foo is being preempted!!!")
                self.service_preempt()
                return 'preempted'
            rospy.sleep(1.0)
        return 'foo_succeeded'

def child_term_cb(outcome_map):
    """
    called after a child state has finished.
    A State Machine Container is also a child state!

        @type child_termination_cb: callale
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
    print('child_term_cb')
    if outcome_map['FOO_CALC'] == 'foo_calc_succeeded':
        print('result of FOO_CALC container is foo_calc_succeeded')
        return True  # preempt the state monitor because we only receive the flag once.
    elif outcome_map['FOO_RESET'] == 'invalid':
        print('result of FOO_RESET is invalid')
        return True
    else:
        print('else')
        return False

def out_cb(outcome_map):
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

        B{NOTE: This callback should be a function ONLY of the outcomes of
        the child states. It should not access any other resources.}
    """
    print('out_cb')
    if outcome_map['FOO_RESET'] == 'invalid':
        print('foo_reset')
        return 'foo_reset'
    elif outcome_map['FOO_CALC'] == 'foo_calc_succeeded':
        print('foo_done')
        return 'foo_done'
    else:
        print('auto reset')
        return 'foo_reset'

def monitor_cb(ud, msg):
    return msg.data

def main():
    foo1 = foo()
    foo2 = foo()
    foo3 = foo()
    rospy.init_node("preemption_example")

    foo_concurrence = smach.Concurrence(outcomes=['foo_done', 'foo_reset'],
                                        default_outcome='foo_done',
                                        child_termination_cb=child_term_cb,
                                        outcome_cb=out_cb)

    with foo_concurrence:
        sm_nested = smach.StateMachine(outcomes=['foo_calc_succeeded', 'preempted'])
        with sm_nested:
            smach.StateMachine.add('FOO_CALC1', foo1, transitions={'foo_succeeded':'FOO_CALC2', 'preempted':'preempted'})
            smach.StateMachine.add('FOO_CALC2', foo2, transitions={'foo_succeeded':'FOO_CALC3', 'preempted':'preempted'})
            smach.StateMachine.add('FOO_CALC3', foo3, transitions={'foo_succeeded':'foo_calc_succeeded', 'preempted':'preempted'})
        smach.Concurrence.add('FOO_CALC', sm_nested)
        smach.Concurrence.add('FOO_RESET', smach_ros.MonitorState("/sm_reset", Bool, monitor_cb))

    sm = smach.StateMachine(outcomes=['DONE'])
    with sm:
        smach.StateMachine.add('SETUP', setup(), transitions={'setup_done':'FOO'})
        smach.StateMachine.add('FOO', foo_concurrence, transitions={'foo_done':'BAR', 'foo_reset':'SETUP'})
        smach.StateMachine.add('BAR', foo(), transitions={'foo_succeeded':'FOO', 'preempted':'SETUP'})

    sis = smach_ros.IntrospectionServer('smach_server', sm, '/SM_ROOT')
    sis.start()
    sm.execute()
    rospy.spin()
    sis.stop()

if __name__=="__main__":
    
    # main()
    rospy.init_node("test")
    # from tf.transformations import quaternion_from_euler
    # from geometry_msgs.msg import PoseStamped
    # import numpy as np
    # place_pose_pub = rospy.Publisher('/place_pose',PoseStamped, queue_size=10)
    # euler = np.array([0, 0, 30])
    # quaternion = quaternion_from_euler(euler[0], euler[1], euler[2])
    # place_pose = PoseStamped()
    # place_pose.pose.position.x = 3.9
    # place_pose.pose.position.y = 1.48
    # place_pose.pose.position.z = 0.8
    # place_pose.pose.orientation.x = quaternion[0]
    # place_pose.pose.orientation.y = quaternion[1]
    # place_pose.pose.orientation.z = quaternion[2]
    # place_pose.pose.orientation.w = quaternion[3]
    # place_pose_pub.publish(place_pose)
    # print(place_pose)
    import subprocess
    result = "hello world"
    command = ["rosrun", "gtts_tts", "gtts_tts_rosrun.py", f"_sentence:='{result}'", "_language:='en'"]
    process = subprocess.call(command)
    print("published")

    # shut down the node
    rospy.signal_shutdown("test done")



    