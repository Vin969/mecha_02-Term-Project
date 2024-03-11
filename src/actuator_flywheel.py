import utime
import motor_driver as moe
import pyb

class actuator_driver:
    def __init__(self):
        # Stuff copied over from last lab below
        # Code needed to initalize motor
        en_pin = pyb.Pin(pyb.Pin.board.PA10, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value = 1)
        a_pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
        another_pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
        m_timer = pyb.Timer(3, freq=5000)
        chm1 = m_timer.channel(1, pyb.Timer.PWM, pin=a_pin)
        chm2 = m_timer.channel(2, pyb.Timer.PWM, pin=another_pin)
        
        self.pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
        
        # Motor Initialization done through imported MotorDriver class
        self.actuator = moe.MotorDriver(en_pin,a_pin,another_pin,m_timer,chm1,chm2)
        self.state = 0
        self.counter = 0
        
        
    def act_test(self, pan_lock):
        # 180 degree turn lol
        if self.state == 0:
            self.counter += 1
            print(self.state)
            if self.counter == 40:
                self.state += 1 
                self.counter = 0
                
        # Priming state
        elif self.state == 1:
            self.actuator.set_duty_cycle(100)
            self.counter += 1
            if self.counter == 20:
                self.state += 1 
                self.counter = 0
                self.actuator.duty_zero()
                
        # Turning on flywheel
        elif self.state == 2:
            self.counter += 1    
            if self.counter == 40:
                self.pinC0.value(1)
                self.state += 1 
                self.counter = 0
                
        # Wait to stop turning for target
        elif self.state == 3:
            # if pan_lock == True:
            #     self.state += 1 
            
            self.counter += 1
            if self.counter == 40:
                self.state += 1 
                self.counter = 0
                
        # Extend actuator fully
        elif self.state == 4:
            self.actuator.set_duty_cycle(100)
            self.counter += 1 
            if self.counter == 20:
                self.state += 1 
                self.counter = 0
            
if __name__ == "__main__":
    act = actuator_driver()
    while True:
        try:
            act.act_test(None)
            utime.sleep_ms(20)
        except KeyboardInterrupt:
            break