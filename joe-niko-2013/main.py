'''
@author Joe Crozier & Niko Savas
'''
import pygame
import player

pygame.init()
#import shit

#GAME SETTINGS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
pressed_down = False
pressed_up = False
pressed_left = False
pressed_right = False


tick_timer = pygame.time.Clock() #This timer will cap fps and tick once every ~16ms (60fps)

# Init function:

class Main:
    def __init__(self):
        pygame.init() #Initialize PyGame
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        
        #self.background = pygame.Surface(self.screen.get_size())
        #self.background = self.background.convert()
        #self.background.fill((255, 250, 250))

        
        self.screen.blit(self.background, (0,0))
        self.guy = player.Player(300,300)
        self.sprites = pygame.sprite.RenderPlain(self.guy)
        self.pressed_down = False
        self.pressed_up = False
        self.pressed_left = False
        self.pressed_right = False

        
    # Main loop:
    ## Check if the game is still running, otherwise close game
    ## Tick clock
    ## Check for user inputs
    def game_loop(self):
        self.running = True #If running is true, the game will play
        self.framecount = 0 #how many frames have elapsed (resets every second)
        self.total_frames = 0 #Total frames since start
        
        while self.running:

            tick_timer.tick(60) #tick
            self.framecount+=1 #Count frames
            self.screen.blit(self.background, (0, 0)) #Draw background
            self.sprites.draw(self.screen)          #Draw sprites
            pygame.display.flip()                   #Make it happen

            #Check for inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False #Quit Game
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:          # check for key presses          
                    if event.key == pygame.K_LEFT:        # left arrow turns left
                        self.pressed_left = True
                        self.guy.changeSprite('left')
                    elif event.key == pygame.K_RIGHT:     # right arrow turns right
                        self.pressed_right = True
                        self.guy.changeSprite('right')
                    elif event.key == pygame.K_UP:        # up arrow goes up
                        self.pressed_up = True
                        self.guy.changeSprite('up')
                    elif event.key == pygame.K_DOWN:     # down arrow goes down
                        self.pressed_down = True
                        self.guy.changeSprite('down')
                elif event.type == pygame.KEYUP:            # check for key releases
                    if event.key == pygame.K_LEFT:        # left arrow turns left
                        self.pressed_left = False
                    elif event.key == pygame.K_RIGHT:     # right arrow turns right
                        self.pressed_right = False
                    elif event.key == pygame.K_UP:        # up arrow goes up
                        self.pressed_up = False
                    elif event.key == pygame.K_DOWN:     # down arrow goes down
                        self.pressed_down = False

                #Now, make the guy move based on the values of pressed_*
                        
            if self.pressed_down:
                self.guy.didMove(0,3)
            if self.pressed_up:
                self.guy.didMove(0,-3)
            if self.pressed_left:
                self.guy.didMove(-3,0)
            if self.pressed_right:
                self.guy.didMove(3,0)
            
 
            
            if(self.framecount==60):
                self.framecount=0
                self.total_frames += 1
                print self.total_frames,"--",pygame.time.get_ticks()

#Run the game loop
MainObject = Main()
MainObject.game_loop()
