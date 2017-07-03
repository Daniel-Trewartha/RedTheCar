from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import sys, tty, termios, time, atexit, os

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
# resolution = (128,128)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

##### DC motor test!
myRightMotor = mh.getMotor(3)
myLeftMotor = mh.getMotor(2)

# camera = picamera.PiCamera()
# camera.resolution = resolution
# time.sleep(2)

myRightMotor.run(Adafruit_MotorHAT.FORWARD)
myLeftMotor.run(Adafruit_MotorHAT.FORWARD)


# The getch method can determine which key has been pressed
# by the user on the keyboard by accessing the system files
# It will then return the pressed key as a variable
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# Instructions for when the user has an interface
print("w/s: acceleration")
print("a/d: steering")
print("x: exit")

# Infinite loop that will not end until the user presses the
# exit key
while True:
    # Keyboard character retrieval method is called and saved
    # into variable
    char = getch()

    # The car will drive forward when the "w" key is pressed
    if(char == "w"):
            myRightMotor.setSpeed(100)
            myLeftMotor.setSpeed(100)

    # The car will reverse when the "s" key is pressed
    if(char == "s"):
            myRightMotor.setSpeed(0)
            myLeftMotor.setSpeed(0)

    # The "a" key will toggle the steering left
    if(char == "a"):
            myRightMotor.setSpeed(125)
            myLeftMotor.setSpeed(75)

    # The "d" key will toggle the steering right
    if(char == "d"):
            myRightMotor.setSpeed(75)
            myLeftMotor.setSpeed(125)

    # The "x" key will break the loop and exit the program
    if(char == "x"):
        print("Program Ended")
        break

    # The keyboard character variable will be set to blank, ready
    # to save the next key that is pressed
    char = ""

# Program will cease all GPIO activity before terminating
turnOffMotors()
