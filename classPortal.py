import pygame
import vars

# ----------------- DOORS AND PORTALS --------------------------------

class Portal(object):
    def __init__(self, x, y, length, height, spawnPortal):
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.spawnPortal = spawnPortal

    def drawPortal(self, win):
        #pygame.draw.rect(win, (12, 12, 255), (self.x, self.y, self.length, self.height), 2)
        win.blit(vars.portal[0], (self.x - 25, self.y - 15))
