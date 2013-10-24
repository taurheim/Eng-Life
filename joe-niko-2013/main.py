'''
@author Joe Crozier & Niko Savas
'''
import pygame
import player

pygame.init()
#import shit

#GAME SETTINGS
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


running = True #If running is true, the game will play
tick_timer = pygame.time.Clock() #This timer will cap fps and tick once every ~16ms (60fps)

# Init function:

class Main:
    def __init__(self):
        pygame.init() #Initialize PyGame
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 250, 250))

        
        self.screen.blit(self.background, (0,0))
        self.guy = player.Player(300,300)
        self.sprites = pygame.sprite.RenderPlain(self.guy)
        

        
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

            self.screen.blit(self.background, (0, 0)) #Draw background
            self.sprites.draw(self.screen)          #Draw sprites
            pygame.display.flip()                   #Make it happen
            

            ##Event Handling (not sure if this is how we'll actually do it, just testing)
            keys = pygame.key.get_pressed()
            print keys[pygame.K_DOWN]
            print pygame.key.get_focused()
            if keys[pygame.K_DOWN]:                     #NONE OF THIS IS ACTUALLY WORKING
                print "moving"
                self.guy.didMove(0,1)
            
 
            
            if(self.framecount==60):
                self.framecount=0
                total_frames+=1
                print total_frames,"--",pygame.time.get_ticks()
            
            
#Run the game loop
MainObject = Main()
MainObject.game_loop()
