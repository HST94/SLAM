from math import pi
import rospy
from geometry_msgs.msg import Twist

class move_around():
    def __init__(self):
        rospy.init_node('outdoor_move', anonymous=False)
        rospy.on_shutdown(self.stop)
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.rate = 50
        self.r = rospy.Rate(self.rate)
        self.linear_speed = 0.1
        self.angular_speed = 1.0
        self.goal_angle = pi / 2
        self.angular_duration = self.goal_angle / self.angular_speed
        
    def go_forward(self):
        move_cmd = Twist()
        move_cmd.linear.x = self.linear_speed
        self.cmd_vel.publish(move_cmd)
    
    def turn_left(self):
        move_cmd = Twist()
        move_cmd.angular.z = self.angular_speed
        ticks = int(self.goal_angle * self.rate * 200)
        for t in range(ticks):
            self.cmd_vel.publish(move_cmd)
        move_cmd = Twist()
        self.cmd_vel.publish(move_cmd)

    def turn_right(self):
        move_cmd = Twist()
        move_cmd.angular.z = - self.angular_speed
        ticks = int(self.goal_angle * self.rate * 200)
        for t in range(ticks):
            self.cmd_vel.publish(move_cmd)
        move_cmd = Twist()
        self.cmd_vel.publish(move_cmd)

    def stop(self):
        move_cmd = Twist()
        self.cmd_vel.publish(move_cmd)

if __name__ == "__main__":
    twist = move_around()
    while True:
        s = raw_input("Input: ")
        if s == "start":
            twist.go_forward()
        elif s == "left":
            twist.turn_left()
        elif s == "right":
            twist.turn_right()

