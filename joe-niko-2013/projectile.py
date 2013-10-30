'''
@author Joe Crozier & Niko Savas
'''
import pygame,os,math


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
    def __init__(self,playerPos,mousePos,proj_type):
        #print playerPos,mousePos
        pygame.sprite.Sprite.__init__(self)

        #Calculate angle (dx,dy)
        change_xpos=(mousePos[0])-playerPos[0]
        change_ypos=(mousePos[1])-playerPos[1]
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
        
        self.image,self.rect = load_image('projectile.gif',-1)
        self.rect = pygame.Rect(playerPos[0],playerPos[1],8,21)
    def update(self,phys):
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

        #print self.placeholder
