# ME 405 Term Project: Learn by Dueling

## Team Edge_Case (Kishor Natarajan, Candice Espitia, Vinayak Sharath)

## Introduction

The goal of this term project was to design a fully autonomous heat-seeking foam-dart-firing turret to be used in duels against other devices of this nature (and their creators from our ME 405 lab section). Required specifications included the use of a brushed DC motor with an encoder to control a panning axis as well as the use of some other motors to control other aspects of the design. The motor controlling the panning axis along with other devices (including a provided thermal camera) were to be run cooperatively with each other using a scheduler in MicroPython.

## Hardware Design

### Mechanical Hardware

<img width="628" alt="CAD_General" src="https://github.com/dijonm53/mecha_02-Term-Project/assets/156120325/4d38798f-c207-4811-b94a-76a4e4a44f6a">

**Figure 1:** Isometric CAD view of the system

<img width="489" alt="CAD_Front" src="https://github.com/dijonm53/mecha_02-Term-Project/assets/156120325/31f14035-b6fe-439e-ab79-8e46c3b96f94">

**Figure 2:** Front CAD view of the system


The above images provide a detailed CAD rendering of our design. The panning axis is driven by a Pittman/Ametek 24V Brushed DC motor w/ Encoder and has its speed reduced by a worm gear drivetrain. This specific worm gear set is a 041A2817 model from LiftMaster, providing at least a 1:30 speed reduction (selected since initial calculations suggested at least a 1:27 gear ratio to support the weight of the original design). The firing mechanism is comprised of a flywheel cage (designed from a NERF<sup>TM</sup> Stryfe semi-auto blaster) with crush flywheels, two hobby DC motors to spin the wheels, and a linear actuator to push the darts into the mechanism. The base (designed with a 5-degree incline to shoot darts further), flywheel cage, flywheels, driving shaft, and panning shaft were 3D printed using an Ender 3 V2 Printer. The linear actuator (1.96" stroke) had an output force of 8.8 lbf and moved at 0.6" per second. This was driven via an H-bridge on the STM32L476RG (Nucleo) to control the actuation direction. All shafts were placed through 0.5" flange bearings and the gearbox was constructed from wooden slabs. Shown below is a picture of the final turret.

![Geartrain_pic](https://github.com/dijonm53/mecha_02-Term-Project/assets/156120325/6333c84c-e6af-4f01-b4af-9c242e19443e)

**Figure 3:** Isometric Picture of Final System


### Electrical Hardware

<img alt="WiringDiagram" src="https://github.com/dijonm53/mecha_02-Term-Project/blob/6250bb24f4d4b3dee401efe956c9abd81eba4704/WiringDiagram.png">

**Figure 4:** Electrical Wiring Diagram

The schematic depicting the wiring configuration of our system is shown in the figure above. We employed a single bench power supply linked to an emergency stop, which was then connected to a breadboard. The breadboard served as the central point for interconnecting various components of our system, including the flywheel, thermal camera, DC motor with encoder, and linear actuator. To properly distribute the power supply and optimize the performance of the flywheel, we arranged the connections to the flywheel and the rest of the system in parallel. This is due to preliminary testing showing the flywheel operates best at current levels at around 2 A, contrary to the optimum current of the rest of the system of about 0.5A. The DC motor responsible for the panning axis is wired to H-bridge Port B, while the linear actuator is connected to H-bridge Port A. On the shoe, notably, we interfaced with pins B6/B7 for the DC motor encoder channels, and B8/B9 for the SCL and SDA thermal camera signals, respectively. 

## Software Design

When the program is run on the STM32L476RG, three tasks (`turret_driver.py`, `thermal_camera.py`, and 
`actuator_flywheel.py`) are run cooperatively using a scheduler. Each task controls a specific electrical/mechanical
hardware component (Turret motor, Thermal Camera, and Linear Actuator) at different priorities and frequencies. These 
tasks also share data to run certain functions. All of this is done during the 10-second window of the duel. 

For a more detailed explanation regarding the Software Design, please refer to the [Github Pages](https://dijonm53.github.io/mecha_02-Term-Project/).

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

Once these functions were all tested separately, we then implemented the scheduler and placed all the tasks in. After some troubleshooting, we then performed 6 runs of the program to test the reliability of the system. 2 runs where the target was to the left of the sensor, 2 runs directly in front of the center, and 2 runs to the right of the sensor. Out of the 6 runs, the turret was successfully able to shoot the target 5 times. For the failed attempt, the turret rotated in the opposite direction and shot; meaning that there was something wrong with the sensor reading.

Even though the test runs were a success in our eyes, during the actual duels, our turret did not perform well. Out of the 6 total runs we did for the duels, we were only able to shoot the target once. During these failed attempts, the system did one or more of the following: Aimed at the target but didn't shoot, turned in the wrong direction, and/or the flywheel changed the trajectory of the bullet. These issues will be discussed in detail in the following section.

## Takeaways and Recommendations

Our project did a great job mechanically; in that, during testing and dueling, we never experienced major mechanical failures. However, given more time, there are several improvements we would make to our design.  

As explained in the previous section, our thermal sensor seemed to work well during testing but failed to perform properly during dueling. This is because we did not apply any additional filtering to the thermal sensor data besides the required filtering needed for the highest temperature column. This is because the sensor was set up in a way that a significant portion of the information it was capturing was 'wasteful data'. Shown below is an image of how our turret was set up for dueling.

![System_pic](https://github.com/dijonm53/mecha_02-Term-Project/assets/79309467/783e646e-79f2-4001-a16e-a414c93c9d6a)

**Figure 5:** Dueling View

As you can imagine, a good portion of the image was taken up by the table/ceiling, and we also weren't using the full horizontal range of the camera. This irrelevant data could have been skewing the final reading in a different direction to where the target is. If we filtered out these unnecessary rows and columns captured by the sensor, the final reading may have been more precise to where the target was. 

Furthermore, we struggled to properly utilize a MOSFET for controlling our flywheels. This resulted in our flywheel being on from the moment the power supply was turned on. This made runs noisy but otherwise did not majorly affect functionality. After speaking with our professor during dueling, he suggested the use of two MOSFETs to control the flywheel, as one wouldn't have enough output voltage to turn on the motors. Nonetheless, a MOSFET should be used for this flywheel design.  

Although earlier it was stated that our mechanical design was reliable, it was quite slow to pan compared to other teams. This is due to the worm gear having a very high gear ratio and therefore decreasing the output speed too much. The worm gear allowed for our design to be more compact and have more torque potential. However, helical spur gears, for example, would've worked much better for this application.  

While on the topic of mechanical constraints, our flywheels sometimes changed the trajectory of the bullet, even if the turret was aimed directly at the target. This is because the prints for these flywheels may not have been of high enough quality, or because the flywheels were slightly misaligned. For a future project, buying the flywheel rollers/cage separately, or using a better printing method for these components, may mitigate these issues. 

Lastly, in trying to make our design more time efficient we found it to be useful to “prime” the linear actuator during the initial turnaround. In other words, let it extend just enough that the bullet is about to enter the flywheels. However, in doing so, we used a time-based method of stopping the linear actuator (the appropriate time increment was found during the experimental testing of the system). In general, it is good software design to eliminate time-based coding; since it is known to be inconsistent. The better practice would be to utilize a limit switch to signal when the linear actuator should end its priming state. 
