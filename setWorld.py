from turtle import setworldcoordinates
from classPlatform import Platform
from classPortal import Portal
import vars

#Kan lage funksjoner som setWorld1() osv. Sånn at man kan ha flere valg av "baner". Kanskje de endrer seg når bossen blir vanskeligere.



def setWorld(worldNo):
    
    if worldNo == 0:
        platforms = []
        platforms.append(Platform(450, 450, 300, 50))
        platforms.append(Platform(-10, vars.screenHeight - 20, vars.screenWidth + 20,50))
        platforms.append(Platform(700, 300, 300, 50))
        platforms.append(Platform(200, 300, 300, 50))

        portals = []
        portals.append(Portal(vars.screenWidth/2 + 150, vars.screenHeight - 20 - 64 - 1, 40, 64, 1))
        portals.append(Portal(850, 236 - 1, 40, 64, 0))
        portals.append(Portal(vars.screenWidth/2 - 200, vars.screenHeight - 20 - 64 - 1, 40, 64, 3))
        portals.append(Portal(350, 236 - 1, 40, 64, 2))

    if worldNo == 1:
        platforms = []
        platforms.append(Platform(-10, vars.screenHeight - 20, vars.screenWidth + 20,50))        
        platforms.append(Platform(vars.screenWidth*6/8, vars.screenHeight*6/8, vars.screenWidth*1/8, 50))
        platforms.append(Platform(vars.screenWidth*1/8, vars.screenHeight*6/8, vars.screenWidth*1/8, 50))
        platforms.append(Platform(vars.screenWidth*6/8, vars.screenHeight*3/8, vars.screenWidth*1/8, 50))
        platforms.append(Platform(vars.screenWidth*1/8, vars.screenHeight*3/8, vars.screenWidth*1/8, 50))
        platforms.append(Platform(vars.screenWidth*2.5/8, vars.screenHeight*4.5/8, vars.screenWidth*3/8, 50))

        portals = []
        portals.append(Portal(vars.screenWidth/2 -20, vars.screenHeight - 20 - 64 - 1, 40, 64, 1))
        portals.append(Portal(vars.screenWidth/2 - 20 ,vars.screenHeight*4.5/8 - 65, 40, 64, 0))
        portals.append(Portal(vars.screenWidth*1.5/8 -20, vars.screenHeight - 20 - 64 - 1, 40, 64, 3))
        portals.append(Portal(vars.screenWidth*1.5/8 -20, vars.screenHeight*3/8 - 65, 40, 64, 2))
        portals.append(Portal(vars.screenWidth*6.5/8 -20, vars.screenHeight - 20 - 64 - 1, 40, 64, 5))
        portals.append(Portal(vars.screenWidth*6.5/8 -20, vars.screenHeight*3/8 - 65, 40, 64, 4))

    
    if worldNo == 2:
        platforms = []
        platforms.append(Platform(450, 450, 300, 50))
        platforms.append(Platform(-10, vars.screenHeight - 20, vars.screenWidth + 20,50))
        platforms.append(Platform(700, 300, 300, 50))
        platforms.append(Platform(200, 300, 300, 50))

        portals = []
        portals.append(Portal(vars.screenWidth/2 + 150, vars.screenHeight - 20 - 64 - 1, 40, 64, 1))
        portals.append(Portal(850, 236 - 1, 40, 64, 0))
        portals.append(Portal(vars.screenWidth/2 - 200, vars.screenHeight - 20 - 64 - 1, 40, 64, 3))
        portals.append(Portal(350, 236 - 1, 40, 64, 2))

    if worldNo == 3:
        platforms = []
        platforms.append(Platform(-10, vars.screenHeight - 20, vars.screenWidth + 20,50))        
        platforms.append(Platform(vars.screenWidth*6/8, vars.screenHeight*6/8, vars.screenWidth*1/8, 50))
        platforms.append(Platform(vars.screenWidth*1/8, vars.screenHeight*6/8, vars.screenWidth*1/8, 50))
        platforms.append(Platform(vars.screenWidth*6/8, vars.screenHeight*3/8, vars.screenWidth*1/8, 50))
        platforms.append(Platform(vars.screenWidth*1/8, vars.screenHeight*3/8, vars.screenWidth*1/8, 50))
        platforms.append(Platform(vars.screenWidth*2.5/8, vars.screenHeight*4.5/8, vars.screenWidth*3/8, 50))

        portals = []
        portals.append(Portal(vars.screenWidth/2 -20, vars.screenHeight - 20 - 64 - 1, 40, 64, 1))
        portals.append(Portal(vars.screenWidth/2 - 20 ,vars.screenHeight*4.5/8 - 65, 40, 64, 0))
        portals.append(Portal(vars.screenWidth*1.5/8 -20, vars.screenHeight - 20 - 64 - 1, 40, 64, 3))
        portals.append(Portal(vars.screenWidth*1.5/8 -20, vars.screenHeight*3/8 - 65, 40, 64, 2))
        portals.append(Portal(vars.screenWidth*6.5/8 -20, vars.screenHeight - 20 - 64 - 1, 40, 64, 5))
        portals.append(Portal(vars.screenWidth*6.5/8 -20, vars.screenHeight*3/8 - 65, 40, 64, 4))

    return platforms, portals

