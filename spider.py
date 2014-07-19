import pygame, glob, math, os
from random import randint

from functions import pointDirection, pointDistance, rotate, matchCentre

class Spider():
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, playerLevel):
        self.spriteEyeStart = pygame.image.load(os.path.join("centipede", "eye.png")).convert_alpha()
        self.spriteIndex = glob.glob(os.path.join("centipede", "spider_*.png"))
        
        maskSprite = pygame.image.load(os.path.join("centipede", "spiderMask.png")).convert_alpha()
        self.mask = pygame.mask.from_surface(maskSprite)
        
        self.sprite = pygame.image.load(self.spriteIndex[0]).convert_alpha()
        rect = self.sprite.get_rect()
        self.width = rect.width
        self.height = rect.height
        
        self.spriteCounter = 0
        self.imageIndex = 0
        
        self.smartness = playerLevel
        
        if randint(0, 1) == 0:
            self.x = -self.width
        else:
            self.x = SCREEN_WIDTH
        self.y = randint(int(SCREEN_HEIGHT * 0.6), SCREEN_HEIGHT - self.height)
        
        self.spiderSpeed = 4
        
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        self.screenWidth = SCREEN_WIDTH
        self.screenHeight = SCREEN_HEIGHT
        
        # pick a place at the bottom of the screen
        self.targetX = randint(0, SCREEN_WIDTH - self.width)
        self.targetY = SCREEN_HEIGHT - self.height
        
        # setup the spider to move there
        self.setUpMovement()
        
        self.destroyed = False
        self.shot = False
        self.moving = True
        # set waitTimer to random number between 1/2 and 6 seconds
        self.waitTimer = randint(30, 360)
        
    
    
    def decisionMaker(self, getOffScreen, playerX = 0, playerY = 0):
        if self.x < -self.width or self.x > self.screenWidth:
            # the spider has moved off the screen, so remove from the array
            self.destroyed = True
            return
        
        MOVE_TO_BOTTOM = 0
        MOVE_OFF_THE_SCREEN = 1
        """ possibles (bias movement to attack player)
        - 0 set target to the bottom of the screen and set waitTimer
        - 1 set target off the screen
        - 2 set target to where the player is"""
        self.moving = True
        if getOffScreen:
            # move the spider off the screen if the player is dead
            decision = MOVE_OFF_THE_SCREEN
        else:
            # otherwise random choice, but with every 3 levels passed by player the spider will favour chasing the player
            decision = randint(0, 2 + int(self.smartness / 3))
            
        
        if decision == MOVE_TO_BOTTOM:
            self.targetX = randint(0, self.screenWidth - self.width)
            self.targetY = self.screenHeight - self.height
            # set waitTimer to random number between 1/2 and 6 seconds
            self.waitTimer = randint(30, 360)
            self.spiderSpeed = 4
        elif decision == MOVE_OFF_THE_SCREEN:
            # set waitTimer to 1 so that it is called immediately once spider reaches the target
            # there is no point in waiting while he sits off the screen somewhere
            self.waitTimer = 1
            self.spiderSpeed = randint(6, 8)
            self.targetY = randint(int(self.screenHeight * 0.6), self.screenHeight - self.height)
            if randint(0, 1) == 0:
                self.targetX = -(self.width + 10)
            else:
                self.targetX = self.screenWidth + 10
        else:# ATTACK THE PLAYER
            # set waitTimer to 1 so that it is called immediately once spider reaches the target
            # do not let the spider wait in the middle of the screen somewhere
            self.waitTimer = 1
            self.spiderSpeed = randint(4, 6)
            self.targetX = playerX
            self.targetY = playerY
        
        self.setUpMovement()
    
    
    
    def setUpMovement(self):
        self.targetDirection = pointDirection(self.x, self.y, self.targetX, self.targetY)
        # setup the movement of the spider
        self.add_x = math.cos(math.radians(self.targetDirection)) * self.spiderSpeed
        self.add_y = -math.sin(math.radians(self.targetDirection)) * self.spiderSpeed
        
    
    
        
    def move(self, player):
        if not self.moving:
            # set the animation to motionless
            self.imageIndex = 0
            
            # watch the player
            self.targetX = player.x
            self.targetY = player.y
            self.targetDirection = pointDirection(self.x, self.y, self.targetX, self.targetY)
            
            # count down the wait timer
            self.waitTimer -= 1
            if self.waitTimer == 0:
                # False is telling the spider NOT to get off the screen
                self.decisionMaker(False, player.x, player.y)
        else:
            # update sprite as the spider moves
            self.spriteCounter += 1
            if self.spriteCounter > 2:
                self.spriteCounter = 0
                self.imageIndex = (self.imageIndex + 1) % len(self.spriteIndex)
            
            # get the distance between the spider and the target point
            testDistance = pointDistance(self.x, self.y, self.targetX, self.targetY)
            # no need to do a for loop test until the spider is close enough to the target
            if testDistance < self.spiderSpeed * 2:            
                tempX = self.add_x / testDistance
                tempY = self.add_y / testDistance
                # now do a pixel by pixel test and once close enough then stop. 3.5 is close enough to stop the spider
                for f in range(int(testDistance)):
                    if math.fabs(self.x + tempX * f - self.targetX) < 3.5 and math.fabs(self.y + tempY * f - self.targetY) < 3:
                        self.add_x = tempX * f
                        self.add_y = tempY * f
                        self.moving = False
                        break
            
            self.x += self.add_x
            self.y += self.add_y
            """            
            # A FAIL SAFE CATCH FOR WHEN THE SPIDER WANDERS OFF THE SCREEN, BUT DOESN'T KNOW HE'S FUCKING LOST
            if math.fabs(self.x) > self.screenWidth * 3 or math.fabs(self.y) > self.screenHeight * 3:
                self.moving = False"""
                
        
        
        self.spriteEye = rotate(self.spriteEyeStart, self.targetDirection).convert_alpha()
        self.spriteEyeCentre = matchCentre(self.spriteEyeStart, self.spriteEye)
        
        eyeRect = self.spriteEye.get_rect() 
        self.spriteEyeSmall = pygame.transform.smoothscale(self.spriteEye, 
                                                           (eyeRect.width / 2, eyeRect.height / 2)).convert_alpha()
        
        # no convert_alpha() needed here. the self.mask is taken from another sprite in __init__
        self.sprite = pygame.image.load(self.spriteIndex[self.imageIndex]).convert_alpha()
        
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        
    
    
    
    def draw(self, window, font):
        """# testing only
        spiderText = font.render(str(self.upperRand), 1, (205,100,0))
        window.blit(spiderText, (0,0))"""
        
        # spider body
        window.blit(self.sprite, (self.x, self.y))
        # left eye
        window.blit(self.spriteEye, (self.x + self.spriteEyeCentre[0] + 13, self.y + self.spriteEyeCentre[1] + 11))
        # right eye
        window.blit(self.spriteEye, (self.x + self.spriteEyeCentre[0] + 25, self.y + self.spriteEyeCentre[1] + 11))
        # the eyes up the back
        window.blit(self.spriteEyeSmall, (self.x + self.spriteEyeCentre[0] + 10, self.y + self.spriteEyeCentre[1] + 5))
        window.blit(self.spriteEyeSmall, (self.x + self.spriteEyeCentre[0] + 17, self.y + self.spriteEyeCentre[1] + 1))
        window.blit(self.spriteEyeSmall, (self.x + self.spriteEyeCentre[0] + 25, self.y + self.spriteEyeCentre[1] + 1))
        window.blit(self.spriteEyeSmall, (self.x + self.spriteEyeCentre[0] + 32, self.y + self.spriteEyeCentre[1] + 5))
        
        
        
