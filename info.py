
class Info():    
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        
        self.sprite = sprite
        
        

    def draw(self, window, offset = 0):
        
        window.blit(self.sprite, (self.x + offset, self.y))
