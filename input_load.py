import RPi.GPIO as GPIO
import time
import utils

GPIO.setmode(GPIO.BOARD)

last = utils.Load()

while(1):
    try:
        last.store(1)
    except:
        pass
    try:
        last.store(2)
    except:
        pass

#pwr = utils.PSU(13, 15)

#pwr.on()

#pwr.off()

GPIO.cleanup()

