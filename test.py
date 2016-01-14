import RPi.GPIO as GPIO
import time
import utils

#GPIO.setmode(GPIO.BOARD)

#pwr = utils.PSU(13, 15)

#pwr.on()

#pwr.off()

#GPIO.cleanup()

#if float(format(utils.get_tset(), '.2f')) >= float(format(utils.get_temp(), '.2f')):
#    print 1
#else:
#    print 0
#a = float(format(utils.get_tset(), '.2f'))
#print a
#print type(a)
#b = float(format(utils.get_temp(), '.2f'))
#print b
#print type(b)

#print round(utils.get_temp(), 2)

#print round(utils.get_tset(), 1)
#print round(utils.get_temp(), 1)


for i in range(-20,20):
    print i % 4
