# ME 405 Term Project

## Team Edge Case (Kishor Natarajan, Candice Espitia, Vinayak Sharath)

## Introduction

(Vin)

## Hardware Design

### Mechanical Hardware

(Vin)

### Electrical Hardware

(Candice)

## Software Design

When the program is run on the STM32L476RG, three tasks (`turret_driver.py`, `thermal_camera.py`, and 
`actuator_flywheel.py`) are run cooperatively using a scheduler. Each task controls a specific electrical/mechanical
hardware component (Turret motor, Thermal Camera, and Linear Actuator) at different priorities and frequencies. These 
tasks also share data to run certain functions. All of this is done during the 10-second window of the duel. For a more 
detailed explanation regarding the Software Design, please refer to the [Github Pages (https://dijonm53.github.io/mecha_02-Term-Project/).

## Testing and Results

Each major component had to be tested separately before putting them all together in a scheduler. 

To begin with, after writing the code for the thermal camera sensor, we tested its accuracy by following a few 
procedures. First, we marked a position on the table where the camera would be positioned (even on the day of the 
duel). After this, we ran the code continuously while another team member was moving around behind the table. The 
program was set up to obtain the degrees the target is from the center of the camera, and continuously print that value 
in the console. We then verified qualitatively if this degree reading matched with where the target was.

For the Turret Driver, we obtained a setpoint that would output a 180-degree turn for the turret (through testing). 
This value was then used to convert the degree reading from the sensor into a setpoint for the turret to turn to. 
Before implementing this task into the scheduler, we ran multiple tests to see if the turret was indeed aiming at the 
target. We did this by manually inputting the degree value obtained from the sensor into the turret driver file. We did 
this until we were confident that the turret would aim at the target.

For the Linear Actuator, since its motion is time-based (not encoder-based), the main functionality we tested was its 
ability to push the bullet into the flywheel, and the time it would take to push the bullet in without shooting.

Once these functions were all tested, we then implemented the scheduler and placed all the tasks in. After some 
troubleshooting, we then performed 6 runs of the program to test the reliability of the system. 2 runs where the target 
is to the left of the sensor, 2 runs directly in front of the center, and 2 runs to the right of the sensor. Out of the 6 runs, 
the turret was successfully able to shoot the target 5 times. For the failed attempt, the turret rotated in the 
opposite direction and shot; meaning that there was something wrong with the sensor reading.

Even though the test runs were a success in our eyes, during the actual duels, our turret did not perform well. Out of the 6 total runs we did for the duels, we were only able to shoot the target once. During these failed attempts, the system did one or more of the following: Aimed at the target but didn't shoot, turned in the wrong direction, and/or the flywheel changed the trajectory of the bullet. These issues will be discussed in detail in the following section.

## Takeaways and Recommendations

(Candice)
