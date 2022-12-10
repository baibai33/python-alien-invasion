import pygame.font


class Button():
    def __init__(self, ai_game, msg, t_R, t_G, t_B):
        """chushihua button 的属性"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        """设置按钮的属性"""
        self.width, self.height = 200, 50
        self.text_color = (t_R, t_G, t_B)
        self.font = pygame.font.SysFont('Times New Roman', 40)
        # 创建按钮的rect对象
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # button标签只创建一次
        self.msg = msg
        self._prep_msg()
        # note_image图片
        self.note_image = pygame.image.load('images/heibai.png')
        self.note_pause_image = pygame.image.load('images/zanting.png')

    def _prep_msg(self):
        """将msg渲染成图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(self.msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midtop = self.rect.midbottom
        self.msg_image_rect.top = self.rect.bottom + 20

    def draw_button(self):
        # self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_note_image(self):
        self.note_image_rect = self.note_image.get_rect()
        self.note_image_rect.center = self.rect.center
        self.screen.blit(self.note_image, self.note_image_rect)

    def draw_note_pause_image(self):
        self.note_pause_image_rect = self.note_pause_image.get_rect()
        self.note_pause_image_rect.center = self.rect.center
        self.screen.blit(self.note_pause_image, self.note_pause_image_rect)


class Music_flag(Button):
    def __init__(self, ai_game, msg, t_R, t_G, t_B):
        super().__init__(ai_game, msg, t_R, t_G, t_B)
        self.music_flag_image = pygame.image.load('images/music_flag.png')
        self.font = pygame.font.SysFont('Times New Roman', 30)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left = self.screen_rect.left
        self.rect.y = 0
        # button标签只创建一次
        self.msg = msg
        self._prep_msg()
        # note_image图片
        self.note_image = pygame.image.load('images/heibai.png')
        self.note_pause_image = pygame.image.load('images/zanting.png')
        self.youxishuoming_image = pygame.image.load('images/xiaohuli.png')

    def _prep_msg(self):
        """将msg渲染成图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(self.msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.y = 65
        self.msg_image_rect.left = self.rect.left + 50

    def draw_note_image(self):
        self.music_flag_image_rect = self.music_flag_image.get_rect()
        self.music_flag_image_rect.left = self.rect.left + 10
        self.music_flag_image_rect.y = 65
        self.screen.blit(self.music_flag_image, self.music_flag_image_rect)


class Youxishuoming(Button):
    def __init__(self, ai_game, msg, t_R, t_G, t_B):
        super().__init__(ai_game, msg, t_R, t_G, t_B)
        self.font = pygame.font.SysFont('Times New Roman', 30)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # button标签只创建一次
        self.msg = msg
        self._prep_msg()
        # note_image图片
        self.note_image = pygame.image.load('images/heibai.png')
        self.note_pause_image = pygame.image.load('images/zanting.png')
        self.youxishuoming_image = pygame.image.load('images/mao11.png')

    def _prep_msg(self):
        """将msg渲染成图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(self.msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.y = 20
        self.msg_image_rect.left = self.rect.left + 30

    def draw_youxishuoming_image(self):
        self.youxishuoming_image_rect = self.youxishuoming_image.get_rect()
        self.youxishuoming_image_rect.top = self.msg_image_rect.bottom
        self.youxishuoming_image_rect.x = 30
        self.screen.blit(self.youxishuoming_image, self.youxishuoming_image_rect)


class Banquanshuoming(Button):
    def __init__(self, ai_game, msg, t_R, t_G, t_B):
        super().__init__(ai_game, msg, t_R, t_G, t_B)
        self.font = pygame.font.SysFont('Times New Roman', 20)
        # 创建按钮的rect对象
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # button标签只创建一次
        self.msg = msg
        self._prep_msg()

    def _prep_msg(self):
        """将msg渲染成图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(self.msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.left = self.screen_rect.left + 33
        self.msg_image_rect.y = 3.5
