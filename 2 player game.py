# Import packages
import vars
import pygame
from classPlayer import Player
from classPlatform import Platform
from classPortal import Portal
from classEnemy import Enemy
from classProjectile import Projectile
from nyttigeFunksjoner import checkBullets, checkInBox, checkInScreen
from setWorld import setWorld
from gameWindow import redrawGameWindow, startMenu, redrawMenuWindow
#import objectContainer





# ------------ MAIN ----------------
#objectContainer.init()

def main():

    pygame.display.set_caption("Two player game")

    #Sounds and music
    pygame.mixer.music.load("Music/" +  vars.music[0])  
    pygame.mixer.music.play(-1)
                                                                                                                    
    # build world
    #Egentlig burde bullets legges inn i player osv. Jaja. Fikses senere.
    platforms, portals = setWorld(0)
    players = []
    man = Player(900, vars.screenHeight-190, 64, 64, 1)
    players.append(man)
    enemy = Enemy(vars.screenWidth//2, vars.screenHeight//4, 20, 64, 200)
    bullets = [[]]
    enemyBullets = []
    run = True

    # --------- Start menu --------------
    noPlayers = startMenu(vars.music)
    if (noPlayers == 2):
        man2 = Player(200, vars.screenHeight - 190, 64, 64, 2)
        players.append(man2)
        bullets.append([])
    # --------- Main loop --------------
    while run:  
        vars.clock.tick(60)
        # ----------- Quit game ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # ------------ BULLETS -----------------
        checkBullets(bullets, enemy, enemyBullets, players)
        enemy.checkEnemyAttack(enemyBullets)

        # ------------- KEYS -------------------
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        # ------------ PLAYER ACTIONS -----------
        for player in players:
            player.pressedKeys(keys, bullets, portals)
            # Jump animation
            player.jump(events, keys, platforms)

        # ---------- DRAW WINDOW ----------------
        redrawGameWindow(enemy, bullets, players, enemyBullets, platforms, portals)

        # ---------- LEVELUP ANIMATION -----------
        if enemy.gainedLevel:
            enemyBullets = []
            enemy.levelupAnimation(bullets, players, enemyBullets)
            platforms, portals = setWorld(enemy.level)

    pygame.quit()

    return 0

main()