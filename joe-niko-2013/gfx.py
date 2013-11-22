import os,pygame,itertools


def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    #image = image.convert()
    image = image.convert_alpha()
    ##image.set_colorkey(image.get_at((1,1)))
    return image, image.get_rect()


class preloadedgfx(object):
    def __init__(self): 
        #Load all of the basic images
        self.swish_down = []
        self.swish_left = []
        self.swish_up = []
        self.swish_right = []
        for i in range(1,12):
            newimg,null = load_image('swish-down/frame'+str(i)+'.png',-1)
            self.swish_down.append(newimg)
            self.swish_left.append(pygame.transform.rotate(newimg,270))
        #Swing animations
    

def animate(sprite, animation):
    try:
        if(sprite.currentAnimationType==0):
            sprite.currentAnimationType=animation
            sprite.currentAnimationFrame=0
        spriteType = sprite.__class__.__name__
    
        if "Player" == spriteType:
            if 'down' == animation: #down
                filename = 'player-melee-down/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'left' == animation: #left
                filename = 'player-melee-left/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'right' == animation: #right
                filename = 'player-melee-left/frame'+str(9-sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 'up' == animation: #up
                filename = 'player-melee-up/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'downleft' == animation: #downleft
                filename = 'player-melee-downleft/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'downright' == animation: #downright
                filename = 'player-melee-downleft/frame'+str(9-sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 'upleft' == animation: #upleft
                filename = 'player-melee-upleft/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'upright' == animation: #upright
                filename = 'player-melee-upleft/frame'+str(9-sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
        elif "Projectile" == spriteType:
            if(sprite.proj_type == 'art'):
                filename = "Enemy-1/projectiles/frames/"+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif(sprite.proj_type == 'boomer'):
                filename = "boss-art/boomer/palette"+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif(sprite.proj_type == 'boss_football'):
                frame = str(sprite.currentAnimationFrame)
                if sprite.currentAnimationFrame>5:
                    frame = '0'
                filename= "football/frame"+frame+'.png'
                sprite.image,null = load_image(filename,-1)
        elif "Swish" == spriteType:
            #filename = 'swish-down/frame'+str(sprite.currentAnimationFrame)+'.png'
            #sprite.image,null = load_image(filename,-1)
            sprite.image = preloaded_gfx.swish_down[sprite.currentAnimationFrame-2]
            if 'down' == animation: #down
                pass
            elif 'left' == animation: #left
                sprite.image = pygame.transform.rotate(sprite.image,270)
                #sprite.image = preloaded_gfx.swish_left[sprite.currentAnimationFrame-2]
            elif 'right' == animation: #right
                sprite.image = pygame.transform.rotate(sprite.image,90)
            elif 'up' == animation: #up
                sprite.image = pygame.transform.rotate(sprite.image,180)
            elif 'downleft' == animation: #downleft
                sprite.image = pygame.transform.rotate(sprite.image,325)
            elif 'downright' == animation: #downright
                sprite.image = pygame.transform.rotate(sprite.image,45)
            elif 'upleft' == animation: #upleft
                sprite.image = pygame.transform.rotate(sprite.image,245)
            elif 'upright' == animation: #upright
                sprite.image = pygame.transform.rotate(sprite.image,135)
        elif "Mob" == spriteType and sprite.mobtype == 'football':
            if 'down' == animation: #down
                filename = 'Enemy-2/down-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'left' == animation: #left
                filename = 'Enemy-2/left-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'right' == animation: #right
                filename = 'Enemy-2/left-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 'up' == animation: #up
                filename = 'Enemy-2/up-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'downleft' == animation: #downleft
                filename = 'Enemy-2/down-left-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'downright' == animation: #downright
                filename = 'Enemy-2/down-left-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 'upleft' == animation: #upleft
                filename = 'Enemy-2/up-left-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'upright' == animation: #upright
                filename = 'Enemy-2/up-left-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
        elif "Mob" == spriteType and sprite.mobtype == 'commerce':
            animation = sprite.direction
            if 'down' == animation: #down
                filename = 'Enemy-3/Down-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'left' == animation: #left
                filename = 'Enemy-3/Right-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 'right' == animation: #right
                filename = 'Enemy-3/Right-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'up' == animation: #up
                filename = 'Enemy-3/Up-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'downleft' == animation: #downleft
                filename = 'Enemy-3/Down-right-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 'downright' == animation: #downright
                filename = 'Enemy-3/Down-right-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'upleft' == animation: #upleft
                filename = 'Enemy-3/Up-right-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 'upright' == animation: #upright
                filename = 'Enemy-3/Up-right-attack/Animation000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
        elif "Mob" == spriteType and sprite.mobtype == 'art':
            animation = sprite.direction
            if 'down' == animation: #down
                filename = 'Enemy-1/down-attack/Animation-Down000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'left' == animation: #left
                filename = 'Enemy-1/left-attack/Animation-Left000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'right' == animation: #right
                filename = 'Enemy-1/left-attack/Animation-Left000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 'up' == animation: #up
                filename = 'Enemy-1/up-attack/Animation-Up000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'downleft' == animation: #downleft
                filename = 'Enemy-1/down-left-attack/Animation-down-left000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'downright' == animation: #downright
                filename = 'Enemy-1/down-left-attack/Animation-down-left000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 'upleft' == animation: #upleft
                filename = 'Enemy-1/up-left-attack/Animation-up-left000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 'upright' == animation: #upright
                filename = 'Enemy-1/up-left-attack/Animation-up-left000'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
        elif "Boss" == spriteType:
            if(sprite.level==1):
                if(sprite.currentphase ==1):
                    filename = 'boss-art/throw000'+str(sprite.currentAnimationFrame)+'.png'
                    sprite.image,null = load_image(filename,-1)
                elif sprite.currentphase ==2:
                    filename = 'boss-art/throw-boomerang000'+str(sprite.currentAnimationFrame)+'.png'
                    sprite.image,null = load_image(filename,-1)
                elif sprite.currentphase ==4:
                    filename = 'boss-art/rage/rage000'+str(sprite.currentAnimationFrame)+'.png'
                    sprite.image,null = load_image(filename,-1)
                elif sprite.currentphase ==5:
                    filename = 'boss-art/death/death000'+str(sprite.currentAnimationFrame+1)+'.png'
                    sprite.image,null = load_image(filename,-1)
            if(sprite.level==2):
                if(sprite.currentphase==1):
                    filename= 'coach-art/throw'+str(sprite.currentAnimationFrame/5)+'.png'
                    sprite.image,null = load_image(filename,-1)
                elif(sprite.currentphase==2):
                    filename='coach-art/blow'+str(sprite.currentAnimationFrame/5)+'.png'
                    sprite.image,null = load_image(filename,-1)
                elif(sprite.currentphase==3):
                    pass
                elif(sprite.currentphase==4):
                    pass
                elif(sprite.currentphase==5):
                    pass
        else:
            print "Unable to animate sprite of type: ",spriteType+sprite.mobtype
    except pygame.error:
        #sprite.currentAnimationType=0
        sprite.currentAnimationFrame=0
    #sprite.image,sprite.rect = load_image('character2.png',-1)
    #print "done"
