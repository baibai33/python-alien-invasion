import pygame.font
from ship import Ship


class Scoreboard():
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        # 显示得分信息的字体设置
        self.text_color = (169, 89, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备得分图像
        self.prep_score()
        self.ships_sign = pygame.sprite.Group()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        score_str = f"score: {str(self.stats.score)}"
        self.score_image = self.font.render(score_str, True, self.text_color)
        # 右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_ships_sign(self):
        self.ships_sign = pygame.sprite.Group()
        for ship_number in range(self.stats.ships_left):
            ship_sign = Ship(self.ai_game, 'images/niangkou.png')
            ship_sign.rect.x = 10 + ship_number * (ship_sign.rect.width + 3)
            ship_sign.rect.y = 10
            self.ships_sign.add(ship_sign)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.ships_sign.draw(self.screen)


class History():
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.text_color = (169, 89, 30)
        self.font = pygame.font.SysFont(None, 48)

    def prep_history(self):
        history_str = f"History: {str(self.stats.history)}"
        self.history_image = self.font.render(history_str, True, self.text_color)
        self.history_rect = self.history_image.get_rect()
        self.history_rect.midtop = self.screen_rect.midtop

    def show_history(self):
        self.screen.blit(self.history_image, self.history_rect)
