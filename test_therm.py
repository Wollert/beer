import RPi.GPIO as GPIO
import time
import utils
import therm

GPIO.setmode(GPIO.BOARD)

#pwr = utils.PSU(13, 15)
#pwr.on()
#pwr.off()

adresses = therm.get_adr()
samples = 5
therms = []
now = time.time()

t_amb = therm.Therm('28-000004e08693')
t_c_b = therm.Therm('28-000004e0f7cc')
t_c_m = therm.Therm('28-000004e0840a')
t_c_t = therm.Therm('28-000004e08e26')
t_hs  = therm.Therm('28-000004e0804f')

print time.time() - now
now = time.time()

for i in range(samples):
    temp_row = [t_amb.read_temp(), t_c_b.read_temp(), t_c_m.read_temp(), t_c_t.read_temp(), t_hs.read_temp()]
    print temp_row
    therms.append(temp_row)
    print time.time() - now
    now = time.time()

print therms

#GPIO.cleanup()

