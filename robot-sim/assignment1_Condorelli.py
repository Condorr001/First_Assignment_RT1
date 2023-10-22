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


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

n_tokens = 0
""" int: number of tokens detected at the beginning of the program"""

list_found_token = []
""" list: list of found golden token at the beginning of the program """

list_moved_token = []
""" list: list of moved golden token so that they won't be picked up twice """

firsttoken = False
""" boolean: check if I need to detect the first golden token to reach it"""

holding = False
""" boolean: check if the robot is holding a token"""

R = Robot()
""" instance of the class Robot"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: 
    - speed (int): the speed of the wheels
    - seconds (int): the time interval for which the robot should move
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: 
    - speed (int): the speed of the wheels
    - seconds (int): the time interval for which the robot should move
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
        dist (float): distance of the closest golden token (-1 if no golden token is detected)
        rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
        token_code (int): numeric code of the token
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            if token.info.code in list_moved_token:
                return -1, -1, token.info.code
            dist = token.dist
            rot_y = token.rot_y
            token_code = token.info.code
    if dist == 100:
        return -1, -1, -1
    else:
        return dist, rot_y, token_code

def find_first_token(first_token_code):
    """
    Function to find the position of the first (reference) token

    Returns:
        dist (float): distance of the first token (-1 if it is not detected)
        rot_y (float): angle between the robot and the first token(-1 if it is not detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.code == first_token_code:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

for i in range(11):
    print("Looking for tokens")
    turn(10, 1)
    markers = R.see()
    for m in markers:
        if m.info.code not in list_found_token:
            list_found_token.append(m.info.code)

print(len(list_found_token), " token found")

while 1:
    #at the beginning of the program, the if condition is true so that the first token can be detected and saved in the list
    if not firsttoken:
        dist, rot_y, token_code = find_golden_token()
    else:
        dist, rot_y = find_first_token(list_moved_token[0])

    #if the list is empty, add the code of the detected token to the list and use it as the reference for the repositioning of all other tokens
    if not list_moved_token:
        list_moved_token.append(token_code)

    else:
        if dist == -1:  # if no token is detected, we make the robot turn
            print("No token detected. Adjusting my orientation")
            turn(10, 1)

        elif dist < d_th:  # if we are close to the token
            print("Token detected")
            #if the robot is not holding a token, it means it reached it to grab it
            if not holding:
                if R.grab():  # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
                    print("Token grabbed")
                    holding = True
                    firsttoken = True
                    d_th = 0.8
                else:
                    print("Golden token still too far to be grabbed")

            #if the robot is holding a token, it means it reached the reference one and needs to release the token it is holding
            else:
                R.release()
                drive(-10, 2) #move backwards
                #turn(30, 2) #turn about 180° to reposition to find the next token

                if token_code not in list_moved_token:
                    list_moved_token.append(token_code)

                holding = False
                firsttoken = False
                d_th = 0.4

        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Orientation set. Moving towards the token")
            drive(20, 0.5)

        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Turning left to align with the center of the token")
            turn(-2, 0.5)

        elif rot_y > a_th:
            print("Turning right to align with the center of the token")
            turn(2, 0.5)

        if len(list_found_token) == len(list_moved_token):
            turn(0, 0.5)
            print("Task completed")
            break