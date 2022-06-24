import pygame

# ------------------- PLATFORMS -------------------------------

class Platform(object):
    def __init__(self, x, y, length, height):
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        # Høyden til hitboxen vil fortsatt være 50, trekker fra 30 her slik at den ser tynnere ut i vinduet.
        self.hitbox = (self.x, self.y, length, height-30)
        self.active = [False, False]
    def drawrect(self, win):
        pygame.draw.rect(win, (250, 250, 250), self.hitbox, 2)