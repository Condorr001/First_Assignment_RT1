# First_Assignment_RT1
 First assignment of the Research Track 1 course of the Robotics Engineering master, at UniGe. 
 Made by Valentina Condorelli, S4945679.


# Simulator and graphics

For the graphic part of this project, a 2D simulator was provided, along with different pictures that are used to create the background and spawn the various objects in the field. The main object belonging to the simulator is the **robot**, which has an associated class called **Robot()**. To know more about the simulator, the Robot() class and the method it provides, please check the following repo, provided by our professor: https://github.com/CarmineD8/python_simulator. In the `README.md` file, you can find all the details about the simulator.

The reference for this project is the `assignment23_python3` branch of the professor repo. 

# First assignment
## Introduction

The first assignment of Research Track 1 consists of writing a Python node that controls the robot such that it brings all the **golden tokens** near one of them, called the **reference token**. Therefore, the robot should define one token as the reference, move all the other tokens close to it and stop.
### How to run the program
To run the program, please:
- Clone this repo
- Move into the `robot-sim` folder
- Open the terminal in there
- Type `$ python3 run.py assignment1_Condorelli.py`

## The field
After the program is launched, you should see the field organized as follows:
- Robot in the top left corner of the field
- 6 golden tokens, positioned in a circle
- A silver square at the center of the field, called the *arena*
### Generality

This is the configuration provided for this assignment, but the code was made to be as general as possible. Therefore, the robot should be able to complete its task even with different configurations. In order to achieve that, at the start of the program, the robot makes an almost 360° turn on itself and all the tokens it detects are saved in a list. Since the robot can see all the tokens in the field that are strictly in front of it, this procedure guarantees that all the tokens are seen.

## Constants
The program is based on the following constants:
- *a_th*: threshold for the control of the orientation. This value is used to check the orientation of the center of the robot with respect to (w.r.t.) the token it's moving to. 
As provided, a_th = 2.0: this means that the robot is aligned with the token if the orientation of its center differs from the token position of at max 2.0;
- *b_th*: threshold for the control of the linear distance. This value is used to check the linear distance of the center of the robot w.r.t. the token it's moving to. 
As provided, d_th = 0.4, since the distance between the center of the robot and its arm is 0.4 meters. This means that the robot is near to the token and can grab it if the distance between its center and the token is at max 0.4m.

## Functions
A total of 4 functions were declared for this prgram. Using functions is the best procedure to avoid long and repeated blocks of code.

The first two functions had already been implemented in previous exercises. They are:
- `drive(speed, seconds)`: move the robot forwards or backwards according to the given linear `speed` for the defined amount of `seconds`;
- `turn(speed, seconds)`: turn the robot on itself by setting an angular velocity, defined by the `speed` value, for the defined amount of `seconds`.

Please note that, for the amount of `seconds` passed to the function, the program **sleeps**. Therefore, it's impossible to implement an action during those seconds.

The third function is partially inspired to a similar function used in the previous exercises, but has some differences. This is:
- `find_golden_token()`: find the closest golden token to the robot. If a token is found, return:
	- *dist*: the linear distance between the token and the center of the robot;
	- *rot_y*: the orientation of the center of the robot w.r.t. the token
	- *token_code*: the unique code of the token

The last returned value was add for this specific context. Indeed, it is necessary to have the unique identifier of a token in order to add it to the necessary lists only if it wasn't already found previously.

The last function was created during this assignment and it behaves as follows:
- `find_first_token()`: find the reference token and return:
 	- *dist*: the linear distance between the reference token and the center of the robot;
	- *rot_y*: the orientation of the center of the robot w.r.t. the reference token

This function is used each time the robot has grabbed a token and needs to move it close to the reference token.

Lastly, it has to be mentioned that both `find_golden_token()` and `find_first_token()` ise the function `R.see()` of the Robot() class. Check the professor repo for detailed information about this function.

## Flowchart
The following flowchart summarized the behaviour of the program:

![alt text](https://github.com/Condorr001/First_Assignment_RT1/blob/main/robot-sim/flowchart/assignment_1_flowchart.png)


## Further Improvements
This program can be improved in a few ways. First of all, the general movement of the robot is slow: this is necessary has nothing can be done while the robot is moving due to the `sleep()` function used in `move()` and `turn()`.
Secondly and lastly, it would be more efficient and elegant to move the reference token to the center of the arena, so that all the tokens are grouped at the center. In this particular example, the efficiency would improve, as all the tokens are placed in a circle with the arena as its center.
