'''
@author Joe Crozier & Niko Savas
'''
import os, pygame, gfx


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
        self.rect = pygame.Rect(X,Y,32,32) 
        return
    def didMove(self, x, y): #Amount that Player moved
        
        self.rect.move_ip(x, y) #Moves the rect in place
    def changeSprite(self, direction):
        if direction == 'left':
            fullname = os.path.join('sprites', 'left.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image.set_colorkey(self.image.get_at((1,1)))
        if direction == 'right':
            fullname = os.path.join('sprites', 'left.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image = pygame.transform.flip(self.image,True,False)
            self.image.set_colorkey(self.image.get_at((1,1)))
        if direction == 'up':
            fullname = os.path.join('sprites', 'up.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image.set_colorkey(self.image.get_at((1,1)))
        if direction == 'down':
            fullname = os.path.join('sprites', 'down.png')
            self.image = pygame.image.load(fullname)
            self.image.convert()
            self.image.set_colorkey(self.image.get_at((1,1)))
        self.dir = direction
    def update(self):
        if self.currentAnimationType != 0 :
            self.currentAnimationFrame += 1
        gfx.animate(self,self.currentAnimationType)
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
