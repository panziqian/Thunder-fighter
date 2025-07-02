import pygame
from pygame import *

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
PLANE_HIGHT = 148
STEP = 5
SPEED = 0.3

x, y = (WIDTH - PLANE_WIDTH) / 2, HEIGHT - PLANE_HIGHT
dx, dy = 0, 0

bg = pygame.image.load("./imgs/map1.jpg").convert_alpha()
plane = pygame.image.load("./imgs/plane.png").convert_alpha()

clock = pygame.time.Clock()

ctn = True
while ctn:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
        elif event.type == pygame.QUIT:
            ctn = False

    dx, dy = 0, 0
    key_press = pygame.key.get_pressed()
    if key_press[K_SPACE]:  # space
        ctn = True
    elif (key_press[K_a] or key_press[K_LEFT]) and x - STEP > 0:  # left
        dx = -SPEED * dt
        # x -= STEP
    elif (key_press[K_d] or key_press[K_RIGHT]) and x + STEP < WIDTH - PLANE_WIDTH:  # right
        dx = SPEED * dt
        # x += STEP
    elif (key_press[K_s] or key_press[K_DOWN]) and y + STEP < HEIGHT - PLANE_HIGHT:  # down
        dy = SPEED * dt
        # y += STEP
    elif (key_press[K_w] or key_press[K_UP]) and y - STEP > 0:  # up
        dy = -SPEED * dt
        # y -= STEP

    x, y = x + dx, y + dy
    x = max(0, min(WIDTH - PLANE_WIDTH, x))
    y = max(0, min(HEIGHT - PLANE_HIGHT, y))
    screen.blit(bg, (0, 0))
    screen.blit(plane, (x, y))
    pygame.display.update()  # 将背景图显示到屏幕上

pygame.quit()
