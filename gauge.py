import pygame as py
import pygame.gfxdraw
import math
import serial

# import pygame module in this program
import pygame
 
# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()
 
# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
 
# assigning values to X and Y variable
X = 480
Y = 480
 
# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))
 
# set the pygame window name
pygame.display.set_caption('Show Text')
 
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 64)
 
# create a text surface object,
# on which text is drawn on it.
text = font.render('Loading', True, green, blue)
 
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
 
# set the center of the rectangular object.
textRect.center = (X // 2, Y // 2)
 
# infinite loop



def loading():
    display_surface.fill(white)  
    display_surface.blit(text, textRect)
    time.sleep(5)
    imp = pygame.image.load("./logo.jpg").convert() 
    display_surface.blit(imp, (0, 0))    
    pygame.display.flip()




loading();