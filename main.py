import pygame
from pygame import *
import random

WIDTH = 512
HEIGHT = 768

pygame.init()  # 初始化pygame库
print("Pygame version:", pygame.__version__)
# print(pygame.display.list_modes())

if pygame.display.mode_ok((512, 768)) != 0:
    screen = pygame.display.set_mode((512, 768))
    print("current screen size is ", pygame.display.get_surface())
else:
    print("the screen setting is not supported")
    exit(0)

pygame.display.set_caption("坤坤战机")

# ------------------Page 1---------------------------

# 加载背景图
bg = pygame.image.load("./imgs/start_bg0.jpg")
screen.blit(bg, (0, 0))  # 将背景图加载到显存中

myFont = pygame.font.SysFont("simhei", 60)
color = 0, 0, 0
textImage = myFont.render("坤坤战机", True, color)
screen.blit(textImage, (145, 100))
color = 255, 0, 0
textImage1 = myFont.render("坤坤战机", True, color)
screen.blit(textImage1, (150, 100))

myFont2 = pygame.font.SysFont("simhei", 25)
color = 0, 0, 0
textImage2 = myFont2.render("按WASD控制，按space发射子弹", True, color)
screen.blit(textImage2, (100, 580))

plane = pygame.image.load("./imgs/jet.png").convert_alpha()
screen.blit(plane, ((WIDTH - 77) / 2, 400))
start_button = pygame.image.load("./imgs/start.png").convert_alpha()
screen.blit(start_button, ((WIDTH - 138) / 2, 600))

ctn = True
while ctn:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            key_press = pygame.key.get_pressed()
            if key_press[K_SPACE]:
                ctn = False
            elif key_press[K_ESCAPE]:
                pygame.quit()
                exit(0)
        elif event.type == pygame.QUIT:
            ctn = False
    pygame.display.update()  # 将背景图显示到屏幕上

# -------------Page 2----------------------
PLANE_WIDTH = 100
PLANE_HEIGHT = 148
STEP = 5
SPEED = 0.3

bg = pygame.image.load("./imgs/map1.jpg").convert_alpha()
plane = pygame.image.load("./imgs/plane.png").convert_alpha()
x, y = (WIDTH - PLANE_WIDTH) / 2, HEIGHT - PLANE_HEIGHT

enemy = pygame.image.load("./imgs/alien_" + str(random.randint(1, 5)) + ".png").convert_alpha()
enemy_W, enemy_H = 128, 128
enemy_x, enemy_y = random.randint(0, WIDTH - enemy_W), -150
enemy_event = pygame.USEREVENT
pygame.time.set_timer(enemy_event, 10)

bullet = pygame.image.load("./imgs/bullet.png").convert_alpha()
bullet_W, bullet_H = 44, 48
bullet_x, bullet_y = enemy_x + (enemy_W / 2) - bullet_W / 2, enemy_y + enemy_H / 2
bullet_event = pygame.USEREVENT + 1
pygame.time.set_timer(bullet_event, 3)

missile = pygame.image.load("./imgs/bullet_1.png").convert_alpha()
missile_W, missile_H = 37, 32
missile_x, missile_y = x + (PLANE_WIDTH / 2), y
missile_event = pygame.USEREVENT + 2
pygame.time.set_timer(missile_event, 5)

dx, dy = 0, 0

clock = pygame.time.Clock()

ctn = True
missile_shot=False
while ctn:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if missile_shot == False:
                    missile_shot = True
                    missile_x, missile_y = x + (PLANE_WIDTH / 2), y
            if event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
        elif event.type == pygame.QUIT:
            ctn = False
        elif event.type == enemy_event:
            if enemy_y == HEIGHT:
                enemy = pygame.image.load("./imgs/alien_" + str(random.randint(1, 5)) + ".png").convert_alpha()
                enemy_x = random.randint(0, WIDTH - enemy_W)
                enemy_y = -150
            else:
                enemy_y += 1
        elif event.type == bullet_event:
            bullet_y += 1
            if bullet_y > HEIGHT:
                bullet_x, bullet_y = enemy_x + (enemy_W / 2) - bullet_W / 2, enemy_y + enemy_H / 2
        elif event.type == missile_event and missile_shot:
            missile_y -= 1
            if missile_y <= 0:
                missile_shot = False
        print(missile_x, missile_y)

    dx, dy = 0, 0
    key_press = pygame.key.get_pressed()
    if key_press[K_SPACE]:  # space
        ctn = True
    elif key_press[K_a] or key_press[K_LEFT]:  # left
        dx = -SPEED * dt
    elif key_press[K_d] or key_press[K_RIGHT]:  # right
        dx = SPEED * dt
    elif key_press[K_s] or key_press[K_DOWN]:  # down
        dy = SPEED * dt
    elif key_press[K_w] or key_press[K_UP]:  # up
        dy = -SPEED * dt

    x, y = x + dx, y + dy
    x = max(0, min(WIDTH - PLANE_WIDTH, x))
    y = max(0, min(HEIGHT - PLANE_HEIGHT, y))
    screen.blit(bg, (0, 0))
    if missile_shot:
        screen.blit(missile, (missile_x, missile_y))
    screen.blit(bullet, (bullet_x, bullet_y))
    screen.blit(enemy, (enemy_x, enemy_y))
    screen.blit(plane, (x, y))
    pygame.display.update()  # 将背景图显示到屏幕上

pygame.quit()
