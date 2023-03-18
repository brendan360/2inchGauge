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
import git 

 
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

Loadingfont = pygame.font.Font('freesansbold.ttf', 80)


###
#
#GLOABL variables
#
###
sea_level_pressure = 1010
presURL = "https://api.manly.hydraulics.works/api.php?page=latest-readings&id=60284042&username=publicwww"
address="/home/pi/gauge/"



####
#
#FUNCTIONS
#
####
def functFIRSTBOOT():

    display_surface.fill(white)

    imp = pygame.image.load(address+"logo.jpg").convert() 
    logo_rect = imp.get_rect(center = display_surface.get_rect().center)
    display_surface.blit(imp, logo_rect)    
    pygame.display.update()
    time.sleep(5)
    newtext=functGETIPADDRESS()
    text = Loadingfont.render(newtext, True, red, white)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2)
    display_surface.blit(text, textRect)
    pygame.display.update()
    functGETSEALEVEL()
    
    
    
def functREINITIALISE():
    firstBoot()

 
def funtREBOOTPI():
    drawimage=setupDisplay()
    image=drawimage[0]
    draw=drawimage[1]
    draw.text((30,85),"REBOOT", font=font, fill=255)
    draw.text((20,150),"Press button to cancel",font=font2, fill="WHITE")
    tempcount=0
    draw.text((60,30),"..........", font=font, fill="WHITE")
    im_r=image.rotate(rotation)
    disp.ShowImage(im_r)
    button_held=False
    while tempcount <=10:
        if not button.value and not button_held:
            button_held = True
        if button.value and button_held:
            button_held = False
            menuloop(4,configmenu)
        diedots="."*tempcount
        draw.text((60,30),diedots, font=font, fill=255)
        im_r=image.rotate(rotation)
        disp.ShowImage(im_r)
        time.sleep(1)
        tempcount+=1

    os.system('sudo reboot')
 
def functUPDATE():
    highlightDisplay("Updating","Car Guage")
    
    git.Repo(address).remotes.origin.fetch()
    diff = str(git.Repo(address).git.diff('origin/master')).splitlines()
    if len(diff) != 0:
        highlightDisplay("Processing","Update")
        git.Repo(address).remote().pull()
        reboot_pi()
    else:
        highlightDisplay("No Update","Update")
        time.sleep(3)
  
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

def functGETSEALEVEL():
    try:
        url=requests.get(presURL)
        text = url.text
        data= json.loads(text)
        pressure=data['60284042']['value']
        cleanpressure=str(pressure).replace("[","")
        cleanpressure=cleanpressure.replace("]","")
        print(cleanpressure)
    except:
        print("no internet using defeault sealevel")
        cleanpressure=sea_level_pressure  
        




####
#
# Starting bit
#
####
functFIRSTBOOT()