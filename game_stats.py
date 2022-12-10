class Gamestats():
    def __init__(self, ai_game):
        """初始化统计信息"""
        self.game_active = False
        self.settings = ai_game.settings
        self.reset_stats()
        self.score = 0
        self.amount = 0
        self.history = 0
        self.zifa_limit_flag = False
        self.create_m_limit = False
        self.play_click = False

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
