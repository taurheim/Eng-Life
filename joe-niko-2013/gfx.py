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
            filename = "Enemy-1/projectiles/frames/"+str(sprite.currentAnimationFrame)+'.png'
            sprite.image,null = load_image(filename,-1)
        elif "Swish" == spriteType:
            filename = 'swish-down/frame'+str(sprite.currentAnimationFrame)+'.png'
            sprite.image,null = load_image(filename,-1)
            if 'down' == animation: #down
                pass
            elif 'left' == animation: #left
                sprite.image = pygame.transform.rotate(sprite.image,270)
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
        elif "Mob" == spriteType:
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
        else:
            print "Unable to animate sprite of type: ",spriteType
    except pygame.error:
        #sprite.currentAnimationType=0
        sprite.currentAnimationFrame=0
    #sprite.image,sprite.rect = load_image('character2.png',-1)
    #print "done"
