import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Rogue")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

ship = pygame.image.load("spaceshipSprite.png")
shipX = 500
shipY = 650
shipChangeX = 0

alien, alienX, alienY, alienChangeX, alienChangeY = [], [], [], [], [] 
noa = 3
for i in range(noa):
    alien.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0, 930))
    alienY.append(random.randint(50, 200))
    alienChangeX.append(4)
    alienChangeY.append(40)

laser = pygame.image.load("laser.png")
laserX = 0
laserY = 650
laserChangeY = 5
laserState = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
fontX, fontY = 10, 10

background = pygame.image.load("space.jpg")
background = pygame.transform.scale(background, (1000,800))

# track = mixer.music.load("backtrack.mp3")
# mixer.music.play(-1)

def shipDraw(X, Y):
    screen.blit(ship, (X, Y))

def alienDraw(X, Y, i):
    screen.blit(alien[i], (X, Y))

def fireBullet(X, Y):
    global laserState
    laserState = "fire"
    screen.blit(laser, (X, Y))

def distance(X1, Y1, X2, Y2):
    dis = math.sqrt(math.pow((X2 - X1), 2) + math.pow((Y2 - Y1), 2))
    if dis <= 20:
        return True
    else:
        return False

def showScore(X, Y):
    global score
    scoreDisplay = font.render("SCORE : " + str(score), True, (255, 255, 255))
    screen.blit(scoreDisplay, (X, Y))

def gameOver():
    scoreDisplay = font.render("GAMEOVER", True, (255, 255, 255))
    screen.blit(scoreDisplay, (300, 400))
    gamerunnning = False

running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            shipChangeX = -3
        if event.key == pygame.K_RIGHT:
            shipChangeX = 3
        if event.key == pygame.K_SPACE:
            if laserState == "ready":
                laserX = shipX 
                bulletSound = mixer.Sound('laser.wav')
                bulletSound.play()
                fireBullet(laserX, laserY)
        # if event.type = pygame.K_ENTER:        
                
    # if event.type == pygame.KEYUP:
    #     if event.key == pygame.K_LEFT:
    #         shipChangeX = 0
    #     if event.key == pygame.K_RIGHT:
    #         shipChangeX = 0           
                   
    shipX += shipChangeX

    if shipX <= 0:
        shipX = 0
    if shipX >= 930:
        shipX = 930 

    for i in range(noa):
        alienX[i] += alienChangeX[i]
        if alienX[i] <= 0:
            alienChangeX[i] = 3
            alienY[i] += alienChangeY[i]
        elif alienX[i] >= 930:
            alienChangeX[i] = -3
            alienY[i] += alienChangeY[i]
        if distance(alienX[i], alienY[i], laserX, laserY):
            laserY = shipY
            laserState = "ready"
            score += 1
            collision = mixer.Sound('explosion.wav')
            collision.play()
            alienX[i] = random.randint(0, 930)
            alienY[i] = random.randint(50, 200)
        if alienY[i] >= 650:
            for j in range(noa):
                alienX[j] = 2000
            gameOver()
            break;   
        alienDraw(alienX[i], alienY[i], i)     

    if laserState == "fire":
        fireBullet(laserX, laserY)
        laserY -= laserChangeY
    if laserY <= 0:
        laserY = shipY
        laserState = "ready"

    showScore(fontX, fontY)
    shipDraw(shipX, shipY)        
    pygame.display.update()