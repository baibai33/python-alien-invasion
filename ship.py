import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game, image):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.bianshen_time = 0
        self.suoxiao_time = 0
        # 加载飞船图像并获取其外接矩形
        self.image_prep = image
        self.image = pygame.image.load(self.image_prep)
        self.rect = self.image.get_rect()
        # 对于每艘飞船，都将其放在屏幕的底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 飞船属性x，y存储小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.x < self.screen_rect.right - 100:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.x > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.y > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ship底部居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
