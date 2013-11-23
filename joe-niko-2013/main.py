'''
@author Joe Crozier & Niko Savas
'''

#>>>> Possible optimization options:
#>>>>  1. Make sure all grouped if statements are if/elif
#>>>>  2. Order if/elif statements to be in order of most likely to least likely
#>>>>  3. Store images in variables and call them (avoid the use of gfx.load_image)
#>>>>  4. 

#Import PyGame & initialize it
import pygame,player,projectile,physics,ai,level,random,menu,gfx
tick_timer = pygame.time.Clock() #This timer will cap fps and tick once every ~16ms (60fps)

#GAME SETTINGS
class GAME_SETTINGS:
    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 800
    GAME_SPEED = 60 # FPS

class Main: ## __init__, game_loop

    
    # Initialize Game
    def __init__(self,levelNumber):
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
        self.health = pygame.sprite.Group() #Health packs
        self.fireballs = pygame.sprite.Group() # Player projectiles
        self.fire = pygame.sprite.Group() #Fire, used for boss #3
        self.flameseeds = pygame.sprite.Group() #Fire starter, used for boss #3

        #Font
        #self.kill_text = pygame.font.Font.render("0",1,(255,255,255))
        
        #inputs
        self.pressed_down = False
        self.pressed_up = False
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_leftmouse = False
        self.pressed_rightmouse = False

        self.fireballCount = 5
        self.fireballsChanged = False
        self.addFireball = False
        self.fireballTimer = 0


        #Level set up
        self.currentLevel = level.Level(levelNumber,self.background)
        for obstacle in self.currentLevel.obstacles:
            obstacle.height-=48
            self.Physics.addBody(obstacle)
        self.background.blit(self.currentLevel.bg,(0,0))
        if self.currentLevel.fg:                        #Only blit the foreground if there actually is one
            self.foreground.blit(self.currentLevel.fg,(0, 0))

        #Health set up

        self.bossHealthChanged = False
        self.killCount = 0
        self.spawnMobs = True
        self.healthBar = pygame.sprite.Sprite()
        pygame.sprite.Sprite.__init__(self.healthBar)
        self.healthBar.image, null = gfx.load_image('health/10.png',-1)
        self.healthBar.rect = (50,550,100,20)
        self.all_sprites.add(pygame.sprite.RenderPlain(self.healthBar))
        self.healthChanged = False

        if self.currentLevel.level > 2:
            self.fireball1 = pygame.sprite.Sprite()
            self.fireball2 = pygame.sprite.Sprite()
            self.fireball3 = pygame.sprite.Sprite()
            self.fireball4 = pygame.sprite.Sprite()
            self.fireball5 = pygame.sprite.Sprite()
            pygame.sprite.Sprite.__init__(self.fireball1)
            pygame.sprite.Sprite.__init__(self.fireball2)
            pygame.sprite.Sprite.__init__(self.fireball3)
            pygame.sprite.Sprite.__init__(self.fireball4)
            pygame.sprite.Sprite.__init__(self.fireball5)

            self.fireball1.image,null = gfx.load_image('engfireball.png',-1)
            self.fireball2.image,null = gfx.load_image('engfireball.png',-1)
            self.fireball3.image,null = gfx.load_image('engfireball.png',-1)
            self.fireball4.image,null = gfx.load_image('engfireball.png',-1)
            self.fireball5.image,null = gfx.load_image('engfireball.png',-1)
            self.fireball1.rect = (200,550,32,32)
            self.fireball2.rect = (250,550,32,32)
            self.fireball3.rect = (300,550,32,32)
            self.fireball4.rect = (350,550,32,32)
            self.fireball5.rect = (400,550,32,32)
            self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball1))
            self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball2))
            self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball3))
            self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball4))
            self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball5))


        #Health pack set up
        
        self.healthSpawnRate = 3   #Every x seconds, a pack is spawned (only if the previous pack has been picked up)
        self.spawnHealth = True
        self.secondsPassed = 0

        #gfx testing
        self.preloaded_gfx = gfx.preloadedgfx()
        gfx.preloaded_gfx = self.preloaded_gfx
        #Sounds

        self.Sounds = pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        self.musicChannel = pygame.mixer.Channel(0)
        self.soundsChannel1 = pygame.mixer.Channel(1)
        self.soundsChannel2 = pygame.mixer.Channel(2)
        self.musicSound = pygame.mixer.music.load('sounds/Kalimba.mp3')
        pygame.mixer.music.play()
        
    # Main loop:
    def game_loop(self):
        #for x in range(10000):
        #    pass
        self.running = True #If running is true, the game will play
        self.framecount = 0 #how many frames have elapsed (resets every second)
        self.total_frames = 0 #Total frames since start

        #gfx.preloadedgfx.loadbasic()
        #print gfx.preloadedgfx.swish_down

        
        
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
            #COULD CLEAN THIS UP^^
            self.screen.blit(self.foreground, (0, 0)) #Draw foreground
            self.projectiles.draw(self.screen)
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
                    elif event.key == pygame.K_s:
                        self.boss = level.Boss(1000,-250,self.currentLevel.level)
                        self.boss.add(pygame.sprite.RenderPlain(self.boss))
                        self.all_sprites.add(pygame.sprite.RenderPlain(self.boss))
                        self.boss.walkTo(700,250)
                        self.bossHealthBar = pygame.sprite.Sprite()
                        pygame.sprite.Sprite.__init__(self.healthBar)
                        self.bossHealthBar.image, null = gfx.load_image('health/10.png',-1)
                        self.bossHealthBar.rect = (550,550,100,20)
                        self.all_sprites.add(pygame.sprite.RenderPlain(self.bossHealthBar))
                        self.bossHealthChanged = False
                    elif event.key == pygame.K_SPACE:
                        self.pressed_leftmouse = True
                        
                elif event.type == pygame.KEYUP:    # check for key releases
                    if event.key == pygame.K_LEFT:        # left arrow turns left
                        self.pressed_left = False
                    elif event.key == pygame.K_RIGHT:     # right arrow turns right
                        self.pressed_right = False
                    elif event.key == pygame.K_UP:        # up arrow goes up
                        self.pressed_up = False
                    elif event.key == pygame.K_DOWN:      # down arrow goes down
                        self.pressed_down = False
                    elif event.key == pygame.K_SPACE:
                        self.pressed_leftmouse = False
                
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button==1): #Click
                    self.pressed_leftmouse = True
                elif(event.type == pygame.MOUSEBUTTONDOWN and event.button==3) and self.currentLevel.level > 2 and self.fireballCount > 0:
                     self.pressed_rightmouse = True
                     new_projectile = projectile.Projectile(self.guy.rect.center,pygame.mouse.get_pos(),'fireball',1)
                     self.all_sprites.add(pygame.sprite.RenderPlain(new_projectile))
                     self.fireballs.add(pygame.sprite.RenderPlain(new_projectile))
                     self.fireballCount += -1
                     self.fireballsChanged = True
                elif event.type == pygame.MOUSEBUTTONUP and event.button==1:
                     self.pressed_leftmouse = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button==3:
                     self.pressed_rightmouse = False


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


            #Draw fireballs
            if self.fireballsChanged:
                if self.fireballCount == 4:
                    self.fireball5.kill()
                if self.fireballCount == 3:
                    self.fireball4.kill()
                if self.fireballCount == 2:
                    self.fireball3.kill()
                if self.fireballCount == 1:
                    self.fireball2.kill()
                if self.fireballCount == 0:
                    self.fireball1.kill()
                self.fireballsChanged = False
            if self.addFireball:
                if self.fireballCount == 4:
                    self.fireball5 = pygame.sprite.Sprite()
                    pygame.sprite.Sprite.__init__(self.fireball5)
                    self.fireball5.image,null = gfx.load_image('engfireball.png',-1)
                    self.fireball5.rect = (400,550,32,32)
                    self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball5))
                    self.fireballCount += 1
                if self.fireballCount == 3:
                    self.fireball4 = pygame.sprite.Sprite()
                    pygame.sprite.Sprite.__init__(self.fireball4)
                    self.fireball4.image,null = gfx.load_image('engfireball.png',-1)
                    self.fireball4.rect = (350,550,32,32)
                    self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball4))
                    self.fireballCount += 1
                if self.fireballCount == 2:
                    self.fireball3 = pygame.sprite.Sprite()
                    pygame.sprite.Sprite.__init__(self.fireball3)
                    self.fireball3.image,null = gfx.load_image('engfireball.png',-1)
                    self.fireball3.rect = (300,550,32,32)
                    self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball3))
                    self.fireballCount += 1
                if self.fireballCount == 1:
                    self.fireball2 = pygame.sprite.Sprite()
                    pygame.sprite.Sprite.__init__(self.fireball2)
                    self.fireball2.image,null = gfx.load_image('engfireball.png',-1)
                    self.fireball2.rect = (250,550,32,32)
                    self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball2))
                    self.fireballCount += 1
                if self.fireballCount == 0:
                    self.fireball1 = pygame.sprite.Sprite()
                    pygame.sprite.Sprite.__init__(self.fireball5)
                    self.fireball1.image,null = gfx.load_image('engfireball.png',-1)
                    self.fireball1.rect = (200,550,32,32)
                    self.all_sprites.add(pygame.sprite.RenderPlain(self.fireball1))
                    self.fireballCount += 1
                self.addFireball = False
                    
                
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
                    if(enemy.takedamage(5)):
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
            #Boss stuff
            if(self.currentLevel.level==1 and not self.spawnMobs):
                if(self.boss.attack_1): #Throwing ball
                    colors = ['red','orange','yellow','green','blue','purple','black','white']
                    playerPos = [self.guy.rect.x, self.guy.rect.y]
                    selfPos = [self.boss.rect.x+125, self.boss.rect.y+125]
                    paintball = projectile.Projectile(playerPos,selfPos,'paint',colors[random.randrange(0,8,1)])
                    self.all_sprites.add(paintball)
                    self.projectiles.add(paintball)
                    self.boss.attack_1= False
                elif(self.boss.attack_2): #Boomerang
                    playerPos = [self.guy.rect.x, self.guy.rect.y]
                    selfPos = [self.boss.rect.x+125, self.boss.rect.y+125]
                    boomer = projectile.Projectile(playerPos,selfPos,'boomer',0)
                    self.all_sprites.add(boomer)
                    self.projectiles.add(boomer)
                    self.boss.attack_2= False
                elif(self.boss.attack_3): #Shoot tiny
                    key = ['red','orange','yellow','green','blue','purple','black','white']
                    loc_key = {'red':[56,128],'orange':[30,132],'yellow':[17,142],'green':[8,155],'blue':[5,170],'purple':[1,189],'black':[12,200],'white':[28,205]}
                    fire = []
                    for i in range(8):
                        if(self.boss.curr_tiny[i]):
                            fire.append(key[i])
                    playerPos = [self.guy.rect.x, self.guy.rect.y]
                    for color in fire:
                        selfPos = [self.boss.rect.x+loc_key[color][0], self.boss.rect.y+loc_key[color][1]]
                        tiny = projectile.Projectile(playerPos,selfPos,'tiny',color)
                        self.all_sprites.add(tiny)
                        self.projectiles.add(tiny)
                        self.boss.attack_3= False
                elif(self.boss.attack_4): #Drop paint
                    colors = ['red','orange','yellow','green','blue','purple','black','white']
                    randcolor = colors[random.randrange(0,8,1)]
                    randtype = random.randrange(0,2,1)
                    randx = random.randrange(10,790,1)
                    randy = random.randrange(10,590,1)
                    paintdrop = projectile.Projectile([randx,randy],[randx,0],'drop_paint',[randtype,randcolor])
                    self.all_sprites.add(paintdrop)
                    self.projectiles.add(paintdrop)
                    self.boss.attack_4 = False

                    #shadow
                    shadow = projectile.Projectile([randx,randy],[randx,randy],'shadow',[randtype,(randy+32)/1.5])
                    self.all_sprites.add(shadow)
                        
                if(self.guy.attacking and self.boss.rect.colliderect(self.swish.createSwishBox())):
                    self.boss.takeDamage(50)
                    self.bossHealthChanged = True
                    
            elif(self.currentLevel.level==2 and not self.spawnMobs):
                if(self.boss.attack_1):
                    #Throwing football
                    playerPos = [self.guy.rect.x,self.guy.rect.y]
                    selfPos = [self.boss.rect.x+50,self.boss.rect.y+50]
                    football = projectile.Projectile(playerPos,selfPos,'boss_football',0)
                    self.all_sprites.add(football)
                    self.projectiles.add(football)
                    self.boss.attack_1 = False
                elif(self.boss.attack_2):
                    #Summoning players
                    for i in range(random.randrange(10)):
                        spawnloc = self.currentLevel.spawnPoints[random.randrange(len(self.currentLevel.spawnPoints))]
                        self.newmob = ai.Mob(spawnloc[0],spawnloc[1], self.currentLevel.mobType)
                        self.mobs.add(pygame.sprite.RenderPlain(self.newmob))
                        self.all_sprites.add(pygame.sprite.RenderPlain(self.newmob))
                    self.boss.attack_2 = False
                elif(self.boss.attack_3):
                    yelltype = random.randrange(2)
                    #Yelling
                    bossPos = [self.boss.rect.x-128,self.boss.rect.y-64]
                    yell = projectile.Projectile(bossPos,bossPos,'yell',yelltype)
                    self.all_sprites.add(yell)
                    self.projectiles.add(yell)
                    self.boss.attack_3 = False
                    self.boss.attack_4 = yelltype
                    self.boss.attack_5 = True

                if self.boss.attack_5: #attack_4 :: 0 = stop moving, 1 = keep moving
                    if (not(self.boss.attack_4) and (self.guy.moving or self.guy.attacking)) or (self.boss.attack_4 and not(self.guy.moving)):
                        self.guy.tookDamage(1)
                        self.healthChanged = True
                    else:
                        pass
                
                if(self.guy.attacking and self.boss.rect.colliderect(self.swish.createSwishBox())):
                    self.boss.takeDamage(50)
                    self.bossHealthChanged = True
                    
            elif(self.currentLevel.level==3 and not self.spawnMobs):
                if(self.boss.attack_1):
                    #Remove all seeds
                    for seed in self.flameseeds:
                        seed.kill()
                    attack_type = self.boss.attack_3
                    ## LEGEND
                    # 0 : flames go right in 3 lines
                    # 1 : flames go left in 3 lines
                    # 2 : flames go from the bottom right and bottom left to opposite corners
                    # 3 : flames go from the top right and top left to opposite corners
                    # 4 : flames go in a huge line down the center left to right
                    # 5 : flames go in a huge line down the center right to left
                    # 6 : flames go up in 3 lines
                    # 7 : flames go down in 3 lines
                    # 8 : flames go in two huge lines right
                    # 9 : flames go in two huge lines left
                    if 0==attack_type: #l>r
                        numflames = 6
                        flamePos = [[0,100],[0,132],[0,300],[0,332],[0,450],[0,482]]
                        flameDir = [[1,0],[1,0],[1,0],[1,0],[1,0],[1,0]]
                    elif 1==attack_type: #r>l
                        numflames = 6
                        flamePos = [[800,100],[800,132],[800,300],[800,332],[800,450],[800,482]]
                        flameDir = [[-1,0],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0]]
                    elif 2==attack_type: #diag
                        numflames = 4
                        flamePos = [[0,580],[20,600],[800,580],[780,600]]
                        flameDir = [[1,-1],[1,-1],[-1,-1],[-1,-1]]
                    elif 3==attack_type: #diag
                        numflames = 4
                        flamePos = [[0,20],[20,0],[800,20],[780,0]]
                        flameDir = [[1,1],[1,1],[-1,1],[-1,1]]
                    elif 4==attack_type:
                        numflames = 6
                        flamePos = [[0,200],[0,240],[0,280],[0,320],[0,360],[0,400]]
                        flameDir = [[1,0],[1,0],[1,0],[1,0],[1,0],[1,0]]
                    elif 5==attack_type:
                        numflames = 6
                        flamePos = [[800,200],[800,240],[800,280],[800,320],[800,360],[800,400]]
                        flameDir = [[-1,0],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0]]
                    elif 6==attack_type:
                        numflames = 6
                        flamePos = [[100,0],[132,0],[400,0],[432,0],[650,0],[682,0]]
                        flameDir = [[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]]
                    elif 7==attack_type:
                        numflames = 6
                        flamePos = [[100,600],[132,600],[400,600],[432,600],[650,600],[682,600]]
                        flameDir = [[0,-1],[0,-1],[0,-1],[0,-1],[0,-1],[0,-1]]
                    elif 8==attack_type:
                        numflames = 6
                        flamePos = [[0,100],[0,132],[0,164],[0,500],[0,468],[0,436]]
                        flameDir = [[1,0],[1,0],[1,0],[1,0],[1,0],[1,0]]
                    elif 9==attack_type:
                        numflames = 6
                        flamePos = [[800,100],[800,132],[800,164],[800,500],[800,468],[800,436]]
                        flameDir = [[-1,0],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0]]
                        
                    for i in range(numflames):
                        flame = projectile.Projectile(flamePos[i],flamePos[i],'fire',flameDir[i])
                        self.all_sprites.add(flame)
                        self.fire.add(flame)
                    self.boss.attack_1 = False
                elif self.boss.attacking and not self.boss.attack_4:
                    self.boss.attack_3 = random.randrange(0,10)
                    attack_type = self.boss.attack_3
                    
                    if 0==attack_type:
                        numseeds = 3
                        flamePos = [[0,100],[0,300],[0,450]]
                    elif 1==attack_type:
                        numseeds = 3
                        flamePos = [[800,100],[720,300],[720,450]]
                    elif 2==attack_type:
                        numseeds = 2
                        flamePos = [[0,520],[720,520]]
                    elif 3==attack_type:
                        numseeds = 2
                        flamePos = [[0,20],[720,20]]
                    elif 4==attack_type:
                        numseeds = 4
                        flamePos = [[0,200],[0,250],[0,300],[0,350]]
                    elif 5==attack_type:
                        numseeds = 4
                        flamePos = [[720,200],[720,250],[720,300],[720,350]]
                    elif 6==attack_type:
                        numseeds = 3
                        flamePos = [[100,0],[400,0],[650,0]]
                    elif 7==attack_type:
                        numseeds = 3
                        flamePos = [[100,520],[400,520],[650,520]]
                    elif 8==attack_type:
                        numseeds = 2
                        flamePos = [[0,100],[0,500]]
                    elif 9==attack_type:
                        numseeds = 2
                        flamePos = [[720,100],[720,500]]
                        
                    for i in range(numseeds):
                        flameseed = projectile.Projectile(flamePos[i],flamePos[i],'fireseed',0)
                        self.all_sprites.add(flameseed)
                        self.flameseeds.add(flameseed)
                    self.boss.attack_4 = True
                if(self.guy.attacking and self.boss.rect.colliderect(self.swish.createSwishBox())):
                    self.boss.takeDamage(50)
                    self.bossHealthChanged = True


            
            if self.bossHealthChanged:
                healthStr = str(self.boss.hp/35)
                self.bossHealthBar.image, null = gfx.load_image('health/'+healthStr+'.png',-1)
                self.bossHealthChanged = False
                if self.boss.hp <= 0:
                    self.boss.kill()
                    self.menuScreen = menu.deathScreen(False,self.currentLevel.level)
                    self.running = False
                    if self.menuScreen.screen_loop(MainObject.screen):
                        restartGame(self.currentLevel.level+1)
                        return
                    else:
                        pygame.quit()                                        #This recreates the entire main object and loads the next level.
            #Boss 3 Flames
            for flame in self.fire:
                #Fire "extra" value
                ## extra[0] : change in x value each time
                ## extra[1] : change in y value each time
                newpos = [flame.rect.x+(flame.extra[0]*16),flame.rect.y+(flame.extra[1]*16)]
                if(newpos[0]<800 and newpos[0]>0 and newpos[1]<600 and newpos[1]>0):
                    newflame = projectile.Projectile(newpos,newpos,'fire',flame.extra)
                    self.fire.remove(flame)
                    self.projectiles.add(flame)
                    self.all_sprites.add(newflame)
                    self.fire.add(newflame)

            
            #Testing player projectile collisions
            for fireball in self.fireballs:
                for mob in self.mobs:
                    if fireball.rect.colliderect(mob.rect):
                        if(mob.takedamage(5)):
                            self.killCount+=1
                if((not self.spawnMobs) and self.boss.rect.colliderect(fireball.rect)):
                        self.boss.takeDamage(50)
                        fireball.kill()
                        self.bossHealthChanged = True

            #Testing enemy projectile collisions
            if not self.spawnMobs:
                self.boss.attack_5 = False
            for proj in self.projectiles:
                if(proj.proj_type=='yell'):
                    self.boss.attack_5 = True
                self.projRect = pygame.Rect(proj.rect.left, proj.rect.top, proj.rect.width,proj.rect.height)
                if(proj.proj_type=='boomer'):
                    self.projRect = pygame.Rect(proj.rect.left+50,proj.rect.top+40,175,175)
                self.playerRect = pygame.Rect(self.guy.rect.left, self.guy.rect.top, 64, 64)
                
##                self.obstacle = pygame.Surface((self.projRect.width,self.projRect.height))
##                self.obstacle = self.obstacle.convert()
##                self.obstacle.fill((0, 255, 0))
##                self.foreground.blit(self.obstacle, (self.projRect.x,self.projRect.y))
                
                if self.projRect.colliderect(self.playerRect):
                    if proj.proj_type == 'art':
                        proj.die()
                        self.guy.tookDamage(10)
                        self.healthChanged = True
                    elif proj.proj_type == 'paint':
                        self.guy.tookDamage(1)
                        self.healthChanged = True
                        pass
                    elif proj.proj_type == 'boomer':
                        self.guy.tookDamage(2)
                        self.healthChanged = True
                    elif proj.proj_type == 'tiny':
                        self.guy.tookDamage(3)
                        self.healthChanged = True
                        proj.die()
                    elif proj.proj_type == 'drop_paint' and proj.dy==0 and self.playerRect.colliderect(pygame.Rect(self.projRect.x,self.projRect.y+40,self.projRect.width,10)):
                        self.guy.tookDamage(1)
                        self.healthChanged = True
                    elif proj.proj_type == 'commerce':
                        self.guy.tookDamage(10)
                        self.healthChanged = True
                        proj.die()
                    elif proj.proj_type == 'fire':
                        self.guy.tookDamage(2)
                        self.healthChanged = True
                    elif proj.proj_type == 'football':
                        self.guy.tookDamage(10)
                        self.healthChanged = True
                        proj.die()
                    elif proj.proj_type == 'boss_football':
                        self.guy.tookDamage(5)
                        self.healthChanged = True
                if proj.proj_type == "boomer" and proj.extra == "back" and proj.rect.colliderect(pygame.Rect(self.boss.rect.x+200,self.boss.rect.y+130,50,50)):
                    proj.die()
                for solid in self.Physics.collisionRects:
                    
##                    self.obstacle = pygame.Surface((solid.width,solid.height))
##                    self.obstacle = self.obstacle.convert()
##                    self.obstacle.fill((0, 255, 0))
##                    self.foreground.blit(self.obstacle, (solid.x,solid.y))
                    
                    if proj.proj_type is not 'paint' and proj.proj_type is not 'boomer' and proj.proj_type is not 'drop_paint' and self.projRect.colliderect(solid) :
                        proj.die()

                        
            #Testing healthpack collisions
            for pack in self.health:
                
                if pack.rect.colliderect(self.guy.rect):
                    pack.kill()
                    self.guy.tookDamage(-50)
                    self.healthChanged = True
                    self.spawnHealth = True
                
            #Tick level
            self.currentLevel.tick()

            #Health bar logic

            if self.healthChanged:
                if self.guy.health > 100:
                    self.guy.health = 100
                elif self.guy.health < 0:
                    self.guy.health = 0
                healthStr = str(self.guy.health/10)
                self.healthBar.image, null = gfx.load_image('health/'+healthStr+'.png',-1)
                self.healthChanged = False

            #Death conditions
                
                if healthStr == '0':
                    self.deathScreen = menu.deathScreen(True,self.currentLevel.level)
                    self.running = False
                    if self.deathScreen.screen_loop(MainObject.screen):
                        restartGame(self.currentLevel.level)
                        return
                    else:
                        pygame.quit()
                        

            self.fireballTimer += 1
            
            #If something needs to be done every second, put it here
            if (self.framecount == 30 or self.framecount == 60):
                self.guy.canAttack = True
                print self.fireballCount

            if self.fireballTimer == 300 and not self.fireballCount == 5:
                self.addFireball = True
                self.fireballTimer = 0

            
                
                
            
            if(self.framecount==60):
                self.secondsPassed += 1
                if self.secondsPassed%self.healthSpawnRate==0 and self.spawnHealth:
                    X = random.randint(50,750)
                    Y = random.randint(50,550)
                    pack = player.Healthpack(X,Y)
                    self.all_sprites.add(pygame.sprite.RenderPlain(pack))
                    self.health.add(pygame.sprite.RenderPlain(pack))
                    self.spawnHealth = False
                    

                

                
                if(self.killCount>=2 and self.spawnMobs):
                    self.spawnMobs=False
                    self.boss = level.Boss(1000,-250,self.currentLevel.level)
                    self.boss.add(pygame.sprite.RenderPlain(self.boss))
                    self.all_sprites.add(pygame.sprite.RenderPlain(self.boss))
                    self.boss.walkTo(700,250)
                    self.bossHealthBar = pygame.sprite.Sprite()
                    pygame.sprite.Sprite.__init__(self.healthBar)
                    self.bossHealthBar.image, null = gfx.load_image('health/10.png',-1)
                    self.bossHealthBar.rect = (550,550,100,20)
                    self.all_sprites.add(pygame.sprite.RenderPlain(self.bossHealthBar))
                    self.bossHealthChanged = False
                self.framecount=0
                self.total_frames += 1
                self.currentLevel.leveltimer +=1
                self.mobs.update()
                try:
                    self.boss.livingfor+=1
                except AttributeError as e:
                    pass
            #Enemy projectile spawning/attacking
                for enemy in self.mobs:
                        playerPos = [self.guy.rect.x, self.guy.rect.y]
                        selfPos = [enemy.rect.x, enemy.rect.y]
                        proj = projectile.Projectile(playerPos, selfPos, self.currentLevel.mobType,enemy.direction)
                        enemy.currentAnimationType = 1
                        enemy.currentAnimationFrame = 0
                        self.projectiles.add(proj)
                        self.all_sprites.add(proj)

                    

                if self.spawnMobs and (self.currentLevel.leveltimer==self.currentLevel.spawnRate):
                    #Spawn a Mob
                    self.currentLevel.leveltimer=0
                    spawnloc = self.currentLevel.spawnPoints[random.randrange(len(self.currentLevel.spawnPoints))]
                    self.newmob = ai.Mob(spawnloc[0],spawnloc[1], self.currentLevel.mobType)
                    self.mobs.add(pygame.sprite.RenderPlain(self.newmob))
                    self.all_sprites.add(pygame.sprite.RenderPlain(self.newmob))

                    
    def changeLevel(self):
        pass

    def mobAttack(mobPos, proj_type):
        playerPos = [player.rect.x, player.rect.y]
        mobPos = [self.rect.x, self.rect.y]





def restartGame(levelNumber):
    MainObject = 0
    MainObject = Main(levelNumber)
    MainObject.game_loop()

#Load title screen
#Run the game loop

MainObject = Main(1)
#import cProfile as profile
#profile.run('MainObject.game_loop()')
if(MainObject.titlescreen.screen_loop(MainObject.screen)):
    MainObject.game_loop()
else:
    pygame.quit()
