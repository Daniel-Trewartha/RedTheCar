#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import picamera
import picamera.array
import os
import numpy as np
from collections import deque

"""
A little wrapper class for driving about
Implements two functions:
Reset: Back away if you hit a wall, set motors to forward, 0 speed, return an image
Step(action): set motors to speed determined by action, take an image, reture image, reward, done(bool)
"""

class driving_env:
    def __init__(self,height,width):
        #Motor objects
        self.mh = Adafruit_MotorHAT(addr=0x60)
        self.rightMotor = self.mh.getMotor(3)
        self.leftMotor = self.mh.getMotor(2)

        #Camera objects
        self.resolution = (height,width)
        self.camera = picamera.PiCamera()
        self.camera.resolution = self.resolution
        self.camera_output_raw = np.empty((height,width,3), dtype=np.uint8)
        self.camera_output = np.zeros((height*width*3))
        
        #Last 5 images, to determine if we hit a wall
        self.queue = deque([])
        self.queue_size = 5
        
        for i in range(self.queue_size): 
            self.camera.capture(self.camera_output_raw, 'rgb')
            self.queue.append(self.camera_output_raw.flatten())

        #threshold before we decide we're hitting a wall
        #I have no idea what a sensible value for this is....
        self.threshold = 3000000
        
        #On exit shut down motors, release camera
        atexit.register(self._turnOffMotors)
        atexit.register(self.camera.close)

    def reset(self):
        #Back away if you hit a wall, set motors to forward at 0 speed, return an image of where you are
        if (self._hittingWall()):
            self._backOutOfTrouble()
        self.leftMotor.setSpeed(0)
        self.rightMotor.setSpeed(0)
        self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
        self.rightMotor.run(Adafruit_MotorHAT.FORWARD)

        self._capture()
        return self.camera_output

    def step(self,action):
        #Implement action
        self._takeAction(action)
        #Calculate reward
        self._capture()
        reward, done = self._calculateReward()

        return self.camera_output,reward,done,""

    def _takeAction(self,action):
        #Implement a given action

        #left, right, forward
        if (action == 0):
            print("Left")
            self.leftMotor.setSpeed(125)
            self.rightMotor.setSpeed(75)
        elif(action == 1):
            print("RIGHT")
            self.leftMotor.setSpeed(75)
            self.rightMotor.setSpeed(125)
        elif(action == 2):
            print("FORWARD")
            self.leftMotor.setSpeed(125)
            self.rightMotor.setSpeed(125)
        else:
            #Shouldn't get here, if you do, just stop
            self.leftMotor.setSpeed(0)
            self.rightMotor.setSpeed(0)
    
    def _calculateReward(self):
        #Calculate a reward
        #if hitting something, reward -1
        #else reward 0.1
        if (self._hittingWall()):
            self._turnOffMotors()
            return -1,True
        else:
            return 0.1,False
        
    def _hittingWall(self):
        #return true if we're hitting a wall, false otherwise
        #Check the gaps in the queue
        pictureDifference = 0
        for i,im in enumerate(self.queue):
            if (i > 0):
                pictureDifference += np.sum(np.abs(im - lastIm))
            lastIm = im

        if pictureDifference > self.threshold:
            return False
        else:
            print("HIT WALL")
            return True

    def _capture(self):
        #capture image, store it in camera_output
        self.camera.capture(self.camera_output_raw, 'rgb')
        self.camera_output = self.camera_output_raw.flatten()
        self.queue.popleft()
        self.queue.append(self.camera_output)
        return ""
    
    def _backOutOfTrouble(self):
        #Hit a wall? Get outta here then stop and re-evaluate
        self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
        self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
        self.leftMotor.setSpeed(125)
        self.rightMotor.setSpeed(125)
        time.sleep(1.0)
        self._turnOffMotors()
        return ""
        
    def _turnOffMotors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
        return ""
