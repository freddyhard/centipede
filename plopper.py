import pygame, glob, os

from random import randint

from functions import pointDirection, rotate, matchCentre, placeEmpty

from mushrooms import Mushroom

class Plopper():
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.spriteIndex = glob.glob(os.path.join("centipede", "plopper_*.png"))
        self.spriteEyeStart = pygame.image.load(os.path.join("centipede", "eye.png")).convert_alpha()
        
        self.x = randint(0, SCREEN_WIDTH - 24)
        self.y = 0
        
        self.sprite = pygame.image.load(self.spriteIndex[0]).convert_alpha()
        rect = self.sprite.get_rect()
        self.width = rect.width
        self.height = rect.height
        
        self.OFF_SCREEN = SCREEN_HEIGHT - self.height
         
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.spriteCounter = 0
        self.imageIndex = 0
        
        self.soundPlop = pygame.mixer.Sound(os.path.join("sounds", "mushroomPop.wav"))
        
        self.destroyed = False
        
    def move(self, playerX, playerY, mushrooms, createMushroom):
        # do the watching eye
        eyeDirection = pointDirection(self.x, self.y, playerX, playerY)
        self.spriteEye = rotate(self.spriteEyeStart, eyeDirection).convert_alpha()
        self.spriteEyeCentre = matchCentre(self.spriteEyeStart, self.spriteEye)
        
        # just moves straight down the screen
        self.y += 4        
        if self.y > self.OFF_SCREEN:
            self.destroyed = True
        
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        
        if (createMushroom and randint(0, 100) == 0 and placeEmpty(mushrooms, self.x, self.y)
                                                 and self.y < self.OFF_SCREEN - self.height):
            self.soundPlop.play()
            mushrooms.append(Mushroom(self.x, self.y))
        
        # update the body sprite
        self.spriteCounter += 1
        if self.spriteCounter > 2:
            self.spriteCounter = 0
            self.imageIndex = (self.imageIndex + 1) % len(self.spriteIndex)
            self.sprite = pygame.image.load(self.spriteIndex[self.imageIndex]).convert_alpha()
        
                
        
    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))
        """
        fontArial = pygame.font.SysFont('arial', 18, True, False)
        test = fontArial.render(str(self.eyeDirection), 1, (0,0,0))
        #test = fontArial.render(str(self.string), 1, (0,0,0))
        window.blit(test, (self.x, self.y - 24))"""
        
        window.blit(self.spriteEye, (self.x  + self.spriteEyeCentre[0] + 7, self.y  + self.spriteEyeCentre[1] + 19))
        #window.blit(self.spriteEye, (self.x  + self.spriteEyeCentre[0] + 3, self.y  + self.spriteEyeCentre[1] + 19))
        #window.blit(self.spriteEye, (self.x  + self.spriteEyeCentre[0] + 12, self.y  + self.spriteEyeCentre[1] + 19))
        
