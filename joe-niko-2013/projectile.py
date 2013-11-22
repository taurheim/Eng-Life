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
    def __init__(self,playerPos,mobPos,proj_type,extra):
        self.proj_type = proj_type
        self.aimingat = playerPos
        self.extra = extra
        self.frames = 0
        self.direction = extra

        #print playerPos,mousePos
        pygame.sprite.Sprite.__init__(self)

        #Calculate angle (dx,dy)
        change_xpos=(playerPos[0])-mobPos[0]
        change_ypos=(playerPos[1])-mobPos[1]
        l = math.sqrt(change_xpos**2 + change_ypos**2)
        if not l==0:
            tempx = ((10*change_xpos)/l)
            tempy = ((10*change_ypos)/l)
        else:
            tempx = 0
            tempy = 0

        #dx,dy
        self.dx = tempx/10.0
        self.dy = tempy/10.0


        #velocity
        if self.proj_type == 'tiny':
            v = 2
        elif self.proj_type == 'drop_paint':
            v = 3
        elif self.proj_type == 'fireball':
            v =5
            self.dy*=-1
        else:
            v = 5
        self.dx*=v
        self.dy*=v

        
        self.placeholder = [0,0]

        #Animation stuff
        self.doubleTick = True
        self.currentAnimationType = 1
        self.currentAnimationFrame = 1
        if self.proj_type == 'fireball':
            self.image,self.rect = load_image('engfireball.png')
            colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey)
            self.dx*=-1
            self.rect = pygame.Rect(playerPos[0],playerPos[1],32,32)
        elif self.proj_type == 'art' or self.proj_type == 'commerce':
            self.image, self.rect = load_image('Enemy-1/projectiles/Left.png')
            self.rect = pygame.Rect(mobPos[0],mobPos[1],26,26)
        elif self.proj_type == 'paint':
            self.image, self.rect = load_image('boss-art/ball-'+self.extra+'.png')
            colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey)
            self.rect = pygame.Rect(mobPos[0],mobPos[1],0,0)
        elif self.proj_type == 'boomer':
            self.image,self.rect = load_image('boss-art/palette.png')
            colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey)
            self.rect = pygame.Rect(mobPos[0],mobPos[1],175,175)
        elif self.proj_type == 'tiny':
            self.image,self.rect = load_image('boss-art/tiny/'+self.extra+'.png')
            self.rect = pygame.Rect(mobPos[0],mobPos[1],32,32)
            colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey)
        elif self.proj_type == 'drop_paint':
            if(self.extra[0]):
                self.image,self.rect = load_image('boss-art/ball-'+self.extra[1]+'.png')
            else:
                self.image,self.rect = load_image('boss-art/tiny/'+self.extra[1]+'.png')
            self.rect = pygame.Rect(mobPos[0],mobPos[1],0,0)
            colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey)
        elif self.proj_type == 'shadow':
            if(self.extra[0]):
                self.image,self.rect = load_image('boss-art/shadow-large.png')
                self.rect = pygame.Rect(mobPos[0]-55,mobPos[1]-20,0,0)
                self.image = pygame.transform.scale(self.image,(150,84))
            else:
                self.image,self.rect = load_image('boss-art/shadow-large.png')
                self.rect = pygame.Rect(mobPos[0]-16,mobPos[1],0,0)
            colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey)
        elif self.proj_type == 'football':
            if self.direction == 'up' :
                self.image, self.rect = load_image('Enemy-2/projectiles/Up.png')
                self.rect = pygame.Rect(mobPos[0],mobPos[1],23,45)
            if self.direction == 'down':
                self.image, self.rect = load_image('Enemy-2/projectiles/Down.png')
                self.rect = pygame.Rect(mobPos[0],mobPos[1],23,45)
            if self.direction == 'right' or self.direction == 'left' or self.direction == 'upleft' or self.direction == 'upright' or self.direction == 'downleft' or self.direction == 'downright':
                self.image, self.rect = load_image('Enemy-2/projectiles/Left.png')
                self.rect = pygame.Rect(mobPos[0],mobPos[1],26,26)
            colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey)
        elif self.proj_type == 'boss_football':
            self.image = pygame.image.load('sprites/football/frame0.png').convert_alpha()
            self.rect = pygame.Rect(mobPos[0],mobPos[1],32,32)
            self.frames=1
        elif self.proj_type == 'yell':
            if(self.extra):
                self.image = pygame.image.load('sprites/coach-art/keepmoving.png').convert_alpha()
            else:
                self.image = pygame.image.load('sprites/coach-art/stopmoving.png').convert_alpha()
            self.rect = pygame.Rect (mobPos[0],mobPos[1],0,0)
        else:
            print "Projectile type not recognized: ",self.proj_type
            

        #Bounds of game

        self.gameRect = pygame.Rect(0,0,800,600)
    def update(self):
        if(self.frames or self.proj_type=="boomer"):
            self.frames+=1
            if(self.frames==90 and (self.proj_type=="paint" or self.proj_type=="drop_paint")):
                self.kill()
            elif(self.frames%2==0 and self.proj_type=="boomer"):
                self.currentAnimationFrame+=1
                gfx.animate(self,self.currentAnimationType)
            elif(self.frames%2==0 and self.proj_type=="boss_football"):
                self.currentAnimationFrame+=1
                gfx.animate(self,self.currentAnimationType)
        if self.proj_type=='shadow':
            self.frames+=1
            if(self.frames >= self.extra[1]):
                self.kill()
        elif self.proj_type=='yell':
            self.frames+=1
            if(self.frames >= 8*60):
                self.kill()
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

        if self.frames >= 90:
            self.kill()

        
        if self.doubleTick == True:  
            if self.currentAnimationType is not 0 and self.proj_type=='paint':
                self.currentAnimationFrame += 1
                gfx.animate(self,self.currentAnimationType)
<<<<<<< HEAD
            if (self.currentAnimationFrame == 8 and self.proj_type=='paint') or (self.currentAnimationFrame==11 and self.proj_type=='boomer') or (self.currentAnimationFrame == 8 and self.proj_type=='art'):
=======
            if (self.currentAnimationFrame == 8 and self.proj_type=='paint') or (self.currentAnimationFrame==11 and self.proj_type=='boomer') or (self.currentAnimationFrame==12 and self.proj_type=='boss_football'):
>>>>>>> 9b94d262fa4ee043f26358e59b448e9f70bab336
                self.currentAnimationFrame=1
                gfx.animate(self,self.currentAnimationType)
                self.currentAnimationFrame=0
            if self.proj_type == 'art':
                self.currentAnimationFrame += 1
                gfx.animate(self,self.currentAnimationType)
            self.doubleTick == False
        else:
            self.doubleTick == True
        #print self.placeholder
        if not self.gameRect.collidepoint(self.rect.center):
            if self.proj_type == 'boomer' and self.extra is not "back":
                self.dx*=-1
                self.dy*=-1
                self.extra="back"
                pass
            elif self.proj_type == "boomer":
                pass
            else:
                self.die()
        if (self.proj_type == 'paint' or self.proj_type=='drop_paint') and self.rect.left <= self.aimingat[0]+5 and self.rect.top <= self.aimingat[1]+5 and self.rect.left >= self.aimingat[0]-5 and self.rect.top >= self.aimingat[1]-5:
            #Trying to hit here
            self.dx=0
            self.dy=0
            if(self.proj_type == 'paint'):
                self.image,null = load_image('boss-art/splat-'+self.extra+'.png')
                self.rect.left-=32
                self.rect.width = 128
                self.rect.height = 32
            elif(self.proj_type == 'drop_paint'):
                self.image,null = load_image('boss-art/splat-'+self.extra[1]+'.png')
                if self.extra[0]:
                    self.image = pygame.transform.scale(self.image,(192,96))
                    self.rect.left-=64
                    self.rect.width = 192
                    self.rect.height = 96
                    self.rect.top-=24
                else:
                    self.rect.left-=40
                    self.rect.top-=20
                    self.rect.width = 128
                    self.rect.height = 32
            self.frames+=1
            colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey)
    def die(self):
        self.kill()
