import pygame


class Miaobir():
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.sb = ai_game.score_board
        self.stats = ai_game.stats
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/miaobi_note.png')
        self.rect = self.image.get_rect()
        # 显示喵币信息的字体设置
        self.text_color = (169, 89, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备喵币数图像
        self.prep_miaobi_amount()
        # 位置
        self.rect.top = self.sb.score_rect.bottom + 14
        self.rect.x = self.screen_rect.right - 40

    def show_miaobi_note(self):
        self.screen.blit(self.image, self.rect)

    def prep_miaobi_amount(self):
        amount_str = f"{str(self.stats.amount)} x "
        self.miaobi_amount_image = self.font.render(amount_str, True, self.text_color)
        self.miaobi_amount_rect = self.miaobi_amount_image.get_rect()
        self.miaobi_amount_rect.right = self.rect.right - 40
        self.miaobi_amount_rect.top = self.rect.bottom - 30

    def show_amount(self):
        self.screen.blit(self.miaobi_amount_image, self.miaobi_amount_rect)
