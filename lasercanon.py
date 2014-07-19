import pygame, glob, os

from laser import Laser

from functions import limits, removeDestroyed, removeElement



class LaserCanon():    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.lasers = []
        self.fireTimer = 0
        
        self.spriteSplat = glob.glob(os.path.join("centipede", "splat_*.png"))
        self.splatTimer = 0
        
        self.sprite = pygame.image.load(os.path.join("centipede", "lasercanon.png")).convert_alpha()
        self.mask = pygame.mask.from_surface(self.sprite)
        
        self.width = self.sprite.get_rect().width
        self.height = self.sprite.get_rect().height
        self.spriteArea = pygame.Rect(x, y, self.width, self.height)
        
        self.score = 0
        # the createSnake() will +1 to level at the very start
        self.level = 0
        self.lives = 3
        self.dyingTimer = 0
        self.playerKilled = False
        self.soundDead = pygame.mixer.Sound(os.path.join("sounds", "die.wav"))


    
    def reinit(self, x, y, gameOver):
        self.sprite = pygame.image.load(os.path.join("centipede", "lasercanon.png")).convert_alpha()
        self.x = x
        self.y = y
        if gameOver:
            self.lives = 3
            self.level = 0
            self.score = 0
            self.playerKilled = False
            
     
        
    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, mushrooms, snakes, ploppers, spiders):
        # assume the player is not pressing any keys
        add_x = 0
        add_y = 0
        
        # laser timed fire control
        if self.fireTimer > 0:
            self.fireTimer -= 1
        #-----------------------------------------------------------------------------------------------
        #                                        PLAYER  DYING
        #-----------------------------------------------------------------------------------------------
        # this lets the player's sprite animate the dying sequence and lets the player see he got killed
        if self.dyingTimer > 0:
            self.dyingTimer -= 1
            
            # update dying sprite
            self.splatTimer += 1
            if self.splatTimer < 18:
                self.sprite = pygame.image.load(self.spriteSplat[int(self.splatTimer / 3)])
            
            if self.dyingTimer == 10:
                for f in range(len(snakes)):
                    # this will remove all snakes from the screen
                    snakes[f].destroyed = True
                for f in range(len(ploppers)):
                    # this will remove all ploppers from the screen
                    ploppers[f].destroyed = True
            
            if self.dyingTimer == 0:
                self.splatTimer = 0
                self.playerKilled = True
                # last argument is False because we know the game is NOT over
                self.reinit(SCREEN_WIDTH / 2, SCREEN_HEIGHT, False)
        else:
        #-----------------------------------------------------------------------------------------------
        #                                        PLAYER  ALIVE
        #-----------------------------------------------------------------------------------------------
        # the player is alive so check the keyboard
            userInput = pygame.key.get_pressed()
            if userInput[pygame.K_LEFT]:
                add_x = -4
            if userInput[pygame.K_RIGHT]:
                add_x = 4
            if userInput[pygame.K_UP]:
                add_y = -4
            if userInput[pygame.K_DOWN]:
                add_y = 4
            # fire a laser
            if userInput[pygame.K_SPACE] and len(self.lasers) < 3 and self.fireTimer == 0:
                self.lasers.append(Laser(self.x + 6, self.y - 24))
                self.fireTimer = 10
            #    ------------------------------------------------------------------------
            #                              SEE IF THE PLAYER DIES
            #    ------------------------------------------------------------------------
            finished = False
            for f in range(len(snakes)):
                # finished is a second break to get out of the first for loop after 'break'ing from the second
                # snake body loop
                if finished:
                    break
                # do a rectangle collision first
                if self.spriteArea.colliderect(snakes[f].spriteArea):
                    # now do a bitmap collision
                    x_offset = self.spriteArea[0] - snakes[f].spriteArea[0]
                    y_offset = self.spriteArea[1] - snakes[f].spriteArea[1]
                    if snakes[f].mask.overlap(self.mask, (x_offset, y_offset)):
                        self.dyingTimer = 120
                        break
                
                for t in range(len(snakes[f].body)):
                    # do a rectangle collision first
                    if self.spriteArea.colliderect(snakes[f].body[t].spriteArea):
                        # now do a bitmap collision
                        x_offset = self.spriteArea[0] - snakes[f].body[t].spriteArea[0]
                        y_offset = self.spriteArea[1] - snakes[f].body[t].spriteArea[1]
                        if snakes[f].body[t].mask.overlap(self.mask, (x_offset, y_offset)):
                            self.dyingTimer = 120
                            finished = True
                            break
            
            if self.dyingTimer == 0:
                for f in range(len(ploppers)):
                    if self.spriteArea.colliderect(ploppers[f].spriteArea):
                        self.dyingTimer = 120
                        break
            
            if self.dyingTimer == 0:
                for f in range(len(spiders)):
                    if self.spriteArea.colliderect(spiders[f].spriteArea):
                        x_offset = self.spriteArea[0] - spiders[f].spriteArea[0]
                        y_offset = self.spriteArea[1] - spiders[f].spriteArea[1]
                        if spiders[f].mask.overlap(self.mask, (x_offset, y_offset)):
                            self.dyingTimer = 120
                            break
            #    ---------------------------  SEE IF THE PLAYER DIES FINISH  -----------------------------
                        
            if self.dyingTimer > 0:
                # i subtract the life here so when the player looks at his lives he will see immediately how many remain
                self.lives -= 1
                # play the dead sound?
                self.soundDead.play()
                # send any spiders off the screen now by passing True into decisionMaker()
                for f in range(len(spiders)):
                    spiders[f].decisionMaker(True)
            else:
            # collision detection with mushrooms, but only because the player is alive
                for f in range(len(mushrooms)):
                    if mushrooms[f].spriteArea.colliderect(pygame.Rect(self.x + add_x, self.y + add_y,
                                                                       self.width, self.height)):
                        # rectangle collision found, now test a bitmap collision
                        x_offset = int(self.x + add_x) - mushrooms[f].x
                        y_offset = int(self.y + add_y) - mushrooms[f].y
                        if mushrooms[f].mask.overlap(self.mask, (x_offset, y_offset)):
                            add_x = 0
                            add_y = 0
        
        # while moving lasers check for collisions as well
        for f in range(len(self.lasers)):
            self.score = self.lasers[f].move(mushrooms, snakes, ploppers, spiders, self.score)
        
        # remove lasers that move off the screen
        for f in range(len(self.lasers)):
            if self.lasers[f].y < -self.lasers[f].height:
                self.lasers = removeElement(self.lasers, f)
                # we break because only 1 can move into -height(i.e. -24) at any one time
                break
        
        # move the player
        self.x += add_x
        self.y += add_y
        # stop the player from moving outside of his play area
        self.x = limits(self.x, self.width, SCREEN_WIDTH, self.width)
        self.y = limits(self.y, int(SCREEN_HEIGHT * 0.6), SCREEN_HEIGHT, self.height)
        # update the collision rectangle for the player
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        

        

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))
        #pygame.draw.rect(window, (255,0,0), (self.x, self.y, 24, 24), 1)
        for f in range(len(self.lasers)):
            self.lasers[f].draw(window)
        
        """ testing only stuff
        fontArial = pygame.font.SysFont('arial', 18, True, False)
        test = fontArial.render(str(self.x) + "," + str(self.y), 1, (0,0,0))
        window.blit(test, (self.x, self.y - 24))"""
        
        # removing lasers after they have been drawn - so the player gets to see the laser when it is fired
        # at point blank range
        self.lasers = removeDestroyed(self.lasers)













        
        
