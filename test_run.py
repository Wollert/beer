import RPi.GPIO as GPIO
import time
import utils


GPIO.setmode(GPIO.BOARD)

pwr = utils.PSU(13, 15)

pwr.on()
print "Power on"

fan = utils.Fan(32)
fan.setDC(90)
print "Fan set at 90%"

pump = utils.NMOS(11)
pump.on()
print "Pump on"

relay = utils.NMOS(16)
relay.on()
print "Peltier on"

t_amb = utils.Therm('28-000004e08693')
t_c_b = utils.Therm('28-000004e0f7cc')
t_c_m = utils.Therm('28-000004e0840a')
t_c_t = utils.Therm('28-000004e08e26')
t_hs  = utils.Therm('28-000004e0804f')

try:
    while(1):
        print "Ambient temperature: " + str(t_amb.store_temp())
        print "Down temperature in cooler: " + str(t_c_b.store_temp())
        print "Middle temperature in cooler: " + str(t_c_m.store_temp())
        print "Up temperture in cooler: " + str(t_c_t.store_temp())
        print "Heatsink temperature: " + str(t_hs.store_temp())

except KeyboardInterrupt:
    print "Exiting gracefully"

relay.off()
print "Peltier off"

pump.off()
print "Pump off"

pwr.off()
print "Power off"

GPIO.cleanup()
print "Goodbye!"
