# 以下为烟花绽放完整代码：

#  模块导入
import pygame, math, random
from sys import exit

#  定义相关初始
#  win定义窗口大小（窗口的w=宽，h=高）
WIN_W = 2200
WIN_H = 1300
#  定义时间、显示、频率
t1 = 0.18   #  时间流速
show_n = 0
show_frequency = 0.0015    #  烟花绽放频率，数值越大频率越高

#  烟花颜色列表，下面随机抽出，红色、绿色、蓝色、黄色、紫色、天蓝色、白色
color_list = [
                [255, 50, 50],
                [50, 255, 50],
                [50, 50, 255],
                [255, 255, 50],
                [255, 50, 255],
                [50, 255, 255],
                [255, 255, 255]
             ]

#  初始化pygame
pygame.init()

#  创建一个窗口,可调节大小的pygame.RESIZABLE窗口和标题
screen = pygame.display.set_mode((WIN_W, WIN_H),pygame.RESIZABLE, 32)
pygame.display.set_caption("绽放烟花")

# 加载字体
font = pygame.font.Font(None, 36)

#  Fireworks=烟花，定义主类
class Fireworks():
    #  定义主类中的各个参数
    is_show = False
    x, y = 0, 0
    vy = 0
    p_list = []
    color = [0, 0, 0]
    v = 0

    def __init__(self, x, y, vy, n=300, color=[0, 255, 0], v=10):
        self.x = x
        self.y = y
        self.vy = vy
        self.color = color
        self.v = v
        for i in range(n):
            self.p_list.append([random.random() * 2 * math.pi, 0, v * math.pow(random.random(), 1 / 3)])

    def again(self):
        self.is_show = True
        self.x = random.randint(WIN_W // 2 - 350, WIN_W // 2 + 350)
        self.y = random.randint(int(WIN_H / 2), int(WIN_H * 3 / 5))
        self.vy = -40 * (random.random() * 0.4 + 0.8) - self.vy * 0.2
        self.color = color_list[random.randint(0, len(color_list) - 1)].copy()
        n = len(self.p_list)
        self.p_list = []
        for i in range(n):
            self.p_list.append([random.random() * 2 * math.pi, 0, self.v * math.pow(random.random(), 1 / 3)])

    def run(self):
        global show_n
        for p in self.p_list:
            p[1] = p[1] + (random.random() * 0.6 + 0.7) * p[2]
            p[2] = p[2] * 0.97
            if p[2] < 1.2:
                self.color[0] *= 0.9999
                self.color[1] *= 0.9999
                self.color[2] *= 0.9999

            if max(self.color) < 10 or self.y>WIN_H+p[1]:
                show_n -= 1
                self.is_show = False
                break
        self.vy += 10 * t1
        self.y += self.vy * t1

#  烟花列表，调用主类
fk_list = []
fk_list.append(Fireworks(300, 300, -20, n=100, color=[0, 255, 0], v=10))
fk_list.append(Fireworks(300, 300, -20, n=200, color=[0, 0, 255], v=11))
fk_list.append(Fireworks(300, 300, -20, n=200, color=[0, 0, 255], v=12))
fk_list.append(Fireworks(300, 300, -20, n=500, color=[0, 0, 255], v=12))
fk_list.append(Fireworks(300, 300, -20, n=600, color=[0, 0, 255], v=13))
fk_list.append(Fireworks(300, 300, -20, n=700, color=[255, 0, 0], v=15))
fk_list.append(Fireworks(300, 300, -20, n=800, color=[255, 255, 0], v=18))
clock = pygame.time.Clock()

#  烟花放送（游戏）的主循环：
while True:
    for event in pygame.event.get():
        #  pygame这个不能少，否则退出还在循环
        if event.type == pygame.QUIT:
            exit()

    screen.fill((0, 0, 0))
    # 创建字体表面
    text_surface = font.render('Hello, Pygame!', True, (0, 0, 0))

    # 将字体表面放置在屏幕上的指定位置
    screen.blit(text_surface, (100, 100))

    # 放烟花
    for i, fk in enumerate(fk_list):
        if not fk.is_show:
            fk.is_show = False
            if random.random() < show_frequency * (len(fk_list) - show_n):
                show_n += 1
                fk.again()
            continue
        fk.run()
        for p in fk.p_list:
            x, y = fk.x + p[1] * math.cos(p[0]), fk.y + p[1] * math.sin(p[0])
            if random.random() < 0.055:
                screen.set_at((int(x), int(y)),(255,255,255))
            else:
                screen.set_at((int(x), int(y)), (int(fk.color[0]), int(fk.color[1]), int(fk.color[2])))
    pygame.display.update()
