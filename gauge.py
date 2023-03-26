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
import threading

from random import randint
 
 
###
#
#GLOBAL CONFIGS
#
###

address="/home/pi/2inchGauge/"

bootState={"bluetooth":[0,"fail",0],
           "obd":[0,"fail",0]
           }


#              obd name    PID,enabled or false, Friendly Name,value,pid squence, pid array,alertlow,alerthigh,rangelow,rangehigh,measurment,alertcount
gaugeItems={
"FUEL_LEVEL":["2F",0,"Fuel %","0",1,"b","na","na","20","90","%",0],
"SPEED":["0D",0,"Speed","0",2,"a","na","na","na","120","Km/h",0],
"INTAKE_TEMP":["0F",0,"Intake C","0",3,"a","na","100","20","80","°C",0],
"RPM":["0C",0,"RPM","0",4,"a","na","6000","1000","6000","RPM",0],
"OIL_PRESSURE":["D1",0,"Oil Pres","0",5,"d","na","na","10","150","Kpa",0],
"OIL_TEMP":["D1",0,"Oil Temp","0",5,"d","na","na","100","20","80","°C",0],
"COOLANT_PRESSURE":["D1",0,"Water Pres","0",5,"d","na","na","10","150","Kpa",0],
"COOLANT_TEMP":["D1",0,"Water Temp","0",5,"d","na","na","100","20","80","°C",0],
"FUEL_RAIL_PRES":["D1",0,"Fuel Pres","0",5,"d","na","na","10","150","Kpa",0],
"BOOST":["D1",0,"Boost","0",5,"d","na","na","0","15", "psi",0],
"WIDEBAND_02":["D1",0,"AFR","0",5,"d","na","na","4","10","A/F",0],
"BLOCK_TEMP":["D1",0,"Block Temp","0",5,"d","na","na","100","20","80","°C",0]

#"TIMING_ADVANCE":["0E",0,"Timing","0",13,"a","na","100",0],
#BAROMETRIC_PRESSURE":["33",0,"Air Pres","0",18,"b","na","na",0],
#"AMBIANT_AIR_TEMP":["46",0,"Air °C","0",5,"c","na","na",0],
#"THROTTLE_POS":["11",0,"Throttle","0",15,"a","na","na",0],
#"RUN_TIME":["1F",0,"Run Time","0",30,"a","na","na",0],
#"COOLANT_TEMP":["05",0,"Water °C","0",4,"a","na","100",0],
#"FUEL_PRESSURE":["0A",0,"Fuel Pres","0",9,"a","na","100",0],
#"INTAKE_PRESSURE":["0B",0,"Intake Pres","0",10,"a","na","100",0],
#"ENGINE_LOAD":["04",0,"Engine Load","0",3,"a","na","100",0],
#"MAF":["10",0,"MAF","0",15,"a","na","100",0],

}
 
 
 
 
 
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
font1 = pygame.font.Font('freesansbold.ttf', 30)
font2 = pygame.font.Font('freesansbold.ttf', 50)
font3 = pygame.font.Font('freesansbold.ttf', 60)
font4 = pygame.font.Font('freesansbold.ttf', 70)
font5 = pygame.font.Font('freesansbold.ttf', 80)
font6 = pygame.font.Font('freesansbold.ttf', 90)
font7 = pygame.font.Font('freesansbold.ttf', 115)


###
#
#touch setup
#
###
touch = Touch(bus=11, i2c_addr=0x15, interrupt_pin=27)



####
#
#FUNCTIONS
#
####

### booting functions
def functFIRSTBOOT():

    display_surface.fill(white)
    pygame.display.update()
    imp = pygame.image.load(address+"logo.jpg").convert() 
    logo_rect = imp.get_rect(center = display_surface.get_rect().center)
    display_surface.blit(imp, logo_rect)    
    pygame.display.update()
    time.sleep(2)
                
    display_surface.fill(black)         
    pygame.display.update()
    functINITCOMMS()

def functINITCOMMS():
#    functHIGHLIGHTDISPLAY("BOOTING","")
    functCONNECTBT()
    functCONNECTOBD()
  
def functCONNECTBT():
    global statusState
    statusState="na"
    i=0
    while i<5:
        time.sleep(2)
        try:
            threading.Thread(target=funtMENULOOP, args=(0,topmenu)).start()
         
            
        #    connection = obd.OBD(obdConnection, check_voltage=False, baudrate=9600)
        #    statusState=connection.status()
            if statusState == "Car Connected":
                bootState['bt']=(i,"win",1)
                functHIGHLIGHTBOOTDISPLAY()
                connection.close()
                return
            else:
                print("failing after winning")
                i=i+1
                time.sleep(1)
                bootState['bt']=(i,"fail",0)
                functHIGHLIGHTBOOTDISPLAY()
                continue
        except:
            print("failed thread")
            i=i+1
            bootState['bt']=(i,"fail",0)
            functHIGHLIGHTBOOTDISPLAY()   
            
    

def functCONNECTOBD():
    global statusState
    statusState="na"
    print("Connecting OBD")
    i=0
    while i<5:
        time.sleep(2)
        try:
            print("trying thread")
            threading.Thread(target=funtMENULOOP, args=(0,topmenu)).start()
         
            
        #    connection = obd.OBD(obdConnection, check_voltage=False, baudrate=9600)
        #    statusState=connection.status()
            if statusState == "Car Connected":
                print("     OBD conected")
                bootState['obd']=(i,"win",1)
                functHIGHLIGHTBOOTDISPLAY()
                connection.close()
                return
            else:
                print("failing after winning")
                i=i+1
                time.sleep(1)
                bootState['obd']=(i,"fail",0)
                functHIGHLIGHTBOOTDISPLAY()
                continue
        except:
            i=i+1
            bootState['obd']=(i,"fail",0)
            functHIGHLIGHTBOOTDISPLAY()   
    
    
     # if bootState['bt'][1]=="fail":
       # bootState['obd']=(5,"fail",0) 
       # return
    
     # if statusState == "Car Connected": 
        # return
        
     # else:
        # statusState=""
        # while i<5:
            # try:
                # connection = obd.OBD(obdConnection, check_voltage=False, baudrate=9600)
                # statusState=connection.status()
                # if statusState == "Car Connected":
                    # print("     OBD conected")
                    # bootState['obd']=(i,"win",1)
                    # functHIGHLIGHTBOOTDISPLAY()
                    # connection.close()
                    # return
                # else:
                    # i=i+1
                    # time.sleep(1)
                    # bootState['obd']=(i,"fail",0)
                    # functHIGHLIGHTBOOTDISPLAY()
                    # continue
            # except:
                # i=i+1
                # bootState['obd']=(i,"fail",0)
                # functHIGHLIGHTBOOTDISPLAY()
    print("")
        

### Printing functions
def functHIGHLIGHTBOOTDISPLAY():
    if bootState['bt'][1]=="fail":
        faildot="."*bootState['bt'][0]
        text = Loadingfont.render("bluetooth", True, white, black)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2 -80)
        display_surface.blit(text, textRect)

        display_surface.blit(text, textRect)
        text = Loadingfont.render(faildot, True, red, black)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2 -30)
        display_surface.blit(text, textRect)
        pygame.display.update()
        if bootState['bt'][0]==5:
            text = Loadingfont.render("bluetooth", True, red, black)
            textRect = text.get_rect()
            textRect.center = (X // 2, Y // 2 -80)
            display_surface.blit(text, textRect)
            pygame.display.update()

    else:
        faildot="."*bootState['bt'][0]
        text = Loadingfont.render("bluetooth", True, green, black)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2 -80)
        display_surface.blit(text, textRect)
        text = Loadingfont.render(faildot, True, green, black)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2 -30)
        display_surface.blit(text, textRect)
        pygame.display.update()
    
    
    if bootState['obd'][1]=="fail":
        faildot="."*bootState['obd'][0]
        text = Loadingfont.render("OBD", True, white, black)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2 +60)
        display_surface.blit(text, textRect)

        display_surface.blit(text, textRect)
        text = Loadingfont.render(faildot, True, red, black)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2 +120)
        display_surface.blit(text, textRect)
        pygame.display.update()
        if bootState['obd'][0]==5:
            text = Loadingfont.render("OBD", True, red, black)
            textRect = text.get_rect()
            textRect.center = (X // 2, Y // 2 +60)
            display_surface.blit(text, textRect)
            pygame.display.update()
            time.sleep(5)
    else:
        faildot="."*bootState['obd'][0]
        text = Loadingfont.render("OBD", True, green, black)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2+60)
        display_surface.blit(text, textRect)
        text = Loadingfont.render(faildot, True, green, black)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2 +120)
        display_surface.blit(text, textRect)
        pygame.display.update()
       

def functHIGHLIGHTDISPLAY(text1,text2):
    display_surface.fill(black)
    text = Loadingfont.render(text1, True, red, black)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2 -80)
    display_surface.blit(text, textRect)
    text = Loadingfont.render(text2, True, red, black)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2 +10 )
    display_surface.blit(text, textRect)
    pygame.display.update()
    time.sleep(5)
    
def functDISPLAYGAUGE(gaugeItem):
    display_surface.fill(black)

    center = (X // 2, Y // 2)
    radius = 220
    thickness =60
    start_angle = 6 * math.pi / 5  # 135 degrees
    end_angle = start_angle + 8 * math.pi / 5

    input_value =randint(10, 100)

# Determine gauge color based on input value
    if input_value < 30:
        gauge_color = blue
    elif input_value < 80:
        gauge_color = green
    else: 
        gauge_color = red

# Calculate the angle range based on input value
    angle_range = (end_angle - start_angle) * input_value / 100

# Draw the gauge background
    pygame.draw.arc(display_surface, black, (center[0]-radius, center[1]-radius, radius*2, radius*2), start_angle, end_angle, thickness)

# Draw the gauge fill
    pygame.draw.arc(display_surface, gauge_color, (center[0]-radius, center[1]-radius, radius*2, radius*2), start_angle, start_angle + angle_range, thickness)
    thickness = 40  
 
# Draw the center circle
    pygame.draw.circle(display_surface, black, center, thickness//2)
    
    text = font1.render(gaugeItems[gaugeItem][2], True, white, black)
    textRect = text.get_rect()
    textRect.center = (X // 2 -180 , Y // 2)
    display_surface.blit(text, textRect)
    text = font3.render(postfix, True, white, black)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2 +100)
    display_surface.blit(text, textRect)
    text = font7.render(str(input_value), True, white, black)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2)
    display_surface.blit(text, textRect) 
    pygame.draw.line(display_surface, black, (center[0] + radius * math.cos(start_angle + 0.2*(end_angle-start_angle)), center[1] + radius * math.sin(start_angle + 0.2*(end_angle-start_angle))), (center[0] + radius * math.cos(start_angle + 0.2*(end_angle-start_angle)), center[1] + radius * math.sin(start_angle + 0.2*(end_angle-start_angle))), thickness)
    pygame.draw.line(display_surface, black, (center[0] + radius * math.cos(start_angle + 0.8*(end_angle-start_angle)), center[1] + radius * math.sin(start_angle + 0.8*(end_angle-start_angle))), (center[0] + radius * math.cos(start_angle + 0.8*(end_angle-start_angle)), center[1] + radius * math.sin(start_angle + 0.8*(end_angle-start_angle))), thickness)
 


    pygame.display.update()


    pygame.display.flip()

 
    
    


### Helper functions
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



### Menu functions
def funtMENULOOP (item,menu):
    print("")
    
   







####
#
# Runtime
#
####
#functFIRSTBOOT()

while True:
        # FOR SHOWING CHANGE IN GAUGE
     # rangauge = ser.readline()
     # percentage = int(rangauge)
 #   percentage=randint(10, 100)
           # percentage = 0
         #       screen.fill(bg_c)
      #my_gauge.draw(percent=20)

    
    functDISPLAYGAUGE("SPEED")
    time.sleep(1)
 


#try:
#    threading.Thread(target=funtMENULOOP, args=(0,topmenu)).start()


#except:
#    functHIGHLIGHTDISPLAY("FAILED", "to START")
    
