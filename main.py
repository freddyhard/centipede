#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

import pygame, sys, glob, os
import math
from random import randint

from mushrooms import Mushroom
from snake import Snake
from lasercanon import LaserCanon
from plopper import Plopper
from spider import Spider
from info import Info

from functions import placeEmpty, removeDestroyed, panelUpdate, removeElementSequence


#-------------------------------------------------------------------------------
#                                 GAME PARAMETERS
#-------------------------------------------------------------------------------
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 576
DISPLAY_PANEL = 36
FPS = 60
MUSHROOM_MINIMUM = 20
MAX_SPIDERS = 1
MAX_PLOPPERS = 3
#-------------------------------------------------------------------------------
#                                   FUNCTIONS
#-------------------------------------------------------------------------------

def updateHiScore():
    global HIGH_SCORE
    
    hiScoreFile = open('hiscore', 'w')
    hiScoreFile.write(str(HIGH_SCORE))
    hiScoreFile.close()



def moveEverything():
    global spiderTimer, ploppers, snakes, spiders, gamePlaying
    
    if gamePlaying:
        player.move(SCREEN_WIDTH, SCREEN_HEIGHT, mushrooms, snakes, ploppers, spiders)
    
    for f in range(len(snakes)):
        snakes[f].move(SCREEN_WIDTH, SCREEN_HEIGHT, mushrooms, snakes)
    
    for f in range(len(ploppers)):
        ploppers[f].move(player.x, player.y, mushrooms, createMushrooms)
    
    for f in range(len(spiders)):
        spiders[f].move(player)
        # only set timer when a spider is shot as to runs away
        if spiders[f].shot:
            spiderTimer = FPS * 3



def drawSprites():
    global mushrooms, ploppers, snakes, spiders, gamePaused, gamePlaying
    
    for f in range(len(mushrooms)):
        mushrooms[f].draw(window)
    
    for f in range(len(ploppers)):
        ploppers[f].draw(window)
    
    if gamePlaying:
        player.draw(window)      
    
    for f in range(len(snakes)):
        snakes[f].draw(window)
    
    for f in range(len(spiders)):
        spiders[f].draw(window, fontSmaller)
    
    if gamePaused:
        gamePaused = Info(130, 280, pygame.image.load(os.path.join("centipede", "paused.png")))
        gamePaused.draw(window)




def pauseExitCheck():
    global gamePaused, gamePlaying
    
    for gameEvent in pygame.event.get():
        if (gameEvent.type == pygame.QUIT):
            sys.exit()
        if (gameEvent.type == pygame.KEYDOWN):
            # the gameOver is an attempt to make the player play again. when they press ESC to quit at the game over
            # display then they might continue into another game. 
            if (gameEvent.key == pygame.K_ESCAPE):
                sys.exit()
            # PAUSE    
            if (gamePlaying and gameEvent.key == pygame.K_PAUSE):
                gamePaused = not gamePaused



def demoPlay(player):
    global gamePlaying, plopperTimer, createMushrooms, spiderTimer, FPS, spiders, ploppers, mushrooms, snakes
    
    # set up a temporary spot for the spider while running a demo of the game
    player.x = SCREEN_WIDTH / 2
    player.y = SCREEN_HEIGHT - 24
    
    plopperTimer = 60
    spiderTimer = 1000
    createMushrooms = False
    
    actionDemo = True
    displayTimer = 1
    
    
    mainInfoSprites = glob.glob(os.path.join("centipede", "info_*.png"))
    functionKeys = glob.glob(os.path.join("centipede", "info_text_*.png"))
    gameInfo = []
    keysInfo = []
    for f in range(len(mainInfoSprites)):
        sprite = pygame.image.load(mainInfoSprites[f]).convert_alpha()
        gameInfo.append(Info(130, 350 - 70 * f, sprite))
    
    for f in range(len(functionKeys)):
        sprite = pygame.image.load(functionKeys[f]).convert_alpha()
        keysInfo.append(Info(130,455 + f * 40, sprite))
    
    while True:
        # check if player wants to quit game
        pauseExitCheck()
        
        # control the game play speed
        gameTimer.tick(FPS)
        
        # initialise game when player presses 'p'
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_p]:
            startMushrooms()
            gamePlaying = True
            # clear off any snakes or spiders for game start
            spiders = removeElementSequence(spiders, 0, len(spiders))
            snakes = removeElementSequence(snakes, 0 , len(snakes))
            
            # re-initialise the player. last argument True, because the game is over
            player.reinit(SCREEN_WIDTH / 2, SCREEN_HEIGHT, True)
            return
        
        displayTimer -= 1
        if displayTimer == 0:
            displayTimer = 20 * FPS
            # just toggle between instructions display or game demonstration
            actionDemo = not actionDemo
            
            if actionDemo:
                # initialise objects for the screen
                startMushrooms()
                createSnakes()
                backgroundColour = (randint(50, 115), randint(50, 115), randint(50, 175))
            else:
                x_counter = 150
                flashCounter = 0
                # clear out the arrays
                spiders = removeElementSequence(spiders, 0, len(spiders))
                snakes = removeElementSequence(snakes, 0 , len(snakes))
                backgroundColour = (randint(20, 60), randint(20, 60), randint(20, 100))
                
        
        if actionDemo:
            # create spider
            if len(spiders) < 1 and randint(0, 100) == 0: 
                spiders.append(Spider(SCREEN_WIDTH, SCREEN_HEIGHT, 0))
                
            # create plopper
            if randint(0, 90) == 0 and len(ploppers) < MAX_PLOPPERS:
                ploppers.append(Plopper(SCREEN_WIDTH, SCREEN_HEIGHT))
            
            window.fill(backgroundColour)
            
            # call methods to move and draw objects
            moveEverything()
            drawSprites()
            
        else:
            window.fill(backgroundColour)
            
            # else display the instructions
            if x_counter > 0:
                x_counter -= 1
            else:
                # flash timer for 'P' start game to catch players eye
                flashCounter = (flashCounter + 1) % FPS
                # display function keys
                for f in range(len(keysInfo)):
                    if f > 0 or flashCounter < FPS / 2:
                        keysInfo[f].draw(window)
            
            for f in range(len(gameInfo)):
                x_offset = x_counter - f * 18
                if x_offset < 0:
                    x_offset = 0
                gameInfo[f].draw(window, math.pow(x_offset, 2) / 3.0)
            
        
        panelUpdate(window, SCREEN_WIDTH, SCREEN_HEIGHT, DISPLAY_PANEL, player, HIGH_SCORE)
        pygame.display.flip()

    

def createSnakes():
    global backgroundColour
    
    minSnakeSize = 4
    #maxSnakeSize = 20
    
    # the lasercanon class removes all snakes 10 frames before the player gets reinitialised after being killed
    # this if statement will only increase the level when the player has not been killed
    if player.playerKilled:
        player.playerKilled = False
    else:
        backgroundColour = (0, randint(50, 115), randint(50, 175))
        player.level += 1
    
    snakeParts = (4, 8, 16, 24, 34)
    snakeCount = ((1, 1), (1, 2), (2, 4), (3, 5))
    # 'i' will be used to pull out numbers from the above 2 tuples
    i = (player.level - 1) / 4
    # limit i to 3, because an index out of range will be generated otherwise
    if i > 3:
        i = 3
    # number of snake parts to use
    snakePartsTotal = randint(snakeParts[i], snakeParts[i + 1])
    # number of snakes
    snakeCountTotal = randint(snakeCount[i][0], snakeCount[i][1])
    
    # initialise the snake array to build with the minimum size
    snakesToBuild = []
    for f in range(snakeCountTotal):
        snakesToBuild.append(minSnakeSize)
    
    # see how many body parts are left over?
    spareParts = snakePartsTotal - (snakeCountTotal * minSnakeSize)
    # now add these parts to the initial snakes to be built
    iterator = 0
    while spareParts > 0:
        if len(snakesToBuild) == 1:
            snakesToBuild[0] += spareParts
            break
        addParts = randint(0, spareParts)
        snakesToBuild[iterator] += addParts
        spareParts -= addParts
        # keep cycling through the snakes until all spare parts are used up
        iterator = (iterator + 1) % len(snakesToBuild)
    
    
    for f in range(len(snakesToBuild)):
        searching = True
        
        while searching:
            rand_x = randint(0, (SCREEN_WIDTH / 24) - 1) * 24
            rand_y = randint(0 + f * 32, 32 + f * 32)#(SCREEN_HEIGHT / 48) - 7) * 48
            if placeEmpty(mushrooms, rand_x, rand_y) and placeEmpty(snakes, rand_x, rand_y):
                # snakesToBuild[f] -1 to allow for head as part of the body count
                snakes.append(Snake(rand_x, rand_y, 0, snakesToBuild[f] - 1, player.level) )
                searching = False



def startMushrooms():
    global mushrooms, ploppers
    
    # remove any existing ploppers
    if len(ploppers) > 0:
        ploppers = removeElementSequence(ploppers, 0, len(ploppers))
    
    # remove any existing mushrooms
    if len(mushrooms) > 0:
        mushrooms = removeElementSequence(mushrooms, 0, len(mushrooms))
    
    for f in range(MUSHROOM_MINIMUM):
        searching = True
        while searching:
            rand_x = randint(0, (SCREEN_WIDTH / 24) - 1) * 24
            rand_y = randint(0, (SCREEN_HEIGHT / 24) - 2) * 24
            if placeEmpty(mushrooms, rand_x, rand_y):
                mushrooms.append(Mushroom(rand_x, rand_y))
                searching = False
#-------------------------------------------------------------------------------
#                                 INITIALISE GAME
#-------------------------------------------------------------------------------
pygame.mixer.pre_init(44100, -16, 16, 2048)
pygame.init()

pygame.display.set_icon(pygame.image.load(os.path.join("centipede", "icon.png")))
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + DISPLAY_PANEL))
pygame.display.set_caption("Centipede (1.0.1)")



pygame.mouse.set_visible(False)

gameOver = Info(130, 280, pygame.image.load(os.path.join("centipede", "backtowork.png"))) 

# font for the display panel
fontSmaller = pygame.font.SysFont('arial black', 20, False, False)

gameTimer = pygame.time.Clock()
gamePaused = False
gamePlaying = False

gameOverDisplayTimer = 0


HIGH_SCORE = 0
try:
    hiScoreFile = open('hiscore', 'r')
    HIGH_SCORE = int(hiScoreFile.readline())
    hiScoreFile.close()
except IOError:
    hiScoreFile = open('hiscore', 'w')
    hiScoreFile.write("0")
    hiScoreFile.close()




mushrooms = []
snakes = []
ploppers = []
spiders = []
backgroundColour = (0,0,0)


player = LaserCanon(SCREEN_WIDTH / 2, SCREEN_HEIGHT)

#----------------------------------  GAME LOOP  ----------------------------------
while (True):
    
    gameTimer.tick(FPS)
    
    if player.score > HIGH_SCORE:
        HIGH_SCORE = player.score
    
    # check to see if player wants to quit game. gamePlaying will allow the player to PAUSE the game only if true
    pauseExitCheck()
    
    if not gamePlaying and gameOverDisplayTimer == 0:
        # set this timer for the end of the next game
        gameOverDisplayTimer = 4 * FPS
        # this will go into a continuous loop until the player decides to start a game
        # passing player so this method can set the player back up with some lives
        demoPlay(player)
    
        
    window.fill(backgroundColour)
    
    # 'player.dyingTimer' test just lets the player see the game for 2 seconds after their last life has been deleted
    if player.lives > 0 or player.dyingTimer > 0:
        if len(snakes) == 0 and player.dyingTimer == 0:
            createSnakes()
        
        # let everything move if not paused
        if not gamePaused:
            
            # decrement timers
            if plopperTimer > 0:
                plopperTimer -= 1
              
            if spiderTimer > 0:
                spiderTimer -= 1
            
            # create spider
            if (len(spiders) < MAX_SPIDERS + player.level / 15 and randint(0, 100) == 0 and 
                        player.dyingTimer == 0 and spiderTimer == 0): 
                spiders.append(Spider(SCREEN_WIDTH, SCREEN_HEIGHT, player.level))
                
            # create plopper
            if randint(0, 90) == 0 and plopperTimer == 0 and len(ploppers) < MAX_PLOPPERS:
                ploppers.append(Plopper(SCREEN_WIDTH, SCREEN_HEIGHT))
                plopperTimer = 90
            
            
            # move player, snakes, ploppers and spiders
            moveEverything()
            
            # removed destroyed elements in the arrays below
            # lasers are removed within the laserCanon class in the draw method
            mushrooms = removeDestroyed(mushrooms)
            snakes = removeDestroyed(snakes)
            ploppers = removeDestroyed(ploppers)
            spiders = removeDestroyed(spiders)
            # go the mushroom plopper!
            createMushrooms = len(mushrooms) < MUSHROOM_MINIMUM
            
        # draw the sprite's
        drawSprites()
        
    else:
        # check to see if player wants to quit game. gamePlaying will allow the player to PAUSE the game only if it is playing
        pauseExitCheck()
        # displaying game over
        gameOverDisplayTimer -= 1
        gamePlaying = False
        
        updateHiScore()
        
        gameOver.draw(window)
        
        
    # the score will be with you - always
    panelUpdate(window, SCREEN_WIDTH, SCREEN_HEIGHT, DISPLAY_PANEL, player, HIGH_SCORE)
    
    pygame.display.flip()
    
    
