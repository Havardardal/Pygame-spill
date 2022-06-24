from classPlatform import Platform
from classPortal import Portal
import vars

#Kan lage funksjoner som setWorld1() osv. Sånn at man kan ha flere valg av "verdener". Kanskje de endrer seg når bossen blir vanskeligere.

def setPlatforms():
    platforms = []
    platforms.append(Platform(450, 450, 300, 50))
    platforms.append(Platform(-10, vars.screenHeight - 20, vars.screenWidth + 20,50))
    platforms.append(Platform(700, 300, 300, 50))
    platforms.append(Platform(200, 300, 300, 50))
    return platforms

def setPortals():
    portals = []
    portals.append(Portal(vars.screenWidth/2 + 150, vars.screenHeight - 20 - 64 - 1, 40, 64, 1))
    portals.append(Portal(850, 236 - 1, 40, 64, 0))
    portals.append(Portal(vars.screenWidth/2 - 200, vars.screenHeight - 20 - 64 - 1, 40, 64, 3))
    portals.append(Portal(350, 236 - 1, 40, 64, 2))
    return portals
