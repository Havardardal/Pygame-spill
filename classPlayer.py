import pygame
from classProjectile import Projectile
from nyttigeFunksjoner import checkInBox
import vars



# -------------- OBJECT PLAYER ------------------------

class Player(object):
    def __init__(self, x, y, width, height, player):
        self.x = x                  #Position
        self.y = y
        self.width = width          #Size of hitbox
        self.height = height
        self.player = player        #Player 1 or 2
        # Movement
        self.startVel = 5           #Velocity
        self.vel = self.startVel
        self.isJump = True          #Jumping
        self.startJumpVel = -18
        self.gravity = 1
        self.jumpVel = 0
        self.maxJumpVel = -self.startJumpVel*3/4
        self.jetpackFuel = 1000    #Jetpack
        self.jetpackActive = False
        self.jetpackJump = False 
        self.jetpackAirTime = 0
        self.maxJetpackAirTime = 60
        self.left = False           #Positioning
        self.right = False
        self.walkCount = 0
        self.standing = False
        # Shooting
        self.reload = 0             #Gun
        self.reloadSpeed = 5
        self.upgradeCooldown = 0    #Upgrade (not in use)
        self.laser = 100            #Laser
        self.startLaserTime = 20
        self.laserTime = self.startLaserTime
        self.isLaser = False
        # Hit
        self.hitbox = (self.x + 20, self.y + 5, 20, 60) #Hitbox
        self.hit = False
        self.hitCounter = 0
        self.hitTime = 30
        # Other
        self.portalCount = 0        #Portal cooldown
        self.score = 50             #Score (not in use)
        self.health = 100           #Healthbar (not in use)
        self.lives = 5
        # Keys
        if player == 1: 
            self.keyJump = pygame.K_UP
            self.keyLookUp = pygame.K_UP
            self.keyPortal = pygame.K_DOWN
            self.keyLeft = pygame.K_LEFT
            self.keyRight = pygame.K_RIGHT
            self.keyShoot = pygame.K_SPACE
            self.keyLaser = pygame.K_b
        if player == 2: 
            self.keyJump = pygame.K_w
            self.keyLookUp = pygame.K_w
            self.keyPortal = pygame.K_s
            self.keyLeft = pygame.K_a
            self.keyRight = pygame.K_d
            self.keyShoot = pygame.K_TAB
            self.keyLaser = pygame.K_q
# ------------------- JUMPING AND PLATFORM CHECK -----------
    def jump(self, events, keys, platforms):
        # Initiate jump if key is pressed
        if not (self.isJump):
            if keys[self.keyJump]:
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

        # Calculate physics for player in air.
        # Jetpack: Lag en funksjon som dette kan puttes i?
        else:
            if (keys[self.keyJump] and self.jumpVel > -self.startJumpVel/10 and self.jetpackFuel > 0 and not self.jetpackActive):            
                self.jetpackActive = True
                self.jetpackJump = True
                self.jetpackAirTime = 0
                self.jumpVel -= self.gravity/4
                self.y += self.jumpVel
            else:
                if (self.jetpackJump and keys[self.keyJump] and self.jetpackFuel > 0 \
                    and self.jetpackAirTime < self.maxJetpackAirTime):
                    self.jetpackActive = True
                    self.jetpackAirTime += 1
                    if self.jumpVel > -self.maxJumpVel/4:
                        self.jumpVel -= self.gravity/4
                    self.y += self.jumpVel
                    self.jetpackFuel -= 1
                elif self.jumpVel < self.maxJumpVel:
                    self.jumpVel += self.gravity
                self.y += self.jumpVel

                # Check for platforms 
                if self.jumpVel > 0:
                    for p in platforms:
                        if self.y + self.height >= p.y:
                            if (self.y + self.height > p.y) and (self.y + self.height < p.y + p.height) and (self.x + self.width/2 < p.x + p.length) and (self.x + self.width/2 > p.x):
                                self.isJump = False
                                self.jetpackActive = False
                                self.jetpackJump = False
                                self.y = p.y - self.height
                                self.jumpVel = 0
                                p.active[self.player-1] = True
                                break

# ------------- GET PRESSED KEYS AND ACTION -------------------
    def pressedKeys(self, keys, bullets, portals):

        if keys[self.keyShoot]:
            if self.left:
                facing = -1
            else:
                facing = 1
            if self.reload == 0:
                if len(bullets[self.player-1]) < 5:
                    bullets[self.player-1].append(
                        Projectile(round(self.x + self.width // 2 + facing*(self.width//2 + self.vel + 1)), round(self.y + self.height // 2), 6, self.player, facing))
                    self.reload = self.reloadSpeed
                    vars.gat.play()
        elif self.reload > 0:
            self.reload -= 1

        if keys[self.keyLaser]:
            if (self.isLaser == False) and self.laser:
                self.isLaser = True
                self.laser -= 1
                vars.gat.play()

        if keys[self.keyPortal] and self.portalCount == 0:
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

        if keys[self.keyLeft]:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.standing = False
            self.walkCount += 1
        elif keys[self.keyRight]:
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
            self.x = vars.screenWidth - self.width / 2
        elif (self.x > vars.screenWidth - self.width / 2):
            self.x = 0 - self.width / 2
        elif (self.y < 0 - self.height):
            self.y = vars.screenHeight
        elif (self.y > vars.screenHeight):
            self.y = 0 - self.height


# ------------------ DRAW PLAYER ------------------------------
    def draw(self, win):
        if self.player == 1:
            if not (self.standing):
                if (self.left):
                    win.blit(vars.walkLeft[(self.walkCount % 16) // 4], (self.x, self.y))
                elif (self.right):
                    win.blit(vars.walkRight[(self.walkCount % 16) // 4], (self.x, self.y))
            else:
                if self.left:
                    win.blit(vars.walkLeft[0], (self.x, self.y))
                else:
                    win.blit(vars.walkRight[0], (self.x, self.y))
            #Draw lives
            for i in range(self.lives):
                win.blit(vars.lives[0], (vars.screenWidth - 200 + i * 25, 40))
        else:
            if not (self.standing):
                if (self.left):
                    win.blit(vars.walkLeft2[(self.walkCount % 16) // 4], (self.x, self.y))
                elif (self.right):
                    win.blit(vars.walkRight2[(self.walkCount % 16) // 4], (self.x, self.y))
            else:
                if self.left:
                    win.blit(vars.walkLeft2[0], (self.x, self.y))
                else:
                    win.blit(vars.walkRight2[0], (self.x, self.y))
            #Draw lives
            for i in range(self.lives):
                win.blit(vars.lives[1], (vars.screenWidth-200+i*25, 70))

        # Draw jetpack
        if (self.jetpackActive):
            if (self.left):
                win.blit(vars.jetL[0], (self.x, self.y))                
            else:
                win.blit(vars.jetR[0], (self.x, self.y))    

        #Update hitbox
        self.hitbox = (self.x + 20, self.y+5, 20, 60)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hitDraw(self, win):
        self.hitCounter -= 1
        if (self.hitCounter <= 0):
            self.hit = False
        if (self.hitCounter//2 % 2):
            self.draw(win)




# ------------------- DRAW LASER ------------------------------

    def drawLaser(self, win):
        if self.laserTime < 5:
            if self.left:
                pygame.draw.rect(win, (255, 0, 0), (self.x + 10 - vars.screenWidth, self.y + 30, vars.screenWidth, 5))
                pygame.draw.rect(win, (255, 255, 255), (self.x + 10 - vars.screenWidth, self.y + 32, vars.screenWidth, 1))
            else:
                pygame.draw.rect(win, (255, 0, 0), (self.x + 53, self.y + 30, vars.screenWidth, 5))
                pygame.draw.rect(win, (255, 255, 255), (self.x + 53, self.y + 32, vars.screenWidth, 1))
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