## @file mainpage.py
#  @author mecha02 (Kishor Natarajan, Candice Espitia, Vinayak Sharath)
#  @mainpage
#
#  @section soft_des Software Design
#  This project consists of files used to control the turret system for team
#  Edge_Case's Learn by Dueling project. This code runs on an STM32L476RG
#  microcontroller, where various electrical components (Panning axis motor,
#  MLX90640 Thermal Infrared Camera, and Linear Actuator) are controlled.  
#  The software utilizes a time-based scheduler to run three tasks  
#  (@c turret_driver.py , @c thermal_camera.py , and @c actuator_flywheel.py) 
#  cooperatively of each other. Their functions and code design are described 
#  below. To learn more about the rest of the system (Mechanical
#  and Electrical Hardware), along with its outcomes, please refer to the
#  main GitHub page: https://github.com/dijonm53/mecha_02-Term-Project
#
#  @section code Original Code
#  Here are the main files used to control this system, along with their system
#  diagrams. These files are made by team Edge_Case. One thing to note is that 
#  for almost all of these files, the pins that the components utilize are
#  initialized within their respective files.
#
#  @subsection therm Thermal Camera
#  @c thermal_camera.py is used to acquire/process data from the MLX90640   
#  Thermal Infrared Camera. During the duel, the task repeatedly tries to
#  obtain an image from the camera, using a function within @c mlx_cam.py . 
#  After receiving an image, the task will then process that image to obtain
#  a 'degrees from target' reading to then send to the task that controls the
#  panning axis. However, this degree will only be sent to that task after 5
#  seconds. The logic for converting the degrees for the turret is shown below:
#  \image html Degree_logic.jpg
#  
#  While testing this functionality, we noticed that the initial 
#  degree from the sensor is almost always inaccurate when compared to
#  where the target actually is. That is why the code is set up in a way to 
#  continuously read data from the sensor until 5 seconds is up. The code
#  structure, or Finite-State Machine (FSM), is shown below:
#  \image html Sensor_FSM.jpg
#
#  @subsection tur Turret Driver
#  @c turret_driver.py is used to control the panning axis motor for the system.
#  Before the duel begins, the turret must be facing away from the target. Once
#  the duel begins, the task rotates the turret 180 degrees clockwise to face
#  the end of the table. In order to do this, @c closed_loop_controller.py is
#  run with a setpoint equal to around 180 degrees. The task then waits until 
#  it gets a degree value from the sensor task. After receiving this data, the 
#  task then converts the value into a meaningful motor encoder setpoint, which 
#  is then sent to @c closed_loop_controller.py to run. After turning to the
#  frozen target, the task sends an indication (an integer '1') to the linear
#  actuator task to shoot the bullet. The FSM for this task is shown below:
#  \image html Turret_FSM.jpg
# 
#  @subsection act Actuator Driver
#  @c actuator_flywheel.py is used to control the motion of the linear actuator.
#  Initially (when the duel begins), the actuator is idle for arbitrary period
#  of time (around 1-2 seconds). After this idle state, the linear actuator is
#  pushed out just enough to stop the bullet right before it touches the 
#  flywheel. Because the actuator is very slow, we thought that priming the 
#  actuator before shooting will speed up the process of shooting. After this, 
#  the actuator waits until it gets a signal from @c turret_driver.py to shoot
#  the push the bullet into the spinning flywheel. One thing to note is that 
#  because this linear actuator does not come equipped with an encoder, many of
#  these functions are purely time-based. This behavior this discussed further 
#  in the 'Takeaways' section in the main GitHub page. The FSM for this task is 
#  shown below:
#  \image html Actuator_FSM.jpg   
#    
#  @subsection motor_cont Motor Controller File
#  @c closed_loop_controller.py is used to run a step-response (Proportional 
#  controller) for a given motor. This file is primarily used by the 
#  @c turret_driver.py task. This file was taken from a previous lab assignment
#  that we completed, and further modified to fit better for this project. When
#  this file is called, a step-response is run until completed, with a given 
#  gain and setpoint value. After it has completed, the file sends an indication
#  to whatever file called it (in this case, @c turret_driver.py) that the step-
#  response has been complete. After this is done, all necessary values are 
#  reset and waits until run again. The FSM for this task is shown below:
#  \image html Controller_FSM.jpg
#
#  @section imp_code Imported/Modified Code
#  Here are the files imported from a library (made by the instructor) that was
#  used to make this system run. One of these files has been modified slightly 
#  for the purposes of this project
# 
#  @subsection imp Imported Code
#  @c cotask.py and @c task_share.py were imported to use for this project.
#  These files are unmodified.
#
#  @subsection mod Modified Code
#  @c mlx_cam.py has largely been unchanged from its previous state, except for
#  the function @c get_csv . Originally, after running this function, it would
#  print a 32x24 pixel grid of numbers ranging from 0-99 in a CSV style format,
#  representative of what the camera sees. The higher the number, the higher
#  the temperature. Now, the function has been modified to return the column in
#  that pixel grid representative of the highest total. If a column of values
#  has the highest total, it is likely that the target is in that area.
#
#  @section oth_code Other Code
#  @c motor_driver.py and @c encoder_reader.py are files made by us to run the
#  motor and read encoder data, respectively. These are used by various files
#  within the system to perform certain functions. @ step_control.py was used 
#  to tune the gain values for the motor controller task. 
#
#  @section tsk_dia Task Diagram
#  Shown below is how our three main tasks (@c turret_driver.py , 
#  @c thermal_camera.py , and @c actuator_flywheel.py) cooperatively worked with
#  each other.
#  \image html Task_Diagram.jpg
