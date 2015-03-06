import RPi.GPIO as GPIO
import time
import utils

GPIO.setmode(GPIO.BOARD)

pwr = utils.PSU(13, 15)
fan = utils.Fan(32)

pwr.on()
print "Power on!"

for i in range(10):
    print i
    print pwr.ok()
    time.sleep(1)

pwr.off()
print "Power off!"

for i in range(10):
    print i
    print pwr.ok()
    time.sleep(1)

pwr.on()
print "Power on!"

for i in range(10):
    print i
    print pwr.ok()
    time.sleep(1)

print "Power off!"



GPIO.cleanup()

