from machine import Pin, PWM
class Servo:
    # these defaults work for the standard TowerPro SG90
    __servo_pwm_freq = 50
    __min_u16_duty = 1640 # offset for correction
    __max_u16_duty = 7864  # offset for correction
    min_angle = -90
    max_angle = 90    
    current_angle = 0.001
    desired_angle = 0.001
    motor_speed = 0.06
    
    
    def __init__(self, pin):
        self.__initialise(pin)
        
        
    def update_settings(self, servo_pwm_freq, min_u16_duty, max_u16_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u16_duty = min_u16_duty
        self.__max_u16_duty = max_u16_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)
        
    def interpolate(self, angle, speed = 0.04):
        self.desired_angle = angle
        self.motor_speed = speed
        
    def is_busy(self):
        return self.current_angle != self.desired_angle
        
    def update(self):
        if(self.current_angle > self.desired_angle):
            self.current_angle -= self.motor_speed
        else:
            self.current_angle += self.motor_speed
        
        if(abs(self.current_angle - self.desired_angle) < self.motor_speed):
            self.current_angle = self.desired_angle
        
        self.move(self.current_angle)
        
    def move(self, angle):
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u16 = self.__angle_to_u16_duty(angle)        
        self.__motor.duty_u16(duty_u16)
        
        
    def __angle_to_u16_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u16_duty
    
    
    def __initialise(self, pin):
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u16_duty - self.__min_u16_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)
