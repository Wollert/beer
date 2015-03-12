# Various classes to cover different types of simple hardware
# http://sourceforge.net/p/raspberry-gpio-python/wiki/Home/

import RPi.GPIO as GPIO
import time
import os
import glob
import MySQLdb
import signal
import sys
from Adafruit_ADS1x15 import ADS1x15

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

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

    def set_DC(self, dc):
        if dc <= 100 and dc >= 0:
            self.dc = dc
        self.p.ChangeDutyCycle(self.dc)
        return dc

    def setDC(self, dc):
        return self.set_DC(dc)

    def change_DC(self, reldc):
        self.reldc = reldc
        return self.p.set_DC(self.dc + self.reldc)

    def changeDC(self, reldc):
        return self.change_DC(reldc)

# Get data from 1-wire temperature probes
class Therm(object):

    def __init__(self, adr):
        self.adr = adr
        self.device_file = '/sys/bus/w1/devices/' + self.adr + '/w1_slave'

    def read_raw(self):
        self.f = open(self.device_file, 'r')
        self.lines = self.f.readlines()
        self.f.close()
        return self.lines

    def read_temp_raw(self):
        return self.read_raw()

    def read(self):
        self.lines = self.read_raw()
        while self.lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            self.lines = self.read_temp_raw()
        self.equals_pos = self.lines[1].find('t=')
        if self.equals_pos != -1:
            self.temp_string = self.lines[1][self.equals_pos+2:]
            self.temp_c = float(self.temp_string) / 1000.0
            return self.temp_c

    def read_temp(self):
        return self.read()

    def store(self):
        self.temp = self.read_temp()
        db = MySQLdb.connect(user="beeruser",db="beerdb")
        c = db.cursor()
        c.execute("""UPDATE Temperature SET Value=%s, Time=now() where Address=%s""",(self.temp, self.adr))
        db.commit()
        return self.temp

    def store_temp(self):
        return self.store()

# Returns the addresses of all connected 1-wire devices
def get_1w_adr():
    folders = glob.glob('/sys/bus/w1/devices/*')
    adr = []
    for i in range(len(folders)):
       adr.append((folders[i])[-12:])
    return adr


# Get data from ADC and load cells
class Load(object):
    def __init__(self):
        self.adc = ADS1x15(ic=0x01)
        self.pga = 256
        self.sps = 8
        self.load = 0        

    def read(self, ch):
        if ch == 1:
            self.load = self.adc.readADCDifferential(0, 1, self.pga, self.sps)
        if ch == 2:
            self.load = self.adc.readADCDifferential(2, 3, self.pga, self.sps)
        else:
            pass
        return self.load

    def read_load(self, ch):
        return self.read(ch) 

    def store(self, ch):
        self.read_load(ch)
        db = MySQLdb.connect(user="beeruser",db="beerdb")
        c = db.cursor()
        c.execute("""UPDATE LoadCell SET Value=%s, Time=now() where ID=%s""",(self.load, ch))
        db.commit()
        return self.load

    def store_load(self, ch):
        return self.store(ch)

    def set_empty(self):
        l1 = self.read(1)
        l2 = self.read(2)
        db = MySQLdb.connect(user="beeruser",db="beerdb")
        c = db.cursor()
        c.execute("""UPDATE LoadCell SET Value=%s, Time=now() where ID=3""",(l1 + l2))
        db.commit()
        return (l1 + l2)

    def set_full(self):
        l1 = self.read(1)
        l2 = self.read(2)
        db = MySQLdb.connect(user="beeruser",db="beerdb")
        c = db.cursor()
        c.execute("""UPDATE LoadCell SET Value=%s, Time=now() where ID=4""",(l1 + l2))
        db.commit()
        return (l1 + l2)

    def set_missing(self):
        l1 = self.read(1)
        l2 = self.read(2)
        db = MySQLdb.connect(user="beeruser",db="beerdb")
        c = db.cursor()
        c.execute("""UPDATE LoadCell SET Value=%s, Time=now() where ID=5""",(l1 + l2))
        db.commit()
        return (l1 + l2)


