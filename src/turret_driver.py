"""!
@file turret_driver.py
This file contains code that controls the panning axis motor. This file contains 
multiple states of the motor that are run when certain conditions are met.

@author mecha02 (Kishor Natarajan, Candice Espitia, Vinayak Sharath)
@date   12-Mar-2024 
"""

import utime
import encoder_reader as enc
import motor_driver as moe
import closed_loop_controller as closed
import pyb

class turret_driver:
    """! 
    This class implements the necessary code to run the panning axis motor. 
    """
    
    def __init__(self):
        """! 
        Initializes the appropriate motor driver ports, state values, and more.
        """
        
        # Code needed to initialize motor
        en_pin = pyb.Pin(pyb.Pin.board.PC1, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value = 1)
        a_pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
        another_pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
        m_timer = pyb.Timer(5, freq=5000)
        chm1 = m_timer.channel(1, pyb.Timer.PWM, pin=a_pin)
        chm2 = m_timer.channel(2, pyb.Timer.PWM, pin=another_pin)
        
        # Motor Initialization done through imported MotorDriver class
        self.turret = moe.MotorDriver(en_pin,a_pin,another_pin,m_timer,chm1,chm2)
        
        # Code needed to initialize encoder. 
        tim = 4
        timer = pyb.Timer(tim, prescaler = 0, period = 65535)
        ch1 = timer.channel(1,pyb.Timer.ENC_A,pin = pyb.Pin.board.PB6)
        ch2 = timer.channel(2, pyb.Timer.ENC_B,pin = pyb.Pin.board.PB7)

        # Initializes Encoder (Turret)
        self.tur_enc = enc.encoder(timer,ch1,ch2)          
        
        # Initializes Motor Controller (Turret)
        self.tur_con = closed.control()
        
        # Variable used to indicate whether the motor has reached its desired setpoint
        self.pos = False
        
        # Gain value for motor controller 
        self.gain = 0.045
        self.tur_con.set_Kp(self.gain)
        self.tur_enc.zero()
        
        # Encoder setpoint value for motor controller
        self.position = 65500
        
        # Indication of the state in the task
        self.state = 0
        
        
    def step_test(self, sensor_data):
        """! 
        Controls the behavior of the panning axis motor. 
        @param sensor_data degrees in which turret needs to turn to aim at target
        @returns degrees the panning axis needs to turn to aim at target
        """
        
        # State 0: 180-degree turn
        # Turns panning axis exactly 180 degrees to start the duel
        if self.state == 0:
            self.pos = self.tur_con.cl_loop_response(self.turret, self.tur_enc, self.tur_con, self.position)
            
            # Once turret has turned 180 degrees, set next state
            if self.pos == True:
                self.state += 1 
                self.pos = False
                
        # State 1: Idle state 1
        # Waits until data is received from sensor
        elif self.state == 1:
            
            # Once received, set next state
            if sensor_data != 0:
                self.state += 1 

        # State 2: Data processing
        # Process sensor data to meaningful encoder setpoint
        elif self.state == 2:
            # Converts degree to encoder ticks
            self.position = int((sensor_data - 400)*(65500/180))
            
            # If target is to the left of sensor's center
            if self.position < 0:
                self.state += 1
                self.tur_con.set_Kp(self.gain)
                self.tur_enc.zero()
                
            # If target is to the right of sensor's center
            elif self.position > 0:
                self.state += 1
                self.tur_enc.zero()
                self.tur_con.set_Kp(self.gain)
            
            # If target is directly in front of the sensor
            else: 
                self.state += 2
                self.tur_enc.zero()
                self.tur_con.set_Kp(self.gain)
                
        # State 3: Turning to target
        # Turns turret towards target
        elif self.state == 3:
            self.pos = self.tur_con.cl_loop_response(self.turret, self.tur_enc, self.tur_con, self.position)
            
            # Once target is aimed at, set next state
            if self.pos == True:
                self.state += 1 
                self.pos = False
                
        # State 4: Send indication to actuator
        # Sends indication to linear actuator to shoot bullet
        elif self.state == 4:
            return 1
            self.state += 1

## Code to test functionality     
if __name__ == "__main__":
    tur = turret_driver()
    while True:
        try:
            tur.step_test(-8.284675)
            utime.sleep_ms(10)
        except KeyboardInterrupt:
            break