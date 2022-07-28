from machine import Pin, UART, PWM
import time
import _thread
from sys import stdin
from servo import Servo
from kinematics import Kinematics


class DoubleServo:
    def __init__(self, pin1, pin2):
        self.motor1 = Servo(pin1)
        self.motor2 = Servo(pin2)
        
    def interpolate(self, angle):
        self.motor1.interpolate(angle)
        self.motor2.interpolate(-angle)
        
    def move(self, angle):
        self.motor1.move(angle)
        self.motor2.move(-angle)
        
    def update(self):
        self.motor1.update()
        self.motor2.update()
        
rotation_offset = 9
shoulder_offset = -94
elbow_offset = 103
align_offset = -21

position = [-18, 7, 3.2]

curr_rot = -18
curr_y = 7
curr_z = 2.9

rotation = Servo(15)
shoulder = DoubleServo(14, 13)
elbow = Servo(11)
align = Servo(12)

kinematics = Kinematics()

rotation.move(0)
shoulder.move(0)
elbow.move(0)
align.move(-90)

# Turn the LED on
def switch():
    global led_state
    led_state = not led_state
    led.value(led_state)

def closer(n, desired_n, step):
    if(abs(n - desired_n) <= step):
        n = desired_n
    if(n > desired_n):
        n -= step
    elif(n < desired_n):
        n += step
    
    return n

def InterpolationThread():
    global shoulder, elbow, align, rotation
    global curr_rot, curr_y, curr_z
    
    while True:
        
        curr_rot = closer(curr_rot, position[0], 0.08)
        curr_y = closer(curr_y, position[1], 0.01)
        curr_z = closer(curr_z, position[2], 0.01)
        
        result = kinematics.calc(curr_y, curr_z)
        
        rotation.interpolate(curr_rot + rotation_offset)
        shoulder.interpolate(result[0] / 3.14159 * 180 + shoulder_offset)
        elbow.interpolate(result[1] / 3.14159 * 180 + elbow_offset)
        align.interpolate(result[2] / 3.14159 * 180 + align_offset)
        
        rotation.update()
        shoulder.update()
        elbow.update()
        align.update()
        
        time.sleep_ms(1)

enterLowPosRight = [-18, 6.5, 1.2]
lowPosRight = [-18, 15, 0.5]
enterMiddlePosRight = [-18, 6.5, 2]
middlePosRight = [-18, 14.5, 2]
enterUpperPosRight = [-18, 6.5, 3.4]
upperPosRight = [-18, 14.5, 3.3]
exitPosRight = [-18, 15, 9.5]

enterLowPosMiddle = [1.3, 5.5, 1.3]
lowPosMiddle = [1.3, 13.5, 0.1]
enterMiddlePosMiddle = [1.3, 5.5, 2]
middlePosMiddle = [1.7, 12.5, 1.8]
enterUpperPosMiddle = [1.3, 5.5, 2.7]
upperPosMiddle = [1.3, 13.5, 2.7]
exitPosMiddle = [2.1, 13, 8]

enterLowPosLeft = [21, 6.5, 1]
lowPosLeft = [21, 13.5, 0.2]
intermediateFromLowPosLeft = [21, 13.5, 4]
intermediateFromExitPosLeft = [21, 15.5, 4]
enterMiddlePosLeft = [21, 7, 1.6]
middlePosLeft = [21, 13.5, 1.6]
enterUpperPosLeft = [21, 7.5, 2.7]
upperPosLeft = [21, 15.5, 2.7]
exitPosLeft = [21, 16.5, 8]

solve = [ enterUpperPosRight, upperPosRight, exitPosRight, exitPosLeft, upperPosLeft, enterUpperPosLeft, enterMiddlePosRight, middlePosRight, exitPosRight, exitPosMiddle, upperPosMiddle, enterUpperPosMiddle, enterLowPosLeft, lowPosLeft, intermediateFromLowPosLeft, intermediateFromExitPosLeft, exitPosLeft, exitPosMiddle, upperPosMiddle, enterUpperPosMiddle, enterLowPosMiddle, enterLowPosRight, lowPosRight, exitPosRight, exitPosLeft, intermediateFromExitPosLeft, intermediateFromLowPosLeft, lowPosLeft, enterLowPosLeft, enterMiddlePosMiddle, middlePosMiddle, exitPosMiddle, exitPosRight, upperPosRight, enterUpperPosRight, enterLowPosMiddle, lowPosMiddle, exitPosMiddle, exitPosLeft, upperPosLeft, enterUpperPosLeft, enterLowPosRight, lowPosRight, exitPosRight, exitPosLeft, upperPosLeft, enterUpperPosLeft, enterUpperPosMiddle ]

_thread.start_new_thread(InterpolationThread, ())

time.sleep_ms(5000)

cnt = 0
while cnt < len(solve):
    position = solve[cnt]
    
    print(position)
    
    if([curr_rot, curr_y, curr_z] == position):
        cnt += 1
        time.sleep_ms(1000)