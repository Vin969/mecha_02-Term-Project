import utime
import encoder_reader as enc
import motor_driver as moe
import closed_loop_controller as closed
import pyb

class turret_driver:
    def __init__(self):
        # Stuff copied over from last lab below
        # Code needed to initalize motor
        en_pin = pyb.Pin(pyb.Pin.board.PC1, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value = 1)
        a_pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
        another_pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
        m_timer = pyb.Timer(5, freq=5000)
        chm1 = m_timer.channel(1, pyb.Timer.PWM, pin=a_pin)
        chm2 = m_timer.channel(2, pyb.Timer.PWM, pin=another_pin)
        
        # Motor Initialization done through imported MotorDriver class
        self.turret = moe.MotorDriver(en_pin,a_pin,another_pin,m_timer,chm1,chm2)
        
        # Code needed to initialize encoder. Set 'tim' to the correct timer
        # for the pins being used.
        tim = 4
        timer = pyb.Timer(tim, prescaler = 0, period = 65535)
        
        ch1 = timer.channel(1,pyb.Timer.ENC_A,pin = pyb.Pin.board.PB6)
        ch2 = timer.channel(2, pyb.Timer.ENC_B,pin = pyb.Pin.board.PB7)

        # Initializes Encoder (Turret)
        self.tur_enc = enc.encoder(timer,ch1,ch2)          
        
        # Initializes Motor Controller (Turret)
        self.tur_con = closed.control()
        
        self.pos = False
        self.counter = 0
        
        self.gain = 1.2
        self.position = 65500
        
        self.state = 0
        
        
    def step_test(self, sensor_data):
        # 180 degree turn lol
        if self.state == 0:
            self.pos = self.tur_con(self.turret, self.tur_enc, self.tur_con, self.gain, self.position)
            if self.pos == True:
                self.state += 1 
                self.pos = False
                
        # Idle state
        elif self.state == 1:
            self.counter += 1 
            if self.counter == 100:
                self.state += 1 
                self.counter = 0
        
        elif self.state == 2:
            ## Math for position caclulation
            if self.position < 0:
                self.gain *= 1
                self.state += 1
            elif self.position > 0:
                self.state += 1 
            else: 
                self.state += 2 
        
        elif self.state == 3:
            self.pos = self.tur_con(self.turret, self.tur_enc, self.tur_con, self.gain, self.position)
            if self.pos == True:
                self.state += 1 
                self.pos = False
        
        elif self.state == 4:
            return True
            self.state += 1
            
if __name__ == "__main__":
    tur = turret_driver()
    while True:
        try:
            tur.step_test(3.68)
            utime.sleep_ms(80)
        except KeyboardInterrupt:
            break