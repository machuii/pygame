import pygame
import random
import time
import math
import mysql.connector
from pygame import mixer




pygame.init()
screen = pygame.display.set_mode((800, 1000))

pygame.display.set_caption('Pacman')
icon = pygame.image.load('Packman-512.png')
pygame.display.set_icon(icon)
background=pygame.image.load('background.png')


mixer.music.load('Intergalactic Odyssey.ogg')
mixer.music.set_volume(0.1)
mixer.music.play(-1)

score=0
font1 = pygame.font.Font('Caramel Candy .ttf', 32)
textx = 10
texty = 10

font2=pygame.font.Font('freesansbold.ttf',32)

playerimg = pygame.image.load('videogame.png')
playerx = random.randint(0,100)
playery = random.randint(0,100)
playerxchng=0
playerychng=0

#map
map1="""
w    w       w   www         w
w             w
w         w                   ww
w            w w


  w            w       w     w

"""
map1=map1.splitlines()
#enemy
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
enemy_img=[]
enemy_number=5
for i in range(enemy_number):
    enemyx.append(400)
    enemyy.append(500)
    enemyx_change.append(0)
    enemyy_change.append(0)
    enemy_img.append(pygame.image.load('ghost.png'))

powerup1=pygame.image.load('thunder.png')
power1x=200
power1y=200


powerup2=pygame.image.load('nuclear.png')
power2x=random.randint(30,540)
power2y=random.randint(30,540)
l=[]
c=0
n=0
t=0
def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

def enemy_movt(i):
    if enemyx[i]<=0:
        enemyx_change[i]=10
        return True
    elif enemyx[i]>=740:
        enemyx_change[i]=-10
        return True
    if enemyy[i]<=0:
        enemyy_change[i]=10
        return True
    elif enemyy[i]>=925:
        enemyy_change[i]=-10
        return True
    enemyx_change[i]=random.randint(-50,50)
    enemyy_change[i]=random.randint(-50,50)

def iscollision(enemyx, enemyy, playerx, playeryy,i):
    distance = math.sqrt(math.pow(enemyx[i] - playerx, 2) + math.pow(enemyy[i] - playery, 2))
    if distance < 40:
        return True
    else:
        return False



def player(x, y):
    screen.blit(playerimg, (x, y))
clock=pygame.time.Clock()


def power1(powerup1,power1x,power1y):
    screen.blit(powerup1,(power1x,power1y))
def power2(powerup2,power2x,power2y):
    screen.blit(powerup2,(power2x,power2y))

def power1collision(playerx,playery,power1x,power1y):
    distance = math.sqrt(math.pow(power1x - playerx, 2) + math.pow(power1y - playery, 2))
    if distance < 40:
        return True
    else:
        return False


def power2collision(playerx,playery,power2x,power2y):
    distance = math.sqrt(math.pow(power2x - playerx, 2) + math.pow(power2y - playery, 2))
    if distance < 50:
        return True
    else:
        return False
def enemyremove(enemyx, enemyy, playerx, playeryy,i):
    distance = math.sqrt(math.pow(enemyx[i] - playerx, 2) + math.pow(enemyy[i] - playery, 2))
    if distance < 150:
        l.append(i)
def start_screen_text():
    start_text=font1.render('PRESS SPACEBAR TO START',True,(255,0,0))
    screen.blit(start_text,(100,500))
def showscore(x,y):
    score_text = font1.render('Score:' + str(score), True, (255, 255, 255))
    screen.blit(score_text,(textx,texty))
def gameover():
    gameover_text=font2.render('GAME OVER',True,(0,0,255))
    screen.blit(gameover_text,(400,500))
playername=input('Enter player name')
running_startscreen=True
running = True
while running_startscreen:
    screen.fill((0,0,0))
    start_screen_text()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            running_startscreen=False
            pygame.quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                running_startscreen=False
    pygame.display.update()
while running:
    n+=1
    if n%30==0:
        enemy_number+=1
        enemyx.append(400)
        enemyy.append(500)
        enemyx_change.append(0)
        enemyy_change.append(0)
        enemy_img.append(pygame.image.load('ghost.png'))
        score+=1
    clock.tick(5)
    screen.fill((0, 0, 0))
    power1(powerup1,power1x,power1y)
    power2(powerup2, power2x, power2y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print('keystroke is pressed')
            if event.key == pygame.K_LEFT:
                print('left key pressed')
                playerxchng = -30
            if event.key == pygame.K_RIGHT:
                print('right arrow pressed')
                playerxchng = 30
            if event.key==pygame.K_DOWN:
                playerychng=30
            if event.key==pygame.K_UP:
                playerychng=-30
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print('KEY REL')
                playerxchng = 0
            if event.key==pygame.K_DOWN or event.key==pygame.K_UP:
                playerychng=0
    playerx += playerxchng
    playery += playerychng
    if playerx <= 0:
        playerx = 0
    elif playerx >= 750:
        playerx = 750
    if playery<=0:
        playery=0
    elif playery>=925:
        playery=925
    if power1collision(playerx,playery,power1x,power1y):
        score+=5
        power1x = random.randint(20,750)
        power1y = random.randint(20, 950)
    if power2collision(playerx,playery,power2x,power2y):
        for i in range(enemy_number):
            enemyremove(enemyx,enemyy,playerx,playery,i)
        power2x = random.randint(20, 750)
        power2y = random.randint(20, 950)
    for i in range(enemy_number):
        if i in l:
            continue
        else:
            enemy_movt(i)
            a = random.randint(0, 1)
            if a == 0:
                enemyx[i] += enemyx_change[i]
            else:
                enemyy[i] += enemyy_change[i]

        enemy(enemyx[i],enemyy[i],i)
        if iscollision(enemyx,enemyy,playerx,playery,i):
            t+=1
            print('game over')
            if t==5:
                running = False


    print(score)
    if t>0:
        gameover()
    player(playerx, playery)
    showscore(textx,texty)
    pygame.display.update()


