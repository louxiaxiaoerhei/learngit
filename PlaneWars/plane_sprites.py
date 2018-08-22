import pygame
import random

# 定义屏幕常量
SCREEN_RECT = pygame.Rect(0, 0, 400, 600)
# 定义帧率常量
FRAME_PER_SEC = 60
# 英雄机初始位置
HERO_RECT = pygame.Rect(170, 400, 120, 80)
# 定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1, hp = 5):
        # 调用父类初始化方法
        super().__init__()
        # 定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = pygame.Rect(self.image.get_rect())
        self.speed = speed
        self.hp = hp

    def update(self):
        # 在屏幕上向上移动
        self.rect.y += self.speed
        if self.hp == 0:
            self.kill()


class Background(GameSprite):
    """背景游戏精灵"""

    def __init__(self):
        super().__init__("./image/background/background_2.png")
        self.rect.y = SCREEN_RECT.height - self.rect.height

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 0:
            self.rect.y = SCREEN_RECT.height - self.rect.height


class HeroSprite(GameSprite):
    """英雄机游戏精灵"""

    def __init__(self, image_name="./image/1s.png"):
        super().__init__(image_name)
        self.rect = HERO_RECT
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()


    def update(self):
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= SCREEN_RECT.width - self.rect.width:
            self.rect.x = SCREEN_RECT.width - self.rect.width
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y >= SCREEN_RECT.height - self.rect.height:
            self.rect.y = SCREEN_RECT.height - self.rect.height

    def fire(self):
        bullet = BulletSprite(speed=-6)
        bullet.rect.x = self.rect.x
        bullet.rect.y = self.rect.y
        self.bullets.add(bullet)
        bullet1 = BulletSprite(speed=-6)
        bullet1.rect.x = self.rect.x + self.rect.width - bullet1.rect.width
        bullet1.rect.y = self.rect.y
        self.bullets.add(bullet1)
        bullet2 = BulletSprite(image_name="./image/bullet/bullet_2.png",speed=-8)
        bullet2.rect.x = self.rect.x + self.rect.width/2 - bullet2.rect.width/2
        bullet2.rect.y = self.rect.y
        self.bullets.add(bullet2)


    def fire1(self):
        rocketSprite = RocketSprite(speed=-6)
        rocketSprite.rect.x = self.rect.x
        rocketSprite.rect.y = self.rect.y
        self.rockets.add(rocketSprite)
        rocketSprite1 = RocketSprite(speed=-6,islift=True)
        rocketSprite1.rect.x = self.rect.x + self.rect.width - rocketSprite1.rect.width
        rocketSprite1.rect.y = self.rect.y
        self.rockets.add(rocketSprite1)


class EnemySprite(GameSprite):
    """敌机游戏精灵"""

    def __init__(self, image_name, speed=1, hp = 5):
        super().__init__(image_name, speed, hp)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        super().update()
        # self.rect.x += 1
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()


class BulletSprite(GameSprite):
    """子弹精灵"""

    def __init__(self, image_name="./image/bullet/bullet_1.png", speed=-2):
        super().__init__(image_name, speed)

    def update(self):
        super().update()
        if self.rect.bottom <= 0:
            self.kill()


class RocketSprite(GameSprite):
    """火箭精灵"""
    def __init__(self, image_name="./image/bullet/bullet_5.png", speed=-2, islift = False):
        super().__init__(image_name, speed)
        self.islift = islift

    def update(self):
        super().update()
        if self.islift:
            self.rect.x += 2
        else:
            self.rect.x -= 2
        if self.rect.bottom <= 0:
            self.kill()

def groupcollide(groupa, groupb, dokilla, dokillb, collided=None):

    crashed = {}
    SC = pygame.sprite.spritecollide
    if dokilla:
        for s in groupa.sprites():
            c = SC(s, groupb, dokillb, collided)
            if c:
                crashed[s] = c
                s.hp -= 1
                if s.hp == 0:
                    s.kill()
    else:
        for s in groupa:
            c = SC(s, groupb, dokillb, collided)
            if c:
                crashed[s] = c
    return crashed