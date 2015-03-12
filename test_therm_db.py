import RPi.GPIO as GPIO
import time
import utils

GPIO.setmode(GPIO.BOARD)

#pwr = utils.PSU(13, 15)
#pwr.on()
#pwr.off()

adresses = utils.get_1w_adr()
samples = 5
therms = []
now = time.time()

t_amb = utils.Therm('28-000004e08693')
t_c_b = utils.Therm('28-000004e0f7cc')
t_c_m = utils.Therm('28-000004e0840a')
t_c_t = utils.Therm('28-000004e08e26')
t_hs  = utils.Therm('28-000004e0804f')

print time.time() - now
now = time.time()

#t_hs.store_temp()

#print time.time() - now
#now = time.time()

for i in range(samples):
    temp_row = [t_amb.store_temp(), t_c_b.store_temp(), t_c_m.store_temp(), t_c_t.store_temp(), t_hs.store_temp()]
    print temp_row
    therms.append(temp_row)
    print time.time() - now
    now = time.time()

print therms

#GPIO.cleanup()

