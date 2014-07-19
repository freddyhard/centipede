import pygame, copy, os
from random import random

from snakebody import SnakeBody
from mushrooms import Mushroom

from functions import moveCentre, rotate, removeElement, removeElementSequence


class Snake():    
    def __init__(self, x, y, direction, bodyParts, playerLevel):
        self.spriteHeadStart = pygame.image.load(os.path.join("centipede", "snakeHead.png")).convert_alpha()
        self.spriteStartRECT = self.spriteHeadStart.get_rect()
        
        self.x = x# - self.spriteStartRECT.width / 2
        self.y = y# - self.spriteStartRECT.height / 2
        
        self.NEW_X = self.x
        self.NEW_Y = self.y
        
        self.playerLevel = playerLevel
        
        # will have to factor in player level!!!!
        if bodyParts + 1 < 4:
            self.snakeSpeed = 3 + (playerLevel > 4) + (playerLevel > 9) + (playerLevel > 14)
        elif bodyParts + 1 < 8:
            self.snakeSpeed = 2 + (playerLevel > 4) + (playerLevel > 9) + (playerLevel > 14)
        elif bodyParts + 1 < 10:
            self.snakeSpeed = 2 + (playerLevel > 9) + (playerLevel > 14)
        elif bodyParts + 1 < 14:
            self.snakeSpeed = 2 + (playerLevel > 9)
        else:
            self.snakeSpeed = 2
        
        
        #self.snakeSpeed = 2#speed
        self.snakeDirection = direction
        self.destroyed = False
        
        self.weaveAngle = random() * 20 - 10
        self.weaving = -1.3333
        
        #self.spriteSnakeHead = rotate(self.spriteHeadStart, self.snakeDirection + self.weaveAngle)
        #self.spriteCentre = moveCentre(self.spriteHeadStart, self.spriteSnakeHead, 3, self.snakeDirection + self.weaveAngle)
        
        self.spriteArea = pygame.Rect(x, y, self.spriteStartRECT.width, self.spriteStartRECT.height)
        
        self.turnTimer = 0
        self.hitBottomEdge = False
        
        # build the body of the centipede
        self.body = []
        bodySubImage = 0
        # number of positions to remember per snake body part
        self.positionCount = int(self.spriteStartRECT.width / self.snakeSpeed) + 1
        
        for f in range(bodyParts):
            self.body.append(SnakeBody(x, y, bodySubImage))# - 24 * (f + 1)
            bodySubImage = (bodySubImage + 1) % 2
        
        # set up array to hold positions for all the body parts
        self.positions = [[0 for col in range(3)] for row in range(self.positionCount * (bodyParts + 1))]
        
        # initialise all positions to match snake head
        for f in range(len(self.positions)):
            self.positions[f][0] = self.x
            self.positions[f][1] = self.y
            #self.positions[f][2] = 0

    
    
    def headShot(self):
        if len(self.body) == 0:
            self.destroyed = True
        else:
            self.body = removeElement(self.body, 0)
            self.positions = removeElementSequence(self.positions, 0, self.positionCount)
            self.NEW_X = self.positions[0][0]
            self.NEW_Y = self.positions[0][1]
            #self.snakeDirection = self.positions[0][2]
    
    
            
    def bodyShot(self, mushrooms, snakes, bodyIndex):
        # put in a mushroom anyway
        mushrooms.append(Mushroom(self.body[bodyIndex].x, self.body[bodyIndex].y))
        
        if bodyIndex == len(self.body) - 1:
            # if it is the last body part just remove it
            self.body = removeElement(self.body, bodyIndex)
        else:
            # a double check to make sure the new snake does not start in a downward direction
            newDirection = self.body[bodyIndex + 1].direction
            if newDirection == 270 or newDirection == 90:
                if self.body[bodyIndex + 1].x > 100:
                    newDirection = 180
                else:
                    newDirection = 0    
            # we need to create a new snake with the remaining body parts, with the first body part forming the new head
            snakes.append(Snake(self.body[bodyIndex + 1].x, self.body[bodyIndex + 1].y, newDirection, 
                                (len(self.body) - (bodyIndex + 2)), self.playerLevel))
            
            # make a COPY of the positions array of the snake that got shot
            tempPositions = copy.deepcopy(self.positions)
            
            # trim off the appropriate front amount of the positions array, before writing it to the new snake being created
            snakes[len(snakes) - 1].positions = removeElementSequence(tempPositions, 0, self.positionCount * (bodyIndex + 2))
            
            # removing trailing body parts of the snake that got shot
            self.body =  removeElementSequence(self.body, bodyIndex, len(self.body) - bodyIndex)
            
            # remove excess part of the array that holds the positions for the snake body that just got shot 
            self.positions = removeElementSequence(self.positions, (bodyIndex + 1) * self.positionCount,
                                                    len(self.positions) - (bodyIndex + 1) * self.positionCount)    
            
    
    
    def scanAhead(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self.hitBottomEdge and self.NEW_Y < SCREEN_HEIGHT / 2:
            self.hitBottomEdge = False
        
        # reset these values
        self.NEW_X = self.x
        self.NEW_Y = self.y
        
        if self.snakeDirection == 0:
            self.snakeDirection = 270 - 180 * self.hitBottomEdge
            self.snakeTimedTurn = 180
            self.turnTimer = self.positionCount
        elif self.snakeDirection == 180:
            self.snakeDirection = 270 - 180 * self.hitBottomEdge
            self.snakeTimedTurn = 0
            self.turnTimer = self.positionCount            
        
    
    
    def screenEdge(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self.hitBottomEdge and self.NEW_Y < SCREEN_HEIGHT / 2:
            self.hitBottomEdge = False
                    
        if self.NEW_X > SCREEN_WIDTH - self.spriteCentre.width:
            self.snakeDirection = 270 - 180 * self.hitBottomEdge
            self.snakeTimedTurn = 180
            self.turnTimer = self.positionCount
            self.NEW_X = SCREEN_WIDTH - (self.spriteCentre.width + 6)
        elif self.NEW_X < 0:
            self.snakeDirection = 270 - 180 * self.hitBottomEdge
            self.snakeTimedTurn = 0
            self.turnTimer = self.positionCount
            self.NEW_X = 6    
        elif self.NEW_Y > SCREEN_HEIGHT - self.spriteCentre.height:
            self.hitBottomEdge = True
            self.snakeDirection = self.snakeTimedTurn
            self.turnTimer = 0
            self.NEW_Y = SCREEN_HEIGHT - (self.spriteCentre.height + 2)


    
    def updatePositionList(self, x_pos, y_pos, direction):
        # for loop moves all rows down 1 - over writing the last one
        for f in range(len(self.positions) - 1, 0, -1):
            for x in range(3):
                self.positions[f][x] = self.positions[f - 1][x]
        # now over write the first row with the current data
        self.positions[0][0] = x_pos
        self.positions[0][1] = y_pos
        self.positions[0][2] = direction

    
    
    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, mushrooms, snakes):
        oldDirection = self.snakeDirection
        
        if self.turnTimer > 0:
            self.turnTimer -= 1
            if self.turnTimer == 0:
                self.snakeDirection = self.snakeTimedTurn
        
        #---------------------  DO HEAD SHAKE FIRST  ---------------------
        self.weaveAngle += self.weaving
        if self.weaveAngle < -10 or self.weaveAngle > 10:
            self.weaving = -self.weaving
                
        #-----------------------  UPDATE SPRITE  -------------------------
        self.spriteSnakeHead = rotate(self.spriteHeadStart, self.snakeDirection + self.weaveAngle).convert_alpha()
        self.mask = pygame.mask.from_surface(self.spriteSnakeHead)
        self.spriteCentre = moveCentre(self.spriteHeadStart, self.spriteSnakeHead, 3, self.snakeDirection + self.weaveAngle)
        
        #--------------------  UPDATE NEW POSITION  ---------------------        
        if self.snakeDirection == 0:
            self.NEW_X += self.snakeSpeed
        elif self.snakeDirection == 180:
            self.NEW_X += -self.snakeSpeed
        elif self.snakeDirection == 270:
            self.NEW_Y += self.snakeSpeed
        elif self.snakeDirection == 90:
            self.NEW_Y += -self.snakeSpeed
        
        if self.turnTimer == 0:
            hitObject = False
            testArea = pygame.Rect(self.NEW_X, self.NEW_Y, self.spriteCentre.width, self.spriteCentre.height)
            for f in range(len(mushrooms)):
                if testArea.colliderect(mushrooms[f].spriteArea):
                    hitObject = True
                    break
            """
            if not hitObject:
                tempSnakes = copy.deepcopy(snakes)
                for f in range(len(snakes)):
                    if self.x == snakes[f].x and self.y == snakes[f].y:
                        tempSnakes = removeElement(tempSnakes, f)
                        break
                for f in range(len(tempSnakes)):
                    if pygame.Rect(self.NEW_X, self.NEW_Y, self.spriteCentre.width, self.spriteCentre.height
                                   ).colliderect(tempSnakes[f].spriteArea):
                        hitObject = True
                        break
            """           
            
            if hitObject:
                # this will have to do some complicated shit - or maybe not?
                self.scanAhead(SCREEN_WIDTH, SCREEN_HEIGHT)
            else:
                # if not hit a mushroom then do a screen edge test
                self.screenEdge(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.x = self.NEW_X
        self.y = self.NEW_Y
        # spriteArea will be used for collision testing
        self.spriteArea = pygame.Rect(self.x, self.y, self.spriteCentre.width, self.spriteCentre.height)
        
        # update array of positions
        self.updatePositionList(self.x, self.y, oldDirection)
        
        for f in range(len(self.body)):
            self.body[f].move(self.positions[self.positionCount * (f + 1)][0],
                              self.positions[self.positionCount  * (f + 1)][1],
                              self.positions[self.positionCount * (f + 1)][2])
        
    
    
    def draw(self, window):
        """
        fontArial = pygame.font.SysFont('arial', 18, True, False)
        test = fontArial.render(str(self.snakeSpeed), 1, (0,0,0))
        #test = fontArial.render(str(self.string), 1, (0,0,0))
        window.blit(test, (self.x, self.y - 24))
        """
        # count in reverse so snake does not go under itself when crossing itself
        for f in range(len(self.body) - 1, -1, -1):
            self.body[f].draw(window)
        # draw head last to be on top
        window.blit(self.spriteSnakeHead, (self.x + self.spriteCentre[0], self.y + self.spriteCentre[1]))
        # test collision rectangle (for visual purposes only)
        #pygame.draw.rect(window, (255,0,0), (self.x, self.y, self.spriteCentre.width, self.spriteCentre.height), 1)
        

