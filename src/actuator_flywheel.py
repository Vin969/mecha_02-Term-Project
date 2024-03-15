"""!
@file actuator_flywheel.py
This file contains code that controls the linear actuator and flywheel system
present in the design. This file contains multiple states of the linear actuator
that are run when certain conditions are met.

@author mecha02 (Kishor Natarajan, Candice Espitia, Vinayak Sharath)
@date   12-Mar-2024 
"""

import utime
import motor_driver as moe
import pyb

class actuator_driver:
    """! 
    This class implements the necessary code to run the linear actuator. 
    """
    
    def __init__(self):
        """! 
        Initializes the appropriate motor driver ports, state values, and counter.
        """
        
        # Code needed to initialize linear actuator motor
        en_pin = pyb.Pin(pyb.Pin.board.PA10, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value = 1)
        a_pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
        another_pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
        m_timer = pyb.Timer(3, freq=5000)
        chm1 = m_timer.channel(1, pyb.Timer.PWM, pin=a_pin)
        chm2 = m_timer.channel(2, pyb.Timer.PWM, pin=another_pin)
        
        # Motor Initialization done through imported MotorDriver class
        self.actuator = moe.MotorDriver(en_pin,a_pin,another_pin,m_timer,chm1,chm2)
        
        # Indication of the state in the task
        self.state = 0
        
        # Counter used for time based tasks
        self.counter = 0
        
        
    def act_test(self, pan_lock):
        """! 
        Controls the behavior of the linear actuator. 
        @param pan_lock indication of whether turret is aiming at target
        """
        
        # State 0: Idle state 1
        # Actuator is idle for an arbitrary amount of time
        if self.state == 0:
            self.counter += 1
            
            # After 10 iterations, moves onto next state
            if self.counter == 10:
                self.state += 1 
                self.counter = 0
                
        # State 1: Priming state
        # Actuator pushes bullet right before it touches flywheel
        # Speeds up the process of shooting, due to the fact that the actuator is
        # very slow
        elif self.state == 1:
            # Actuator extends
            self.actuator.set_duty_cycle(100)
            self.counter += 1
            
            # Stops after 35 iterations
            if self.counter == 35:
                self.state += 1 
                self.counter = 0
                self.actuator.duty_zero()
        
        # State 2: Idle state 2        
        # Actuator is idle until the turret is aiming at the target
        elif self.state == 2:
            
            # Sets next state if turret is aiming at target
            if pan_lock == 1:
                self.state += 1
                                
        # State 3: Shoot Bullet        
        # Extends actuator fully to shoot bullet
        elif self.state == 3:
            # Shoots bullet
            self.actuator.set_duty_cycle(100)
            self.counter += 1 
            
            # Stops after an arbitrary amount of time to avoid running motor continuously
            if self.counter == 40:
                self.state += 1 
                self.counter = 0

## Code to test functionality            
if __name__ == "__main__":
    act = actuator_driver()
    while True:
        try:
            act.act_test(None)
            utime.sleep_ms(20)
        except KeyboardInterrupt:
            break
