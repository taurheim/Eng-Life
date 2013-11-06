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
                        pass
            mouse = pygame.mouse.get_pos()
            if self.playbtn[1].collidepoint(mouse):
                screen.blit(self.playbtn[0],(109,460))
                #hoverimg = self.playbtn[0].copy()
                #hoverimg.fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
                #print hoverimg
                #screen.blit(hoverimg,(150,460))
            elif self.instbtn[1].collidepoint(mouse):
                screen.blit(self.instbtn[0],(344,460))
                
    def fade(self,):
        DURATION = 2.0 # seconds
        start_time = time.clock()
        ratio = 0.0 # alpha as a float [0.0 .. 1.0]
        while ratio < 1.0:
            current_time = time.clock()
            ratio = (current_time - start_time) / DURATION
            if ratio > 1.0: # we're a bit late
                ratio = 1.0
            # all your drawing details go in the following call
            #screen.blit((self.playbtn[0][0], alpha = 255 * ratio)
