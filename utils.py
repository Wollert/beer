# Various classes to cover different types of simple hardware
# http://sourceforge.net/p/raspberry-gpio-python/wiki/Home/

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# GPIO.setwarnings(False)

# Controling a power supply 
class PSU:

    def __init__(self, pson, psok):
        self.pson = pson
        self.psok = psok
        
        GPIO.setup(self.pson, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.psok, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def on(self):
        GPIO.output(self.pson, 0)

    def off(self):
        GPIO.output(self.pson, 1)

    def ok(self):
        return GPIO.input(self.psok)

    def get(self):
        return not GPIO.input(self.pson)


# Controling a NMOS transistor
class NMOS:

    def __init__(self, ctrl):
        self.ctrl = ctrl
        GPIO.setup(self.ctrl, GPIO.OUT, initial=GPIO.LOW)
        
    def on(self):
        GPIO.output(self.ctrl, 1)

    def off(self):
        GPIO.output(self.ctrl, 0)

    def get(self):
        return GPIO.input(self.ctrl)


# Control fan-speed with a 25kHz pwm-signal
class Fan:

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.dc = 0
        GPIO.setup(self.ctrl, GPIO.OUT)
        self.p = GPIO.PWM(self.ctrl, 25000)
        self.p.start(self.dc)

    def setDC(self, dc):
        if dc <= 100 and dc >= 0:
            self.dc = dc
        self.p.ChangeDutyCycle(self.dc)
        return dc

    def changeDC(self, reldc):
        self.reldc = reldc
        return self.p.setDC(self.dc + self.reldc)
