import pygame
import random
import numpy as np
from math import atan2
from classProjectile import Projectile
from nyttigeFunksjoner import randomMovement, findLengthOfVector, shortenVector
from setWorld import setWorld
from gameWindow import redrawGameWindow
import vars

class Enemy(object):
    walkLeft = vars.enemyHav[0]
    walkRight = vars.enemyHav[1]
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [self.x, self.x + end]
        self.walkCount = 0
        self.maxVel = 1
        self.accVector = [0,0]
        self.velVec = [0,0]
        self.vel = findLengthOfVector(self.velVec)
        self.hitbox = (self.x, self.y, width, height)
        self.fullHealth = 100
        self.health = self.fullHealth
        self.healthBarScale = 2
        self.fullHealthBar = (vars.screenWidth//2-self.fullHealth*self.healthBarScale//2, 40, self.fullHealth*self.healthBarScale, 40)
        self.level = 0
        self.gainedLevel = False
        #Bevegelsesmønster
        self.lastPlayerShot = 0
        self.nearestPlayer = [self.vel, 0]
        #Kode som trengs for å generere prosjektiler. Legger inn litt tilfeldige movements.
        self.attackProbability = 0.00           #Prob of attack at a certain timestep
        self.attackCheck = 20                   #Number of timesteps between each prob check and prob increase.
        self.attackProbabilityIncrease = 0.1
        self.randomAttackNumber = random.uniform(0, 1)  #Variable for random attack check
        self.attack = False                     #Is attacking?
        self.attackCounter = 0
        self.attackSpeed = 10                   #Timesteps between projectiles
        self.startAttackDuration = 120          #Duration of attack
        self.attackDuration = 0

    def levelUp(self): #Level of enemy. Enemy is gradually becoming stronger.
        #Check if healthbar has sunk under 75%, 50% or 25%.
        if (self.health <= self.fullHealth * (3-self.level)/4):
            self.level += 1
            self.attackProbabilityIncrease += 0.01
            self.maxVel += 0.5
            self.gainedLevel = True
            #Kan dette flyttes til main?:
            #self.levelupAnimation(bullets, players, enemyBullets, platforms, portals)
            #platforms, portals = setWorld(self.level)

    def levelupAnimation(self, bullets, players, enemyBullets):
        for p in players:
            p.isJump = True
        self.gainedLevel = False
        self.x = vars.screenWidth/2
        self.y =  vars.screenHeight/4
        run = True
        counter = 0
        add = -1
        while (run):
            vars.clock.tick(8)
            #draw
            redrawGameWindow(self, bullets, players, enemyBullets, [], [])
            self.level += add
            add = add*(-1)
            counter += 1
            if counter > 5*8 -1:
                run = False

    def checkEnemyAttack(self, enemyBullets): #Calculate probability for attack. Initiate attack and reset variables if enemy is attacking.
        self.attackCounter += 1
        if self.attackCounter % self.attackCheck == 0 and not self.attack:
            self.attackProbability += self.attackProbabilityIncrease
            if self.attackProbability > self.randomAttackNumber:
                self.attack = True
                self.attackDuration = self.startAttackDuration
                self.attackProbability = 0.00
                self.randomAttackNumber = random.uniform(0,1)
                self.attackCounter = 0

        if self.attack:
            self.attackDuration -= 1
            self.createEnemyProjectile(enemyBullets)
            if self.attackDuration < 0:
                self.attack = False


    def createEnemyProjectile(self, enemyBullets):
        if self.level == 0:
            if not self.attackCounter % self.attackSpeed:
                self.enemyProjectile1(enemyBullets)
        if self.level == 1:
            if not self.attackCounter % self.attackSpeed:
                self.enemyProjectile2(enemyBullets)
            a = 1#Skriv kode her
        if self.level == 2:
            if not self.attackCounter % self.attackSpeed:
                self.enemyProjectile3(enemyBullets)
            a = 2#Skriv kode her
        if self.level == 3:
            if not self.attackCounter % self.attackSpeed:
                self.enemyProjectile4(enemyBullets)
            a = 3#Skriv kode her

    def enemyProjectile1(self, enemyBullets):
        randAngle = random.uniform(0, 1)*360                                              
        enemyBullets.append(Projectile(self.x + self.width*3, self.y + self.height//4, 5, 3, vel = 4, angle = randAngle))

    def enemyProjectile2(self, enemyBullets):
        a = self.attackDuration/self.startAttackDuration*360                            
        enemyBullets.append(Projectile(self.x + self.width*3, self.y + self.height//4, 5, 3, vel = 4, angle = a))

    def enemyProjectile3(self, enemyBullets):
        slowdown = 2*self.attackSpeed
        if self.attackCounter % slowdown == 0:   
            for i in range(10):
                a = i/10*360
                enemyBullets.append(Projectile(self.x + self.width*3, self.y + self.height//4, 5, 3, vel = 4, angle = a))

    def enemyProjectile4(self, enemyBullets):
        a = atan2(self.nearestPlayer[1], self.nearestPlayer[0])*180/np.pi
        enemyBullets.append(Projectile(self.x + self.width*3, self.y + self.height//4, 5, 3, vel = 4, angle = a))

    def enemyProjectile5(self, enemyBullets):
        a = atan2(self.nearestPlayer[1], self.nearestPlayer[0])*180/np.pi
        enemyBullets.append(Projectile(self.x + self.width*3, self.y + self.height//4, 5, 3, vel = 4, angle = a))

    def draw(self, win, players):
        self.move(players)
        self.walkCount += 1
        if self.vel < 0:
            win.blit(self.walkLeft[self.level], (self.x, self.y))
            self.hitbox = (self.x + 30, self.y + 5, 20, 53)
        else:
            win.blit(self.walkRight[self.level], (self.x, self.y))
            self.hitbox = (self.x + 30, self.y + 5, 20, 53)
        pygame.draw.rect(win, (255, 255, 255), self.fullHealthBar)
        pygame.draw.rect(win, (255, 0, 0), (int(vars.screenWidth/2)-int(self.fullHealth*self.healthBarScale/2), 40, self.health*self.healthBarScale, 40))
        pygame.draw.rect(win, (0, 0, 0), self.fullHealthBar, 2)

    def move(self, players):
        if self.level < 10:
            self.findVecToClosestPlayer(players) 
            self.updateAccVector()
            self.updateVelVector()
            self.x += self.velVec[0]
            self.y += self.velVec[1]
        else: #Denne fungerer dårlig..
            self.findVecToClosestPlayer(players)
            move = randomMovement(self.nearestPlayer, self.vel)
            self.x += move[0]
            self.y += move[1]

    def findVecToClosestPlayer(self, players):
        distances = []
        for p in players:
            distances.append(np.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2))
        distances = np.array(distances)
        if distances[self.lastPlayerShot] < 50:
            self.nearestPlayer = [0,0]
        else:
            self.nearestPlayer = [((players[self.lastPlayerShot].x - self.x) / distances[self.lastPlayerShot]), ((players[self.lastPlayerShot].y - self.y) / distances[self.lastPlayerShot])]
    
    def updateAccVector(self):
        self.accVector[0] = self.nearestPlayer[0]*0.1
        self.accVector[1] = self.nearestPlayer[1]*0.1
        
    def updateVelVector(self):
        self.velVec[0] += self.accVector[0]
        self.velVec[1] += self.accVector[1]
        self.velVec = shortenVector(self.velVec, self.maxVel)
        self.vel = findLengthOfVector(self.velVec)