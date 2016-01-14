import RPi.GPIO as GPIO
import time
import utils
import subprocess

GPIO.setmode(GPIO.BOARD)

def door_event(event):
    if event == utils.Button.BUTTONDOWN:
        light.off()
    elif event == utils.Button.BUTTONUP:
        light.on()
    return

utils.start_running()

cooling_state = 0 # 0: cooler off, 1: cooler off, 2: relay off & fan on

pwr = utils.PSU(13, 15)
fan = utils.Fan(32)
pump = utils.NMOS(11,8)
relay = utils.NMOS(16,2)
light = utils.NMOS(12,4)
door = utils.Button(31, door_event,5)

gui = subprocess.call("sudo python /home/pi/beer/run_gui.py &", shell=True)
load = subprocess.call("sudo python /home/pi/beer/run_load.py &", shell=True)
therm = subprocess.call("sudo python /home/pi/beer/run_therm.py &", shell=True)

pwr.on()

# Temporary solution ##
#fan.setDC(90)
#pump.on()
#relay.on()
#######################

while utils.keep_running():
    if utils.get_thsmax() <= utils.get_ths():
        print "Heat sink is: %s" %utils.get_ths()
        cooling_state = 0
        print cooling_state
        utils.stop_running()
        break
    elif cooling_state == 0:
        if round(utils.get_tset(), 1) <= round(utils.get_temp(), 1):
            cooling_state = 1
            print cooling_state
            fan.setDC(90)
            pump.on()
            relay.on()
    elif cooling_state == 1:
        if round(utils.get_tset(), 1) > round(utils.get_temp(), 1):
            cooling_state = 2
            print cooling_state
            relay.off()
    elif cooling_state == 2:
        if round(utils.get_tset(), 1) <= round(utils.get_temp(), 1):
            cooling_state = 1
            print cooling_state
            relay.on()
        elif round(utils.get_tamb(), 1) > round(utils.get_ths(), 1):
            cooling_state = 0
            print cooling_state
            fan.setDC(0)
            pump.off()
    else:
        utils.stop_running()
    time.sleep(0.01)
    

print "Shutting down."
light.off()
relay.off()
time.sleep(1)
pump.off()
fan.setDC(0)
pwr.off()
GPIO.cleanup()
print "Goodbye!"
