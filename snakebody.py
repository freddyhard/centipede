import glob, pygame, os

from functions import rotate, matchCentre



class SnakeBody():
    def __init__(self, x, y, imageIndex):
        self.spriteIndex = glob.glob(os.path.join("centipede", "snakeBody?.png"))
        self.spriteStart = pygame.image.load(self.spriteIndex[imageIndex]).convert_alpha()
        self.sprite = self.spriteStart
        
        self.spriteArea = pygame.Rect(x, y, self.spriteStart.get_rect().width,self.spriteStart.get_rect().height)
        
        self.x = x# - self.spriteArea.width / 2
        self.y = y# - self.spriteArea.height / 2
        
        self.imageIndex = imageIndex
        self.spriteCounter = 0
        self.direction = 0
        
        
    def move(self, x, y, direction):        
        self.spriteCounter += 1
        if self.spriteCounter > 6:
            self.spriteCounter = 0
            self.imageIndex = (self.imageIndex + 1) % 2
            self.spriteStart = pygame.image.load(self.spriteIndex[self.imageIndex]).convert_alpha()
        
        self.direction = direction
        self.sprite = rotate(self.spriteStart, self.direction).convert_alpha()
        self.spriteCentre = matchCentre(self.spriteStart, self.sprite)
        
        self.mask = pygame.mask.from_surface(self.sprite)
        
        self.x = x# - self.spriteCentre.width / 2
        self.y = y# - self.spriteCentre.height / 2
        
        # spriteArea will be used for collision testing
        self.spriteArea = pygame.Rect(self.x, self.y, self.spriteCentre.width, self.spriteCentre.height)
        
        
    
    def draw(self, window):
        window.blit(self.sprite, (self.x + self.spriteCentre[0], self.y + self.spriteCentre[1]))

