'''
@author Joe Crozier & Niko Savas
'''
import os, pygame, gfx, physics

class Swish(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        self.currentAnimationFrame = 1
        self.currentAnimationType = 1
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
        self.image, self.rect = gfx.load_image('character3.png', -1)
        self.rect = pygame.Rect(X,Y,32,32)
        return
    def didMove(self, x, y): #Amount that Player moved
        self.rect.move_ip(x, y) #Moves the rect in place
    def setDir(self,direction):
        # 1. Set player's direction
        # 2. Change player's image to match direction
        self.dir = direction
        
        if self.currentAnimationType==0:
            if direction == 'down':
                self.image,null = gfx.load_image('player-melee-down/frame1.png',-1)
            if direction == 'left':
                self.image,null = gfx.load_image('player-melee-left/frame1.png',-1)
            if direction == 'right':
                self.image,null = gfx.load_image('player-melee-left/frame8.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            if direction == 'up':
                self.image,null = gfx.load_image('player-melee-up/frame1.png',-1)
            if direction == 'downleft':
                self.image,null = gfx.load_image('player-melee-downleft/frame1.png',-1)
            if direction == 'downright':
                self.image,null = gfx.load_image('player-melee-downleft/frame8.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            if direction == 'upleft':
                self.image,null = gfx.load_image('player-melee-upleft/frame1.png',-1)
            if direction == 'upright':
                self.image,null = gfx.load_image('player-melee-upleft/frame8.png',-1)
                self.image = pygame.transform.flip(self.image,True,False)
            if direction == 'static':
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
        
        if self.currentAnimationType != 0 :
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
