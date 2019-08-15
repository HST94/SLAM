#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
import os, sys


class GoToPose():
    points = dict()
    def __init__(self):
        self.goal_sent = False
	# What to do if shut down (e.g. Ctrl-C or failure)
	rospy.on_shutdown(self.shutdown)
	# Tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("Wait for the action server to come up")
	# Allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))
        self.cfg_path = "/home/hh/HiDOG/points/points.cfg"

    def load_cfg(self):
        if os.path.isfile(self.cfg_path):
            cfg_file = open(self.cfg_path, mode="r+")#, encoding='UTF-8')
        else:
            cfg_file = open(self.cfg_path, mode='a+')#, encoding='UTF-8')
            cfg_file.write("#Every line is a point, CFG File Format :\n")
            cfg_file.write("#bed is on (x,y), you may write in bed:(x,y) ")

        for line in cfg_file.readlines():
            line = line.strip()
            if (not len(line)):
                continue
            elif line[0] == '#':
                continue
            self.points[line.split(':')[0]] = eval(line[line.find(':')+1:])
        cfg_file.close()
        print self.points

    def goto(self, pos, quat):
        # Send a goal
        self.goal_sent = True
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))
	# Start moving
        self.move_base.send_goal(goal)
	# Allow TurtleBot up to 120 seconds to complete task
	success = self.move_base.wait_for_result(rospy.Duration(120)) 
        state = self.move_base.get_state()
        result = False
        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()
        self.goal_sent = False
        return result
    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)

def go_somewhere(dest):
    point = dest
    try:
        print "Go Start"
        # rospy.init_node('go_to_point', anonymous=False)
        navigator = GoToPose()
        navigator.load_cfg()
        loaded_points = navigator.points
        # Customize the following values so they are appropriate for your location
        position = {'x': loaded_points[point][0], 'y':loaded_points[point][1]}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Reached the desired pose")
        else:
            rospy.loginfo("The base failed to reach the desired pose")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")


if __name__ == '__main__':
    point = sys.argv[-1]
    go_somewhere(point)
