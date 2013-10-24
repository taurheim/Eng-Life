'''
@author Joe Crozier & Niko Savas
'''
import pygame

pygame.init()
#import shit


running = True #If running is true, the game will play
tick_timer = pygame.time.Clock() #This timer will cap fps and tick once every ~16ms (60fps)
last_second = 0

# Init function:
## make display, set clock for framerate,

# Main loop:
## Check if the game is still running, otherwise close game
## Tick clock
## Check for user inputs

def rungame():
    while running:
        tick_timer.tick(60)
        last_second = pygame.time.get_ticks() - last_second
        print last_second
        
