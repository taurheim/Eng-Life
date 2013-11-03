import os, pygame, gfx

class Level(object):
    def __init__(self,level,bg):

        self.leveltimer = 0
        
        self.level = level #int, which level we are currently on.
        self.obstacles = []

        #### MOBS ####
        # 1. Art Student
        # 2. Commerce Student
        # 3. Health Sci Student
        # 4. Football Player
        # 5. All of the above

        self.mobType = 0
        self.spawnRate = 0
        self.spawnPoints = []

        
        if 1==level:
            self.bg,null = gfx.load_image("level-1-bg.png",-1)
            self.fg,null = gfx.load_image("level-1-fg.png",-1)
            
            self.obstacles.append(pygame.Rect(312,440,80,55))
            self.obstacles.append(pygame.Rect(106,197,65,62))
            self.obstacles.append(pygame.Rect(372,197,65,62))
            self.obstacles.append(pygame.Rect(634,197,65,62))

            self.mobType='art'
            self.spawnRate = 5
            self.spawnPoints = [(800,600),(0,600),(300,600)]
            
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
        
