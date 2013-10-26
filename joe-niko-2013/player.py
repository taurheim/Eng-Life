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
        self.image, self.rect = load_image('character3.png', -1)
        
        #playerSurface = pygame.image.load('character2.png').convert()

        self.rect = pygame.Rect(X,Y,100,100) 
        return
    def didMove(self, x, y): #Amount that Player moved
        
        self.rect.move_ip(x, y) #Moves the rect in place
    def changeSprite(self, direction):
        if direction == 'left':
            fullname = os.path.join('sprites', 'left.jpg')
            self.image = pygame.image.load(fullname)
            self.image.convert()
        if direction == 'right':
            fullname = os.path.join('sprites', 'right.jpg')
            self.image = pygame.image.load(fullname)
            self.image.convert()
        if direction == 'up':
            fullname = os.path.join('sprites', 'up.jpg')
            self.image = pygame.image.load(fullname)
            self.image.convert()
        if direction == 'down':
            fullname = os.path.join('sprites', 'down.jpg')
            self.image = pygame.image.load(fullname)
            self.image.convert()
    
