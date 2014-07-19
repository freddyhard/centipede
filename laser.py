import pygame, os

class Laser():    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(os.path.join("centipede", "laser.png")).convert_alpha()
        area = self.sprite.get_rect()
        self.width = area[2]
        self.height = area[3]
        self.spriteArea = pygame.Rect(x, y, self.width, self.height)
        self.destroyed = False
            
        soundLaser = pygame.mixer.Sound(os.path.join("sounds", "laser.wav"))
        #soundLaser = pygame.mixer.Sound("sounds\mushroomPop.wav")
        soundLaser.play()
        self.soundLaserHit = pygame.mixer.Sound(os.path.join("sounds", "laserHit.wav"))
        self.soundLaserHit.set_volume(0.5)
    

    def move(self, mushrooms, snakes, ploppers, spiders, playerScore):
        self.y -= 14
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
                
        finished = False
        for f in range(len(snakes)):
            if finished:
                break
            if self.spriteArea.colliderect(snakes[f].spriteArea):
                # headShot method will move snake head to bodyPart[0] position and delete 1 body part
                snakes[f].headShot()
                playerScore += 15
                self.destroyed = True
                self.soundLaserHit.play()
                break
            for count in range(len(snakes[f].body)):
                if self.spriteArea.colliderect(snakes[f].body[count].spriteArea):
                    # need to create method to remove body and deal with separate bits if any
                    snakes[f].bodyShot(mushrooms, snakes, count)
                    playerScore += 5
                    self.destroyed = True
                    self.soundLaserHit.play()
                    # break out of the snake loop as well
                    finished = True
                    break
        
        if not self.destroyed:
            for f in range(len(ploppers)):
                if self.spriteArea.colliderect(ploppers[f].spriteArea):
                    playerScore += 3
                    self.destroyed = True
                    ploppers[f].destroyed = True
                    self.soundLaserHit.play()
                    break
        
        if not self.destroyed:
            for f in range(len(spiders)):
                if self.spriteArea.colliderect(spiders[f].spriteArea):
                    playerScore += 25
                    self.destroyed = True
                    spiders[f].destroyed = True
                    spiders[f].shot = True
                    self.soundLaserHit.play()
                    break
        
        if not self.destroyed:
            for f in range(len(mushrooms)):
                if self.spriteArea.colliderect(mushrooms[f].spriteArea):
                    mushrooms[f].damageLevel -= 1
                    playerScore += 1
                    if mushrooms[f].damageLevel < 0:
                        mushrooms[f].destroyed = True
                    self.destroyed = True
                    self.soundLaserHit.play()
                    # break to avoid hitting 2 mushrooms at once and no point in checking the rest anyway
                    break
        return playerScore
                

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))
        #pygame.draw.rect(window, (0,100,205), (self.x, self.y, self.width, self.height), 1)
