'''
@author Joe Crozier & Niko Savas
'''
import os,pygame,gfx,time

class GAME_INFO:
    GAME_TITLE = "Epic Game Challenge"
    GAME_SUBTITLE = ""
# Run title screen

class TitleScreen():
    def __init__(self,size):
        self.screensurface = pygame.Surface(size)
        self.screensurface = self.screensurface.convert()
        self.back,null = gfx.load_image("titlescreen/bg.png",-1)
        self.playbtn = [gfx.load_image("titlescreen/playhover.png",-1)[0],pygame.Rect(109,460,174,72)]
        self.instbtn = [gfx.load_image("titlescreen/insthover.png",-1)[0],pygame.Rect(344,460,375,72)]
        self.inst,rand = gfx.load_image("titlescreen/inst.png",-1)
        self.backbtn = [gfx.load_image("titlescreen/backhover.png",-1)[0],pygame.Rect(19,514,268,72)]
    def screen_loop(self,screen):
        self.running = True
        tick_timer = pygame.time.Clock()
        while self.running:
            pygame.display.flip()
            tick_timer.tick(60)
            screen.blit(self.back, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if self.playbtn[1].collidepoint(mouse):
                        self.running = False
                        return True
                    elif self.instbtn[1].collidepoint(mouse):
                        #Run instruction loop
                        instructions = True
                        screen.blit(self.inst, (0,0))
                        while instructions:
                            pygame.display.flip()
                            mouse = pygame.mouse.get_pos()
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and self.backbtn[1].collidepoint(mouse):
                                    instructions = False
                            if self.backbtn[1].collidepoint(mouse):
                                screen.blit(self.backbtn[0],(19,514))
                            else:
                                screen.blit(self.inst, (0,0))
            mouse = pygame.mouse.get_pos()
            if self.playbtn[1].collidepoint(mouse):
                screen.blit(self.playbtn[0],(109,460))
            elif self.instbtn[1].collidepoint(mouse):
                screen.blit(self.instbtn[0],(344,460))


class deathScreen():
    def __init__(self,dead,level):
        self.screensurface = pygame.Surface((500,300))
        self.screensurface.convert()
        if dead == True:
            self.image,null = gfx.load_image("menus/death.png",-1)
        else:
            self.image,null = gfx.load_image('menus/level'+str(level)+'win.png',-1)
        self.playRect = pygame.Rect(170,380,210,50)
        self.quitRect = pygame.Rect(530,380,80,50)
    def screen_loop(self,screen):
        self.running = True
        tick_timer = pygame.time.Clock()
        while self.running:
            pygame.display.flip()
            tick_timer.tick(60)
            screen.blit(self.image, (150,150))
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if self.playRect.collidepoint(mouse):
                        self.running = False
                        return True
                    elif self.quitRect.collidepoint(mouse):
                        self.running = False
                        return False

                
                
            
