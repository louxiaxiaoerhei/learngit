import pygame
from plane_sprites import *
import sys


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化...")
        pygame.init()
        pygame.display.set_icon(pygame.image.load("image/award/award_2.png"))
        #  1.创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption("打飞机1.0")
        # self.game_font = pygame.font.SysFont("华文仿宋", 16, True)
        # font_list =pygame.font.get_fonts()
        # print(font_list)
        # 2.创建游戏时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法
        self.__create_sprites()
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 200)
        pygame.time.set_timer(HERO_FIRE_EVENT, 100)
        self.moving = False
        self.score = 0
        self.font = pygame.font.SysFont("SimHei", 25)


    def __create_sprites(self):
        # 创建背景精灵
        bg = Background()
        self.back_group = pygame.sprite.Group(bg)
        # 创建英雄机的精灵
        self.hero = HeroSprite()
        self.hero_group = pygame.sprite.Group(self.hero)
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

    def start_game(self):
        print("开始游戏...")

        while True:
            # 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__check_collide()
            # 更新/绘制精灵组
            self.__update_sprites()
            self.textobj = self.font.render("得分：%d" % self.score, 1, (255, 255, 255))
            # 设置文字矩形对象位置
            self.textrect = self.textobj.get_rect(centerx=300, centery=30)
            # 在指定位置绘制指定文字对象
            self.screen.blit(self.textobj, self.textrect)
            # 更新显示
            pygame.display.update()

    def __event_handler(self):
        # 监听上下左右按钮点击
        pressed = pygame.key.get_pressed()
        position = pygame.mouse.get_pos()
        # up
        if pressed[pygame.K_UP]:
            self.hero.rect.y -= 5
        # down
        if pressed[pygame.K_DOWN]:
            self.hero.rect.y += 5
        # left
        if pressed[pygame.K_LEFT]:
            self.hero.rect.x -= 5
        # right
        if pressed[pygame.K_RIGHT]:
            self.hero.rect.x += 5

        # 捕获事件
        even_list = pygame.event.get()
        for event in even_list:
            # 判断是否点击了关闭按钮
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                temp = random.randint(2, 6)
                enemy = EnemySprite("./image/LittlePlane/plane%s.png" % str(temp), speed=temp, hp=12 - temp)
                self.enemy_group.add(enemy)
            elif event.type == pygame.MOUSEBUTTONDOWN and position[0] > self.hero.rect.x and position[0] < self.hero.rect.x + self.hero.rect.width and position[1] > self.hero.rect.y and position[1] < self.hero.rect.y + self.hero.rect.height:  # 获取点击鼠标事件
                if event.button == 1:  # 点击鼠标左键
                    self.moving = True
            elif event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                if event.button == 1:  # 松开鼠标左键
                    self.moving = False
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
                pass
            elif event.type == pygame.KEYDOWN:
                # 监听按钮点击
                if event.type == pygame.KEYDOWN:
                    # 如果是esc键 -> 退出游戏
                    if event.key == pygame.K_ESCAPE:
                        self.__game_over()

                    # 如果是空格键 -> 发射子弹
                    if event.key == pygame.K_SPACE:
                        self.hero.fire1()

            if self.moving:
                self.hero.rect.x = position[0] - self.hero.rect.width / 2
                self.hero.rect.y = position[1] - self.hero.rect.height / 2

    def __check_collide(self):
        enemy = groupcollide(self.enemy_group,self.hero.bullets, True, True)
        enemy1 = pygame.sprite.groupcollide(self.hero.rockets, self.enemy_group, True, True)
        if len(enemy1) > 0:
            self.score += len(enemy)
            # print(self.score)

    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
        self.hero.rockets.update()
        self.hero.rockets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束...")
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()
    # 开始游戏
    game.start_game()
