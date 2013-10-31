'''
@author Joe Crozier & Nikolai Savas
'''
import os, pygame, gfx

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
        
        self.currentAnimationFrame = 0
        self.currentAnimationType = 'static'
        self.dir = 'down'
        self.framecounter = 0

        self.image,self.rect = gfx.load_image("boss-fleisig/frame1.png",-1)
        self.rect = pygame.Rect(x,y,209,182)
        
        pass
    def move(self, x, y):
        pass
    def attack(self):
        pass
    def update(self):
        self.framecounter+=1
        if self.currentAnimationType is not 0:
            self.currentAnimationFrame +=1
            gfx.animate(self,self.currentAnimationType)
        if(self.framecounter%14 == 0):
            self.currentAnimationFrame += 1
        if(self.currentAnimationFrame == 4):
            self.currentAnimationType=0
            self.currentAnimationFrame=0
            self.framecounter = 0
