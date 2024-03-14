"""!
@file main.py
This file contains code that runs the duel that is to be demonstrated during lab.
There are three tasks running simultaneously, with each having their own finite
state machine (FSM). The code uses a priority based scheduler, with different 
time periods for each task.

@author mecha02 (Kishor Natarajan, Candice Espitia, Vinayak Sharath)
@date   12-Mar-2024 
"""

import gc
import pyb
import cotask
import task_share
import thermal_camera as therm
import turret_driver as tur
import actuator_flywheel as act



def actuator_task(shares):
    """!
    Task which runs the actuator and flywheel task.
    @param shares A tuple of a share from which this task gets data.
    """
    # An integer (1 or 0) indicating whether to shoot dart (receive)
    aim_lock = shares
    
    # Initializes the 'actuator_driver' class
    actuator = act.actuator_driver()
    
    # Initializes variable to be used to pass share data to the task
    if_aim = None
    
    # Runs task continuously
    while True:
        # Gets share data (if any)
        if_aim = aim_lock.get()
        
        # Task to be run
        actuator.act_test(if_aim)
        
        yield 0

def turret_task(shares):
    """!
    Task which runs the turret (or panning axis) task.
    @param shares A tuple of a share from which this task gets data
    """
    # degree: A float indicating the number of degrees the turret needs to turn to aim at target (receive)
    # aim_lock: An integer (1 or 0) indicating whether to shoot dart (send)
    degree,aim_lock = shares
    
    # Initializes the 'turret_driver' class
    turret = tur.turret_driver()
    
    # Initializes variables to be used to pass share data to the task
    if_aim = None
    deg = None
    
    # Runs task continuously
    while True:
        # Gets share data (if any)
        deg = degree.get()
        
        # Task to be run
        if_aim = turret.step_test(deg)
        
        # Putting value into share
        if if_aim != None:
            aim_lock.put(if_aim)
            
        yield 0 
            

        
def sensor_task(shares):
    """!
    Task which runs the thermal sensor task.
    @param shares A tuple of a share from which this task gets data
    """
    # A float indicating the number of degrees the turret needs to turn to aim at target (send)
    degree = shares
    
    # Initializes the 'thermal_cam' class
    sensor = therm.thermal_cam()
    
    # Initializes variable to be used to pass share data to the task
    if_deg = None
    
    # Runs task continuously
    while True:
        # Task to be run
        if_deg = sensor.test_MLX_cam(sensor)
        
        # Putting value into share
        if if_deg != None:
            degree.put(if_deg)
            
        yield 0 


# This code creates two shares and three tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":

    # Create two shares to pass between functions
    # Degrees to aim (float)
    s1 = task_share.Share('f',3, name="My Share1")
    
    # Indication of whether to shoot (int)
    s2 = task_share.Share('h',3, name="My Share2")
    
    # Create the tasks
    # Sensor Task
    sensor_t = cotask.Task(sensor_task, name="Sensor", priority=1, period=100,
                        profile=True, trace=False, shares=s1)
    
    # Turret Task
    turret_t = cotask.Task(turret_task, name="Turret", priority=3, period=10,
                        profile=True, trace=False, shares=(s1,s2))
    
    # Actuator Task
    actuator_t = cotask.Task(actuator_task, name="Actuator", priority=2, period=100,
                        profile=True, trace=False, shares = s2)
    
    # Append Tasks in a cotask list
    cotask.task_list.append(sensor_t)
    cotask.task_list.append(turret_t)
    cotask.task_list.append(actuator_t)

    # Run the memory garbage collector to ensure memory is as fragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm.
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(sensor_t.get_trace())
    print('')