'''
@author Joe Crozier & Niko Savas
'''
import pygame

pygame.init()
#import shit

#GAME SETTINGS
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


running = True #If running is true, the game will play
tick_timer = pygame.time.Clock() #This timer will cap fps and tick once every ~16ms (60fps)

# Init function:
## make display


class Main:
    def initgame():
        Game = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        rungame()
    # Main loop:
    ## Check if the game is still running, otherwise close game
    ## Tick clock
    ## Check for user inputs
    def game_loop(self):
        self.framecount = 0 #how many frames have elapsed (resets every second)

        
        while running:
            tick_timer.tick(60)
            self.framecount+=1

            total_frames =0
            
            if(self.framecount==60):
                self.framecount=0
                total_frames+=1
                print total_frames,"--",pygame.time.get_ticks()
            
#Run the game loop
MainObject = Main()
MainObject.game_loop()
