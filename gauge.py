import pygame as py
import pygame.gfxdraw
import math
import serial
import time
import pygame
 
 
pygame.init()
X = 480
Y = 480
display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Gauge')
 
# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)



def FirstBoot():
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render('Loading', True, green, white)
    imp = pygame.image.load("logo.jpg").convert() 
    logo_rect = imp.get_rect(center = display_surface.get_rect().center)
    display_surface.blit(imp, logo_rect)    
    pygame.display.update()
    time.sleep(5)
    textRect = text.get_rect()
    textRect.center = (X // 2, Y // 2)
    display_surface.fill(white)
    display_surface.blit(text, textRect)
    pygame.display.update()
    time.sleep(5)
    
    
    




####
#
# Starting bit
#
####
firstBoot()