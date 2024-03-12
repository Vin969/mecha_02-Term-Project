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
        i2c_bus = I2C(1)
        
        # Create the camera object and set it up in default mode
        self.camera = MLX_Cam(i2c_bus)
        self.camera._camera.refresh_rate = 60.0
        
        self.state = 0
        self.image = None
        self.deg_shoot = 0
        self.counter = 0 
        
    def find_deg(self, col):
        """! 
        Finding the degrees in which the panning axis needs to rotate realtive
        to the camera
        @param col column in the thermal image array with the highest average temp
        @returns degrees the panning axis needs to turn to aim at target
        """
        tick = 55/32
        turn = 0
        deg = 0
        if col < 15:
            turn = (15 - col) + 1
            deg = -1 * turn * tick
        elif col > 16:
            turn = (col - 16) + 1
            deg = turn * tick
        else:
            deg = 0
         
        x = 95.5 
        d = 180.5

        ac_deg = math.atan((x*math.tan(math.radians(deg)))/d)
        return math.degrees(ac_deg)

    def test_MLX_cam(self, therm):
        """!
        Function that runs gets the position of the target
        @returns number of degrees turret is supposed rotate to aim at target
        """
        
        if self.state == 0:
            if self.image is None:
                self.image = self.camera.get_image_nonblocking()
                self.counter += 1
            elif self.image is not None:  
                self.state += 1
                self.counter += 1
                
        elif self.state == 1 :
            col_shoot = self.camera.get_csv(self.image, limits=(0, 99))
#             print("Column with highest average:", col_shoot)
            self.deg_shoot = therm.find_deg(col_shoot)
#             print("Degree to shoot:", self.deg_shoot, "degrees")
            
            self.image = None
            self.counter += 1
            if self.counter >= 40:
                print('hit')
                self.state += 1
            else:
                self.state -= 1
                
                
        elif self.state == 2:
#             print('s2')
#             print('done')
#             print("Degree to shoot:", self.deg_shoot, "degrees")
            self.state += 1
            return self.deg_shoot + 400
            
        elif self.state == 3:
            self.counter += 1
            
            
if __name__ == "__main__":
    therm = thermal_cam()
    while True:
        try:
            therm.test_MLX_cam(therm)
            time.sleep_ms(30)
        except KeyboardInterrupt:
            break
