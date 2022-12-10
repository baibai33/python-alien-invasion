import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game, image):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image_prep = image
        self.image = pygame.image.load(self.image_prep)
        self.rect = self.image.get_rect()

        # 每个外星人最初在屏幕左上角附近
        self.rect.x = self.rect.width - 100
        self.rect.y = self.rect.height - 100
        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """移动"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def a_check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


class Miaobis(Alien):
    def __init__(self, ai_game, image):
        super().__init__(ai_game, image)
        self.create_time = 0
        # 每个喵币最初在屏幕左上角附近
        self.rect.x = self.rect.width - 150
        self.rect.y = self.rect.height - 150
        # 存储喵币的精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """移动"""
        self.y += self.settings.miaobi_speed
        self.rect.y = self.y


class Boss1(Alien):
    def __init__(self, ai_game, image):
        super().__init__(ai_game, image)
        self.hp = 50
        self.rect.midtop = self.screen.get_rect().midtop
        self.rect.y = -100
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.boss1_speed
        self.rect.y = self.y

    def __repr__(self):
        return 'hp:%r' % (self.hp)
