#ifndef ROBOT_CONFOG_H
#define ROBOT_CONFOG_H

#include "vars.hpp"

/*----------------------------------------------------------------------------*/
/* Used to initialize code/tasks/devices added using tools in VEXcode Pro.    */
/* This should be called at the start of your int main function.              */
/*----------------------------------------------------------------------------*/

void vexcodeInit(void);
void initializeRandomSeed(void);
void playVexcodeSound(const char *soundName);

/*----------------------------------------------------------------------------*/
/* Used to initialize code/tasks/devices added using tools in VEXcode Pro.    */
/* This should be called at the start of your int main function.              */
/*----------------------------------------------------------------------------*/

int brain_display(void);
int motor_tracking(void);
int autonomous_background_tasks(void);
int usercontrol_joysticks(void);
int usercontrol_buttons(void);
int joystick_tracking(void);
int PID_loop(void);

void onevent_Controller1_ButtonUp_pressed(void);
void onevent_Controller1_ButtonUp_released(void);
void onevent_Controller1_ButtonDown_pressed(void);
void onevent_Controller1_ButtonDown_released(void);
void onevent_Controller1_ButtonLeft_pressed(void);
void onevent_Controller1_ButtonLeft_released(void);
void onevent_Controller1_ButtonRight_pressed(void);
void onevent_Controller1_ButtonRight_released(void);

void onevent_Controller1_ButtonA_pressed(void);
void onevent_Controller1_ButtonA_released(void);
void onevent_Controller1_ButtonB_pressed(void);
void onevent_Controller1_ButtonB_released(void);
void onevent_Controller1_ButtonX_pressed(void);
void onevent_Controller1_ButtonX_released(void);
void onevent_Controller1_ButtonY_pressed(void);
void onevent_Controller1_ButtonY_released(void);

void onevent_Controller1_ButtonL1_pressed(void);
void onevent_Controller1_ButtonL1_released(void);
void onevent_Controller1_ButtonL2_pressed(void);
void onevent_Controller1_ButtonL2_released(void);
void onevent_Controller1_ButtonR1_pressed(void);
void onevent_Controller1_ButtonR1_released(void);
void onevent_Controller1_ButtonR2_pressed(void);
void onevent_Controller1_ButtonR2_released(void);

#endif