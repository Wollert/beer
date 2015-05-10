import pygame
import os
import time
import utils
import sys
from rotary_class import RotaryEncoder

# Set the PiTFT as display
os.putenv('SDL_FBDEV', '/dev/fb1')

#Definitions
MAIN_PAGE_BACKGROUND_COLOR = (128, 0, 218)
MAIN_PAGE_TEXT_COLOR = (255, 255, 255)
BEER_COLOR = (251, 177, 23)
MAIN_PAGE_FONT_SIZE = 70
TARGET_TEMPERATURE = utils.get_tset()
MAX_TEMPERATURE = utils.get_tsetmax()
MIN_TEMPERATURE = utils.get_tsetmin()
CURRENT_SCREEN = 1
PIN_A = 36 
PIN_B = 38
BUTTON = 40
load = utils.get_load()

# Event callback routine for rotary encoder
def switch_event(event):
    if CURRENT_SCREEN == 1:
        global TARGET_TEMPERATURE
        if event == RotaryEncoder.CLOCKWISE:
            if (TARGET_TEMPERATURE + 0.2) < MAX_TEMPERATURE:
                TARGET_TEMPERATURE = TARGET_TEMPERATURE + 0.2
        if event == RotaryEncoder.ANTICLOCKWISE:
            if (TARGET_TEMPERATURE - 0.2) > MIN_TEMPERATURE:
                TARGET_TEMPERATURE = TARGET_TEMPERATURE - 0.2
        if event == RotaryEncoder.BUTTONDOWN:
            pass
        if event == RotaryEncoder.BUTTONUP:
            pass
        utils.set_tset(TARGET_TEMPERATURE)

# Initiate pygame and fill the screen
pygame.init()
lcd = pygame.display.set_mode((320, 240))
lcd.fill(MAIN_PAGE_BACKGROUND_COLOR)
pygame.display.update()
pygame.mouse.set_visible(False)
font_big = pygame.font.Font(None, MAIN_PAGE_FONT_SIZE)

# Initiate the rotary encoder
rswitch = RotaryEncoder(PIN_A, PIN_B, BUTTON, switch_event)

#for i in range(0,20):
while True:
    if CURRENT_SCREEN == 1:
        lcd.fill(MAIN_PAGE_BACKGROUND_COLOR)
        # Draws the current temperature
        temperature = utils.get_temp()
        text_surface1 = font_big.render('%.1f'%temperature, True, MAIN_PAGE_TEXT_COLOR)
        rect1 = text_surface1.get_rect(center=(100,70))
        lcd.blit(text_surface1, rect1)
        # Draws the target temperature
        text_surface2 = font_big.render('%.0f'%TARGET_TEMPERATURE, True, MAIN_PAGE_TEXT_COLOR)
        rect2 = text_surface2.get_rect(center=(100,170))
        lcd.blit(text_surface2, rect2)
        # Draws the keg
        load = (load + utils.get_load())/2
        pygame.draw.rect(lcd, BEER_COLOR, [200, (220-(2*load)), 100, (2*load)])
        pygame.draw.rect(lcd, (0, 0, 0), [200, 20, 100, 200], 3)

    pygame.display.update()
    time.sleep(0.1)
