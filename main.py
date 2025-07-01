import pygame
from pygame import *

WIDTH = 512
HEIGHT = 768

pygame.init()
print("Pygame version:", pygame.__version__)
print(pygame.display.list_modes())

if pygame.display.mode_ok((512,768))!=0:
    screen=pygame.display.set_mode((512,768))
    print("current screen size is ",pygame.display.get_surface())
else:
    print("the screen setting is not supported")
    exit(0)

# 加载背景图
pygame.display.set_caption("坤坤战机")
bg=pygame.image.load("./imgs/start_bg0.jpg")
screen.blit(bg,(0,0)) #将背景图加载到显存中

ZiTi=pygame.font.get_fonts()
for i in ZiTi:
    print(i)

myFont=pygame.font.SysFont("simhei",60)
color=0,0,0
textImage=myFont.render("坤坤战机",True,color)
screen.blit(textImage,(145,100))
color=255,0,0
textImage=myFont.render("坤坤战机",True,color)
screen.blit(textImage,(150,100))

myFont2=pygame.font.SysFont("simhei",25)
color=0,0,0
textImage2=myFont2.render("按WASD控制，按空格发射子弹",True,color)
screen.blit(textImage2,(100,580))

plane=pygame.image.load("./imgs/jet.png").convert_alpha()
screen.blit(plane,((WIDTH-77)/2,400))
start_button=pygame.image.load("./imgs/start.png").convert_alpha()
screen.blit(start_button,((WIDTH-138)/2,600))

ctn=True
while ctn:
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            key_press=pygame.key.get_pressed()
            if key_press[K_SPACE]:
                ctn=False
            elif key_press[K_ESCAPE]:
                pygame.quit()
                exit(0)
        elif event.type==pygame.QUIT:
            ctn=False
    pygame.display.update() #将背景图显示到屏幕上


pygame.quit()