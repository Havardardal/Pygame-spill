import pygame
import numpy as np
import random
pygame.init()
screenHeight = 640
screenWidth = 1270
win = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("Two player game")

# This goes outside the while loop, near the top of the program. Loading the images.
walkRight = [pygame.image.load('Bilder/H0.png'), pygame.image.load('Bilder/H1.png'), pygame.image.load('Bilder/H0.png'), pygame.image.load('Bilder/H2.png')]
walkLeft = [pygame.image.load('Bilder/V0.png'), pygame.image.load('Bilder/V1.png'), pygame.image.load('Bilder/V0.png'), pygame.image.load('Bilder/V2.png')]
walkRight2 = [pygame.image.load('Bilder/H0-2.png'), pygame.image.load('Bilder/H1-2.png'), pygame.image.load('Bilder/H0-2.png'), pygame.image.load('Bilder/H2-2.png')]
walkLeft2 = [pygame.image.load('Bilder/V0-2.png'), pygame.image.load('Bilder/V1-2.png'), pygame.image.load('Bilder/V0-2.png'), pygame.image.load('Bilder/V2-2.png')]
lives = [pygame.image.load('Bilder/P1_head.png'), pygame.image.load('Bilder/P2_head.png')]
enemyHav = [[pygame.image.load('Bilder/enemy1L.png'), pygame.image.load('Bilder/enemy1L2.png'),pygame.image.load('Bilder/enemy1L3.png'),pygame.image.load('Bilder/enemy1L4.png')], [pygame.image.load('Bilder/enemy1R.png'), pygame.image.load('Bilder/enemy1R2.png'), pygame.image.load('Bilder/enemy1R3.png'), pygame.image.load('Bilder/enemy1R4.png')]]
enemyBulletImg = [pygame.image.load('Bilder/enemyProjectile1.png'), pygame.image.load('Bilder/enemyProjectile2.png')]
menuTabs = [pygame.image.load('Bilder/menu2.png')]
bg = pygame.image.load('Bilder/bgplanet2.png')

clock = pygame.time.Clock()

#Sounds and music
gat = pygame.mixer.Sound("Sounds/gat.wav")
hit = pygame.mixer.Sound("Sounds/Ooh.wav")
music = ["Music/Heinesang.wav", "Music/Hakensang.wav", "Music/STAR WARS EPIC.wav"]
pygame.mixer.music.load(music[0])
pygame.mixer.music.play(-1)


# -------------- OBJECT PLAYER ------------------------

class player(object):
    def __init__(self, x, y, width, height, player):
        self.x = x                  #Position
        self.y = y
        self.width = width          #Size of hitbox
        self.height = height
        self.player = player        #Player 1 or 2
        self.startVel = 5           #Velocity
        self.vel = self.startVel
        self.isJump = True          #Jumping
        self.startJumpVel = -20
        self.gravity = 1
        self.jumpVel = 0
        self.left = False           #Positioning
        self.right = False
        self.walkCount = 0
        self.standing = False
        self.reload = 0             #Gun
        self.reloadSpeed = 5
        self.upgradeCooldown = 0    #Upgrade (not in use)
        self.laser = 100            #Laser
        self.startLaserTime = 20
        self.laserTime = self.startLaserTime
        self.isLaser = False
        self.portalCount = 0        #Portal cooldown
        self.hitbox = (self.x + 20, self.y + 5, 20, 60) #Hitbox
        self.score = 50             #Score (not in use)
        self.health = 100           #Healthbar (not in use)
        self.lives = 5

# ------------------- JUMPING AND PLATFORM CHECK -----------
    def jump(self):
        # Initiate jump if key is pressed
        if not (self.isJump):
            if self.player == 1:
                if keys[pygame.K_UP]:
                    self.isJump = True
                    self.walkCount = 0
                    self.jumpVel = self.startJumpVel
            else:
                if keys[pygame.K_w]:
                    self.isJump = True
                    self.walkCount = 0
                    self.jumpVel = self.startJumpVel
            # Check if player is leaving the platform
            for p in platforms:
                if p.active[self.player-1]:
                    if (self.x + self.width/2 > p.x + p.length) or (self.x + self.width/2 < p.x):
                        self.isJump = True
                        #self.jumpCount = 0
                        p.active[self.player-1] = False

        # Calculate physics for player in air
        else:
            self.jumpVel += self.gravity
            self.y += self.jumpVel

            # Check for platforms
            if self.jumpVel > 0:
                for p in platforms:
                    if self.y + self.height - self.jumpVel <= p.y:
                        if (self.y + self.height > p.y) and (self.y + self.height < p.y + p.height) and (self.x + self.width/2 < p.x + p.length) and (self.x + self.width/2 > p.x):
                            self.isJump = False
                            self.y = p.y - self.height
                            self.jumpVel = 0
                            p.active[self.player-1] = True
                            break

# ------------- GET PRESSED KEYS AND ACTION -------------------
    def pressedKeys(self):

    # ------------------ PLAYER 1 -----------------------------
        if self.player == 1:
            if keys[pygame.K_SPACE]:
                if self.left:
                    facing = -1
                else:
                    facing = 1
                if self.reload == 0:
                    if len(bullets[0]) < 5:
                        bullets[0].append(
                            projectile(round(self.x + self.width // 2 + facing*(self.width//2 + self.vel + 1)), round(self.y + self.height // 2), 6, 1, facing))
                        self.reload = self.reloadSpeed
                        gat.play()
            elif self.reload > 0:
                self.reload -= 1

            if keys[pygame.K_b]:
                if (self.isLaser == False) and self.laser:
                    self.isLaser = True
                    self.laser -= 1
                    gat.play()

            if keys[pygame.K_DOWN] and self.portalCount == 0:
                for port in portals:
                    if checkInBox((self.x + self.width / 2, self.y + self.height / 2),
                                  (port.x, port.y, port.length, port.height)):
                        self.x = portals[port.spawnPortal].x - 15
                        self.y = portals[port.spawnPortal].y
                        self.jumpCount = 0
                        self.isJump = True
                        self.portalCount = 30
                        break  # for
            if not self.portalCount == 0:
                self.portalCount -= 1

            if keys[pygame.K_LEFT]:
                self.x -= man.vel
                self.left = True
                self.right = False
                self.standing = False
                self.walkCount += 1
            elif keys[pygame.K_RIGHT]:
                self.x += man.vel
                self.right = True
                self.left = False
                self.standing = False
                self.walkCount += 1
            else:
                self.walkCount = 0
                self.standing = True

    # ------------------ PLAYER 2 -----------------------------
        if self.player == 2:
            if keys[pygame.K_TAB]:
                if self.left:
                    facing2 = -1
                else:
                    facing2 = 1
                if self.reload == 0:
                    if len(bullets[1]) < 5:
                        bullets[1].append(
                            projectile(round(self.x + self.width//2 + facing2*(self.width//2 + self.vel + 1)), round(self.y + self.height // 2), 6, 2,
                                       facing2))
                        self.reload = self.reloadSpeed
                        gat.play()
            elif self.reload > 0:
                self.reload -= 1

            if keys[pygame.K_q]:
                if (self.isLaser == False) and self.laser:
                    self.isLaser = True
                    self.laser -= 1
                    gat.play()

            if keys[pygame.K_s] and self.portalCount == 0:
                for port in portals:
                    if checkInBox((self.x + self.width / 2, self.y + self.height / 2),
                                  (port.x, port.y, port.length, port.height)):
                        self.x = portals[port.spawnPortal].x - 15
                        self.y = portals[port.spawnPortal].y
                        self.jumpCount = 0
                        self.isJump = True
                        self.portalCount = 10
                        break  # for
            if not self.portalCount == 0:
                self.portalCount -= 1

            if keys[pygame.K_a]:
                self.x -= self.vel
                self.left = True
                self.right = False
                self.standing = False
                self.walkCount += 1
            elif keys[pygame.K_d]:
                self.x += self.vel
                self.right = True
                self.left = False
                self.standing = False
                self.walkCount += 1
            else:
                self.walkCount = 0
                self.standing = True

        # Out of screen check.
        if (self.x < 0 - self.width / 2):
            self.x = screenWidth - self.width / 2
        elif (self.x > screenWidth - self.width / 2):
            self.x = 0 - self.width / 2
        elif (self.y < 0 - self.height):
            self.y = screenHeight
        elif (self.y > screenHeight):
            self.y = 0 - self.height


# ------------------ DRAW PLAYER ------------------------------
    def draw(self, win):
        if self.player == 1:
            if not (self.standing):
                if (self.left):
                    win.blit(walkLeft[(self.walkCount % 16) // 4], (self.x, self.y))
                elif (self.right):
                    win.blit(walkRight[(self.walkCount % 16) // 4], (self.x, self.y))
            else:
                if self.left:
                    win.blit(walkLeft[0], (self.x, self.y))
                else:
                    win.blit(walkRight[0], (self.x, self.y))
            #Draw lives
            for i in range(self.lives):
                win.blit(lives[0], (screenWidth - 200 + i * 25, 40))
        else:
            if not (self.standing):
                if (self.left):
                    win.blit(walkLeft2[(self.walkCount % 16) // 4], (self.x, self.y))
                elif (self.right):
                    win.blit(walkRight2[(self.walkCount % 16) // 4], (self.x, self.y))
            else:
                if self.left:
                    win.blit(walkLeft2[0], (self.x, self.y))
                else:
                    win.blit(walkRight2[0], (self.x, self.y))
            #Draw lives
            for i in range(self.lives):
                win.blit(lives[1], (screenWidth-200+i*25, 70))

        #Update hitbox
        self.hitbox = (self.x + 20, self.y+5, 20, 60)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)




# ------------------- DRAW LASER ------------------------------

    def drawLaser(self, win):
        if self.laserTime < 5:
            if self.left:
                pygame.draw.rect(win, (255, 0, 0), (self.x + 10 - screenWidth, self.y + 30, screenWidth, 5))
                pygame.draw.rect(win, (255, 255, 255), (self.x + 10 - screenWidth, self.y + 32, screenWidth, 1))
            else:
                pygame.draw.rect(win, (255, 0, 0), (self.x + 53, self.y + 30, screenWidth, 5))
                pygame.draw.rect(win, (255, 255, 255), (self.x + 53, self.y + 32, screenWidth, 1))
        else:
            if self.left:
                pygame.draw.circle(win, (255, 0, 0), (round(self.x + 8), round(self.y + 33)), 6)
                pygame.draw.circle(win, (255, 255, 255), (round(self.x + 8), round(self.y + 33)), 2)
            else:
                pygame.draw.circle(win, (255, 0, 0), (round(self.x + 56), round(self.y + 33)), 6)
                pygame.draw.circle(win, (255, 255, 255), (round(self.x + 56), round(self.y + 33)), 2)
        self.laserTime -= 1
        if self.laserTime == 0:
            self.laserTime = self.startLaserTime
            self.isLaser = False


# ------------------- PLATFORMS -------------------------------

class platform(object):
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


platforms = []
platforms.append(platform(450, 450, 300, 50))
platforms.append(platform(-10, screenHeight - 20, screenWidth + 20,50))
platforms.append(platform(700, 300, 300, 50))
platforms.append(platform(200, 300, 300, 50))


# ----------------- DOORS AND PORTALS --------------------------------

class portal(object):
    def __init__(self, x, y, length, height, spawnPortal):
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.spawnPortal = spawnPortal

    def drawPortal(self, win):
        pygame.draw.rect(win, (12, 12, 255), (self.x, self.y, self.length, self.height), 2)


portals = []
portals.append(portal(screenWidth/2 + 150, screenHeight - 20 - 64 - 1, 40, 64, 1))
portals.append(portal(850, 236 - 1, 40, 64, 0))
portals.append(portal(screenWidth/2 - 200, screenHeight - 20 - 64 - 1, 40, 64, 3))
portals.append(portal(350, 236 - 1, 40, 64, 2))

# ---------------------------- ENEMY OBJECT --------------------------------

class enemyObject(object):
    walkLeft = enemyHav[0]
    walkRight = enemyHav[1]
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [self.x, self.x + end]
        self.walkCount = 0
        self.vel = 2.2
        self.hitbox = (self.x, self.y, width, height)
        self.fullHealth = 100
        self.health = self.fullHealth
        self.healthBarScale = 2
        self.fullHealthBar = (screenWidth//2-self.fullHealth*self.healthBarScale//2, 40, self.fullHealth*self.healthBarScale, 40)
        self.level = 0
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
            #Her må det legges inn en level-up animasjon

    def checkEnemyAttack(self): #Calculate probability for attack. Initiate attack and reset variables if enemy is attacking.
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
            self.createEnemyProjectile()
            if self.attackDuration < 0:
                self.attack = False


    def createEnemyProjectile(self):
        if self.level == 0:
            if not self.attackCounter % self.attackSpeed:
                self.enemyProjectile1()
        if self.level == 1:
            if not self.attackCounter % self.attackSpeed:
                self.enemyProjectile1()
            a = 1#Skriv kode her
        if self.level == 2:
            if not self.attackCounter % self.attackSpeed:
                self.enemyProjectile1()
            a = 2#Skriv kode her
        if self.level == 3:
            if not self.attackCounter % self.attackSpeed:
                self.enemyProjectile1()
            a = 3#Skriv kode her

    def enemyProjectile1(self):
        randAngle = random.uniform(0, 1)*3600
        enemyBullets.append(projectile(self.x + self.width//2, self.y + self.height//2, 5, 3, vel = 4, angle = randAngle))

    def draw(self, win):
        self.move()
        self.walkCount += 1
        if self.vel < 0:
            win.blit(self.walkLeft[self.level], (self.x, self.y))
            self.hitbox = (self.x + 30, self.y + 5, 20, 53)
        else:
            win.blit(self.walkRight[self.level], (self.x, self.y))
            self.hitbox = (self.x + 30, self.y + 5, 20, 53)
        pygame.draw.rect(win, (255, 255, 255), self.fullHealthBar)
        pygame.draw.rect(win, (255, 0, 0), (int(screenWidth/2)-int(self.fullHealth*self.healthBarScale/2), 40, self.health*self.healthBarScale, 40))
        pygame.draw.rect(win, (0, 0, 0), self.fullHealthBar, 2)

    def move(self):
        #Slette denne if-en?
        if self.level == -1:
            if self.vel > 0:
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel*(-1)
                    self.walkCount = 0
            else:
                if self.x + self.vel > self.path[0]:
                   self.x += self.vel
                else:
                    self.vel = self.vel*(-1)
                    self.walkCount = 0
        else:
            self.findVecToClosestPlayer()
            self.x += self.nearestPlayer[0]
            self.y += self.nearestPlayer[1]


    def findVecToClosestPlayer(self):
        distances = []
        for p in players:
            distances.append(np.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2))
        distances = np.array(distances)
        if distances[self.lastPlayerShot] < 60:
            self.nearestPlayer = [0,0]
        else:
            self.nearestPlayer = [np.round((players[self.lastPlayerShot].x - self.x) * self.vel / distances[self.lastPlayerShot]), np.round((players[self.lastPlayerShot].y - self.y) * self.vel / distances[self.lastPlayerShot])]


# ----------- OBJECT PROJECTILE ------------------------

class projectile(object):
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
        self.vec = [int(vel*np.cos(angle*np.pi/180)), int(vel*np.sin(angle*np.pi/180))] #Vektor for bevegelse per tidssteg
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
            win.blit(enemyBulletImg[self.enemyBulletType], (self.x, self.y))

        # pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# --------------- POWER UPS ------------------------
class powerUp(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = False
        self.laser = False



# ----------- NYTTIGE FUNKSJONER -------------------

def checkInBox(position, box): # Coordinates: (x, y) and (x, y, length, height)
    inBox = False
    if position[0] > box[0] and position[0] < box[0] + box[2]:
        if position[1] > box[1] and position[1] < box[1] + box[3]:
            inBox = True
    return inBox

def checkInScreen(position):
    return checkInBox(position, (0, 0, screenWidth, screenHeight))

# ------------------ BULLET CHECK -------------------

#Denne kan jeg skrive om slik at spilelre ikke kan treffe hverandre, og for å se om enemy treffer spillere.
def checkBullets():
    #Loop through all bullets
    for el in bullets:
        for bullet in el:
            #check if enemy is hit
            if checkInBox((bullet.x, bullet.y), enemy1.hitbox):
                el.pop(el.index(bullet))
                enemy1.health -= 1
                enemy1.lastPlayerShot = bullet.player-1
                #Sjekker om enemy ikke er maks level 
                if enemy1.level < 3:
                    enemy1.levelUp()
            #bullet movement
            if bullet.x > 0 and bullet.x < screenWidth: bullet.x += bullet.vel
            else: el.pop(el.index(bullet))

    #Loop through enemy bullets.
    for bullet in enemyBullets:
        if checkInScreen((bullet.x, bullet.y)): bullet.moveProjectile()
        else: enemyBullets.pop(enemyBullets.index(bullet))
        # check if player is hit
        for guy in players:
            if checkInBox((bullet.x, bullet.y), guy.hitbox):
                enemyBullets.pop(enemyBullets.index(bullet))
                guy.lives -= 1


# ---------------- GAME MENU -------------------------

def startMenu(music):
    noPlayers = 1
    musicNo = 0
    musicTimer = 0
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        redrawMenuWindow(noPlayers)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1] and noPlayers == 2:
            noPlayers = 1
            gat.play()
        if keys[pygame.K_2] and noPlayers == 1:
            noPlayers = 2
            gat.play()
        if keys[pygame.K_m] and musicTimer < 1:
            musicNo += 1
            musicNo = musicNo % len(music)
            pygame.mixer.music.load(music[musicNo])
            pygame.mixer.music.play(-1)
            musicTimer = 30
        musicTimer -= 1
        if keys[pygame.K_RETURN]:
            run = False
    return noPlayers

# ------------ GAME WINDOW ---------------------------

def redrawGameWindow():
    win.blit(bg, (0,0))
    for plat in platforms:
        plat.drawrect(win)
    for port in portals:
        port.drawPortal(win)

    #Draw enemy and players
    enemy1.draw(win)
    for bullet in enemyBullets:
        bullet.draw(win)
    for p in players:
        p.draw(win)
        if p.isLaser:
            p.drawLaser(win)
        for b in bullets:
            for bullet in b:
                bullet.draw(win)


    pygame.display.update()

def redrawMenuWindow(noPlayers):
    win.blit(bg, (0, 0))
    play = font.render('PRESS ENTER TO START', True, (0, 0, 0))
    players = font.render(str(noPlayers) + ' Player mode', True, (0,0,0))
    win.blit(walkLeft[0], (screenWidth//3 + 120, screenHeight//2 - 64))
    if noPlayers == 2:
        win.blit(walkRight2[0], (screenWidth/3 + 160, screenHeight/2 - 64))
    win.blit(play, (screenWidth//3 , screenHeight//2))
    win.blit(players, (screenWidth//3 + 80, screenHeight//2-120))
    win.blit(menuTabs[0], (screenWidth//2-170, screenHeight-240))
    pygame.display.update()

# ---------------------------------------------------------


# ------------ MAIN ----------------
font = pygame.font.SysFont('comicsans', 30, False)
players = []
man = player(900, screenHeight-190, 64, 64, 1)
players.append(man)
enemy1 = enemyObject(screenWidth//2, screenHeight//4, 20, 64, 200)
bullets = [[]]
enemyBullets = []
run = True
rin1 = True
# --------- Start menu --------------
noPlayers = startMenu(music)
if (noPlayers == 2):
    man2 = player(200, screenHeight - 190, 64, 64, 2)
    players.append(man2)
    bullets.append([])

# --------- Main loop --------------
while run:
    clock.tick(60)
    # ----------- Quit game ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # ------------ BULLETS -----------------
    checkBullets()
    enemy1.checkEnemyAttack()

    # ------------- KEYS -------------------
    keys = pygame.key.get_pressed()

    # ------------ PLAYER ACTIONS -----------
    for player in players:
        player.pressedKeys()
        # Jump animation
        player.jump()

    # ---------- DRAW WINDOW ----------------
    redrawGameWindow()

pygame.quit()

#print('\nScores: \nPlayer 1: ' + str(man.score) + '\nPlayer 2: ' + str(man2.score))

