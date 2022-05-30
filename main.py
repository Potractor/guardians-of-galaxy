import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()
# create the screen 800 is the width and 600 is the height
screen = pygame.display.set_mode((800, 600))
# background

background = pygame.image.load('background.png')

#Bsckground music
mixer.music.load('background (1).wav')
mixer.music.play(-1)
# title and icon

pygame.display.set_caption("Guardians of Galaxy")

icon = pygame.image.load('arcade-game.png')
pygame.display.set_icon(icon)
# player
playerImg = pygame.image.load('arcade-game (1).png')
playerX = 370
playerY = 480
playerX_change = 0
# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# ready- you cant see the bullet  on the screen
# fire - bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# score
score_value =0
font =pygame.font.Font('freesansbold.ttf',32)

testX = 10
testY = 10

# game over
over_font =pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_test =over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_test,(200,250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # inorder to shoot the bullet from the middle of the jet we are increasing the values of the coordinates
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX - enemyX, 2) + math.pow(bulletY - enemyY, 2))
    if distance >= 30:
        return False
    else:

        return True


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2

            if event.key == pygame.K_RIGHT:
                playerX_change = 2

            if event.key == pygame.K_SPACE:
                # here when we gave this coordinates the bullet takes it and the bullet move along with the jet
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # RGB=red,green,blue
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value +=1

            enemyX[i] = random.randint(70, 730)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # collision

    player(playerX, playerY)
    show_score(testX,testY)
    pygame.display.update()
