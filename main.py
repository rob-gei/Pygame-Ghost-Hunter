import math
import random
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Ghost Hunter')

background = pygame.image.load('assets/background.png')

mixer.music.load('assets/bgsound.wav')
mixer.music.play(-1)

enemyImg = []   	
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('assets/ghost.png'))
    enemyX.append(random.randint(0,636))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(0.8)
    enemyY_change.append(40)
  

starImg = pygame.image.load('assets/star.png')
starX = 0
starY = 411
starX_change = 0
starY_change = 4
star_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

playerImg = pygame.image.load('assets/character.png')
playerX = 10
playerY = 411
playerX_change = 0

over_font = pygame.font.Font('freesansbold.ttf',64)

restart_font = pygame.font.Font('freesansbold.ttf',32)



def player(x,y):
    screen.blit(playerImg,(x, y))

def enemy (x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_star (x ,y):
    global star_state
    star_state = "fire"
    screen.blit(starImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, starX, starY):
    distance = math.sqrt(math.pow (enemyX-starX,2)+ math.pow(enemyY-starY,2))
    if distance < 27:
        return True
    else:
        return False

def show_score(x, y):
    score = font.render("Score : "+ str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text ():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (150, 200))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                    playerX_change = -1.5

            if event.key == pygame.K_RIGHT:
                playerX_change= 1.5
            
            if event.key == pygame.K_SPACE:
                if star_state is "ready":
                    star_sound = mixer.Sound('assets/starsound.wav')
                    star_sound.play()
                    starX = playerX
                    fire_star(playerX, starY)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    elif playerX >= 636:
        playerX = 636

    for i in range(num_of_enemies):

        if enemyY[i] > 310:
            for j in  range(num_of_enemies):
                enemyY[i]= 2000
            game_over_text()  
            break
      


        enemyX[i] += enemyX_change[i]

        if enemyX[i] <=0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >= 636:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
    
        collision = isCollision (enemyX[i], enemyY[i], starX, starY)
        if collision:
            starY = 411
            star_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,636)
            enemyY[i] = random.randint(50, 100) 
        enemy(enemyX[i], enemyY[i], i)

    if  starY <= 0 :
        starY = 411
        star_state = "ready"

    if star_state is "fire":
        fire_star(starX, starY)
        starY -= starY_change

    
    
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()

    