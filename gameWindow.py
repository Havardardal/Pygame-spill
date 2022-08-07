import vars
import pygame

# ---------------- GAME MENU -------------------------

def startMenu(music):
    noPlayers = 1
    musicNo = 0
    musicTimer = 0
    run = True
    while run:
        vars.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        redrawMenuWindow(noPlayers)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1] and noPlayers == 2:
            noPlayers = 1
            vars.gat.play()
        if keys[pygame.K_2] and noPlayers == 1:
            noPlayers = 2
            vars.gat.play()
        if keys[pygame.K_m] and musicTimer < 1:
            musicNo += 1
            musicNo = musicNo % len(music)
            pygame.mixer.music.load("Music/" + music[musicNo])
            pygame.mixer.music.play(-1)
            musicTimer = 30
        musicTimer -= 1
        if keys[pygame.K_RETURN]:
            run = False
    return noPlayers

# ------------ GAME WINDOW ---------------------------

def redrawGameWindow(enemy, bullets, players, enemyBullets, platforms, portals):
    vars.win.blit(vars.bg, (0,0))
    for plat in platforms:
        plat.draw(vars.win)
    for port in portals:
        port.drawPortal(vars.win)

    #Draw enemy and players
    enemy.draw(vars.win, players)
    for bullet in enemyBullets:
        bullet.draw(vars.win)
    for p in players:
        if p.hit: 
            p.hitDraw(vars.win)
        else:    
            p.draw(vars.win)
        if p.isLaser:
            p.drawLaser(vars.win)
        for b in bullets:
            for bullet in b:
                bullet.draw(vars.win)


    pygame.display.update()

def redrawMenuWindow(noPlayers):
    vars.win.blit(vars.bg, (0, 0))
    play = vars.font.render('PRESS ENTER TO START', True, (0, 0, 0))
    players = vars.font.render(str(noPlayers) + ' Player mode', True, (0,0,0))
    vars.win.blit(vars.walkLeft[0], (vars.screenWidth//3 + 120, vars.screenHeight//2 - 64))
    if noPlayers == 2:
        vars.win.blit(vars.walkRight2[0], (vars.screenWidth/3 + 160, vars.screenHeight/2 - 64))
    vars.win.blit(play, (vars.screenWidth//3 , vars.screenHeight//2))
    vars.win.blit(players, (vars.screenWidth//3 + 80, vars.screenHeight//2-120))
    vars.win.blit(vars.menuTabs[0], (vars.screenWidth//2-170, vars.screenHeight-240))
    pygame.display.update()

# ---------------------------------------------------------