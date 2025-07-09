import pygame
from pygame import *
import random
import cv2
import numpy as np


def collision(x1, y1, w1, h1, x2, y2, w2, h2):
    if abs(x1 - x2) < (w1 + w2) and abs(y1 - y2) < (h1 + h2):
        return True
    else:
        return False

def detect_faces_dnn(image, min_confidence=0.5):
    """
    使用DNN检测人脸
    :param image: 输入图像（BGR格式）
    :param min_confidence: 置信度阈值
    :return: 带检测框的图像
    """
    (h, w) = image.shape[:2]
    # 预处理：缩放 + 均值减法 (104, 177, 123)
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)),
        scalefactor=1.0,
        size=(300, 300),
        mean=(104.0, 177.0, 123.0)
    )
    # 输入网络并获取检测结果
    net.setInput(blob)
    detections = net.forward()
    # 绘制检测框
    (startX, startY) = (0,0)
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > min_confidence:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            print((startX, startY), (endX, endY))
            # 绘制矩形和置信度
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(image, text, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    return image,startX,startY

WIDTH = 512
HEIGHT = 768

pygame.init()  # 初始化pygame库
print("Pygame version:", pygame.__version__)

cap = cv2.VideoCapture(0) #width:.640.0 height:480

if pygame.display.mode_ok((512, 768)) != 0:
    screen = pygame.display.set_mode((512, 768))
    print("current screen size is ", pygame.display.get_surface())
else:
    print("the screen setting is not supported")
    exit(0)

pygame.display.set_caption("坤坤战机")
mode=0 #模式1为键盘控制，模式2为鼠标控制，模式3为人脸识别控制
running = True
while running:

    # ------------------Page 1---------------------------

    # 加载背景图
    bg = pygame.image.load("./imgs/start_bg0.jpg")
    screen.blit(bg, (0, 0))  # 将背景图加载到显存中

    black = 0, 0, 0
    ground_yellow = 210, 180, 100
    red = 255, 0, 0
    myFont = pygame.font.SysFont("simhei", 60)
    textImage = myFont.render("坤坤战机", True, black)
    screen.blit(textImage, (145, 100))
    textImage1 = myFont.render("坤坤战机", True, red)
    screen.blit(textImage1, (150, 100))

    myFont2 = pygame.font.SysFont("simhei", 25)
    textImage2 = myFont2.render("按WASD控制，按space发射子弹", True, black)
    screen.blit(textImage2, (100, 580))

    plane = pygame.image.load("./imgs/jet.png").convert_alpha()
    screen.blit(plane, ((WIDTH - 77) / 2, 400))
    start_button = pygame.image.load("./imgs/start.png").convert_alpha()
    start_button_x, start_button_y = (WIDTH - 138) / 2, 600
    start_button_W, start_button_H = start_button.get_width(), start_button.get_height()
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
                elif key_press[K_1]:
                    mode=0
                elif key_press[K_2]:
                    mode=1
                elif key_press[K_3]:
                    mode=2
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_x <= mouse_pos[0] <= start_button_x + start_button_W and start_button_y <= mouse_pos[
                    1] <= start_button_y + start_button_H:
                    ctn = False
        pygame.display.update()  # 将背景图显示到屏幕上

    # -------------Page 2----------------------
    PLANE_WIDTH = 100
    PLANE_HEIGHT = 148
    STEP = 5
    SPEED = 0.3

    bg = pygame.image.load("./imgs/map1.jpg").convert_alpha()
    plane = pygame.image.load("./imgs/plane.png").convert_alpha()
    plane_x, plane_y = (WIDTH - PLANE_WIDTH) / 2, HEIGHT - PLANE_HEIGHT
    plane_life = 100000

    model_weights = "./models/res10_300x300_ssd_iter_140000.caffemodel"
    model_config = "./models/deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(model_config, model_weights)

    enemy = pygame.image.load("./imgs/alien_" + str(random.randint(1, 5)) + ".png").convert_alpha()
    enemy_W, enemy_H = enemy.get_width(), enemy.get_height()
    enemy_x, enemy_y = random.randint(0, WIDTH - enemy_W), -150
    enemy_event = pygame.USEREVENT
    pygame.time.set_timer(enemy_event, 7)

    bullet = pygame.image.load("./imgs/bullet.png").convert_alpha()
    bullet_W, bullet_H = 44, 48
    bullet_x, bullet_y = enemy_x + enemy_W / 2 - bullet_W / 2, enemy_y + enemy_H / 2
    bullet_event = pygame.USEREVENT + 1
    pygame.time.set_timer(bullet_event, 5)

    missile = pygame.image.load("./imgs/bullet_1.png").convert_alpha()
    missile_W, missile_H = 37, 32
    missile_x, missile_y = plane_x + (PLANE_WIDTH / 2), plane_y
    missile_event = pygame.USEREVENT + 2
    pygame.time.set_timer(missile_event, 1)

    current_score = 0
    dx, dy = 0, 0

    clock = pygame.time.Clock()

    ctn = True
    missile_shot = False
    while ctn:
        dx, dy = 0, 0
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not missile_shot:
                        missile_shot = True
                        missile_x, missile_y = plane_x + (PLANE_WIDTH / 2), plane_y
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit(0)
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == enemy_event:
                if enemy_y == HEIGHT:
                    enemy = pygame.image.load("./imgs/alien_" + str(random.randint(1, 5)) + ".png").convert_alpha()
                    enemy_x, enemy_y = random.randint(0, WIDTH - enemy_W), -150
                else:
                    enemy_y += 1
            elif event.type == bullet_event:
                bullet_y += 1
                if bullet_y > HEIGHT:
                    bullet_x, bullet_y = enemy_x + enemy_W / 2 - bullet_W / 2, enemy_y + enemy_H / 2
            elif event.type == missile_event and missile_shot:
                missile_y -= 1
                if missile_y <= 0:
                    missile_shot = False
            if event.type == pygame.MOUSEBUTTONDOWN and mode==1:
                mouse_press = pygame.mouse.get_pressed()
                if mouse_press == (1, 0, 0):
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] < plane_x:
                        dx = -SPEED * dt
                    elif mouse_pos[0] > plane_x + PLANE_WIDTH:
                        dx = SPEED * dt
                    if mouse_pos[1] < plane_y:
                        dy = -SPEED * dt
                    elif mouse_pos[1] > plane_y + PLANE_HEIGHT:
                        dy = SPEED * dt
        key_press = pygame.key.get_pressed()
        if mode==0:
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

        plane_x, plane_y = plane_x + dx, plane_y + dy
        if mode==2:
            ret, frame = cap.read()
            if not ret:
                break
            output,plane_x,plane_y = detect_faces_dnn(frame)
            plane_x,plane_y=(plane_x/640)*WIDTH,(plane_y/480)*HEIGHT
            cv2.imshow("Real-Time DNN Face Detection", output)
        plane_x = max(0, min(WIDTH - PLANE_WIDTH, plane_x))
        plane_y = max(0, min(HEIGHT - PLANE_HEIGHT, plane_y))
        screen.blit(bg, (0, 0))
        if missile_shot:
            screen.blit(missile, (missile_x, missile_y))

        if collision(missile_x, missile_y, missile_W, missile_H, enemy_x, enemy_y, enemy_W, enemy_H):
            missile_shot = False
            enemy_x, enemy_y = random.randint(0, WIDTH - enemy_W), -150
            current_score += 1
        if collision(bullet_x, bullet_y, bullet_W, bullet_H, plane_x, plane_y, PLANE_WIDTH, PLANE_HEIGHT):
            plane_life -= 1
            print(f"Constant life is {plane_life}! Pay attention!")
            if plane_life <= 0:
                print("Game Over!")
                ctn = False
            bullet_x, bullet_y = enemy_x + enemy_W / 2 - bullet_W / 2, enemy_y + enemy_H / 2
        if collision(missile_x, missile_y, missile_W, missile_H, bullet_x, bullet_y, bullet_W, bullet_H):
            missile_shot = False
            bullet_x, bullet_y = enemy_x + enemy_W / 2 - bullet_W / 2, enemy_y + enemy_H / 2
            missile_y = -1000
        if collision(enemy_x, enemy_y, enemy_W, enemy_H, plane_x, plane_y, PLANE_WIDTH, PLANE_HEIGHT):
            plane_life -= 1
            print(f"Constant life is {plane_life}! Pay attention!")
            if plane_life <= 0:
                print("Game Over!")
                ctn = False
            enemy = pygame.image.load("./imgs/alien_" + str(random.randint(1, 5)) + ".png").convert_alpha()
            enemy_x, enemy_y = random.randint(0, WIDTH - enemy_W), -150
        show_score = myFont.render(f"{current_score}", True, ground_yellow)
        screen.blit(show_score, (WIDTH - 400, 0))
        screen.blit(bullet, (bullet_x, bullet_y))
        screen.blit(enemy, (enemy_x, enemy_y))
        screen.blit(plane, (plane_x, plane_y))
        pygame.display.update()  # 将背景图显示到屏幕上

    # ------------------Page 3----------------

    restart_button = pygame.image.load("./imgs/restart.png").convert_alpha()
    restart_button_x, restart_button_y = WIDTH / 2 - restart_button.get_width() / 2, HEIGHT / 2 + 50
    restart_button_W, restart_button_H = restart_button.get_width(), restart_button.get_height()
    ctn = True
    while ctn:
        bg = pygame.image.load("./imgs/map2.jpg").convert_alpha()
        txt_GameOver = pygame.image.load("./imgs/gameover.png").convert_alpha()
        txt_GameOver_x, txt_GameOver_y = 192, 42
        final_score = myFont.render("Score: " + str(current_score), True, ground_yellow)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    ctn = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_x <= mouse_pos[0] <= restart_button_x + restart_button_W and restart_button_y <= \
                        mouse_pos[
                            1] <= restart_button_y + restart_button_H:
                    ctn = False

        screen.blit(bg, (0, 0))
        screen.blit(txt_GameOver, (WIDTH / 2 - txt_GameOver_x / 2, HEIGHT / 2 - 100))
        screen.blit(final_score, (WIDTH / 2 - txt_GameOver_x / 2 - 25, HEIGHT / 2 - 50))
        screen.blit(restart_button, (restart_button_x, restart_button_y))
        pygame.display.update()
cap.release()
cv2.destroyAllWindows()
pygame.quit()
exit(0)
