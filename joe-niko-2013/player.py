'''
@author Joe Crozier & Niko Savas
'''
import os, pygame

def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    return image, image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('character1.png', -1)
        
        #playerSurface = pygame.image.load('character1.png').convert()
        self.X = X
        self.Y = Y
        return
