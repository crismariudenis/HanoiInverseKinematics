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

curr_rot = 0
curr_y = 15
curr_z = 17.5

rot = 0
y = 15
z = 17.5

rotation = Servo(15)
shoulder = DoubleServo(14, 13)
elbow = Servo(11)
align = Servo(12)

kinematics = Kinematics()

rotation.move(0)
shoulder.move(0)
elbow.move(0)
align.move(0)

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
    global curr_rot, curr_y, curr_z, rot, y, z
    
    while True:
        
        curr_rot = closer(curr_rot, rot, 0.08)
        curr_y = closer(curr_y, y, 0.01)
        curr_z = closer(curr_z, z, 0.01)
        
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

_thread.start_new_thread(InterpolationThread, ())

while True:
    position = stdin.readline()
    print(position)
    position = position.split()
    print(position)
    result = []
    if(len(position) == 4 and position[0] == 'go'):
        rot = float(position[1])
        y = float(position[2])
        z = float(position[3])
        
    if(len(position) == 2 and position[0] == 'shoulder'):
        shoulder.interpolate(float(position[1]))
        
    if(len(position) == 2 and position[0] == 'elbow'):
        elbow.interpolate(float(position[1]))
            
    if(len(position) == 2 and position[0] == 'align'):
        align.interpolate(float(position[1]))
            
    if(len(position) == 2 and position[0] == 'rotation'):
        rotation.interpolate(float(position[1]))
        



