import os, pygame, gfx

class Level(object):
    def __init__(self,level,bg):
        self.level = level #int, which level we are currently on.
        self.obstacles = []
        if 1==level:
            self.bg,null = gfx.load_image("bg-test-2-b.png",-1)
            self.fg,null = gfx.load_image("bg-test-2-f.png",-1)
            #self.obstacles.append(pygame.Rect(100,140,200,110))
        if 2==level:
            pass
        if 3==level:
            pass
        if 4==level:
            pass
        if 5==level:
            pass
    def tick(self):
        pass
        
