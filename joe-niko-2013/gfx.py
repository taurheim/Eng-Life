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
            if 1 == animation:
                filename = 'player-melee-down/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 2 == animation:
                filename = 'player-melee-left/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
            elif 3 == animation:
                filename = 'player-melee-left/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
                sprite.image = pygame.transform.flip(sprite.image,True,False)
            elif 4 == animation:
                filename = 'player-melee-up/frame'+str(sprite.currentAnimationFrame)+'.png'
                sprite.image,null = load_image(filename,-1)
        elif "Projectile" == spriteType:
            return
    except pygame.error:
        sprite.currentAnimationType=0
        sprite.currentAnimationFrame=0
    #sprite.image,sprite.rect = load_image('character2.png',-1)
    #print "done"
