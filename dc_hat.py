#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
# mh = Adafruit_MotorHAT(addr=0x40)
mh = Adafruit_DCMotor(addr=0x40)


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


atexit.register(turnOffMotors)


################################# DC motor test!
myMotor = mh.getMotor(0)

# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(20)
myMotor.run(Adafruit_MotorHAT.FORWARD)
# turn on motor
myMotor.run(Adafruit_MotorHAT.RELEASE)


while (True):
    print("Forward! ")
    myMotor.run(Adafruit_MotorHAT.FORWARD)

    print("\tSpeed up...")
    for i in range(20):
        myMotor.setSpeed(i)
        time.sleep(0.1)

    print("\tSlow down...")
    for i in reversed(range(255)):
        myMotor.setSpeed(i)
        time.sleep(0.1)

    print("Backward! ")
    myMotor.run(Adafruit_MotorHAT.BACKWARD)

    print("\tSpeed up...")
    for i in range(20):
        myMotor.setSpeed(i)
        time.sleep(0.1)

    print("\tSlow down...")
    for i in reversed(range(20)):
        myMotor.setSpeed(i)
        time.sleep(0.1)

    print("Release")
    myMotor.run(Adafruit_MotorHAT.RELEASE)
time.sleep(1.0)
