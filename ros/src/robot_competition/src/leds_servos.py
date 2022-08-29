#!/usr/bin/env python3
#coding=utf-8

import rospy
import numpy as np
import math
#import RPi.GPIO as GPIO
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovariance
from geometry_msgs.msg import Pose


# Pin Definitions

# PWM pin
output_pins = {
    'JETSON_XAVIER': 18,
    'JETSON_NANO': 33,
    'JETSON_NX': 33,
    'CLARA_AGX_XAVIER': 18,
    'JETSON_TX2_NX': 32,
    'JETSON_ORIN': 18,
}
"""
output_pwm = output_pins.get(GPIO.model, None)
if output_pwm is None:
    raise Exception('PWM not supported on this board')

# Board pin-numbering scheme
GPIO.setmode(GPIO.BOARD)

# Set pin as an output pin with optional initial state of LOW
GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)
p = GPIO.PWM(output_pin, 50) # frecuency 50Hz
p.start(50) # 50% of duty cycle means half position

# LED pin
#output_pin = 12  # BCM pin 18, BOARD pin 12
#GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH) # Set pin as an output pin with optional initial state of HIGH --- High is OFF
"""
def laserData(msg):
    obsDetec(140, 220, 0.2, msg)


def odomData(msg):
    robot_orientation = msg.pose.pose.orientation
    servo(robot_orientation)

    
def obsDetec(initialAngle, finalAngle, obsDistance, msg):
    lidar_min_angle_rad   = msg.angle_min
    lidar_max_angle_rad   = msg.angle_max
    lidar_angle_incre_rad = msg.angle_increment
    distances = msg.ranges

    iniAngle = np.deg2rad(initialAngle)
    finAngle = np.deg2rad(finalAngle)
    ini_index = int((iniAngle - lidar_min_angle_rad) / lidar_angle_incre_rad)
    fin_index = int((finAngle - lidar_min_angle_rad) / lidar_angle_incre_rad)

    count = 0
    for i in range(ini_index,fin_index):
        if distances[i] <= obsDistance:
            count = count + 1

    if count >= (fin_index-ini_index)/2:
        print("LED ON")
        #GPIO.output(output_pin, GPIO.LOW)

    else:
        print("LED OFF")
        #GPIO.output(output_pin, GPIO.HIGH)


def servo(orientation):
    roll, pitch, yaw = euler_from_quaternion(orientation.x, orientation.y, orientation.z, orientation.w)
    percent = angle2percent(yaw)
    print(percent)
    #p.ChangeDutyCycle(percent)



def angle2percent(angle):
    percent = (5/90)*np.rad2deg(angle) + 2
    return percent


def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    rospy.init_node('objectives')
    rospy.Subscriber("/scan", LaserScan, laserData, queue_size=1)
    rospy.Subscriber("/odom", Odometry, odomData, queue_size=1)
    rospy.spin()
