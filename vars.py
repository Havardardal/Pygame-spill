import pygame
from os import listdir
pygame.init()

# Images
walkRight = [pygame.image.load('Bilder/H0.png'), pygame.image.load('Bilder/H1.png'), pygame.image.load('Bilder/H0.png'), pygame.image.load('Bilder/H2.png')]
walkLeft = [pygame.image.load('Bilder/V0.png'), pygame.image.load('Bilder/V1.png'), pygame.image.load('Bilder/V0.png'), pygame.image.load('Bilder/V2.png')]
walkRight2 = [pygame.image.load('Bilder/H0-2.png'), pygame.image.load('Bilder/H1-2.png'), pygame.image.load('Bilder/H0-2.png'), pygame.image.load('Bilder/H2-2.png')]
walkLeft2 = [pygame.image.load('Bilder/V0-2.png'), pygame.image.load('Bilder/V1-2.png'), pygame.image.load('Bilder/V0-2.png'), pygame.image.load('Bilder/V2-2.png')]
lives = [pygame.image.load('Bilder/P1_head.png'), pygame.image.load('Bilder/P2_head.png')]
enemyHav = [[pygame.image.load('Bilder/enemy1L.png'), pygame.image.load('Bilder/enemy1L2.png'),pygame.image.load('Bilder/enemy1L3.png'),pygame.image.load('Bilder/enemy1L4.png')], [pygame.image.load('Bilder/enemy1R.png'), pygame.image.load('Bilder/enemy1R2.png'), pygame.image.load('Bilder/enemy1R3.png'), pygame.image.load('Bilder/enemy1R4.png')]]
enemyBulletImg = [pygame.image.load('Bilder/enemyProjectile1.png'), pygame.image.load('Bilder/enemyProjectile2.png')]
menuTabs = [pygame.image.load('Bilder/menu2.png')]
bg = pygame.image.load('Bilder/bgplanet2.png')

# Sounds
gat = pygame.mixer.Sound("Sounds/gat.wav")
hit = pygame.mixer.Sound("Sounds/Ooh.wav")

# Music
music = [f for f in listdir("Music")]
#music = ["Music/Heinesang.wav", "Music/Hakensang.wav", "Music/STAR WARS EPIC.wav"]

# Window
screenHeight = 640
screenWidth = 1270
win = pygame.display.set_mode((screenWidth, screenHeight))
font = pygame.font.SysFont('comicsans', 30, False)

# Clock
clock = pygame.time.Clock()