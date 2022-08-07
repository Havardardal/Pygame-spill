import vars
import random
import numpy as np

# ----------- NYTTIGE FUNKSJONER -------------------

def checkInBox(position, box): # Coordinates: (x, y) and (x, y, length, height)
    inBox = False
    if position[0] > box[0] and position[0] < box[0] + box[2]:
        if position[1] > box[1] and position[1] < box[1] + box[3]:
            inBox = True
    return inBox

def checkBoxOverlap(box1, box2): # box: (x, y, width, height)
    overlap = False
    if not (box1[0] > box2[0]+box2[2] or box1[1] > box2[1]+box2[3] or box1[0]+box1[2] < box2[0] or box1[1]+box1[3] < box2[1]):
        overlap = True
    return overlap

def checkInScreen(position):
    return checkInBox(position, (0, 0, vars.screenWidth, vars.screenHeight))

def findLengthOfVector(vec):
    return np.sqrt(vec[0]**2+vec[1]**2)

#Denne må fikses
def randomMovement(probVec, vel):
    mov = [0,0]
    for i in range(int(vel)):
        n = random.uniform(0,1)
        if n < np.abs(probVec[0]**2):
            mov[0] += 0.5*np.sign(probVec[0])
        else:
            mov[1] += 1*np.sign(probVec[1])
    return mov

# ------------------ BULLET AND HIT CHECK -------------------

#Denne kan jeg skrive om slik at spilelre ikke kan treffe hverandre.
def checkBullets(bullets, enemy, enemyBullets, players):
    #Loop through all bullets
    for el in bullets:
        for bullet in el:
            #check if enemy is hit
            if checkInBox((bullet.x, bullet.y), enemy.hitbox):
                el.pop(el.index(bullet))
                enemy.health -= 1
                enemy.lastPlayerShot = bullet.player-1
                #Sjekker om enemy ikke er maks level 
                if enemy.level < 3:
                    enemy.levelUp()
            #bullet movement
            if bullet.x > 0 and bullet.x < vars.screenWidth: bullet.x += bullet.vel
            else: el.pop(el.index(bullet))

    #Loop through enemy bullets.
    for bullet in enemyBullets:
        if checkInScreen((bullet.x, bullet.y)): bullet.moveProjectile()
        else: enemyBullets.pop(enemyBullets.index(bullet))
        # check if player is hit #Her er det en bug. bullet.pop kjøres for andre gang!
        for guy in players:
            if not guy.hit and checkInBox((bullet.x, bullet.y), guy.hitbox):
                enemyBullets.pop(enemyBullets.index(bullet))
                guy.lives -= 1
                guy.hit = True
                guy.hitCounter = guy.hitTime
    
    for guy in players:
        if (not guy.hit and checkBoxOverlap(guy.hitbox, enemy.hitbox)):
                guy.lives -= 1
                guy.hit = True
                guy.hitCounter = guy.hitTime


#Funksjon som forkorter en vektor til en maks lengde.
def shortenVector(vector, maxLength):
    l = findLengthOfVector(vector)
    if l > maxLength:
        vector = [vector[0]/l*maxLength, vector[1]/l*maxLength] # Endre denne. Arccos returnerer radianer? 
    return vector



