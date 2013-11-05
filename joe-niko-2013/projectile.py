'''
@author Joe Crozier & Niko Savas
'''
import pygame,os,math,gfx


#We will move this eventually to gfx
def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    return image, image.get_rect()


class Projectile(pygame.sprite.Sprite):
    def __init__(self,playerPos,mobPos,proj_type):
        #print playerPos,mousePos
        pygame.sprite.Sprite.__init__(self)

        #Calculate angle (dx,dy)
        change_xpos=(playerPos[0])-mobPos[0]
        change_ypos=(playerPos[1])-mobPos[1]
        l = math.sqrt(change_xpos**2 + change_ypos**2)
        tempx = ((10*change_xpos)/l)
        tempy = ((10*change_ypos)/l)

        #dx,dy
        self.dx = tempx/10.0
        self.dy = tempy/10.0


        #velocity
        v = 5
        self.dx*=v
        self.dy*=v

        
        self.placeholder = [0,0]

        #Animation stuff
        self.doubleTick = True
        self.currentAnimationType = 1
        self.currentAnimationFrame = 1
        if proj_type == 'art':
            self.image, self.rect = load_image('Enemy-1/projectiles/Left.png')
            
        self.rect = pygame.Rect(mobPos[0],mobPos[1],26,26)

        #Bounds of game

        self.gameRect = pygame.Rect(0,0,800,600)
    def update(self):
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
        if self.doubleTick == True:  
            if self.currentAnimationType is not 0 :
                self.currentAnimationFrame += 1
                gfx.animate(self,self.currentAnimationType)
            if self.currentAnimationFrame == 8:
                self.currentAnimationFrame=1
                gfx.animate(self,self.currentAnimationType)
                self.currentAnimationFrame=0
            self.doubleTick == False
        else:
        
            self.doubleTick == True
        #print self.placeholder

        if not self.gameRect.contains(self.rect):
            self.die()

    def die(self):
        self.kill()
