'''
@author Joe Crozier & Niko Savas
'''

#>>>> Possible optimization options:
#>>>>  1. Make sure all grouped if statements are if/elif
#>>>>  2. Order if/elif statements to be in order of most likely to least likely
#>>>>  3. Store images in variables and call them (avoid the use of gfx.load_image)
#>>>>  4. 

#Import PyGame & initialize it
import pygame,player,projectile,physics,gfx,ai,level,random,menu
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

        #Initialize Displays
        self.screen = pygame.display.set_mode((GAME_SETTINGS.WINDOW_WIDTH,GAME_SETTINGS.WINDOW_HEIGHT)) #Initialize Screen
        
        self.background = pygame.Surface(self.screen.get_size()) #Set Background
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        
        self.foreground = pygame.Surface(self.screen.get_size())
        self.foreground = self.foreground.convert()

        #Load title screen
        self.titlescreen = menu.TitleScreen((GAME_SETTINGS.WINDOW_WIDTH,GAME_SETTINGS.WINDOW_HEIGHT))

        #Initialize Physics.py
        self.Physics = physics.Physics(self.background)

        #Sprites
        self.guy = player.Player(300,300) #Create Player object
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


        #Level set up
        self.currentLevel = level.Level(1,self.background)
        for obstacle in self.currentLevel.obstacles:
            obstacle.height-=48
            self.Physics.addBody(obstacle)
        self.background.blit(self.currentLevel.bg,(0,0))
        self.foreground.blit(self.currentLevel.fg,(0, 0))

        #Health set up

        self.killCount = 0
        self.healthBar = pygame.sprite.Sprite()
        pygame.sprite.Sprite.__init__(self.healthBar)
        self.healthBar.image, null = gfx.load_image('health/10.png',-1)
        self.healthBar.rect = (50,550,100,20)
        self.all_sprites.add(pygame.sprite.RenderPlain(self.healthBar))
        self.healthChanged = False

        
    # Main loop:
    def game_loop(self):
        
        self.running = True #If running is true, the game will play
        self.framecount = 0 #how many frames have elapsed (resets every second)
        self.total_frames = 0 #Total frames since start
        
        while self.running:

            tick_timer.tick(GAME_SETTINGS.GAME_SPEED) #tick
            self.framecount+=1 #Count frames

            ### DRAW ORDER ###
            ## This code makes sure that the background is drawn first, then the foreground
            ## The foreground should have transparent pixels, these pixels should be set 
            ##  to a color (rgb), where that colour in the image file is assumed to be 
            ##  transparent. Which colour is transparent should be held in the (0,0) pixel
            ##  (for example, if the transparent color is red, the top-left-most pixel should be
            ##  set to rgb(255,0,0)
            self.screen.blit(self.background, (0, 0)) #Draw background
            self.all_sprites.draw(self.screen)        #Draw sprites
            self.mobs.draw(self.screen)
            self.screen.blit(self.foreground, (0, 0)) #Draw foreground
            colorkey =self.foreground.get_at((0,0))   #Set transparent color
            self.foreground.set_colorkey(colorkey)

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
            ### 1: down        _       _            ### If a number must be substituted
            ### 2: left       |   / \   |           ###  for a direction, use this.
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

                
            #Make player attack(), make a swish animation, make a swish collision box
            if self.pressed_leftmouse and not self.guy.attacking and self.guy.canAttack == True:
                self.guy.attack()
                self.swish = player.Swish(self.guy.rect.topleft[0]-32,self.guy.rect.topleft[1]-32)
                self.all_sprites.add(pygame.sprite.RenderPlain(self.swish))
                self.guy.canAttack = False
            #If a swish exists, make sure its direction matches the players direction
            
            if self.guy.attacking:
                self.swish.dir = self.guy.dir
                self.swish.rect.topleft = (self.guy.rect.topleft[0] -32,self.guy.rect.topleft[1] -32)

                ### SWISH HITBOX ###
                # enable this to see the swish hitbox
##              sbb = self.swish.createSwishBox()
##              self.obstacle = pygame.Surface((sbb.height,sbb.width))
##              self.obstacle = self.obstacle.convert()
##              self.obstacle.fill((0, 255, 0))
##              self.background.blit(self.obstacle, (sbb.x,sbb.y))

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
            for enemy in self.mobs:

                #If the player's attack hits the enemy, take damage
                if(self.guy.attacking and enemy.rect.colliderect(self.swish.createSwishBox())):
                    enemy.takedamage()
                    self.killCount += 1
                    
                #enemy.move sets the enemy's dx,dy, and direction
                enemy.move(self.guy)

                #Deal with collisions in the game
                if enemy.moving and self.Physics.bodyCanMoveToLocation(enemy, enemy.dx, enemy.dy):
                    #Mob is moving freely
                    enemy.didMove(enemy.dx,enemy.dy)
                    enemy.forced = 0
                    
                elif enemy.moving and self.Physics.bodyCanMoveToLocation(enemy, 0, enemy.dy):
                    if enemy.forced:
                        enemy.didMove(0,enemy.forced)
                    elif not enemy.forced: #If walking into a wall and also not moving
                        num = random.randrange(-2,3,4)
                        enemy.forced =  num #Pick a direction and move
                        
                elif enemy.moving and self.Physics.bodyCanMoveToLocation(enemy,enemy.dx,0):
                    if enemy.forced:
                        enemy.didMove(enemy.forced,0)
                    elif not enemy.forced: #If walking into a wall and also not moving
                        num = random.randrange(-2,3,4)
                        enemy.forced =  num #Pick a direction and move
                        
                elif enemy.moving and self.Physics.bodyCanMoveToLocation(enemy, 0, 2):
                    enemy.didMove(0,2)
                elif enemy.moving and self.Physics.bodyCanMoveToLocation(enemy, -2, 0):
                    enemy.didMove(2,0)
                else:
                    enemy.didMove(0,2)

            #Testing enemy projectile collisions
            for proj in self.projectiles:
                self.projRect = pygame.Rect(proj.rect.left, proj.rect.top, 33, 33)
                self.playerRect = pygame.Rect(self.guy.rect.left, self.guy.rect.top, 64, 64)
                if self.projRect.colliderect(self.playerRect):
                    proj.die()
                    self.guy.tookDamage(10)
                    print "Took 10 damage"
                    self.healthChanged = True
                    
                for solid in self.Physics.collisionRects:
                    if self.projRect.colliderect(solid):
                        proj.die()
                    
                
            #Tick level
            self.currentLevel.tick()

            #Health bar logic

            if self.healthChanged:
                healthStr = str(self.guy.health/10)
                print healthStr
                self.healthBar.image, null = gfx.load_image('health/'+healthStr+'.png',-1)
                self.healthChanged = False

            #Death conditions
                
                if healthStr == '0':
                    self.deathScreen = menu.deathScreen()
                    self.running = False
                    if MainObject.deathScreen.screen_loop(MainObject.screen):
                        restartGame()
                        return
                    else:
                        pygame.quit()
                        

                    
                    
            
            #If something needs to be done every second, put it here
            if (self.framecount == 30 or self.framecount == 60):
                self.guy.canAttack = True
            
            if(self.framecount==60):
                self.framecount=0
                self.total_frames += 1
                self.currentLevel.leveltimer +=1
                self.mobs.update()
            #Enemy projectile spawning
                for enemy in self.mobs:                     
                    playerPos = [self.guy.rect.x, self.guy.rect.y]
                    selfPos = [enemy.rect.x, enemy.rect.y]
                    proj = projectile.Projectile(playerPos, selfPos, 'art')
                    self.projectiles.add(proj)
                    self.all_sprites.add(proj)
            
                if(self.currentLevel.leveltimer==self.currentLevel.spawnRate):
                    #Spawn a Mob
                    self.currentLevel.leveltimer=0
                    spawnloc = self.currentLevel.spawnPoints[random.randrange(len(self.currentLevel.spawnPoints))]
                    self.newmob = ai.Mob(spawnloc[0],spawnloc[1], "art")
                    self.mobs.add(pygame.sprite.RenderPlain(self.newmob))
                    self.all_sprites.add(pygame.sprite.RenderPlain(self.newmob))
                    print "Mob Spawned"
    def changeLevel(self):
        pass

    def mobAttack(mobPos, proj_type):
        playerPos = [player.rect.x, player.rect.y]
        mobPos = [self.rect.x, self.rect.y]





def restartGame():
    MainObject = 0
    MainObject = Main()
    MainObject.game_loop()

#Load title screen
#Run the game loop   
MainObject = Main()
if(MainObject.titlescreen.screen_loop(MainObject.screen)):
    MainObject.game_loop()
else:
    pygame.quit()
