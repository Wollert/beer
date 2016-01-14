# Gets the load (in mV across the Whetstone bridge) and stores it in the database. 

import RPi.GPIO as GPIO
import time
import utils

GPIO.setmode(GPIO.BOARD)

load = utils.Load()

while utils.keep_running():
    load.store(1)
    load.store(2)
    time.sleep(0.1)

#pwr = utils.PSU(13, 15)

#pwr.on()

#pwr.off()

GPIO.cleanup()

