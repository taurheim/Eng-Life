import os,pygame,itertools

def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    #try:
    image = pygame.image.load(fullname)
    #except pygame.error, message:
    #    print 'Cannot load image:', name
    #    raise SystemExit, message
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
            if 1 == animation: #down
                filename = 'player-melee-down/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 2 == animation: #left
                filename = 'player-melee-left/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 3 == animation: #right
                filename = 'player-melee-left/frame'+str(9-sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 4 == animation: #up
                filename = 'player-melee-up/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 5 == animation: #downleft
                filename = 'player-melee-downleft/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 6 == animation: #downright
                filename = 'player-melee-downleft/frame'+str(9-sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 7 == animation: #upleft
                filename = 'player-melee-upleft/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 8 == animation: #upright
                filename = 'player-melee-upleft/frame'+str(9-sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
        elif "Projectile" == spriteType:
            return
        elif "Swish" == spriteType:
            filename = 'swish-down/frame'+str(sprite.currentAnimationFrame)+'.png'
            sprite.image,null = load_image(filename,-1)
            if 1 == animation: #down
                pass
            elif 2 == animation: #left
                sprite.image = pygame.transform.rotate(sprite.image,270)
            elif 3 == animation: #right
                sprite.image = pygame.transform.rotate(sprite.image,90)
            elif 4 == animation: #up
                sprite.image = pygame.transform.rotate(sprite.image,180)
            elif 5 == animation: #downleft
                sprite.image = pygame.transform.rotate(sprite.image,325)
            elif 6 == animation: #downright
                sprite.image = pygame.transform.rotate(sprite.image,45)
            elif 7 == animation: #upleft
                sprite.image = pygame.transform.rotate(sprite.image,245)
            elif 8 == animation: #upright
                sprite.image = pygame.transform.rotate(sprite.image,135)
        else:
            print "Unable to animate sprite of type: ",spriteType
    except pygame.error:
        #sprite.currentAnimationType=0
        sprite.currentAnimationFrame=0
    #sprite.image,sprite.rect = load_image('character2.png',-1)
    #print "done"
