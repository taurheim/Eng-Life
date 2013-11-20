'''
@author Joe Crozier & Nikolai Savas
'''
import os, pygame, gfx, projectile

class Mob(pygame.sprite.Sprite):
    ## Mob
    # 1. Needs to walk towards the player >> move()
    # 2. Needs to attack (melee or range) the player >> attack()
    # 3. Attempt (slowly) to dodge projectiles >> dodge()
    # 4. Needs to animate >> animate()
    # 5. Needs to die when hit >> die()
    # 6. Needs spawning code >> created in main
    def __init__(self, x, y, mobtype):
        pygame.sprite.Sprite.__init__(self)
        self.projectileTimer = 0
        self.currentAnimationFrame = 0
        self.currentAnimationType = 'static'
        self.direction = 'up'
        self.framecounter = 0
        self.dx = 0
        self.dy = 0

        self.moving = True #Don't know if we need this but I'll keep this in here in case we want mobs to stand still
        self.forced = 0

        
        self.image,self.rect = gfx.load_image("Enemy-1/Enemy-1-down.png",-1)
        self.rect = pygame.Rect(x,y,64,64)
        self.projectiles = pygame.sprite.Group()
        self.mobtype = mobtype
        
        self.hp=0
        if(mobtype=='art'):
            self.hp=15

    def move(self,player):
        distancex = player.rect.x - self.rect.x
        distancey = player.rect.y - self.rect.y

        if distancey == 0 and distancex == 0:
            self.dx = 0
            self.dy = 0
            return
        if distancey == 0 and distancex > 0:
            self.dx = 3
            self.dy = 0
            self.direction = 'right'
            return
        if distancey == 0 and distancex < 0:
            self.dx = -3
            self.dy = 0
            self.direction = 'left'
            return
            
        self.xratio = float(distancex/distancey)

        if distancex > 0 and distancey > 0:
            if self.xratio >= 2:
                self.dx = 2
                self.dy = 1
                self.direction = 'downright'
            if 2 > self.xratio > 0.5:
                self.dx = 2
                self.dy = 2
                self.direciton = 'downright'
            if 0.5 >= self.xratio > 0:
                self.dx = 1
                self.dy = 2
                self.direction = 'downright'
            if self.xratio == 0:
                dx = 0
                dy = 2
                self.direction = 'down'

        if distancex < 0 and distancey > 0:
            if abs(self.xratio) >= 2:
                self.dx = -2
                self.dy = 1
                self.direction = 'downleft'
            if 2 > abs(self.xratio) > 0.5:
                self.dx = -2
                self.dy = 2
                self.direction = 'downleft'
            if 0.5 >= abs(self.xratio) > 0:
                self.dx = -1
                self.dy = 2
                self.direction = 'downleft'
            if self.xratio == 0:
                self.dx = 0
                self.dy = 2
                self.direction = 'down'
                
        if distancex > 0 and distancey < 0:
            if abs(self.xratio) >= 2:
                self.dx = 2
                self.dy = -1
                self.direction = 'upright'
            if 2 > abs(self.xratio) > 0.5:
                self.dx = 2
                self.dy = -2
                self.direction = 'upright'
            if 0.5 >= abs(self.xratio) > 0:
                self.dx = 1
                self.dy = -2
                self.direction = 'upright'
            if self.xratio == 0:
                self.dx = 0
                self.dy = -2
                self.direction = 'up'
                
        if distancex < 0 and distancey < 0:
            if abs(self.xratio) >= 2:
                self.dx = -2
                self.dy = -1
                self.direction = 'upleft'
            if 2 > abs(self.xratio) > 0.5:
                self.dx = -2
                self.dy = -2
                self.direction = 'upleft'
            if 0.5 >= abs(self.xratio) > 0:
                self.dx = -1
                self.dy = -2
                self.direction = 'upleft'
            if self.xratio == 0:
                self.dx = 0
                self.dy = -2
                self.direction = 'up'
                
        
        
        
    
    def didMove(self, x, y): 
        self.rect.move_ip(x, y) #Moves the rect in place
    def setDir(self):
        
        
        if self.currentAnimationType==0 and self.mobtype == 'art':
            if self.direction == 'down':
                self.image,null = gfx.load_image('Enemy-1/down-attack/Animation-Down0001.png',-1)
            elif self.direction == 'left':
                self.image,null = gfx.load_image('Enemy-1/left-attack/Animation-Left0001.png',-1)
            elif self.direction == 'right':
                self.image,null = gfx.load_image('Enemy-1/left-attack/Animation-Left0001.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            elif self.direction == 'up':
                self.image,null = gfx.load_image('Enemy-1/up-attack/Animation-Up0001.png',-1)
            elif self.direction == 'downleft':
                self.image,null = gfx.load_image('Enemy-1/down-left-attack/Animation-down-left0001.png',-1)
            elif self.direction == 'downright':
                self.image,null = gfx.load_image('Enemy-1/down-left-attack/Animation-down-left0001.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            elif self.direction == 'upleft':
                self.image,null = gfx.load_image('Enemy-1/up-left-attack/Animation-up-left0001.png',-1)
            elif self.direction == 'upright':
                self.image,null = gfx.load_image('Enemy-1/up-left-attack/Animation-up-left0001.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            elif self.direction == 'static':
                pass
        if self.currentAnimationType==0 and self.mobtype == 'football':
            if self.direction == 'down':
                self.image,null = gfx.load_image('Enemy-2/down-attack/Animation0001.png',-1)
            elif self.direction == 'left':
                self.image,null = gfx.load_image('Enemy-2/left-attack/Animation0001.png',-1)
            elif self.direction == 'right':
                self.image,null = gfx.load_image('Enemy-2/left-attack/Animation0001.png',-1)
            elif self.direction == 'up':
                self.image,null = gfx.load_image('Enemy-2/up-attack/Animation0001.png',-1)
            elif self.direction == 'downleft':
                self.image,null = gfx.load_image('Enemy-2/down-left-attack/Animation0001.png',-1)
            elif self.direction == 'downright':
                self.image,null = gfx.load_image('Enemy-2/down-left-attack/Animation0001.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            elif self.direction == 'upleft':
                self.image,null = gfx.load_image('Enemy-2/up-left-attack/Animation0001.png',-1)
            elif self.direction == 'upright':
                self.image,null = gfx.load_image('Enemy-2/up-left-attack/Animation0001.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            elif self.direction == 'static':
                pass
    def attack(self, player):
        playerPos = [player.rect.x, player.rect.y]
        selfPos = [self.rect.x, self.rect.y]
        self.projectile = projectile.Projectile(playerPos, selfPos, 'art')
        self.projectiles = pygame.sprite.Group()
        self.projectiles.add(self.projectile)
    def update(self):
        self.framecounter+=1
        self.projectileTimer+=1
        self.projectiles.update()
        if self.projectileTimer == 60:
            projectileTimer = 0
        
        if self.currentAnimationType is not 0:
            self.currentAnimationFrame +=1
            gfx.animate(self,self.currentAnimationType)
        if(self.framecounter%14 == 0):
            self.currentAnimationFrame += 1
        if(self.currentAnimationFrame == 10):
            self.currentAnimationType=0
            self.currentAnimationFrame=0
            self.framecounter = 0
        self.setDir()
    def die(self):
        self.kill()

    def takedamage(self):
        self.hp-=2
        if(self.hp<=0):
            self.die()
            return True
        else: return False
        
