"""!
@file closed_loop_controller.py
This file contains code that will implement the associated motor_driver and encoder_reader .py files
for use with step_control.py to visually plot step responses with proportional gains.

@author mecha02 (Kishor Natarajan, Candice Espitia, Vinayak Sharath)
@date   12-Mar-2024 
"""

import encoder_reader as enc
import motor_driver as moe
import utime

class control:
    """! 
    This class implements the necessary code to implement a motor controller
    for an ME405 kit. 
    """
    def __init__(self):
        """! 
        Initializes the proportional gain and setpoint values.
        """
        self.gain = 0
        self.setpoint = 0
        
        # Used for the step response function:
        self.state = 0
        self.steady_counter = 0
        self.print_counter = 0
        self.init_time = 0
        self.position = []
        self.duty_cycle = 0
        self.prev_cycle = 0
    
    def set_setpoint(self, user_p):
        """! 
        Setting the setpoint to be a fixed value for repeated testing
        @param user_p gain given by whatever is calling the function
        """
        self.setpoint = user_p
  
    def set_Kp(self, user_p):
        """! 
        Function that will set the gain for the proportional control loop
        @param user_p gain given by the program
        """
        
        # Sets controller gain to user_p
        self.gain = float(user_p)
        

    def run(self, actual):
        """!
        Function that will be run repeatedly in the main loop to implement
        a control scheme that is a function of the current motor position,
        the desired setpoint, and the user input gain.
        @param actual the current position of the motor read by the encoder
        @returns the duty cycle to be fed into the motor driver
        """
        
        # Equation
        pwm = self.gain*(self.setpoint - actual)
        return pwm
    
    def cl_loop_response(self, motor, encoder, controller, setpoint):
        """!
        Function that runs the step response for the motor. This function
        implements a finite-state-machine and class variables to keep track of 
        what the program needs to do. Near the end of the function, the program
        prints the step response in .CSV-style format to plotting purposes.
        @param motor motor driver object running the motor
        @param encoder encoder object returning the position of the motor
        @param controller controller object responsible for running functions within class
        @param gain gain needed for following run
        @returns indication of whether step response is done
        """
        # State 0: Step-response
        if self.state == 0:
            controller.set_setpoint(setpoint)
            # Continuously runs the step response with a delay of 10 ms ...
            actual = encoder.read()
            self.duty_cycle = controller.run(actual)
            motor.set_duty_cycle(self.duty_cycle)
            self.position.append(actual)
            
            # ... until the set motor position is reached
            if abs(self.duty_cycle) <= 25:
                self.state += 1
                return True
               
        
        # State 1: Resetting Values
        # Resetting Encocder and position values before running another 
        # step response
        elif self.state == 1: 
            self.position.clear()
            encoder.zero()
            self.state = 0
            
            

if __name__ == "__main__":
    # Code needed to initialize motor
    en_pin = pyb.Pin(pyb.Pin.board.PC1, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value = 1)
    a_pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    another_pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    m_timer = pyb.Timer(5, freq=5000)
    chm1 = m_timer.channel(1, pyb.Timer.PWM, pin=a_pin)
    chm2 = m_timer.channel(2, pyb.Timer.PWM, pin=another_pin)
    
    # Motor Initialization done through imported MotorDriver class
    motor = moe.MotorDriver(en_pin,a_pin,another_pin,m_timer,chm1,chm2)
    
    # Code needed to initialize encoder. Set 'tim' to the correct timer
    # for the pins being used.
    tim = 4
    timer = pyb.Timer(tim, prescaler = 0, period = 65535)
    
    # Depending on the timer used, the code will automatically
    # initialize the correct channel and pins. For example, if the timer
    # used is '4', then the B6/B7 pins will be initialized. In this test code,
    # C6/C7 is used.
    if tim == 4:
        ch1 = timer.channel(1,pyb.Timer.ENC_A,pin = pyb.Pin.board.PB6)
        ch2 = timer.channel(2, pyb.Timer.ENC_B,pin = pyb.Pin.board.PB7)
    
    elif tim == 8:
        ch1 = timer.channel(1,pyb.Timer.ENC_A,pin = pyb.Pin.board.PC6)
        ch2 = timer.channel(2, pyb.Timer.ENC_B,pin = pyb.Pin.board.PC7)
    else:
        print("invalid timer")
    
    # Initializes Encoder
    encoder = enc.encoder(timer,ch1,ch2)          
    
    # Initializes Motor Controller
    controller = control()
       
#     controller.set_setpoint(60800)
    controller.set_Kp(1.2)
    position = []
    encoder.zero()
    
    while True:
        controller.cl_loop_response(motor, encoder, controller, -65500)