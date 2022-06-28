import pygame
import numpy as np
import vars

class Projectile(object):
    blueBullet = pygame.image.load('Bilder/blueBullet.png')
    redBullet = pygame.image.load('Bilder/redBullet.png')
    def __init__(self, x, y, radius, player, facing = 0, vel = 15, angle = 0, bulletType = 0):
        self.x = x
        self.y = y
        self.radius = radius    #Radius på prosjektil
        self.player = player    #Hvilken spiller skyter
        self.facing = facing
        self.vel = vel * facing
        #Nedenfor er eksklusivt for enemy
        self.angle = angle      #Vinkel prosjektil skal skytes ut
        self.vec = [vel*np.cos(angle*np.pi/180), vel*np.sin(angle*np.pi/180)] #Vektor for bevegelse per tidssteg
        self.enemyBulletType = bulletType

    def moveProjectile(self):
        self.x += self.vec[0]
        self.y += self.vec[1]


    def draw(self, win):
        if self.player == 1:
            win.blit(self.blueBullet, (self.x, self.y))
        elif self.player == 2:
            win.blit(self.redBullet, (self.x, self.y))
        elif self.player == 3:
            self.moveProjectile()
            win.blit(vars.enemyBulletImg[self.enemyBulletType], (self.x, self.y))

        # pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)