import pygame, glob, os

class Mushroom():    
    def __init__(self, x, y, sprite = os.path.join("centipede", "mushroom_*.png")):
        self.x = x
        self.y = y
        self.spriteIndex = glob.glob(sprite)
        
        self.damageLevel = len(self.spriteIndex) - 1
        self.destroyed = False
        
        self.sprite = pygame.image.load(self.spriteIndex[self.damageLevel]).convert_alpha()
        self.mask = pygame.mask.from_surface(self.sprite)
        area = self.sprite.get_rect()
        self.spriteArea = pygame.Rect(x, y, area[2], area[3])
        
        

    def draw(self, window):
        self.sprite = pygame.image.load(self.spriteIndex[self.damageLevel]).convert_alpha()
        area = self.sprite.get_rect()
        self.spriteArea = pygame.Rect(self.x, self.y, area[2], area[3])
        window.blit(self.sprite, (self.x, self.y))
