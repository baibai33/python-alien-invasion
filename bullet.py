import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""

    def __init__(self, ai_game, image):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image_prep = image
        self.image = pygame.image.load(self.image_prep)
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)


class Jineng1(Bullet):
    def __init__(self, ai_game, image):
        super().__init__(ai_game, image)

    def update(self, x):
        """各方位移动子弹"""
        self.x += x
        self.y -= self.settings.bullet_speed
        self.rect.x = self.x
        self.rect.y = self.y


class Jineng2_1duan(Bullet):
    pass


class Jineng2_2duan(Bullet):
    def __init__(self, ai_game, image, mubiao):
        super().__init__(ai_game, image)
        self.rect.midtop = mubiao.rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, x, y):
        self.x += x
        self.y += y
        self.rect.x = self.x
        self.rect.y = self.y


class Heimao_bullet(Bullet):
    def __init__(self, ai_game, image, alien):
        super().__init__(ai_game, image)
        self.rect.midbottom = alien.rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.heimao_bullet_speed
        self.rect.y = self.y


print(Jineng1.__mro__)
