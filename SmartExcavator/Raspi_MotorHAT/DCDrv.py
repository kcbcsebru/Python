#!/usr/bin/python
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

import time
import atexit
import RPi.GPIO as GPIO
import threading


################################# Definitions #################################
# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f,freq=10000)

#PWM_Speed(0~255)
PWM_para = 100;
PWM_para_faster = 150;
PWM_para_slow = 60;

#GPIO Ports(left to right)
GPIO_port = [21,22,23,24];

#Infra Sample Time
dt = 0.001;


######################### Initialization & Functions ##########################
# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)
	print 'Motor Stopped Successfully!'

atexit.register(turnOffMotors)

#GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_port,GPIO.IN)

# set the speed to start, from 0 (off) to 255 (max speed)
for m in range(4):
	mh.getMotor(m).setSpeed(PWM_para);

# Stop Motor
for m in range(4):
	mh.getMotor(m).run(Raspi_MotorHAT.RELEASE);

myMotorLeft=mh.getMotor(1);
myMotorRight=mh.getMotor(2);

# Cache of the Speed Now
motorspeed=[PWM_para,PWM_para]

# Only when the speed changes we set a new one
def SetSpeed(LR,speed):
	if (LR==0):
		if (speed != motorspeed[0]):
			motorspeed[0]=speed;
			myMotorLeft.setSpeed(speed);
	if (LR==1):
		if (speed != motorspeed[1]):
			motorspeed[1]=speed;
			myMotorRight.setSpeed(speed);

def LeftStop():
	SetSpeed(0,PWM_para);
	myMotorLeft.run(Raspi_MotorHAT.RELEASE);

def LeftGo():
	SetSpeed(0,PWM_para);
	myMotorLeft.run(Raspi_MotorHAT.FORWARD);

def LeftGoHalf():
	SetSpeed(1,PWM_para_slow);
	myMotorLeft.run(Raspi_MotorHAT.FORWARD);

def LeftGoFast():
	SetSpeed(0,PWM_para_faster);
	myMotorLeft.run(Raspi_MotorHAT.FORWARD);

def LeftBack():
	SetSpeed(0,PWM_para);
	myMotorLeft.run(Raspi_MotorHAT.BACKWARD);

def LeftBackFast():
	SetSpeed(0,PWM_para_faster);
	myMotorLeft.run(Raspi_MotorHAT.BACKWARD);


def RightStop():
	SetSpeed(1,PWM_para);
	myMotorRight.run(Raspi_MotorHAT.RELEASE);

def RightGo():
	SetSpeed(1,PWM_para);
	myMotorRight.run(Raspi_MotorHAT.FORWARD);

def RightGoHalf():
	SetSpeed(1,PWM_para_slow);
	myMotorRight.run(Raspi_MotorHAT.FORWARD);

def RightGoFast():
	SetSpeed(1,PWM_para_faster);
	myMotorRight.run(Raspi_MotorHAT.FORWARD);

def RightBack():
	SetSpeed(1,PWM_para);
	myMotorRight.run(Raspi_MotorHAT.BACKWARD);

def RightBackFast():
	SetSpeed(1,PWM_para_faster);
	myMotorRight.run(Raspi_MotorHAT.BACKWARD);

# Refresh the PWM every 100 times
Freshcount=0;
def PWMRefresh():
	global Freshcount;
	Freshcount += 1;
	if (Freshcount > 100):
		myMotorLeft.setSpeed(motorspeed[0]);
		myMotorRight.setSpeed(motorspeed[1]);
		Freshcount=0;

# Run along the Track
def TrackRun():
	while True:
		in_value=[0,0,0,0]
		in_value1 = [ GPIO.input(m) for m in range(21,24+1) ]
		time.sleep(dt)
		in_value2 = [ GPIO.input(m) for m in range(21,24+1) ]
		time.sleep(dt)
		in_value3 = [ GPIO.input(m) for m in range(21,24+1) ]
		time.sleep(dt)
		in_value4 = [ GPIO.input(m) for m in range(21,24+1) ]
		time.sleep(dt)
		in_value5 = [ GPIO.input(m) for m in range(21,24+1) ]
		for m in range(4):
			in_value[m] = (in_value1[m] + in_value2[m] + in_value3[m] + in_value4[m] + in_value5[m]) > 0;
		print in_value
		if in_value == [0,0,1,0]: #Turn Right
			RightStop();
			LeftGo();
			print 'Turn Right'
		elif in_value == [0,1,0,0]: #Turn Left
			LeftStop();
			RightGo();
			print 'Turn Left'
		elif in_value == [1,0,0,0]: #Turn Left
			LeftBackFast();
			RightGo();
			print 'Turn Left'
		elif in_value == [0,0,0,1]: #Turn Right
			RightBackFast();
			LeftGo();
			print 'Turn Right'
		elif ([in_value[0],in_value[1]] == [1,1]) or ([in_value[2],in_value[3]] == [1,1]): #Stop Left or Right
			if in_value[0] == 1:
				LeftBackFast();
				print 'Stop Left'
			else:
				LeftGo();
			if in_value[3] == 1:
				RightBackFast();
				print 'Stop Right'
			else:
				RightGo();
		else: #go
			LeftGo();
			RightGo();
			print 'go'
		if in_value == [1,1,1,1]: #final
			break;
		time.sleep(dt)
		PWMRefresh();
	LeftStop();
	RightStop();
	time.sleep(2);


############################### Run The Program ###############################
# Forward,Tracking
# Run along the Track
TrackRun();

# Return back
# Run back a little for return
RightBack();
LeftBack();

time.sleep(0.2);

LeftStop();
RightStop();

time.sleep(1);

# Turn around
LeftBackFast();
RightGoFast();

time.sleep(1);

count = 0;

# Turn until we find the track again
while True:
	in_value=[0,0,0,0]
	time.sleep(dt)
	in_value1 = [ GPIO.input(m) for m in range(21,24+1) ]
	time.sleep(dt)
	in_value2 = [ GPIO.input(m) for m in range(21,24+1) ]
	time.sleep(dt)
	in_value3 = [ GPIO.input(m) for m in range(21,24+1) ]
	time.sleep(dt)
	in_value4 = [ GPIO.input(m) for m in range(21,24+1) ]
	time.sleep(dt)
	in_value5 = [ GPIO.input(m) for m in range(21,24+1) ]
	for m in range(4):
		in_value[m] = (in_value1[m] + in_value2[m] + in_value3[m] + in_value4[m] + in_value5[m]) > 0;
	print in_value
	if (in_value!=[0,0,0,0]):
		count += 1;
		if (count > 5):
			break;
	else:
		count = 0;
	PWMRefresh();

# Run along the Track
TrackRun();