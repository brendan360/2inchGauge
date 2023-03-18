import pygame as py
import pygame.gfxdraw
import math
import serial
import time
import pygame
import RPi.GPIO as GPIO
import requests
import struct
import os
import socket
from hyperpixel2r import Touch


 
###
#
#display setup
#
### 
pygame.init()
X = 480
Y = 480
display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Gauge')
 
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255,0,0)
black = (0,0,0)

Loadingfont = pygame.font.Font('freesansbold.ttf', 60)

###
#
#touch setup
#
###
touch = Touch(bus=11, i2c_addr=0x15, interrupt_pin=27):


###
#
#GLOABL variables
#
###
address="/home/pi/2inchGauge/"

bootState={"Bluetooth":[0,"fail",0],
           "obd":[0,"fail",0]
           }

####
#
#FUNCTIONS
#
####
def functFIRSTBOOT():

    display_surface.fill(white)
    pygame.display.update()
    imp = pygame.image.load(address+"logo.jpg").convert() 
    logo_rect = imp.get_rect(center = display_surface.get_rect().center)
    display_surface.blit(imp, logo_rect)    
    pygame.display.update()
    time.sleep(4)
    functINITCOMMS()

def functINITCOMMS():
    print("starting comms")
    display_surface.fill(black)
    text = Loadingfont.render("BOOTING", True, black, red)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2 - 70)
    display_surface.blit(text, textRect)
    pygame.display.update()
  
def functCONNECTBT():
    print("starting BT")

def functCONNECTOBD():
    print("starting OBD")
   
    
    
def functREINITIALISE():
    firstBoot()
  
def functGETIPADDRESS():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@touch.on_touch
def handle_touch(touch_id, x, y, state):
    print(touch_id, x, y, state)



####
#
# Starting bit
#
####
functFIRSTBOOT()
time.sleep(5)