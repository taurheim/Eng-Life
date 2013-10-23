#Port of the GameMaker 8 game Space Wars
#Original coding by Mustafa Haddara
#Port by Mustafa Haddara
#Graphics by Mark Overmars & YoYoGames.com
#Minor alterations to graphics by Mustafa Haddara
#Sound by Sam Dillard at samostudios.com

'''Known Bugs'''


'''Known Bugs End'''

import pygame, sys, random, pygame.mixer, os
from pygame.locals import *
#from functions import *
pygame.mixer.pre_init(44100,-16,2, 1024) 
pygame.init()
pygame.font.init
pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT, MOUSEBUTTONDOWN])

path = os.path.abspath("SpaceWars.py")[:-12] #Gets the file path of the folder, allows us to search for resources (ie images, sounds, etc)

rmheight = 480
rmwidth = 640
#Room properties
win = pygame.display.set_mode((rmwidth, rmheight)) #Window

'''GRAPHICS INITIALIZATION'''

# 0-Asteroid 1-Planet1 2-Planet2 3-Planet3 4-Rocket 5-Enemy1 6-Laser 7-background 8-health 9-bomb 10-panel 11-Enemy2A 12-Enemy2B 13-Enemy3 14-PlayButton 15-Exit button

sprites = ["Sprites/meteorite_large1.png", "Sprites/planet1.png", "Sprites/planet2.png", #This is one long list of all of the images used by the game. The above list is for index # reference only
           "Sprites/planet3.png", "Sprites/rocket.png", "Sprites/ufo_1.png",
           "Sprites/Laser.png", "Backgrounds/Space.jpg", "Sprites/health.png",
           "Sprites/nuke.png", "Sprites/panel.png", "Sprites/ufo_2A.png",
           "Sprites/ufo_2B.png", "Sprites/ufo_3.png", "Sprites/button_play.png",
           "Sprites/button_quit.png"]


images = [pygame.image.load(path+i).convert_alpha() for i in sprites] #load all images, store them in a list

#For the explosion, we execute a modified version of the above
#This is necessary because the explosion is made up of a series of images playing one after the other to animate
#Also there are two kinds of explosions, a large one and a small

exploList = [path + "Sprites/explosion/big/" + str(i) + ".png" for i in range(7)]
for i in range(7):
    exploList.append(path + "Sprites/explosion/small/" + str(i) + ".png")

for i in range(14):
    exploList[i] = pygame.image.load(exploList[i]).convert_alpha()
        

'''FONTS INITIALIZATION'''
fnt_main = pygame.font.Font(path + "Fonts/font.ttf", 128) #Font for the main menu
fnt_score = pygame.font.Font(path + "Fonts/font.ttf", 50) #Font to write the score
fnt_hscore = pygame.font.Font(path + "Fonts/font.ttf", 36) #Font to get high score


'''SOUNDS INITIALIZATION'''

## Because background music is actually TWO pieces of music (an intro and then
## a looping section) the way to get python to play one right after the other at the
## right time is different from how we play the sound effects

pygame.mixer.music.load(path+"Sounds/Intro.ogg")
pygame.mixer.music.play()
snd_laser = pygame.mixer.Sound(path+"Sounds/laser.ogg")
snd_explosion = pygame.mixer.Sound(path+"Sounds/explosion.ogg")
snd_health = pygame.mixer.Sound(path+"Sounds/health.ogg")

## Set the volume fo the effects to get a good balance between background music and effects
snd_laser.set_volume(0.15)
snd_explosion.set_volume(0.2)
snd_health.set_volume(0.5)

## Lastly a sentinel value to flag if we have started to play the main looping music or not
mainSnd = False

'''CLASSES BEGIN HERE'''

## Each class is a variation of the same thing. All have the following variables:
## X, Y, speedX, speedY, out
## Out is a bool which tells the game if the object shoudl be deleted or not

## Most objects also have:
## name, padLeft, padTop, padRight, padBottom
## Name is a proprietary identifier for collision checks
## The 4 pads are the modifiers on the rectangular image which tell python where
##  the bounding box to be used for collisions is.

class rocket:
     
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.speedX = 0
        self.speedY = 0
        self.width = 32
        self.height = 32
        self.padLeft = 9
        self.padTop = 0
        self.padRight = 22
        self.padBottom = 30
        self.canShoot = True
        self.laserTimer = -9
        self.out = False
        self.name = "rocket"

    def shoot(self):
        self.canShoot = False
        return laser((self.X, self.Y)) #Sprites/Laser.png

    def move(self):
        self.X += self.speedX 
        if self.X < 10:
            self.X = 10
        if self.X > 598:
            self.X = 598
		
        self.Y += self.speedY
        if self.Y < 4:
            self.Y = 4
        if self.Y > 368:
            self.Y = 368

    def draw(self, win):
        win.blit(images[4], (self.X, self.Y))
        #Loads the image, blits to screen at self.X and self.Y

class background:

    def __init__(self, y):
        self.X = 0
        self.Y = y
        self.speed = 4
        
    def move(self):
        self.Y += self.speed
        if self.Y > 480:
            self.Y = -700

    def draw(self, win):
        win.blit(images[7], (self.X, self.Y))

        
class asteroid:
     
    def __init__(self):
        self.X = random.randint(10, rmwidth - 64 - 10)
        self.Y = -100
        self.speedX = 0
        self.speedY = 8 + random.randint(1, 3)
        self.width = 64
        self.height = 64
        self.padLeft = 0
        self.padTop = 0
        self.padRight = self.width
        self.padBottom = self.height
        self.out = False
        self.name = "asteroid"
        
    def move(self):
        self.Y += self.speedY
        if self.Y > 520:
            self.__init__()

    def jump(self):
        self.__init__()

    def draw(self, win):
        win.blit(images[0], (self.X, self.Y))
        #Loads the image, blits to screen at self.X and self.Y

class laser:
    
    def __init__(self, position):
        self.X = position[0]
        self.Y = position[1]
        self.speedX = 0
        self.speedY = -16
        self.width = 32
        self.height = 32
        self.padLeft = 13
        self.padTop = 4
        self.padRight = 17
        self.padBottom = 27
        self.out = False
        self.name = "laser"

    def move(self):
        self.Y += self.speedY
        if self.Y < -40:
            self.out = True

    def draw(self, win):
        win.blit(images[6], (self.X, self.Y))
        #Loads the image, blits to screen at self.X and self.Y


class explosion:

    def __init__(self, x, y, size):
        #big = 0, small = 1
        self.X = x
        self.Y = y
        self.speedX = 0
        self.speedY = 0
        self.padLeft = 0
        self.padTop = 1
        self.padRight = 30
        self.padBottom = 30
        self.out = False
        self.timer = 0
        self.name = "explosion"
        self.size = size

    def move(self):
        return None
    
    def draw(self, win):
        if self.timer < 7:
            win.blit(exploList[self.timer+7*self.size], (self.X, self.Y))
            self.timer += 1
        else:
            self.out = True

    
class alien1:
    
    def __init__(self):
        self.X = random.randint(10, rmwidth - 64 - 10)
        self.Y = -100
        self.speedX = 8 - random.randint(0, 1) * 16
        self.speedY = 8 + random.randint(1, 3)
        self.width = 64
        self.height = 32
        self.padLeft = 2
        self.padTop = 4
        self.padRight = 61
        self.padBottom = 26
        timer = 100
        self.out = False
        self.name = "alien1"

    def draw(self, win):
        win.blit(images[5], (self.X, self.Y))

    def move(self):
        self.X += self.speedX
        if self.X < 10:
            self.X = 10
            self.speedX *= -1
        if self.X > 566:
            self.X = 566
            self.speedX *= -1
        self.Y += self.speedY
        if self.Y > 520:
            self.__init__()

    def jump(self):
        self.__init__()

class alien2:
    
    def __init__(self):
        self.X = random.randint(10, rmwidth - 64 - 10)
        self.Y = -100
        self.speedX = 8 - random.randint(0, 1) * 16
        self.speedY = 5 + random.randint(1, 3)
        self.width = 64
        self.height = 32
        self.padLeft = 2
        self.padTop = 4
        self.padRight = 61
        self.padBottom = 26
        self.timer = 80
        self.out = False
        self.name = "alien2"
        self.health = 0

    def draw(self, win):
        win.blit(images[11 + self.health], (self.X, self.Y))
            

    def move(self):
        self.X += self.speedX
        if self.X < 10:
            self.X = 10
            self.speedX *= -1
        if self.X > 566:
            self.X = 566
            self.speedX *= -1

        self.Y += self.speedY
        if self.Y > 520:
            self.jump()

        self.timer -= 1

        if self.timer == 0:
            if self.health == 0:
                objects.append(bomb(self.X+16, self.Y+8, 1))
                self.timer = 80

    def jump(self):
        self.X = random.randint(10, rmwidth - 64 - 10)
        self.Y = -100
        self.speedX = 8 - random.randint(0, 1) * 16
        self.speedY = 5 + random.randint(1, 3)

class alien3:
    
    def __init__(self):
        self.X = random.randint(10, rmwidth - 64 - 10)
        self.Y = 500
        self.speedX = 0
        self.speedY = -3 - random.randint(1, 3)
        self.width = 64
        self.height = 32
        self.padLeft = 2
        self.padTop = 4
        self.padRight = 61
        self.padBottom = 26
        self.timer = 30
        self.out = False
        self.name = "alien3"

    def draw(self, win):
        win.blit(images[13], (self.X, self.Y))
            

    def move(self):
        self.X += self.speedX
        if self.X < 10:
            self.X = 10
            self.speedX *= -1
        if self.X > 566:
            self.X = 566
            self.speedX *= -1

        self.Y += self.speedY
        if self.Y < -40:
            self.__init__()

        self.timer -= 1

        if self.timer == 0:
            objects.append(bomb(self.X+16, self.Y, -1))
            self.timer = 30

    def jump(self):
        self.__init__()
        
class planet:
    
    def __init__(self, num):
        self.X = num * 123 + 200
        self.Y = -100 - random.randint(0, 2)*random.randint(0, 200)
        self.speedX = 0
        self.speedY = 4
        self.width = 32
        self.height = 32
        self.num = num
        self.out = False
        self.padRight = 0
        self.padTop = 0
        self.padLeft = 0
        self.padBottom = 0
        self.name = "planet"
    
    def draw(self, win):
        win.blit(images[self.num], (self.X, self.Y))

    def move(self):
        self.Y += self.speedY
        if self.Y > 520:
            self.X = random.randint(10, rmwidth - 64 - 10)
            self.Y = -10 - random.randint(0, 2)*random.randint(0, 200)

class bomb:

    def __init__(self, x, y, direction):
        self.X = x
        self.Y = y
        self.speedX = 0
        self.speedY = direction*14
        self.width = 32
        self.height = 32
        self.out = False
        self.padLeft = 1
        self.padTop = 1
        self.padRight = 30
        self.padBottom = 30
        self.name = "bomb"

    def move(self):
        self.Y += self.speedY
        if self.Y > 650:
            self.out = True

    def draw(self, win):
        win.blit(images[9], (self.X, self.Y))

    def jump(self):
        self.out = True

class healthy:

    def __init__(self):
        self.X = random.randint(10, 438)
        self.Y = 0 - random.randint(300, 450)
        self.speedX = 0
        self.speedY = 10
        self.width = 32
        self.height = 32
        self.out = False
        self.padLeft = 1
        self.padTop = 1
        self.padRight = 30
        self.padBottom = 30
        self.name = "health"

    def move(self):
        self.Y += self.speedY
        if self.Y > 500:
            self.out = True

    def draw(self, win):
        win.blit(images[8], (self.X, self.Y))

    def jump(self):
        self.out = True

class button:

    def __init__(self, X, Y, num):

        #num 0 for play button, 1 for exit button
        self.num = 14+num
        self.X = X
        self.Y = Y
        self.width = 160
        self.height = 48
        self.speedX = 0
        self.speedY = 0
        self.padLeft = 0
        self.padTop = 0
        self.padRight = 0
        self.padBottom = 0
        self.out = False
        self.name = "Button"

    def draw(self, win):
        win.blit(images[self.num], (self.X, self.Y))

    def move(self):
        self.X += self.speedX
        if self.X > 640 or self.X < -170:
            self.out = True

'''CLASSES END HERE'''

'''FUNCTIONS BEGIN HERE'''

def collision(a, b):
    a.box1X = a.X + a.padLeft
    a.box1Y = a.Y + a.padTop
    a.box2X = a.X + a.padRight
    a.box2Y = a.Y + a.padBottom

    b.box1X = b.X + b.padLeft
    b.box1Y = b.Y + b.padTop
    b.box2X = b.X + b.padRight
    b.box2Y = b.Y + b.padBottom
    
    if a.box1X in range(b.box1X, b.box2X+1) or a.box2X in range (b.box1X, b.box2X+1) or b.box1X in range(a.box1X, a.box2X+1) or b.box2X in range(a.box1X, a.box2X+1):
        if a.box1Y in range(b.box1Y, b.box2Y+1) or a.box2Y in range (b.box1Y, b.box2Y+1) or b.box1Y in range(a.box1Y, a.box2Y+1) or b.box2Y in range(a.box1Y, a.box2Y+1):
            return True
        else:
            return False
    else:
        return False

def backScroll(back, speed):
    if backy1 >= 480:
        backy1 = -700
    else:
        backy1 += backspeed

def update(score, win):
    print "You scored " + str(score) + " points!"
    highscores = open("HIGH SCORES.txt", "r")
    scores = highscores.readlines()
    scorelist, namelist = [], []
    highscores.close()

    for i in range(2, 21, 2):
        scorelist.append(scores[i][-6:-1])
        namelist.append(scores[i][3:-10])

    while len(str(score)) < 5:
        score = "0" + str(score)

    i=0
    highscores = open("HIGH SCORES.txt", "w")
    highscores.write('\t=== HIGH SCORES ===\n')
    while i<10:
        if score > scorelist[i]:
            hsName = raw_input("You got a HIGH SCORE! Enter your name: ")
            print "Congratulations, " + hsName +"!"
            highscores.write("\n" + str(i+1) + ".\t" + hsName + " --- " + score + "\n")
            for j in range(i, 9):
                highscores.write("\n" + str(j+2) + ".\t" + namelist[j] + " --- " + scorelist[j] + "\n")
            i=10
        else:
            highscores.write("\n" + str(i+1) + ".\t" + namelist[i] + " --- " + scorelist[i] + "\n")
            i += 1

    highscores.close()

def resetScore():
    highscores = open("HIGH SCORES.txt", "w")
    highscores.write('\t=== HIGH SCORES ===\n')
    for i in range(1, 11):
        highscores.write("\n" + str(i) + ".\t[NONE] --- 00000\n")
    highscores.close()

'''FUNCTIONS END HERE'''


'''BACKGROUNDS INITIALIZATION'''
## This has to happen after the classes definitions
backgrounds = [] ## List of three background images moving in tandem to create illusion of motion
for y in [0, 400, -400]:
    backgrounds.append(background(y))


'''VARIABLES INITIALIZATION'''
objects = []  ## reseting to zero
objects.append(rocket(320, 352))
laserList = []

for i in range(1, 4):
    objects.append(planet(i))

frame = 0 #Frame counter
menuFrame = 0 #Another frame counter jsut for the menu
shoot = False #Flag if spacebar is pressed
laserWait = 4 #Timer to wait between successive laser shots
asteroidHit = 0 #Number of asteroids hit
alien1Hit = 0 #Number of green aliens hit
alien2Hit = 0 #Number of red aliens hit
alien3Hit = 0 #Number of blue aliens hit
score = 0 #Score
health = 0 #Health. We start at zero so it defaults to the menu
playing = False  #Flag if the game is being played, False if the player is in the main menu
mPos = (0, 0) #mouse position


'''MAIN GAME LOOP BEGINS HERE'''

while True:

    if playing == False:
        menuFrame = 0
        if score > 0:
            win.blit(fnt_hscore.render("You got a HIGH SCORE! Enter your name in IDLE.", True, (255, 219, 0)), (60, 100))
            pygame.display.flip()
            update(score, win) ## Update the high scores, if need be
        if health <= 0:
            objects  = []
            objects.append(rocket(304, 192))
            for i in range(1, 4):
                objects.append(planet(i))
            objects.append(button(96, 256, 0))
            objects.append(button(384, 256, 1))
        asteroidHit, alien1Hit, alien2Hit, alien3Hit, score = 0, 0, 0, 0, 0
        health = 100
        
        if mPos[0] > objects[5].X and mPos[0] < objects[5].X+objects[5].width and mPos[1] > objects[5].Y and mPos[1] < objects[5].Y+objects[5].height:
            pygame.quit()
            sys.exit()
            
        if mPos[0] > objects[4].X and mPos[0] < objects[4].X+objects[4].width and mPos[1] > objects[4].Y and mPos[1] < objects[4].Y+objects[4].height:
            objects[5].speedX = 14
            objects[4].speedX = -14
            objects[0].speedY = 10
            playing = True
            mPos = (0, 0)

    for back in backgrounds: #moving+drawing backgrounds
        back.move()
        back.draw(win)

    print pygame.mixer.music.get_pos()
    
    if pygame.mixer.music.get_pos() >= 20000 and mainSnd == False: #controlling music
        pygame.mixer.music.load(path+"Sounds/Main.ogg")
        pygame.mixer.music.play()
        mainSnd = True

    if pygame.mixer.music.get_pos() == -1:
        pygame.mixer.music.play()

    if frame%30 == 0 and playing == True: #Creating asteroids
        if asteroidHit < 10:
            objects.append(asteroid())

    if frame%60 == 0:
        if asteroidHit > 5:
            if alien1Hit < 10:
                objects.append(alien1()) #Creating green aliens
            if alien1Hit > 5:
                if alien2Hit < 10:
                    objects.append(alien2()) #Creating red aliens
            if alien2Hit > 5:
                if alien3Hit < 5:
                    objects.append(alien3()) #Creating blue aliens

    if frame%120 == 0 and playing == True:
        if random.randint(0, 1) == 1:
            objects.append(healthy()) #Creating the health pickups
            
    #Getting Input and setting rocket speeds
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                objects[0].speedX = -10
            if event.key == K_UP:
                objects[0].speedY = -10
            if event.key == K_RIGHT:
                objects[0].speedX = 10
            if event.key == K_DOWN:
                objects[0].speedY = 10

            if event.key == K_SPACE:
                shoot = True

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == KEYUP:
            if event.key == K_LEFT:
                objects[0].speedX = 0
            elif event.key == K_RIGHT:
                objects[0].speedX = 0
            elif event.key == K_DOWN:
                objects[0].speedY = 0
            elif event.key == K_UP:
                objects[0].speedY = 0

            if event.key == K_SPACE:
                shoot = False

        if event.type == MOUSEBUTTONDOWN:
            mPos = pygame.mouse.get_pos()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if shoot == True: #If the spacebar is pressed
        if objects[0].canShoot == True: #If the rocket is allowed to shoot, create a laser
            laserList.append(objects[0].shoot())
            objects[0].laserTimer = frame
            snd_laser.play(0)

    if frame - objects[0].laserTimer == laserWait:
        objects[0].canShoot = True

    ## Collisions with the rocket
    for b in objects:
        if abs(b.X - objects[0].X) < 80 and abs(b.Y - objects[0].Y) < 80:
            if collision(objects[0], b):
                if b.name == "asteroid":
                    health -= 25
                    objects.append(explosion(b.X, b.Y, 0))
                    snd_explosion.play()
                    b.jump()

                if b.name == "alien1":
                    health -= 40
                    objects.append(explosion(b.X, b.Y, 0))
                    snd_explosion.play()
                    b.jump()

                if b.name == "alien2":
                    health -= 50
                    objects.append(explosion(b.X, b.Y, 0))
                    snd_explosion.play()
                    b.jump()

                if b.name == "alien3":
                    health -= 60
                    objects.append(explosion(b.X, b.Y, 0))
                    snd_explosion.play()
                    b.jump()

                if b.name == "bomb":
                    health -= 95
                    objects.append(explosion(b.X, b.Y, 1))
                    snd_explosion.play()
                    b.out = True

                if b.name == "health":
                    health = 100
                    score += 100
                    b.jump()
                    snd_health.play()

    ## Collisions with lasers
    for a in laserList:
        for b in objects:
            if abs(a.X - b.X) < 60 and abs(a.X - b.X) < 60:
                if collision(a, b):
                    if  b.name == "asteroid":
                        a.out = True
                        score += 10
                        asteroidHit += 1
                        objects.append(explosion(b.X, b.Y, 0))
                        snd_explosion.play()
                        b.jump()

                    if  b.name == "alien1":
                        a.out = True
                        score += 10
                        alien1Hit += 1
                        objects.append(explosion(b.X, b.Y, 0))
                        snd_explosion.play()
                        b.jump()

                    if  b.name == "alien2":
                        a.out = True
                        score += 25
                        alien2Hit += 1
                        snd_explosion.play()
                        if b.health == 1:
                            objects.append(explosion(b.X, b.Y, 0))
                            b.__init__()
                        else:
                            objects.append(explosion(b.X, b.Y, 1))
                            b.health = 1

                    if  b.name == "alien3":
                        a.out = True
                        score += 50
                        alien3Hit += 1
                        objects.append(explosion(b.X, b.Y, 0))
                        snd_explosion.play()
                        b.jump()

                    if  b.name == "bomb":
                        a.out = True
                        b.out = True
                        objects.append(explosion(b.X, b.Y, 1))
                        snd_explosion.play()

    for obj in objects:
        obj.move() ## Moving all objects
        if obj.out == True:
            objects.remove(obj)

    ## The following draw commands are in a specific order so that things get drawn in the proper order.
    ## First the objects (except for the lasers), then the text, then the buttons, then the status panel, and then the rocket

    for i in objects:
        i.draw(win)

    if playing == False:
        win.blit(fnt_main.render("Space Wars", True, (255, 219, 0)), (100, 48))
        objects[4].draw(win)
        objects[5].draw(win)
    
    if menuFrame < 60:
        win.blit(fnt_main.render("Space Wars", True, (255, 219, 0)), (100, 48-7*menuFrame))
        
    ## Moving all the lasers and drawing them to the screen
    for obj in laserList:
        obj.move()
        obj.draw(win)
        if obj.out == True:
            laserList.remove(obj)

    win.blit(images[10], (0, 404)) #Drawing the score panel
    win.blit(fnt_score.render(str(score), True, (255, 219, 0)), (235, 415)) #score counter

    if health >= 0: #draw the healthbar
        healthbar = pygame.Rect(12, 449, (health*126)/100.0, 10)
        RED = int(255 - 2.5*health)
        GREEN = int(2.5*health)
        BLUE = 0
        pygame.draw.rect(win, (RED, GREEN, 0), healthbar, 0)

    if health <= 0:
        playing = False

    ## Drawing the rocket last so it sits on top of everything
    objects[0].draw(win)

    #Waiting, counting 
    pygame.time.wait(15)
    frame += 1
    menuFrame += 1
    
    pygame.display.flip() ## Updating the screen

        
    
