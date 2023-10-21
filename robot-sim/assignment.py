from __future__ import print_function

import time
from sr.robot import *

"""
Assignment 1 Research Track 1 - Valentina Condorelli S4945679

The first assignment of RT1 consists of making the robot compute the following steps: 
	- 1) find and grab the closest golden marker (token)
	- 2) move the marker to the center of the Arena marker
	- 3) find and grab the next closest golden marker (token)
	- 4) move the marker and release it near the marker found in step 2
	- 5) start again from 1 and repeat until all the golden markers are placed near each other (in this case, at the center of the Arena)

To run the program, type:
	$ python3 run.py assignment1_Condorelli.py

"""

#defining all the variables needed for the program
a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

list_found_token = []

#defining the functions needed to control the robot
def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: 
    - speed (int): speed of the wheels
    - seconds (int): the time interval for which the robot should move
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    #stop the robot after seconds
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    This makes the robot turn on itself
    
    Args: 
    - speed (int): speed of the wheels
	- seconds (int): the time interval for which the robot should move
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    #stop the robot after seconds
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	- dist (float): distance of the closest golden token (-1 if no golden token is detected)
	- rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)

    The method see() of the class Robot returns an object whose attribute info.marker_type is, in this case, MARKER_TOKEN_GOLD (since there are only golden markers)
    """
    dist=100 #radius of robot sight
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            #check if the marker has already been moved
            if token.info.code in list_found_token:
                return -1, -1
            dist=token.dist
	        rot_y=token.rot_y
            list_found_token.append(token.info.code) #add the marker to the moved list
    #if the distance has not been modified, it means that no token was detected
    if dist==100:
	    return -1, -1
    else:
   	    return dist, rot_y

def find_arena_token():
    """
    Function to find the arena token

    Returns:
	- dist (float): distance of the center of the arena (-1 if no golden token is detected)
	- rot_y (float): angle between the robot and the center of the arena (-1 if no golden token is detected)

    The method see() of the class Robot returns an object whose attribute info.marker_type is, in this case, MARKER_TOKEN_GOLD or MARKER_ARENA
    """
    dist=100 #radius of robot sight
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_ARENA:
            dist=token.dist
	        rot_y=token.rot_y
    #if the distance has not been modified, it means that no token was detected
    if dist==100:
	    return -1, -1
    else:
   	    return dist, rot_y

def go_to_token(gen_dist, gen__rot_y):
    """
    Function to move towards the arena or the token positioned at its center
    """
    #adjust the position of the robot and move towards the arena up until the robot is close enough
    while gen_dist > d_th:
        if -a_th <= gen_rot_y <= a_th:
            printf("Aligned with the center of the token. Moving towards it")
            drive(10, 0.5)
        elif gen_rot_y < -a_th:
            printf("Turning left to align with the center of the token")
            turn(-2, 0.5)
        elif gen_rot_y > a_th:
            printf("Turning right to align with the center of the token")
            turn(2, 0.5)
    R.release()
    turn(50, 2) #turn 180° degrees

R = Robot()

#CODE BEGINS

#the first golden token should be found and positioned at the center of the arena outside the loop, since the behaviour of the robot is different in this case
dist_first_token, rot_y_first_token = find_golden_token()

#check whether the token was found
while dist == -1:
    printf("No token detected. Adjusting my orientation")
    turn(10, 1)
#adjust the position of the robot and move towards the token up until the robot is close enough
while dist > d_th:
    if -a_th <= rot_y <= a_th:
        printf("Aligned with token. Moving towards it")
        drive(10, 0.5)
    elif rot_y < -a_th:
        printf("Turning left to align with the token")
        turn(-2, 0.5)
    elif rot_y > a_th:
        printf("Turning right to align with the token")
        turn(2, 0.5)

printf("I am next to the golden token")
#if the token is successfully grabbed, move it towards the main token at the center of the arena
if(R.grab()):
    printf("Golden token grabbed")
    dist_arena, rot_y_arena = find_arena_token()
    #check whether the token was found
    while dist_arena == -1:
        printf("Arena not detected. Adjusting my orientation")
        turn(10, 1)
    go_to_token(dist_arena, rot_y_arena)
else:
    printf("Not close enough to grab the golden token")

#begin with the loop to find all the other golden token and move them close to the first one
while 1:
    #find the nearest golden token
    dist, rot_y = find_golden_token()

    #check whether the token was found
    if dist == -1:
        printf("No token detected. Adjusting my orientation")
        turn(10, 1)
    #if the token is near, go grab it
    elif dist < d_th:
        printf("Golden token detected")
        #if the token is successfully grabbed, move it towards the main token at the center of the arena
        if(R.grab()):
            printf("Golden token grabbed")
            go_to_token(dist_first_token, rot_y_first_token)
        else:
            printf("Not close enough")
    elif -a_th<= rot_y <= a_th:
	print("Aligned with token. Moving towards it")
        drive(10, 0.5)
    elif rot_y < -a_th:
        print("Turning left to align with the token")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Turning right to align with the token")
        turn(+2, 0.5)
