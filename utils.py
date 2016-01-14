
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
        db = MySQLdb.connect(user="beeruser",db="beerdb")
        c = db.cursor()
        c.execute("""UPDATE Times SET Time=Now(), Flag = 1 WHERE ID = 3""")
        db.commit()

    def off(self):
        GPIO.output(self.pson, 1)
        db = MySQLdb.connect(user="beeruser",db="beerdb")
        c = db.cursor()
        c.execute("""UPDATE Times SET Time=Now(), Flag = 0 WHERE ID = 3""")
        db.commit()

    def ok(self):
        return GPIO.input(self.psok)
        db = MySQLdb.connect(user="beeruser",db="beerdb")
        c = db.cursor()
        c.execute("""UPDATE Times SET Time=Now() WHERE ID = 6""")
        db.commit()

    def get(self):
        return not GPIO.input(self.pson)

# Controling a NMOS transistor
class NMOS:

    def __init__(self, ctrl, dbid = 0):
        self.ctrl = ctrl
        self.dbid = dbid
        GPIO.setup(self.ctrl, GPIO.OUT, initial=GPIO.LOW)
        
    def on(self):
        GPIO.output(self.ctrl, 1)
        if self.dbid != 0:
            db = MySQLdb.connect(user="beeruser",db="beerdb")
            c = db.cursor()
            c.execute("""UPDATE Times SET Time=Now(), Flag = 1 WHERE ID = %s""",(self.dbid))
            db.commit()

    def off(self):
        GPIO.output(self.ctrl, 0)
        if self.dbid != 0:
            db = MySQLdb.connect(user="beeruser",db="beerdb")
            c = db.cursor()
            c.execute("""UPDATE Times SET Time=Now(), Flag = 0 WHERE ID = %s""",(self.dbid))
            db.commit()

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
            if self.dc == 0 and dc > 0:
                db = MySQLdb.connect(user="beeruser",db="beerdb")
                c = db.cursor()
                c.execute("""UPDATE Times SET Time=Now(), Flag = 1 WHERE ID = 1""")
                db.commit()
            elif self.dc > 0 and dc == 0:
                db = MySQLdb.connect(user="beeruser",db="beerdb")
                c = db.cursor()
                c.execute("""UPDATE Times SET Time=Now(), Flag = 0 WHERE ID = 1""")
                db.commit()
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


# Returns the temperature of either ID(1) or address(0), or the average of 
# the probes inside the cooler(adr = 0).
def get_temp(adr=0, mode=1):
    temp = 0
    db = MySQLdb.connect(user="beeruser",db="beerdb")
    c = db.cursor()
    if(adr == 0):
        c.execute("""SELECT avg(Value) FROM Temperature WHERE ID<4""")
    elif(mode):
        c.execute("""SELECT Value FROM Temperature WHERE ID=%s""",(adr))
    else:
        c.execute("""SELECT Value FROM Temperature WHERE Address<%s""",(adr))
    temp = c.fetchone()[0]
    return float(temp)


# Sets the value at position with the given id.
def set_temp(id, val):
    db = MySQLdb.connect(user="beeruser",db="beerdb")
    c = db.cursor()
    c.execute("""UPDATE Temperature SET Value=%s, Time=now() where ID=%s""",(int(val), id))
    db.commit()
 

# Returns the ambient temperature (ID=4)
def get_tamb():
    return get_temp(4)


# Returns the temperature at the heat sink (ID=5)
def get_ths():
    return get_temp(5)


# Returns the maximum permitted temperature at the heat sink (ID=6)
def get_thsmax():
    return get_temp(6)

def set_thsmax(val):
    set_temp(6, val)


# Returns the current target temperature (ID=7)
def get_tset():
    return get_temp(7)

def set_tset(val):
    set_temp(7, val)


# Returns the maximum setable target temperature (ID=8)
def get_tsetmax():
    return get_temp(8)

def set_tsetmax(val):
    set_temp(8, val)


# Returns the minimum setable target temperature (ID=9)
def get_tsetmin():
    return get_temp(9)

def set_tsetmin(val):
    set_temp(9, val)


# Returns the addresses of all connected 1-wire devices
def get_1w_adr():
    folders = glob.glob('/sys/bus/w1/devices/*')
    adr = []
    for i in range(len(folders)):
       print (folders[i])[-13]
       if (folders[i])[-13] == '-':
           adr.append((folders[i])[-15:])
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
        self.read(ch)
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


# Gets the sums of the current loads in the db, mode 0: raw value, mode 1: percent of full keg
def get_load(mode=1):
    db = MySQLdb.connect(user="beeruser",db="beerdb")
    c = db.cursor()
    c.execute("""SELECT sum(Value) FROM LoadCell WHERE ID<3""")
    l = float(c.fetchone()[0])
    if mode:
        c.execute("""SELECT Value FROM LoadCell WHERE ID = 3 OR ID = 4""")
        le = float(c.fetchone()[0])
        lf = float(c.fetchone()[0])
        lpros = 100 * (l - le) / (lf - le)
#        print le
#        print lf
        return lpros
    else:
        return l


# Sets the sum of the current loads in the db as the value for an empty keg
def set_empty_keg():
    db = MySQLdb.connect(user="beeruser",db="beerdb")
    c = db.cursor()
    l = 0
    reps = 10
    for i in range(reps):
        c.execute("""SELECT sum(Value) FROM LoadCell WHERE ID<3""")
        l = l + float(c.fetchone()[0])
        time.sleep(0.2)
    c.execute("""UPDATE LoadCell SET Value=%s, Time=now() where ID=3""",l/reps)
    db.commit()
    return l/reps


# Sets the sum of the current loads in the db as the value for a full keg
def set_full_keg():
    db = MySQLdb.connect(user="beeruser",db="beerdb")
    c = db.cursor()
    l = 0
    reps = 10
    for i in range(reps):
        c.execute("""SELECT sum(Value) FROM LoadCell WHERE ID<3""")
        l = l + float(c.fetchone()[0])
        time.sleep(0.2)
    c.execute("""UPDATE LoadCell SET Value=%s, Time=now() where ID=4""",l/reps)
    db.commit()
    return l/reps


# Sets the sum of the current loads in the db as the value when the keg is missing
def set_missing_keg():
    db = MySQLdb.connect(user="beeruser",db="beerdb")
    c = db.cursor()
    l = 0
    reps = 10
    for i in range(reps):
        c.execute("""SELECT sum(Value) FROM LoadCell WHERE ID<3""")
        l = l + float(c.fetchone()[0])
        time.sleep(0.2)
    c.execute("""UPDATE LoadCell SET Value=%s, Time=now() where ID=5""",l/reps)
    db.commit()
    return l/reps


# Gets the input from a switch/button, with events (without bouncetime) for change of state
class Button:

    BUTTONDOWN = 3
    BUTTONUP = 4

    def __init__(self,button,callback,dbid):
        self.button = button
        self.callback = callback
        self.dbid = dbid

        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)
        GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Add event to the GPIO input
#        GPIO.add_event_detect(self.button, GPIO.BOTH, callback=self.button_event, bouncetime=200)
        GPIO.add_event_detect(self.button, GPIO.BOTH, callback=self.button_event)

    def button_event(self,button):
        if GPIO.input(button):
            event = self.BUTTONUP
            if self.dbid != 0:
                db = MySQLdb.connect(user="beeruser",db="beerdb")
                c = db.cursor()
                c.execute("""UPDATE Times SET Time=Now(), Flag = 1 WHERE ID = %s""",(self.dbid))
                db.commit()
        else:
            event = self.BUTTONDOWN
            if self.dbid != 0:
                db = MySQLdb.connect(user="beeruser",db="beerdb")
                c = db.cursor()
                c.execute("""UPDATE Times SET Time=Now(), Flag = 0 WHERE ID = %s""",(self.dbid))
                db.commit()
        self.callback(event)
        return


# Kill signal
def keep_running():
    db = MySQLdb.connect(user="beeruser",db="beerdb")
    c = db.cursor()
    c.execute("""SELECT Flag FROM Times WHERE ID=7""")
    flag  = int(c.fetchone()[0])
    if not flag:
        return True
    else:
        return False

def start_running():
    db = MySQLdb.connect(user="beeruser",db="beerdb")
    c = db.cursor()
    c.execute("""UPDATE Times SET Flag = 0 WHERE ID = 7""")
    db.commit()

def stop_running():
    db = MySQLdb.connect(user="beeruser",db="beerdb")
    c = db.cursor()
    c.execute("""UPDATE Times SET Flag = 1 WHERE ID = 7""")
    db.commit()
