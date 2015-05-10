# Testing the button class in utils.py

import sys
import time
import utils

def button_event(event):
    if event == utils.Button.BUTTONDOWN:
        print "Button down"
        light.off()
    elif event == utils.Button.BUTTONUP:
        print "Button up"
        light.on()
    return

light = utils.NMOS(12)

button = utils.Button(31,button_event)

while True:
    time.sleep(0.5)
