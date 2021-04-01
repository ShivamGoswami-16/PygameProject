import pygame
import random
import math
from pygame import mixer

pygame.init()
# Create Screen
screen = pygame.display.set_mode((800, 600))

# BG
bg = pygame.image.load("bg.jpg")
# Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player Ship
PlayerImg = pygame.image.load("ship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
numEnemy = 6

for i in range(numEnemy):
    EnemyImg.append(pygame.image.load("alien.png"))
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(0.3)
    EnemyY_change.append(40)

# Bullet
BulletImg = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 1
bullet_state = "ready"

# score
ScoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
TextX = 10
TextY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def showscore(x, y):
    score = font.render("Score :" + str(ScoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


def game_over():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


# Exit loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    BulletX = playerX
                    bullet_fire(BulletX, BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # PlayerMovement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    playerX += playerX_change
    # EnemyMovement
    for i in range(numEnemy):

        # GameOver
        if EnemyY[i] > 450:
            for j in range(numEnemy):
                EnemyY[j] = 2000
            game_over()
            break
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 0.3
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -0.3
            EnemyY[i] += EnemyY_change[i]
        # Collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            BulletY = 480
            bullet_state = "ready"
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(50, 150)
            ScoreValue += 1

        enemy(EnemyX[i], EnemyY[i], i)
    # BulletMovement
    if BulletY <= 0:
        BulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        bullet_fire(BulletX, BulletY)
        BulletY -= BulletY_change

    EnemyX += EnemyX_change

    player(playerX, playerY)
    showscore(TextX, TextY)
    pygame.display.update()
