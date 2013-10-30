'''
@author Joe Crozier & Niko Savas
'''
import os, pygame, gfx

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
        
        if(self.dir == 'down'):
            self.currentAnimationType=1
        if(self.dir == 'left'):
            self.currentAnimationType=2
        if(self.dir == 'right'):
            self.currentAnimationType=3
        if(self.dir == 'up'):
            self.currentAnimationType=4
        if(self.dir == 'downleft'):
            self.currentAnimationType=5
            self.rect.topleft = (self.rect.topleft[0]-16,self.rect.topleft[1]-16)
        if(self.dir == 'downright'):
            self.currentAnimationType=6
            self.rect.topleft = (self.rect.topleft[0]-24,self.rect.topleft[1]-24)
        if(self.dir == 'upleft'):
            self.currentAnimationType=7
            self.rect.topleft = (self.rect.topleft[0]-16,self.rect.topleft[1]-16)
        if(self.dir == 'upright'):
            self.currentAnimationType=8
            self.rect.topleft = (self.rect.topleft[0]-24,self.rect.topleft[1]-16)
        
        self.currentAnimationFrame += 1
        gfx.animate(self,self.currentAnimationType)
        if(self.currentAnimationFrame == 12):
            self.kill()
        return
    
class Player(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        
        self.currentAnimationFrame = 0
        self.currentAnimationType = 0

        self.dir = 'down'
        
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = gfx.load_image('character3.png', -1)
        
        #playerSurface = pygame.image.load('character2.png').convert()
        self.Xpos = X
        self.Ypos = Y
        self.rect = pygame.Rect(X,Y,64,64) 
        return
    def didMove(self, x, y): #Amount that Player moved
        
        self.rect.move_ip(x, y) #Moves the rect in place
    def changeSprite(self, direction):
        if direction == 'left':
            fullname = os.path.join('sprites', 'player-melee-left/frame1.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image.set_colorkey(self.image.get_at((1,1)))
        if direction == 'right':
            fullname = os.path.join('sprites', 'player-melee-left/frame8.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image = pygame.transform.flip(self.image,True,False)
            self.image.set_colorkey(self.image.get_at((1,1)))
        if direction == 'up':
            fullname = os.path.join('sprites', 'player-melee-up/frame1.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image.set_colorkey(self.image.get_at((1,1)))            
        if direction == 'down':
            fullname = os.path.join('sprites', 'player-melee-down/frame1.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image.set_colorkey(self.image.get_at((1,1)))
        if direction == 'downleft':
            fullname = os.path.join('sprites', 'player-melee-downleft/frame1.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image.set_colorkey(self.image.get_at((1,1)))
        if direction == 'downright':
            fullname = os.path.join('sprites', 'player-melee-downleft/frame8.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image = pygame.transform.flip(self.image,True,False)
            self.image.set_colorkey(self.image.get_at((1,1)))
        if direction == 'upleft':
            fullname = os.path.join('sprites', 'player-melee-upleft/frame1.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image.set_colorkey(self.image.get_at((1,1)))
        if direction == 'upright':
            fullname = os.path.join('sprites', 'player-melee-upleft/frame8.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image = pygame.transform.flip(self.image,True,False)
            self.image.set_colorkey(self.image.get_at((1,1)))
            
        self.dir = direction
    def update(self):
        if self.currentAnimationType != 0 :
            self.currentAnimationFrame += 1
            gfx.animate(self,self.currentAnimationType)
        if self.currentAnimationFrame == 8:
            self.currentAnimationFrame=1
            gfx.animate(self,self.currentAnimationType)
            self.currentAnimationType=0
            self.currentAnimationFrame=0

##    def canMove(self):
##        bottomLeftX = self.rect.bottomleft[0]
##        bottomLeftY = self.rect.bottomleft[1]
##        bottomRightX = self.rect.bottomright[0]
##        bottomRightY = self.rect.bottomright[1]
##        
##        topLeftX = self.rect.bottomleft[0]
##        topLeftY = self.rect.topright[1]
##        topRightX = self.rect.topright[0]
##        topRightY = self.rect.topright[1]
##
##        xCorners = [bottomLeftX, bottomRightX, topLeftX, topRightX]
##        yCorners = [bottomLeftY, bottomRightY, topLeftY, topRightY]
##
##        
##        
##
##        if 0 < self.rect.bottom < 600 and 0 < self.rect.top < 600 and 0 < self.rect.left < 800 and 0 < self.rect.left < 800:
##            return True
##        if self.rect.bottom == 600 or self.rect.bottom == 601 or self.rect.bottom == 602:
##            self.rect.bottom = 599
##            print self.rect.bottom
##            return False
##        if self.rect.bottom == 600 or self.rect.bottom == 601 or self.rect.bottom == 602:
##            self.rect.bottom = 599
##            print self.rect.bottom
##            return False
##        
##        else:
##            return False
