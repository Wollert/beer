import RPi.GPIO as GPIO
import time
import utils

GPIO.setmode(GPIO.BOARD)

t_amb = utils.Therm('28-000004e08693')
t_c_b = utils.Therm('28-000004e0f7cc')
t_c_m = utils.Therm('28-000004e0840a')
t_c_t = utils.Therm('28-000004e08e26')
t_hs  = utils.Therm('28-000004e0804f')

try:
    while utils.keep_running():
        t_amb.store_temp()
        t_c_b.store_temp()
        t_c_m.store_temp()
        t_c_t.store_temp()
        t_hs.store_temp()
except:
    pass
