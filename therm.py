import os 
import glob 
import time 
import MySQLdb

#os.system('modprobe w1-gpio') 
#os.system('modprobe w1-therm') 

#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0] 
#device_file = device_folder + '/w1_slave' 

#db = MySQLdb.connect(user="beeruser",db="beerdb")
#c = db.cursor()

class Therm(object):
    
    def __init__(self, adr):
        self.adr = adr
        self.device_file = '/sys/bus/w1/devices/' + self.adr + '/w1_slave'
#        self.db = MySQLdb.connect(user="beeruser",db="beerdb")
#        self.c = self.db.cursor()

    def read_temp_raw(self):
        self.f = open(self.device_file, 'r')
        self.lines = self.f.readlines()
        self.f.close()
        return self.lines

    def read_temp(self):
        self.lines = self.read_temp_raw()
        while self.lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            self.lines = self.read_temp_raw()
        self.equals_pos = self.lines[1].find('t=')
        if self.equals_pos != -1:
            self.temp_string = self.lines[1][self.equals_pos+2:]
            self.temp_c = float(self.temp_string) / 1000.0
            return self.temp_c

    def store_temp(self):
        self.temp = self.read_temp()
        db = MySQLdb.connect(user="beeruser",db="beerdb")
        c = db.cursor()
        c.execute("""UPDATE Temperature SET Value=%s, Time=now() where Address=%s""",(self.temp, self.adr))
        db.commit()
        return self.temp

def get_adr():
    folders = glob.glob('/sys/bus/w1/devices/*')
    adr = []
    for i in range(len(folders)):
       adr.append((folders[i])[-12:])
    return adr

