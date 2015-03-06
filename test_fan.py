import RPi.GPIO as GPIO
import time
import utils

GPIO.setmode(GPIO.BOARD)

pwr = utils.PSU(13, 15)
fan = utils.Fan(32)

pwr.on()

print "Power on!"

while not pwr.ok():
   time.sleep(0.1)

print "Power OK!"

for dc in range(0,101,10):
    print "Fan dc = %d", dc
    time.sleep(3)
    fan.setDC(dc)

time.sleep(3)

#time.sleep(5)

#fan.setDC(100)
#print "Fan dc = 100"

#time.sleep(5)

pwr.off()
print "Power off!"

GPIO.cleanup()

