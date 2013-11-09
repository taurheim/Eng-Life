'''
@author Joe Crozier & Niko Savas
'''
import os, pygame, gfx

class Swish(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        self.currentAnimationFrame = 1
        self.currentAnimationType = 'static'
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = gfx.load_image('swish-down/frame1.png',-1)

        self.dir = 'down'
        
        self.rect = pygame.Rect(X,Y,128,128)
        fullname = os.path.join('sprites', 'swish-down/frame1.png')
        self.image = pygame.image.load(fullname)
        self.image.convert()

    def update(self):

        #Positioning required to make the swish look realistic
        if(self.dir == 'downleft'):
            self.rect.topleft = (self.rect.topleft[0]-16,self.rect.topleft[1]-16)
        elif(self.dir == 'downright'):
            self.rect.topleft = (self.rect.topleft[0]-24,self.rect.topleft[1]-24)
        elif(self.dir == 'upleft'):
            self.rect.topleft = (self.rect.topleft[0]-16,self.rect.topleft[1]-16)
        elif(self.dir == 'upright'):
            self.rect.topleft = (self.rect.topleft[0]-24,self.rect.topleft[1]-16)
        
        self.currentAnimationFrame += 1 #Animate the *next* frame
        gfx.animate(self,self.dir)
        
        if(self.currentAnimationFrame == 12): #After 12 frames, kill the animation
            self.kill()
        return
    def createSwishBox(self):
        swishrect = pygame.Rect(0,0,0,0)
        if(self.dir == 'down'):
            swishrect = pygame.Rect(self.rect.x,self.rect.y+64,64,128)
        elif(self.dir == 'left'):
            swishrect = pygame.Rect(self.rect.x,self.rect.y,128,64)
        elif(self.dir == 'right'):
            swishrect = pygame.Rect(self.rect.x+64,self.rect.y,128,64)
        elif(self.dir == 'up'):
            swishrect = pygame.Rect(self.rect.x,self.rect.y,64,128)
        elif(self.dir == 'downleft'):
            swishrect = pygame.Rect(self.rect.x,self.rect.y+45,90,90)
        elif(self.dir == 'downright'):
            swishrect = pygame.Rect(self.rect.x+45,self.rect.y+45,90,90)
        elif(self.dir == 'upleft'):
            swishrect = pygame.Rect(self.rect.x,self.rect.y,90,90)
        elif(self.dir == 'upright'):
            swishrect = pygame.Rect(self.rect.x+45,self.rect.y,90,90)
        return swishrect
    
class Player(pygame.sprite.Sprite):
    def __init__(self, X, Y):

        self.attacking = False
        self.currentAnimationFrame = 0
        self.currentAnimationType = 0
        self.moving = False

        self.dir = 'down'
        self.dx = 0
        self.dy = 0

        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = gfx.load_image('player-melee-down/frame1.png', -1)
        self.rect = pygame.Rect(X,Y,64,64)
        self.canAttack = True
        self.health = 100

        return

    def tookDamage(self,damage):
        self.health -= damage

    def returnPos(self):
        return self.rect.x, self.rect.yS
    def didMove(self, x, y): #Amount that Player moved
        self.rect.move_ip(x, y) #Moves the rect in place
    def setDir(self,direction):
        # 1. Set player's direction
        # 2. Change player's image to match direction
        self.dir = direction
        
        if self.currentAnimationType==0:
            if direction == 'down':
                self.image,null = gfx.load_image('player-melee-down/frame1.png',-1)
            elif direction == 'left':
                self.image,null = gfx.load_image('player-melee-left/frame1.png',-1)
            elif direction == 'right':
                self.image,null = gfx.load_image('player-melee-left/frame8.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            elif direction == 'up':
                self.image,null = gfx.load_image('player-melee-up/frame1.png',-1)
            elif direction == 'downleft':
                self.image,null = gfx.load_image('player-melee-downleft/frame1.png',-1)
            elif direction == 'downright':
                self.image,null = gfx.load_image('player-melee-downleft/frame8.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            elif direction == 'upleft':
                self.image,null = gfx.load_image('player-melee-upleft/frame1.png',-1)
            elif direction == 'upright':
                self.image,null = gfx.load_image('player-melee-upleft/frame8.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            elif direction == 'static':
                pass
            
    def update(self):
        # 1. Based on input, attempt to move
        # 2. If an animation should be running, run it
        if self.dir == 'down':
            self.dx,self.dy = 0,3
        elif self.dir == 'left':
            self.dx,self.dy = -3,0
        elif self.dir == 'right':
            self.dx,self.dy = 3,0
        elif self.dir == 'up':
            self.dx,self.dy = 0,-3
        elif self.dir == 'downleft':
            self.dx,self.dy = -3,3
        elif self.dir == 'downright':
            self.dx,self.dy = 3,3
        elif self.dir == 'upleft':
            self.dx,self.dy = -3,-3
        elif self.dir == 'upright':
            self.dx,self.dy = 3,-3
        
        if self.currentAnimationType is not 0 :
            self.currentAnimationFrame += 1
            gfx.animate(self,self.currentAnimationType)
        if self.currentAnimationFrame == 8:
            self.attacking = False
            self.currentAnimationFrame=1
            gfx.animate(self,self.currentAnimationType)
            self.currentAnimationType=0
            self.currentAnimationFrame=0

    #Make the Player Attack
    def attack(self):
        self.currentAnimationType = self.dir
        self.currentAnimationFrame = 0
        self.attacking = True
