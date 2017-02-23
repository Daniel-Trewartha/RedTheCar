#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import picamera
import picamera.array
import os
import numpy as np

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
resolution = (128,128)
# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
myRightMotor = mh.getMotor(3)
myLeftMotor = mh.getMotor(2)

camera = picamera.PiCamera()
camera.resolution = resolution
time.sleep(2)

myRightMotor.run(Adafruit_MotorHAT.FORWARD)
myLeftMotor.run(Adafruit_MotorHAT.FORWARD)


while True:
    with picamera.array.PiRGBArray(camera) as output:
        camera.capture(output, 'rgb')
        #camera.capture("test.jpg")
        colorArray = np.zeros((resolution[0],resolution[1],3))
        colorArray = np.copy(output.array)
        redArray = np.zeros((resolution[0],resolution[1]))
        for ix in range(resolution[0]):
            for iy in range(resolution[1]):
                redArray[ix,iy] = float(colorArray[ix,iy,0])/(float(colorArray[ix,iy,0])+float(colorArray[ix,iy,1])+float(colorArray[ix,iy,2])+1)
        redindex = redArray.argmax()
        direction = np.unravel_index(redindex,(resolution[0],resolution[1]))[0]
        if (direction < resolution[0]/3) :
            print "Left!"
            print direction
            myRightMotor.setSpeed(125)
            myLeftMotor.setSpeed(75)
        elif (direction < 2*resolution[0]/3) :
            print "Straight!"
            print direction
            myRightMotor.setSpeed(100)
            myLeftMotor.setSpeed(100)
        else:
            print "Right!"
            print direction
            myRightMotor.setSpeed(75)
            myLeftMotor.setSpeed(125)
        time.sleep(0.1)
        #myRightMotor.setSpeed(0)
        #myLeftMotor.setSpeed(0)
#    print np.unravel_index(greenindex,(32,32))
#    print np.unravel_index(blueindex,(32,32))
#    with open(os.path.join(os.path.dirname(__file__),"Output.txt"),'w') as outFile:
#        output.array[15,:,0].tofile(outFile,sep=", ")

        
#    myRightMotor.run(Adafruit_MotorHAT.FORWARD)
#    myLeftMotor.run(Adafruit_MotorHAT.FORWARD)

#    while true:
#        camera.capture(output, 'rgb')
        
#        output.array[12:,:,0].argmax(0).max()
#for i in range(0,255):
#	myRightMotor.setSpeed(200)
#        myLeftMotor.setSpeed(200)
#        myRightMotor.setSpeed(i)
#	time.sleep(0.01)

turnOffMotors()
