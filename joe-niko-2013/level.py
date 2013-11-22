import os, pygame, gfx, random, math

class Level(object):
    def __init__(self,level,bg):

        self.leveltimer = 0
        
        self.level = level #int, which level we are currently on.
        self.obstacles = []
        self.fg = False
        #### MOBS ####
        # 1. Art Student
        # 2. Commerce Student
        # 3. Health Sci Student
        # 4. Football Player
        # 5. All of the above

        #### BOSS ####
        # 1. Angry Art Student
        # 2. Dr. Fleisig
        # 3. Dr. McLean
        # 4. Football Coach
        # 5. Dr. Smith

        self.spawnRate = 0
        self.spawnPoints = []

        
        if 1==level:
            self.bg,null = gfx.load_image("level-1-bg.png",-1)
            self.fg,null = gfx.load_image("level-1-fg.png",-1)
            
            self.obstacles.append(pygame.Rect(312,440,80,55))
            self.obstacles.append(pygame.Rect(106,197,65,62))
            self.obstacles.append(pygame.Rect(372,197,65,62))
            self.obstacles.append(pygame.Rect(634,197,65,62))

            self.mobType='art'
            self.spawnRate = 2
            self.spawnPoints = [(800,600),(0,600),(300,600)]
            
        if 2==level:
            self.bg,null = gfx.load_image("Level-2.png",-1)
            self.mobType = 'football'
            self.spawnRate = 5
            self.spawnPoints = [(0,0),(800,0),(300,600)]
        if 3==level:
            pass
        if 4==level:
            pass
        if 5==level:
            pass
    def tick(self):
        pass
        
class Boss(pygame.sprite.Sprite):
    def __init__(self,X,Y,level):
        self.livingfor = 0
        self.currentAnimationType=0
        self.currentAnimationFrame=0
        self.tickcount = 0
        self.lastattack = 0
        self.nextattack=5
        self.moving = False
        self.dx = 0
        self.dy = 0
        self.attacking = False
        self.takingdmg = False
        self.attack_1 = False #This is so main.py can throw the ball instead of level.py
        self.attack_2 = False
        self.attack_3 = False
        self.attack_4 = False
        if(level==1):
            self.level = level
            #### ANGRY ART STUDENT ####
            # Phase 1 (350-250)
            ## - Throw paint balls of various colours at the player (explode once they hit the ground)
            ## - 3-8 seconds between each ball
            # Phase 2 (250-150)
            ## - Throw palette (boomerang style)
            # Phase 3 (150-50)
            ## - Shoot tiny paint balls (slow, lots of them)
            # Phase 4 (50-0)
            ## - Paint balls fall from the sky
            self.hp = 350
            self.damage = 15
            self.currentphase = 0
            pygame.sprite.Sprite.__init__(self)
            self.image,self.rect = gfx.load_image("boss-art/boss.png",-1)
            self.rect = pygame.Rect(X,Y,250,250)
        if(level==2):
            self.level = level
            #### FOOTBALL COACH ####
            # Phase 1
            ## Yells
            # Phase 2
            ## Summon players
            # Phase 3
            ## Dump gatorade
            # Phase 4
            ## Throw football
            self.hp = 350
            self.damage = 15
            self.currentphase = 0
            pygame.sprite.Sprite.__init__(self)
            self.image,self.rect = gfx.load_image("coach-art/boss.png",-1)
            self.rect = pygame.Rect(X,Y,150,150)
    def update(self):
        self.tickcount+=1
        if(self.moving):
            self.placeholder[0] += self.dx
            self.placeholder[1] += self.dy
            self.rect.move_ip(int(self.placeholder[0]),int(self.placeholder[1]))

            if(int(self.placeholder[0])!=0):
                if(self.placeholder[0]>0):
                    self.placeholder[0] -= int(self.placeholder[0])
                else:
                    self.placeholder[0] -= int(self.placeholder[0])
                    
            if(int(self.placeholder[1])!=0):
                if(self.placeholder[1]>0):
                    self.placeholder[1] -= int(self.placeholder[1])
                else:
                    self.placeholder[1] -= int(self.placeholder[1])
            if self.rect.left == self.destination[0] and self.rect.top == self.destination[1]:
                self.moving = False
        if(self.level == 1):
            if(self.livingfor ==10 and not self.moving):
                self.walkTo(500,250)
            if(self.hp >=250):
                self.currentphase = 1
                # Phase 1
                if (self.livingfor - self.lastattack)>=self.nextattack:
                    self.nextattack = random.randrange(3,8,1)
                    self.lastattack = self.livingfor
                    self.attacking=True
            elif(self.hp >=150):
                self.currentphase = 2
                # Phase 2
                if (self.livingfor - self.lastattack)>=self.nextattack:
                    self.nextattack = random.randrange(3,8,1)
                    self.lastattack = self.livingfor
                    self.attacking = True
                pass
            elif(self.hp >=50):
                if(self.currentphase ==2):
                    ## red,orange,yellow,green,blue,purple,black,white
                    self.next_tiny = [0,0,0,0,0,0,0,0]
                    self.last_tiny = [0,0,0,0,0,0,0,0]
                    self.curr_tiny = [0,0,0,0,0,0,0,0]
                self.currentphase = 3
                self.curr_tiny = [0,0,0,0,0,0,0,0]
                for i in range(8):
                    if(self.livingfor-self.last_tiny[i])>=self.next_tiny[i]:
                        self.next_tiny[i] = random.randrange(3,8,1)
                        self.last_tiny[i] = self.livingfor
                        self.curr_tiny[i] = 1
                        self.attacking = True
                # Phase 3
                pass
            elif(self.hp > 0):
                if(self.currentphase == 3):
                    self.attacking=True
                    pass
                self.currentphase = 4
                if(self.tickcount-self.lastattack)>20:
                    self.attack_4 = True
                    self.lastattack = self.tickcount
                # Phase 4
            else:
                if not self.currentphase==5:
                    self.attacking=True
                self.currentphase = 5
        elif(self.level == 2):
            if(self.livingfor==10 and not self.moving):
                self.walkTo(500,250)
            if(self.hp >= 250):
                self.currentphase = 1
            elif(self.hp >=150):
                self.currentphase = 2
            elif(self.hp >=50):
                self.currentphase = 3
            elif(self.hp > 0):
                self.currentphase = 4
            else:
                if(self.currentphase ==4):
                    pass
        if(self.attacking):
            if(self.level ==1):
                if 1==self.currentphase:
                    self.currentAnimationFrame+=1
                    gfx.animate(self,1)
                    if self.currentAnimationFrame==5:
                        self.attacking=False
                        self.attack_1=True
                        self.currentAnimationFrame=0
                elif 2==self.currentphase:
                    self.currentAnimationFrame+=1
                    gfx.animate(self,2)
                    if self.currentAnimationFrame==10:
                        self.attacking=False
                        self.attack_2=True
                        self.currentAnimationFrame=0
                elif 3==self.currentphase:
                    self.attacking=False
                    self.attack_3=True
                    self.currentAnimationFrame=0
                elif 4==self.currentphase:
                    self.currentAnimationFrame+=1
                    gfx.animate(self,4)
                    if self.currentAnimationFrame==10:
                        self.attacking=False
                        self.currentAnimationFrame=0
                elif 5==self.currentphase:
                    self.currentAnimationFrame+=1
                    gfx.animate(self,5)
                    print self.currentAnimationFrame
                    if self.currentAnimationFrame==9:
                        self.die()
                        self.attacking = False
            elif(self.level==2):
                pass
        
        if(self.takingdmg):
            if self.level==1 and self.currentphase is not 5:
                self.counter+=1
                if self.counter%5==0:
                    if 4==self.currentphase:
                        self.image,null = gfx.load_image("boss-art/rage/rage00010.png",-1)
                    else:
                        self.image,null = gfx.load_image("boss-art/throw0005.png",-1)
                elif self.counter%5==1:
                    if 4==self.currentphase:
                        self.image,null = gfx.load_image("boss-art/rage/takingdmg.png",-1)
                    else:
                        self.image,null = gfx.load_image("boss-art/takingdmg.png",-1)
                if(self.counter==60):
                    self.takingdmg= False
            if self.level==2 and self.currentphase is not 5:
                self.counter+=1
    def walkTo(self,x,y):
        self.moving = True
        
        #Calculate angle (dx,dy)
        change_xpos= x - self.rect.left
        change_ypos= y - self.rect.top

        l = math.sqrt(change_xpos**2 + change_ypos**2)
        tempx = ((10*change_xpos)/l)
        tempy = ((10*change_ypos)/l)

        #dx,dy
        self.dx = tempx/10.0
        self.dy = tempy/10.0


        #velocity
        v = 1
        self.dx*=v
        self.dy*=v
        
        self.placeholder = [0,0]
        self.destination = [x,y]
    def move(self,pos):
        pass
    def takeDamage(self,dmg):
        if not self.takingdmg:
            self.takingdmg=True
            self.counter =0
            self.hp -= dmg
    def die(self):
        print "Level 1 Boss Dead"
