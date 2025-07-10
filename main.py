import pygame
from pygame import *
import random
import cv2
import numpy as np

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
    (startX, startY) = (0, 0)
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
    return image, startX, startY


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./imgs/plane.png").convert_alpha()
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect(midbottom=(WIDTH / 2 + 50, HEIGHT))
        self.life = 5
        self.speed=0.7
        self.dx, self.dy = 0, 0
        self.cooldowntime=0
        self.missiles=pygame.sprite.Group()

    def input(self, inside_dt):
        
        if mode == "keyboard":
            key_press = pygame.key.get_pressed()
            if key_press[K_a] or key_press[K_LEFT]:  # left
                self.dx = -self.speed * inside_dt
            elif key_press[K_d] or key_press[K_RIGHT]:  # right
                self.dx = self.speed * inside_dt
            elif key_press[K_s] or key_press[K_DOWN]:  # down
                self.dy = self.speed * inside_dt
            elif key_press[K_w] or key_press[K_UP]:  # up
                self.dy = -self.speed * inside_dt
        if mode == "mouse":
            mouse_press = pygame.mouse.get_pressed()
            if mouse_press == (1, 0, 0):
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < self.rect.x:
                    self.dx = -self.speed * dt
                elif mouse_pos[0] > self.rect.x + self.w:
                    self.dx = self.speed * dt
                if mouse_pos[1] < self.rect.y:
                    self.dy = -self.speed * dt
                elif mouse_pos[1] > self.rect.y + self.h:
                    self.dy = self.speed * dt
        if mode == "face":
            ret, frame = cap.read()
            if not ret:
                return
            output, self.rect.x, self.rect.y = detect_faces_dnn(frame)
            self.rect.x, self.rect.y = (self.rect.x / 640) * WIDTH, (self.rect.y / 480) * HEIGHT
            cv2.imshow("Real-Time DNN Face Detection", output)

    def shoot(self):
        key_press=pygame.key.get_pressed()
        if key_press[K_SPACE] and self.cooldowntime == 0:
            self.missiles.add(Missile(self.rect.centerx,self.rect.y))
            self.cooldowntime=15

    def update(self, dt):
        self.input(dt)
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dx, self.dy = 0, 0
        self.rect.x = max(0, min(WIDTH - self.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.h, self.rect.y))
        self.missiles.update()
        if self.cooldowntime>0:
            self.cooldowntime-=1


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./imgs/alien_" + str(random.randint(1, 5)) + ".png").convert_alpha()
        self.w, self.h = self.image.get_width(), self.image.get_height()
        x,y=random.randint(0, WIDTH-self.w), -150
        self.rect = self.image.get_rect(topleft=(x,y))
        self.speed = 5

        self.bullets=pygame.sprite.Group()
        self.bullet_spawn_interval=150
        self.bullet_spawn_timer=self.bullet_spawn_interval-1

    def update(self):
        self.rect.y += self.speed
        self.bullet_spawn_timer+=1
        if self.bullet_spawn_timer >=self.bullet_spawn_interval:
            self.bullet_spawn_timer=0
            self.bullets.add(Bullet(self.rect.centerx,self.rect.y))
        self.bullets.update()
        if self.rect.y > HEIGHT:
            self.kill()

    def kill(self):
        for bullet in self.bullets:
            bullet.kill()
        super().kill()

class Enemies:
    def __init__(self):
        self.enemy_group=pygame.sprite.Group()
        self.spawn_timer=0
        self.spawn_interval=180

    def spawn_enemy(self):
        self.enemy_group.add(Enemy())

    def update(self):
        self.spawn_timer += 1
        if  self.spawn_timer >= self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer=0
        self.enemy_group.update()
    def draw(self):
        self.enemy_group.draw(screen)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("./imgs/bullet.png").convert_alpha()
        self.rect=self.image.get_rect(center=(x,y))
        self.speed=8
    
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y>=HEIGHT:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("./imgs/bullet_1.png").convert_alpha()
        self.rect=self.image.get_rect(center=(x,y))
        self.speed=9
    
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y<=0:
            self.kill()

WIDTH = 512
HEIGHT = 768

pygame.init()  # 初始化pygame库
print("Pygame version:", pygame.__version__)

cap = cv2.VideoCapture(0)

if pygame.display.mode_ok((512, 768)) != 0:
    screen = pygame.display.set_mode((512, 768))
    print("current screen size is ", pygame.display.get_surface())
else:
    print("the screen setting is not supported")
    exit(0)

pygame.display.set_caption("雷电战机")
mode = "keyboard"  # 模式1为键盘控制，模式2为鼠标控制，模式3为人脸识别控制
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
    textImage = myFont.render("雷电战机", True, black)
    screen.blit(textImage, (145, 100))
    textImage1 = myFont.render("雷电战机", True, red)
    screen.blit(textImage1, (150, 100))

    myFont2 = pygame.font.SysFont("simhei", 25)
    textImage2 = myFont2.render("按WASD控制，按space发射子弹", True, black)
    screen.blit(textImage2, (100, 580))

    myFont3 = pygame.font.SysFont("simhei", 25)
    textImage3 = myFont3.render("按1键盘控制，按2鼠标控制，按3人脸识别控制", True, black)
    screen.blit(textImage3, (0, 560))

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
                    mode = "keyboard"
                elif key_press[K_2]:
                    mode = "mouse"
                elif key_press[K_3]:
                    mode = "face"
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
    STEP = 5
    current_score = 0
    clock = pygame.time.Clock()

    bg = pygame.image.load("./imgs/map1.jpg").convert_alpha()

    plane1 = pygame.sprite.GroupSingle()
    plane1.add(Player())
    enemies=Enemies()
    all_enemies_bullets=pygame.sprite.Group()
    all_missiles=pygame.sprite.Group()
    player=plane1.sprite

    #加载人脸识别模型
    model_weights = "./models/res10_300x300_ssd_iter_140000.caffemodel"
    model_config = "./models/deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(model_config, model_weights)
    
    ctn = True
    while ctn:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit(0)
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        plane1.update(dt)
        enemies.update()
        for enemy in enemies.enemy_group: #收集每架敌机的子弹
            all_enemies_bullets.add(enemy.bullets)
        player.shoot()
        for missile1 in player.missiles:
            all_missiles.add(missile1)

        # 碰撞检测
        if len(enemies.enemy_group)>0 and len(all_missiles): #检测导弹与敌机的碰撞
            collisions=pygame.sprite.groupcollide(
                all_missiles,
                enemies.enemy_group,
                True,
                True,
            )
            if collisions:
                for missile,hit_enemy in collisions.items(): 
                    current_score+=len(hit_enemy)

        if len(all_enemies_bullets)>0 and len(all_missiles): #检测导弹与子弹的碰撞
            collisions=pygame.sprite.groupcollide(
                all_missiles,
                all_enemies_bullets,
                True,
                True,
            )

        if  len(all_enemies_bullets): #检测玩家与子弹的碰撞
            collisions=pygame.sprite.spritecollide(
                player,
                all_enemies_bullets,
                True,
            )
            if collisions:
                for hit_bullet in collisions: 
                    player.life-=1
                    print(f"current life is {player.life}")
                    if player.life==0:
                        ctn=False

        if len(enemies.enemy_group)>0: #检测玩家与敌机的碰撞
            collisions=pygame.sprite.spritecollide(
                player,
                enemies.enemy_group,
                True,
            )
            if collisions:
                for hit_enemy in collisions: 
                    player.life-=1
                    print(f"current life is {player.life}")
                    if player.life==0:
                        ctn=False
        #更新画面
        screen.blit(bg, (0, 0))
        show_score = myFont.render(f"{current_score}", True, ground_yellow)
        screen.blit(show_score, (WIDTH - 400, 0))
        plane1.draw(screen)
        all_enemies_bullets.draw(screen)
        all_missiles.draw(screen)
        enemies.draw()
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
