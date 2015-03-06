import RPi.GPIO as GPIO
import time
import utils

GPIO.setmode(GPIO.BOARD)

pwr = utils.PSU(13, 15)
fan = utils.Fan(32)

pwr.on()
print "Power on!"

lights = utils.NMOS(12)

lights.on()
print "Lights on!"

for i in range(5):
    print lights.get()
    time.sleep(1)

lights.off()
print "Lights off!"

for i in range(5):
    print lights.get()
    time.sleep(1)

lights.on()
print "Lights on!"

for i in range(5):
    print lights.get()
    time.sleep(1)

lights.off()
print "Lights off!"

pwr.off()
print "Power off!"

GPIO.cleanup()

