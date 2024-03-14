"""!
@file thermal_camera.py
This file contains code that initializes, receives, processes, and sends thermal
camera data to the rest of the system. This file contains multiple states of 
the sensor that are run when certain conditions are met.

@author mecha02 (Kishor Natarajan, Candice Espitia, Vinayak Sharath)
@date   12-Mar-2024 
"""

from machine import Pin, I2C
from mlx_cam import MLX_Cam
import utime as time
import math
import gc

class thermal_cam:
    """! 
    This class implements the necessary code to track and send MLX90640 Thermal
    Infrared Camera information to the driving motors
    """
    def __init__(self):
        """! 
        Initializes the thermal camera port and state values.
        """
        
        # Sets up I2C
        i2c_bus = I2C(1)
        
        # Create the camera object and set it up in default mode
        self.camera = MLX_Cam(i2c_bus)
        self.camera._camera.refresh_rate = 60.0
        
        # Indication of the state in the task
        self.state = 0
        
        # Image received from thermal camera
        self.image = None
        
        # Number of degrees turret needs to turn in order to aim at target
        self.deg_shoot = 0
        
        # Counter used for time based tasks
        self.counter = 0 
        
    def find_deg(self, col):
        """! 
        Finding the degrees in which the panning axis needs to rotate relative
        to the camera
        @param col column in the thermal image array with the highest average temp
        @returns degrees the panning axis needs to turn to aim at target
        """
        # Divides FOV of the camera by the number of columns images receives
        tick = 55/32
        
        # Initializes variables needed for math below
        turn = 0
        deg = 0
        
        # For targets left to the center of the camera 
        if col < 15:
            turn = (15 - col) + 1
            deg = -1 * turn * tick
            
        # For targets right to the center of the camera 
        elif col > 16:
            turn = (col - 16) + 1
            deg = turn * tick
        
        # For targets centered on the camera
        else:
            deg = 0
         
        # Distance camera is from target
        x = 95.5 
        
        # Distance Turret barrel is from target
        d = 180.5
        
        # Trigonometry needed to calculate angle in which turret needs to turn
        ac_deg = math.atan((x*math.tan(math.radians(deg)))/d)
        
        return math.degrees(ac_deg)

    def test_MLX_cam(self, therm):
        """!
        Function that gets the position of the target
        @returns number of degrees turret is supposed rotate to aim at target
        """
        # State 0: Get image
        # Program repeatedly tries to get image from sensor
        if self.state == 0:
            # If no image received, get image
            if self.image is None:
                self.image = self.camera.get_image_nonblocking()
                self.counter += 1
                
            # Sets next state if camera receives image
            elif self.image is not None:  
                self.state += 1
                self.counter += 1
                
        # State 1: Image processing  
        # Once image is received, it is then processed to find position of target
        elif self.state == 1:
            # Column in the 32x24 pixel grid that represents the highest average temperature.
            # In this case, it's the target.
            col_shoot = self.camera.get_csv(self.image, limits=(0, 99))

            # Converts column to a meaningful rotational degree
            self.deg_shoot = therm.find_deg(col_shoot)
            
            # Image is reset
            self.image = None
                
            # Counting until 5 seconds is up
            self.counter += 1
            
            # Once 5 seconds is up, set next state
            if self.counter >= 40:
                self.state += 1
                
            # Otherwise, get new image
            else:
                self.state -= 1
                
        # State 2: Send degree
        # Sends degree to aim to turret controller
        elif self.state == 2:
            # Ensures that this state is never run again
            self.state += 1
            
            # 400 is added to degrees to avoid any share issues regarding the scheduler
            return self.deg_shoot + 400
                   
## Code to test functionality             
if __name__ == "__main__":
    therm = thermal_cam()
    while True:
        try:
            therm.test_MLX_cam(therm)
            time.sleep_ms(30)
        except KeyboardInterrupt:
            break
