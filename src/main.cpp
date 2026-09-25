/*----------------------------------------------------------------------------*/
/*                                                                            */
/*    Module:       main.cpp                                                  */
/*    Author:       Brandon Montagnani                                        */
/*    Created:      26/3/2026, 6:50:20 PM                                     */
/*    Description:  V5 project                                                */
/*                                                                            */
/*----------------------------------------------------------------------------*/

#define _USE_MATH_DEFINES

#include "vex.h"
#include "robot-config.h"

using namespace vex;

// Define your protofunctions here, if necessary
void pre_auton(void);
void autonomous(void);
void usercontrol(void);

// define your global instances of motors and other devices here
// ---- START VEXCODE CONFIGURED DEVICES ----
// Robot Configuration:
// [Name]                 [Type]        [Port(s)]
// LeftFrontDrive         motor         1
// LeftBackDrive          motor         2
// RightFrontDrive        motor         3
// RightBackDrive         motor         4
// MiddleStrafeDrive      motor         5
// Inertial6              inertial     6
// Rotation7              rotation      7
// GPS8                   gps           8
// Distance9              distance      9
// Optical10              optical       10
// Controller1            controller    primary
// Controller2            controller    partner
// ---- END VEXCODE CONFIGURED DEVICES ----

/*---------------------------------------------------------------------------*/
/* Main will set up the competition functions and callbacks.                 */
/*---------------------------------------------------------------------------*/

int main(void) {
  Brain.Timer.clear();

  competition::bStopAllTasksBetweenModes = false;

  // Set up callbacks for autonomous and driver control periods.
  Competition.autonomous(autonomous);
  Competition.drivercontrol(usercontrol);

  // Initializing Robot Configuration. DO NOT REMOVE!
  vexcodeInit();

  // Run the pre-autonomous function.
  pre_auton();

  // Start background display and tracking threads
  thread brain_display_thread = thread(brain_display);
  thread motor_tracking_thread = thread(motor_tracking);

  // Prevent main from exiting with an infinite loop.
  while(true) {
    wait(100, msec);
  }

  return 0;
}

/*---------------------------------------------------------------------------*/
/*                          Pre-Autonomous Functions                         */
/*                                                                           */
/*  You may want to perform some actions before the competition starts.      */
/*  Do them in the following function.  You must return from this function   */
/*  or the autonomous and usercontrol tasks will not be started.  This       */
/*  function is only called once after the V5 has been powered on and        */
/*  not every time that the robot is disabled.                               */
/*---------------------------------------------------------------------------*/

void pre_auton(void) {
  LeftFrontDrive.setMaxTorque(100, percent);
  LeftBackDrive.setMaxTorque(100, percent);
  RightFrontDrive.setMaxTorque(100, percent);
  RightBackDrive.setMaxTorque(100, percent);
  MiddleStrafeDrive.setMaxTorque(100, percent);

  LeftFrontDrive.setVelocity(100, percent);
  LeftBackDrive.setVelocity(100, percent);
  RightFrontDrive.setVelocity(100, percent);
  RightBackDrive.setVelocity(100, percent);
  MiddleStrafeDrive.setVelocity(100, percent);

  LeftFrontDrive.setStopping(hold);
  LeftBackDrive.setStopping(hold);
  RightFrontDrive.setStopping(hold);
  RightBackDrive.setStopping(hold);
  MiddleStrafeDrive.setStopping(hold);

  LeftFrontDrive.setPosition(0, degrees);
  LeftBackDrive.setPosition(0, degrees);
  RightFrontDrive.setPosition(0, degrees);
  RightBackDrive.setPosition(0, degrees);
  MiddleStrafeDrive.setPosition(0, degrees);
}

/*---------------------------------------------------------------------------*/
/*                                                                           */
/*                              Autonomous Task                              */
/*                                                                           */
/*  This task is used to control your robot during the autonomous phase of   */
/*  a VEX Competition.                                                       */
/*                                                                           */
/*  You must modify the code to add your own robot specific commands here.   */
/*---------------------------------------------------------------------------*/

void autonomous(void) {
  LeftFrontDrive.setMaxTorque(100, percent);
  LeftBackDrive.setMaxTorque(100, percent);
  RightFrontDrive.setMaxTorque(100, percent);
  RightBackDrive.setMaxTorque(100, percent);
  MiddleStrafeDrive.setMaxTorque(100, percent);

  LeftFrontDrive.setVelocity(50, percent);
  LeftBackDrive.setVelocity(50, percent);
  RightFrontDrive.setVelocity(50, percent);
  RightBackDrive.setVelocity(50, percent);
  MiddleStrafeDrive.setVelocity(50, percent);

  LeftFrontDrive.setStopping(hold);
  LeftBackDrive.setStopping(hold);
  RightFrontDrive.setStopping(hold);
  RightBackDrive.setStopping(hold);
  MiddleStrafeDrive.setStopping(hold);

  Brain.Timer.clear();

  thread autonomous_background_tasks_thread = thread(autonomous_background_tasks);

  if(red_alliance == true) {

  }
  else {

  }

  autonomous_background_tasks_thread.interrupt();
}

int autonomous_background_tasks(void) {
  // Having a function run on a thread during the autonomous period.
  while(Competition.isAutonomous() && Competition.isEnabled()) {

    this_thread::sleep_for(20);
  }

  LeftFrontDrive.stop();
  LeftBackDrive.stop();
  RightFrontDrive.stop();
  RightBackDrive.stop();
  MiddleStrafeDrive.stop();

  return 0;
}

/*---------------------------------------------------------------------------*/
/*                                                                           */
/*                              User Control Task                            */
/*                                                                           */
/*  This task is used to control your robot during the user control phase of */
/*  a VEX Competition.                                                       */
/*                                                                           */
/*  You must modify the code to add your own robot specific commands here.   */
/*---------------------------------------------------------------------------*/

void usercontrol(void) {
  LeftFrontDrive.setMaxTorque(100, percent);
  LeftBackDrive.setMaxTorque(100, percent);
  RightFrontDrive.setMaxTorque(100, percent);
  RightBackDrive.setMaxTorque(100, percent);
  MiddleStrafeDrive.setMaxTorque(100, percent);

  LeftFrontDrive.setBrake(brake);
  LeftBackDrive.setBrake(brake);
  RightFrontDrive.setBrake(brake);
  RightBackDrive.setBrake(brake);
  MiddleStrafeDrive.setBrake(brake);

  Brain.Timer.clear();

  thread usercontrol_joysticks_thread = thread(usercontrol_joysticks);
  thread usercontrol_buttons_thread = thread(usercontrol_buttons);
  thread joystick_tracking_thread = thread(joystick_tracking);
  thread PID_loop_thread = thread(PID_loop);

  while(Competition.isDriverControl() && Competition.isEnabled()) {
    axis3 = Controller1.Axis3.position();
    axis4 = Controller1.Axis4.position();
    axis1 = Controller1.Axis1.position();
    axis2 = Controller1.Axis2.position();

    Up = Controller1.ButtonUp.pressing();
    Down = Controller1.ButtonDown.pressing();
    Left = Controller1.ButtonLeft.pressing();
    Right = Controller1.ButtonRight.pressing();

    X = Controller1.ButtonX.pressing();
    B = Controller1.ButtonB.pressing();
    A = Controller1.ButtonA.pressing();
    Y = Controller1.ButtonY.pressing();

    L1 = Controller1.ButtonL1.pressing();
    L2 = Controller1.ButtonL2.pressing();
    R1 = Controller1.ButtonR1.pressing();
    R2 = Controller1.ButtonR2.pressing();

    wait(10, msec); // Sleep the task for a short amount of time to
                    // prevent wasted resources.
  }

  usercontrol_joysticks_thread.interrupt();
  usercontrol_buttons_thread.interrupt();
  joystick_tracking_thread.interrupt();
  PID_loop_thread.interrupt();
}
