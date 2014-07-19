import pygame, math


"""
- rotates a sprite
- image is the sprite
- angle in the rotation in degrees"""
def rotate(image, angle):
    return pygame.transform.rotate(image, angle)


"""
- this just matches the centre of the new rotated sprite with the centre of the original sprite
- oldImage is the original sprite
- rotatedImage is the sprite that has been rotated
- returns a rect of the rotated image"""
def matchCentre(oldImage, rotatedImage):
    oldRect = oldImage.get_rect()
    newRect = rotatedImage.get_rect()
    newRect.center = oldRect.center
    return newRect


"""
- if you need the sprite pivot point not at the centre. this will call the matchCentre function first to align
  centre points of the sprites then move a set number of pixels
- oldImage is the original sprite
- rotatedImage is the new rotated sprite 
- distance is the offset distance for the new pivot point. can be negative
- angle is the angle the rotatedImage was turned
- returns a rect of the rotatedImage that has been moved"""
def moveCentre(oldImage, rotatedImage, distance, angle):
    newRect = matchCentre(oldImage, rotatedImage)
    newRect.centerx += distance * math.cos(math.radians(angle))
    newRect.centery += distance * -math.sin(math.radians(angle))    
    return newRect


"""
- this limits objects movement around the screen, where tolerance was x0.5 the sprite width or height
- value is the current position
- limit is the upper number to test against e.g. the screen width of height - assuming the lower limit to be zero
- tolerance is a distance to increase or lower the upper limit
- returns the original value passed or the new corrected one"""
def limits(value, lowerLimit, upperLimit, tolerance = 0):
    if value + tolerance > upperLimit:
        value = upperLimit - tolerance
    elif value + tolerance < lowerLimit:
        value = lowerLimit - tolerance
    return value


"""
- this function is used to set up the initial number of mushrooms on the starting screen
- x and y are the top left point of the rectangle of a width and a height
- array is the array passed to test for collision with all the elements in it
- returns True/False"""
def placeEmpty(array, x, y, width = 24, height = 24):
    testArea = pygame.Rect(x, y, width, height)
    for f in range(len(array)):
        if testArea.colliderect(array[f].spriteArea):
            return False
    return True


"""
- returns a new array with the single 'element' removed
- array is the array passed
- element is the index number to remove"""
def removeElement(array, element):
    newArray = [0 for x in range(len(array) - 1)]
    skip = 0
    for f in range(len(newArray)):
        skip += (f == element)
        newArray[f] = array[f + skip]
    return newArray


"""
- returns a new array with the sequence of elements removed
- array is the array passed
- elementStart is the starting index number to remove
- numberOfElements is the count from elementStart of elements to remove"""
def removeElementSequence(array, elementStart, numberOfElements):
    newArray = [0 for x in range(len(array) - numberOfElements)]
    skip = 0
    for f in range(len(newArray)):
        skip += (f == elementStart) * numberOfElements
        newArray[f] = array[f + skip]
    return newArray


"""
- returns a new array with specific numbered elements removed
- array is the array passed
- elementsToDelete is an array of the specific elements to remove"""
def removeElementSpecific(array, elementsToDelete):
    newArray = [0 for x in range(len(array) - len(elementsToDelete))]
    if len(newArray) == 0:
        newArray = []
        return newArray
    
    newIndex = 0
    moveOn = True
    for f in range(len(array)):
        newArray[newIndex] = array[f]
        
        for check in range(len(elementsToDelete)):
            if f == elementsToDelete[check]:
                moveOn = False
                break
            else:
                moveOn = True
        
        if moveOn:
            newIndex += 1
            if newIndex == len(newArray):
                return newArray


"""
- returns array with any elements with boolean 'destroyed = True' removed
- array is the array passed"""
def removeDestroyed(array):
    delete = []
    for f in range(len(array)):
        if array[f].destroyed:
            delete.append(f)
    
    if len(delete) > 0:
        array = removeElementSpecific(array, delete)
        
    return array




"""
- this method updates the display panel at the bottom of the screen
- thePlayer is an object created from the lasercanon class, that is the player"""
def panelUpdate(window, SCREEN_WIDTH, SCREEN_HEIGHT, DISPLAY_PANEL, thePlayer, highScore):
    # draw black rectangle first
    pygame.draw.rect(window, (0,40,40), (0,SCREEN_HEIGHT,SCREEN_WIDTH, DISPLAY_PANEL), 0)
    # draw player score
    fontArial = pygame.font.SysFont('arial', 18, True, False)
    playerScore = fontArial.render("SCORE: " + str(thePlayer.score), 1, (205,55,255))
    window.blit(playerScore, (10, SCREEN_HEIGHT + 9))
    # draw player lives
    spriteLives = pygame.image.load("centipede\lasercanon.png").convert_alpha()
    playerLives = fontArial.render("LIVES: ", 1, (205,55,255))
    window.blit(playerLives, (145, SCREEN_HEIGHT + 10))
    for f in range(thePlayer.lives):
        window.blit(spriteLives, (200 + f * 32, SCREEN_HEIGHT + 7))
    # draw player level
    playerLevel = fontArial.render("LEVEL: " + str(thePlayer.level), 1, (205,55,255))
    window.blit(playerLevel, (345, SCREEN_HEIGHT + 10))
    
    highScorePrint = fontArial.render("HIGH SCORE: " + str(highScore), 1, (205,55,255))
    window.blit(highScorePrint, (SCREEN_WIDTH - 200, SCREEN_HEIGHT + 10))
    
"""
- this method keeps angles between 0 and 360
- angle is the direction passed to correct"""
def wrap360(angle):
    if angle > 360:
        angle -= 360
    elif angle < 0:
        angle += 360
    return angle

"""
- this method returns a direction from (x1,y1) to (x2,y2)
- x1, y1 is the start point
- x2, y2 is the finish point"""
def pointDirection(x1, y1, x2, y2):
    xDist = float(x1 - x2)
    yDist = float(y1 - y2)
    
    if xDist == 0:
        if yDist > 0:
            return 90
        elif yDist < 0:
            return 270
    
    if yDist == 0:
        if xDist < 0:
            return 0
        else:
            return 180
    
    return wrap360(math.degrees(math.atan(-yDist / xDist)) + 180 * (xDist > 0))

"""
- this method measures the distance between (x1,y1) and (x2,y2)
- x1, y1 is the first point
- x2, y2 is the second point"""
def pointDistance(x1, y1, x2, y2):
    return (math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))





