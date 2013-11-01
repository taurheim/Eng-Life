'''
@author Joe Crozier & Niko Savas
'''
#Import PyGame & initialize it
import pygame,player,projectile,physics,gfx,ai
tick_timer = pygame.time.Clock() #This timer will cap fps and tick once every ~16ms (60fps)

#GAME SETTINGS
class GAME_SETTINGS:
    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 800
    GAME_SPEED = 60 # FPS

class Main: ## __init__, game_loop

    
    # Initialize Game
    def __init__(self):
        pygame.init() #Initialize PyGame

        self.screen = pygame.display.set_mode((GAME_SETTINGS.WINDOW_WIDTH,GAME_SETTINGS.WINDOW_HEIGHT)) #Initialize Screen
        
        self.background = pygame.Surface(self.screen.get_size()) #Set Background
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        self.Physics = physics.Physics(self.background) #Initialize physics engine

        self.guy = player.Player(300,300) #Create Player object

        #Sprite Lists
        self.all_sprites = pygame.sprite.RenderPlain(self.guy) #Every Sprite goes here
        self.projectiles = pygame.sprite.Group() #Projectiles
        self.solids = pygame.sprite.Group() #Solids
        self.mobs = pygame.sprite.Group() #Mobs
        
        #inputs
        self.pressed_down = False
        self.pressed_up = False
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_leftmouse = False

        #### TEST CODE ####
        self.obstacle = pygame.Surface((200,200)) #Random green obstacle for testing
        self.obstacle = self.obstacle.convert()
        self.obstacle.fill((0, 255, 0))
        self.screen.blit(self.background, (0,0))
        self.background.blit(self.obstacle, (100,100))
        self.Physics.addBody(pygame.Rect(100,100,200,150))

        self.mob = ai.Mob(550,200, "art")
        self.all_sprites.add(pygame.sprite.RenderPlain(self.mob))
        self.mobs.add(pygame.sprite.RenderPlain(self.mob))
        ####/TEST CODE ####
        
    # Main loop:
    def game_loop(self):
        self.running = True #If running is true, the game will play
        self.framecount = 0 #how many frames have elapsed (resets every second)
        self.total_frames = 0 #Total frames since start
        
        while self.running:

            tick_timer.tick(60) #tick
            self.framecount+=1 #Count frames
            self.screen.blit(self.background, (0, 0)) #Draw background
            self.all_sprites.draw(self.screen)            #Draw sprites
            pygame.display.flip()                     #Make it happen

            #Check for inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False #Quit Game
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:  # check for key presses          
                    if event.key == pygame.K_LEFT:        # left arrow turns left
                        self.pressed_left = True
                    elif event.key == pygame.K_RIGHT:     # right arrow turns right
                        self.pressed_right = True
                    elif event.key == pygame.K_UP:        # up arrow goes up
                        self.pressed_up = True
                    elif event.key == pygame.K_DOWN:      # down arrow goes down
                        self.pressed_down = True
                        
                elif event.type == pygame.KEYUP:    # check for key releases
                    if event.key == pygame.K_LEFT:        # left arrow turns left
                        self.pressed_left = False
                    elif event.key == pygame.K_RIGHT:     # right arrow turns right
                        self.pressed_right = False
                    elif event.key == pygame.K_UP:        # up arrow goes up
                        self.pressed_up = False
                    elif event.key == pygame.K_DOWN:      # down arrow goes down
                        self.pressed_down = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1: #Click
                    self.pressed_leftmouse = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.pressed_leftmouse = False

            ###########################################
            ### DIRECTIONS                          ###
            ### 1: down        _       _            ###
            ### 2: left       |   / \   |           ###
            ### 3: right        7  4  8             ###
            ### 4: up        <  2     3  >          ###
            ### 5: downleft     5  1  6             ###
            ### 6: downright  |_  \ /  _|           ###
            ### 7: upleft                           ###
            ### 8: upright                          ###
            ###########################################

            #Change player's direction based on input
            self.guy.moving = True #Assume guy is going to be moving
            if self.pressed_down and not self.pressed_up:
                if self.pressed_left: self.guy.setDir('downleft')
                elif self.pressed_right: self.guy.setDir('downright')
                else: self.guy.setDir('down')
            elif self.pressed_up and not self.pressed_down:
                if self.pressed_left: self.guy.setDir('upleft')
                elif self.pressed_right: self.guy.setDir('upright')
                else: self.guy.setDir('up')
            elif self.pressed_left:
                self.guy.setDir('left')
            elif self.pressed_right:
                self.guy.setDir('right')
            else:
                self.guy.moving = False #Guy is not moving

                
            #Make player attack(), make a swish animation
            if self.pressed_leftmouse and not self.guy.attacking:
                self.guy.attack()
                self.swish = player.Swish(self.guy.rect.topleft[0]-32,self.guy.rect.topleft[1]-32)
                self.all_sprites.add(pygame.sprite.RenderPlain(self.swish))

            #If a swish exists, make sure it's direction matches the players direction
            try:
                self.swish.dir = self.guy.dir
                self.swish.rect.topleft = (self.guy.rect.topleft[0] -32,self.guy.rect.topleft[1] -32)
            except AttributeError as e:
                pass

            #Update movement of all sprites in the game
            self.all_sprites.update()

            #Check for physics collisions with player
            if self.guy.moving and self.Physics.bodyCanMoveToLocation(self.guy, self.guy.dx, self.guy.dy):
                self.guy.didMove(self.guy.dx,self.guy.dy)
                self.guy.dx,self.guy.dy = 0,0
            elif self.guy.moving and self.Physics.bodyCanMoveToLocation(self.guy, 0, self.guy.dy):
                self.guy.didMove(0,self.guy.dy)
                self.guy.dx,self.guy.dy = 0,0
            elif self.guy.moving and self.Physics.bodyCanMoveToLocation(self.guy,self.guy.dx,0):
                self.guy.didMove(self.guy.dx,0)
                self.guy.dx,self.guy.dy = 0,0


            #AI movement

            self.mob.move(self.guy)
            self.mob.didMove(self.mob.dx, self.mob.dy)



            
                
            #If something needs to be done every second, put it here
            if(self.framecount==60):
                self.framecount=0
                self.total_frames += 1
                self.mob

#Run the game loop
MainObject = Main()
MainObject.game_loop()
