'''
@author Niko Savas and Joe Crozier
'''

import pygame

class Sounds(pygame.mixer):
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-1, channels=2, buffer=4096)
        self.musicChannel = pygame.mixer.Channel(0)
        self.soundsChannel1 = pygame.mixer.Channel(1)
        self.soundsChannel2 = pygame.mixer.Channel(2)
        self.musicSound = pygame.mixer.Sound('sounds/Kalimba.mp3')
        

    def playSound(sound):
        if sound == 'music1':
            self.musicChannel.play(self.musicSound)

    def stopSound(channel):
        if sound == 'music1':
            channel.stop()
            
