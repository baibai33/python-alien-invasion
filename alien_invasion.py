import sys
from time import sleep, time
import pygame.image
from bullet import *
from alien import *
from settings import Settings
from game_stats import Gamestats
from button import *
from scoreboard import *
from miaobi_r import Miaobir
from random import choice, randint


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("夏目友人帐")
        # 创建一个用于存储游戏统计信息的实例
        self.stats = Gamestats(self)
        self.ship = Ship(self, 'images/ship.png')
        self.bullets = pygame.sprite.Group()
        self.jineng1 = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.boss1 = pygame.sprite.Group()
        self.miaobi = pygame.sprite.Group()
        self.jineng2_1duan = pygame.sprite.Group()
        self.jineng2_2duan = pygame.sprite.Group()
        self.heimao_bulletgroup = pygame.sprite.Group()
        self._create_fleet()
        self._create_miaobiqun()
        self.play_button = Button(self, 'click to play~', 255, 255, 255)
        self.replay_button = Button(self, 'replay', 255, 255, 255)
        self.music_button = Music_flag(self, 'playing', 255, 255, 255)
        self.youxishuoming = Youxishuoming(self, 'Game Description', 255, 255, 255)
        self.banquanshuoming = Banquanshuoming(self, 'made by bai', 255, 255, 255)
        self.score_board = Scoreboard(self)
        self.history = History(self)
        self.miaobi_note = Miaobir(self)
        self.clock = pygame.time.Clock()
        self.current_time = pygame.time.get_ticks()

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            self._check_events()
            self.music_update()
            if self.stats.game_active == True:
                if self.settings.jiluboss_time_flag:
                    self.settings.create_boss_time = time()
                    self.settings.jiluboss_time_flag = False

                self.ship.update()
                self.update_bullets()
                self.update_jineng1()
                self.update_jineng2_1duan()
                self.update_jineng2_2duan()
                self.update_aliens()
                self.update_boss1()
                self.update_heimaobullet()
                self.update_miaobi()
            self._update_screen()
            # self.clock.tick(100)

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.stats.ships_left == self.settings.ship_limit:
                    self._check_play_button(mouse_pos)
                    self._check_youxishuoming_button(mouse_pos)
                elif self.stats.ships_left == 0:
                    self._check_replay_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def music1_start(self):
        pygame.mixer.init()  # 初始化
        pygame.mixer.music.load('musics/bgmusic1.mp3')  # 加载音乐文件
        pygame.mixer.music.play(-1)

    def music_update(self):
        if self.stats.game_active == False:
            if self.settings.music2_active == False:
                self.music2_start()
                self.settings.music2_active = True
        else:
            if self.settings.music1_active == False:
                self.music1_start()
                self.settings.music1_active = True

    def music2_start(self):
        pygame.mixer.init()  # 初始化
        pygame.mixer.music.load('musics/bgmusic2.mp3')  # 加载音乐文件
        pygame.mixer.music.play(-1)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        if self.stats.play_click == False:
            self.screen.blit(self.settings.background1, (0, 0))
            if self.settings.show_youxishuoming_flag:
                self.screen.blit(self.settings.youxiguize_image, (0, 0))
        if self.stats.play_click == True:
            # self.screen.fill(self.settings.bg_color)
            self.screen.blit(self.settings.background2, (0, 0))
            self.ship_show()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # for heimaobullet in self.new_bulletgroup.copy():
            for bullet in self.heimao_bulletgroup.sprites():
                bullet.draw_bullet()
            self.jineng1.draw(self.screen)
            self.jineng2_1duan.draw(self.screen)
            self.jineng2_2duan.draw(self.screen)
            self.aliens.draw(self.screen)
            self.boss1.draw(self.screen)
            self.miaobi.draw(self.screen)
            self.score_board.show_score()
            self.shuaxin_history()
            self.history.show_history()
            self.miaobi_note.show_miaobi_note()
            self.miaobi_note.show_amount()
            self.music_button.draw_button()
            self.music_button.draw_note_image()

        if not self.stats.game_active:
            if self.stats.ships_left == self.settings.ship_limit and self.stats.play_click == False:
                if self.settings.show_youxishuoming_flag == False:
                    self.play_button.draw_button()
                    self.play_button.draw_note_image()
                self.youxishuoming.draw_button()
                self.youxishuoming.draw_youxishuoming_image()
                self.banquanshuoming.draw_button()
            elif self.stats.ships_left <= self.settings.ship_limit and self.stats.ships_left > 0:
                self.play_button.draw_button()
                self.play_button.draw_note_pause_image()
            elif self.stats.ships_left == 0:
                self.replay_button.draw_button()
                self.replay_button.draw_note_image()
                self.ship.center_ship()

        pygame.display.flip()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_j:
            self._fire_bullet(self.settings.bullet_allowed)
        if self.stats.zifa_limit_flag == False:
            if event.key == pygame.K_u:
                if self.stats.amount >= 5:
                    if len(self.jineng1) < self.settings.jineng1_bullet_allowed:
                        self._fire_jineng1()
                        self.stats.amount -= 5
                        self.miaobi_note.prep_miaobi_amount()
            if event.key == pygame.K_i:
                if self.stats.amount >= 10:
                    self._fire_jineng2_1duan()
                    self.stats.amount -= 10
                    self.miaobi_note.prep_miaobi_amount()
            if event.key == pygame.K_o:
                if self.stats.amount >= 20:
                    self.jineng3_xiangyin()
        if event.key == pygame.K_TAB:
            if self.stats.ships_left <= 3 and self.stats.ships_left > 0:
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
        if event.key == pygame.K_CAPSLOCK:
            if self.stats.ships_left <= 3 and self.stats.ships_left > 0:
                self.stats.game_active = True
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True

        if event.key == pygame.K_d:
            self.ship.moving_right = True
        if event.key == pygame.K_a:
            self.ship.moving_left = True
        if event.key == pygame.K_w:
            self.ship.moving_up = True
        if event.key == pygame.K_s:
            self.ship.moving_down = True
        if event.key == pygame.K_p:
            self.settings.music_switch *= -1
            if self.settings.music_switch == -1:
                self.music_button.msg = 'pause'
                pygame.mixer.music.pause()
            else:
                self.music_button.msg = 'playing'
                pygame.mixer.music.unpause()
            self.music_button._prep_msg()

        if event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False

        if event.key == pygame.K_d:
            self.ship.moving_right = False
        if event.key == pygame.K_a:
            self.ship.moving_left = False
        if event.key == pygame.K_w:
            self.ship.moving_up = False
        if event.key == pygame.K_s:
            self.ship.moving_down = False

    """bullet..."""

    def _fire_bullet(self, bullet_allowed):
        if len(self.bullets) < bullet_allowed:
            if self.ship.image_prep == 'images/ship.png':
                new_bullet = Bullet(self, 'images/maozhua.png')
                self.bullets.add(new_bullet)
            elif self.ship.image_prep == 'images/ban22.png':
                new_bullet = Bullet(self, 'images/sansan1.png')
                self.bullets.add(new_bullet)

    def _fire_jineng1(self):
        i = 0
        while i < 9:
            new_bullet = Jineng1(self, 'images/maozhua.png')
            self.jineng1.add(new_bullet)
            i += 1

    def _fire_jineng2_1duan(self):
        if len(self.jineng2_1duan.sprites()) < 1:
            new_bullet = Jineng2_1duan(self, 'images/feipu.png')
            self.jineng2_1duan.add(new_bullet)

    def update_jineng1(self):
        pianyi_x = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        i = 0
        for bullet in self.jineng1.sprites():
            bullet.update(pianyi_x[i])
            i += 1
            if i == 8:
                i = 0
        for bullet in self.jineng1.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.screen.get_rect().right:
                self.jineng1.remove(bullet)
        self._check_jineng1_alien_collisions()

    def update_jineng2_1duan(self):
        self.jineng2_1duan.update()
        for bullet in self.jineng2_1duan.copy():
            if bullet.rect.bottom <= 0:
                self.jineng2_1duan.remove(bullet)
        self._check_jineng1_1duan_alien_collisions()

    def _check_jineng1_1duan_alien_collisions(self):
        # collisions = pygame.sprite.groupcollide(self.jineng2_1duan, self.aliens, True, True)
        for alien in self.aliens.sprites():
            for bullet in self.jineng2_1duan.sprites():
                if bullet.rect.colliderect(alien):
                    """if collisions:
                    for alien,aliens in collisions.values():
                    self.stats.score += self.settings.alien_point * len(aliens)"""
                    self.stats.score += self.settings.alien_point
                    self.score_board.prep_score()
                    self.aliens.remove(alien)
                    self.jineng2_1duan.remove(bullet)
                    self._fire_jineng2_2duan(alien)
                    break

    def _fire_jineng2_2duan(self, alien):
        i = 0
        while i < 16:
            new_bullet = Jineng2_2duan(self, 'images/maozhua1.jpg', alien)
            self.jineng2_2duan.add(new_bullet)
            i += 1

    def update_jineng2_2duan(self):
        pianyi_x = [0, 0.5, 1, 2, 1, 2, 1, 0.5, 0, -0.5, -1, -2, -1, -2, -1, -0.5]
        pianyi_y = [1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1]
        i = 0
        for bullet in self.jineng2_2duan.sprites():
            bullet.update(pianyi_x[i], pianyi_y[i])
            i += 1
            if i == 15:
                i = 0

        for bullet in self.jineng2_2duan.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.screen.get_rect().right \
                    or bullet.rect.top >= self.screen.get_rect().bottom:
                self.jineng2_2duan.remove(bullet)
        self._check_jineng1_2duan__alien_collisions()

    def _check_jineng1_2duan__alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.jineng2_2duan, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens)
                self.score_board.prep_score()

    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    """alien..."""

    def _create_fleet(self):
        images = ['images/heimao.png', 'images/zifa.png']
        choose_image = choice(images)
        alien = Alien(self, choose_image)
        number_alien_x = 4
        number_rows = 2
        # 创建群体
        i = 1
        j = randint(0, 5)
        while (i <= j):
            row_number = randint(0, number_rows)
            alien_number = randint(0, number_alien_x - 1)
            self._create_alien(alien_number, row_number)
            i += 1

    def _create_alien(self, alien_number, row_number):
        images = ['images/heimao.png', 'images/zifa.png']
        choose_image = choice(images)
        alien = Alien(self, choose_image)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = float(alien.x)
        alien.rect.y = float(alien.rect.height + 1.5 * alien.rect.height * row_number)
        self.aliens.add(alien)

    def update_aliens(self):
        h_time2 = time()
        # print(f"h_time2:{h_time2}")
        h_time1 = self.settings.create_bullet
        # print(f"h_time2-h_time1:{h_time2-h_time1}")

        if h_time2 - h_time1 >= 1:
            self.create_heimao_bullets()
        self._check_fleet_edges()
        self.aliens.update()

        # 检测飞船与目标的碰撞
        for alien in self.aliens.copy():
            if alien.rect.colliderect(self.ship):
                if self.settings.wudi_flag == True:
                    self.aliens.remove(alien)
                else:
                    if alien.image_prep == 'images/zifa.png':
                        self.zifa_xiangyin()
                        self.aliens.remove(alien)
                    if alien.image_prep == 'images/heimao.png':
                        self._ship_hit()
        # 检测目标到达屏幕底端
        self._check_alien_bottom()

    def create_heimao_bullets(self):
        self.settings.create_bullet = time()
        for alien in self.aliens.sprites():
            if alien.image_prep == 'images/heimao.png':
                new_bullet = Heimao_bullet(self, 'images/heimaozhua.png', alien)
                self.heimao_bulletgroup.add(new_bullet)

    def update_heimaobullet(self):
        # for heimao_bullet in self.new_bulletgroup.copy():
        self.heimao_bulletgroup.update()
        self._check_heimaobullet_bottom()
        self._check_heimaobullet_ship_collision()

    def _check_heimaobullet_bottom(self):
        for bullet in self.heimao_bulletgroup.copy():
            if bullet.rect.top > self.screen.get_rect().bottom:
                self.heimao_bulletgroup.remove(bullet)

    def _check_heimaobullet_ship_collision(self):

        for heimaobullet in self.heimao_bulletgroup.sprites():
            if heimaobullet.rect.colliderect(self.ship):
                if self.settings.wudi_flag == True:
                    self.heimao_bulletgroup.remove(heimaobullet)
                else:
                    self._ship_hit()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.a_check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def change_miaobiqun_direction(self):
        for miaobi in self.miaobi.sprites():
            miaobi.rect.y += self.settings.miaobiqun_drop_speed
        self.settings.miaobiqun_direction *= -1

    def _check_bullet_alien_collisions(self):
        # 检查是否击中
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens)
                self.score_board.prep_score()
        # 全部击中后清空子弹并再次生成目标
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

            self.settings.increase_speed()  # 加速

    def _check_jineng1_alien_collisions(self):
        collision = pygame.sprite.groupcollide(self.jineng1, self.aliens, True, True)
        if collision:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_point * len(aliens)
                self.score_board.prep_score()

    def _ship_hit(self):
        self.stats.ships_left -= 1
        if self.stats.ships_left > 0:
            self.score_board.prep_ships_sign()
            print(f"剩余:{self.stats.ships_left}")
            # zhuangji
            self.ship.image = pygame.image.load('images/zhuangji.png')
            self._update_screen()
            # 暂停
            sleep(1.0)
            self.ship.image = pygame.image.load('images/ship.png')
            self._empty_all()
            self.heimao_bulletgroup.empty()
            # 重绘
            self._create_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            self.score_board.prep_ships_sign()
            pygame.mouse.set_visible(True)

            print(f"剩余:{self.stats.ships_left}\nGame over!")

    def _check_alien_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self._ship_hit()  # 像ship被撞到一样处理
                break

    """boss1"""

    def _create_boss1(self):
        self.settings.create_boss_time = time()
        boss1 = Boss1(self, 'images/boss1.png')
        self.boss1.add(boss1)

    def update_boss1(self):
        boss1_time2 = time()
        boss1_time1 = self.settings.create_boss_time
        # print(boss1_time2-boss1_time1)
        if (boss1_time2 - boss1_time1) >= 30:
            self._create_boss1()

        self.boss1.update()
        self._check_boss1_bottom()
        self._check_boss1_gezhong_bullets_collision()

    def _check_boss1_bottom(self):
        for boss1 in self.boss1.copy():
            if boss1.rect.top > self.screen.get_rect().bottom:
                self._ship_hit()
                self.boss1.remove(boss1)

    def _check_boss1_ship_collision(self):
        if self.settings.wudi_flag == False:
            for boss1 in self.boss1.sprites():
                if boss1.rect.colliderect(self.ship):
                    self._ship_hit()
                    boss1.hp -= 15

    def _check_boss1_gezhong_bullets_collision(self):
        for boss1 in self.boss1.sprites():
            for bullet in self.bullets.sprites():
                if boss1.rect.colliderect(bullet):
                    if bullet.image_prep == 'images/maozhua.png':
                        boss1.hp -= 1
                        print(boss1)
                    elif bullet.image_prep == 'images/lanhei.png':
                        boss1.hp -= 4
                    self.bullets.remove(bullet)
                    if boss1.hp == 0:
                        self.hp_0(boss1, 5)
            for bullet1 in self.jineng1.sprites():
                if boss1.rect.colliderect(bullet1):
                    self.jineng1.remove(bullet1)
                    boss1.hp -= 1
                    print(boss1)
                    if boss1.hp == 0:
                        self.hp_0(boss1, 5)
            for bullet2 in self.jineng2_1duan.sprites():
                if boss1.rect.colliderect(bullet2):
                    self.jineng2_1duan.remove(bullet2)
                    self._fire_jineng2_2duan(boss1)
                    boss1.hp -= 1
                    print(boss1)
                    if boss1.hp == 0:
                        self.hp_0(boss1, 5)
            for bullet3 in self.jineng2_2duan.sprites():
                if boss1.rect.colliderect(bullet3):
                    self.jineng2_2duan.remove(bullet3)
                    boss1.hp -= 1
                    print(boss1)
                    if boss1.hp == 0:
                        self.hp_0(boss1, 5)

    def hp_0(self, boss, beishu):
        self.boss1.remove(boss)
        self.stats.score += self.settings.alien_point * beishu
        self.score_board.prep_score()

    """miaobi..."""

    def _create_miaobiqun(self):
        self.miaobi.create_time = time()
        images = ['images/1.png', 'images/xiamu1.png']
        choose_image = choice(images)
        miaobi = Miaobis(self, choose_image)
        miaobi_width, miaobi_height = miaobi.rect.size
        available_space_x = self.settings.screen_width - (2 * miaobi_width)
        number_miaobi_x = available_space_x // (2 * miaobi_width)
        # print(number_alien_x)
        available_space_y = (self.settings.screen_height - 3 * miaobi_height)
        number_rows = available_space_y // (2 * miaobi_height)
        # print(number_rows)

        # 创建群体
        i = 1
        while (i <= 2):
            row_number = randint(0, number_rows)
            miaobi_number = randint(0, number_miaobi_x - 1)
            self._create_miaobi(miaobi_number, row_number)
            i += 1

    def _create_miaobi(self, miaobi_number, row_number):
        images = ['images/1.png', 'images/xiamu1.png']
        choose_image = choice(images)
        miaobi = Miaobis(self, choose_image)
        miaobi_width, miaobi_height = miaobi.rect.size
        miaobi.x = miaobi_width + 2 * miaobi_width * miaobi_number
        miaobi.rect.x = miaobi.x
        miaobi.rect.y = miaobi.rect.height + 1.5 * miaobi.rect.height * row_number
        self.miaobi.add(miaobi)

    def update_miaobi(self):
        # self._check_miaobiqun_edges()
        self.miaobi.update()
        # 检测飞船与喵币的碰撞
        for miaobi in self.miaobi.copy():
            if miaobi.rect.colliderect(self.ship):
                if miaobi.image_prep == 'images/1.png':
                    self.stats.amount += 100
                    self.miaobi_note.prep_miaobi_amount()
                    self.miaobi.remove(miaobi)
                    self.stats.score += 10 * self.settings.miaobi_point
                    self.score_board.prep_score()
                elif miaobi.image_prep == 'images/xiamu1.png':
                    self.ship.image_prep = 'images/ban11.png'
                    self.ship.image = pygame.image.load(self.ship.image_prep)
                    self.settings.xiamu_time = time()
                    self.miaobi.remove(miaobi)

        if not self.miaobi:
            m_time1 = self.miaobi.create_time
            m_time2 = time()
            # print(m_time2 - m_time1)
            if m_time2 - m_time1 > 15:
                self._create_miaobiqun()
        # 检测喵币到达底部
        self._check_miaobi_bottom()

    def _check_miaobi_bottom(self):
        for miaobi in self.miaobi.copy():
            if miaobi.rect.top >= self.screen.get_rect().bottom:
                self.miaobi.remove(miaobi)
        if not self.miaobi:
            m_time1 = self.miaobi.create_time
            m_time2 = time()
            # print(m_time2-m_time1)
            if m_time2 - m_time1 > 15:
                self._create_miaobiqun()

    """..."""

    def _check_youxishuoming_button(self, mouse_pos):
        button_clicked = self.youxishuoming.youxishuoming_image_rect.collidepoint(mouse_pos)
        if button_clicked:
            if self.settings.show_youxishuoming_flag == False:
                self.settings.show_youxishuoming_flag = True
            else:
                self.settings.show_youxishuoming_flag = False

    def _check_play_button(self, mouse_pos):
        button_clicked = self.replay_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.prep()
            self.stats.play_click = True

    def _check_replay_button(self, mouse_pos):
        button_clicked = self.replay_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self._empty_all()
            self.stats.reset_stats()
            self.stats.amount = 0
            self.prep()
            self._update_screen()

    def prep(self):
        print("Game start!")
        self.stats.game_active = True
        self.score_board.prep_score()
        self.shuaxin_history()
        self.score_board.prep_ships_sign()
        self.miaobi_note.prep_miaobi_amount()
        pygame.mouse.set_visible(False)

    def shuaxin_history(self):
        if self.stats.score >= self.stats.history:
            self.stats.history = self.stats.score
            self.history.prep_history()

    def zifa_xiangyin(self):
        self.ship.image_prep = 'images/zifaxiangyin.png'
        self.ship.image = pygame.image.load(self.ship.image_prep)
        self.ship.bianshen_time = time()
        self.stats.zifa_limit_flag = True

    def jineng3_xiangyin(self):
        self.ship.image_prep = 'images/jineng3xiangyin.png'
        self.ship.image = pygame.image.load(self.ship.image_prep)
        self.ship.suoxiao_time = time()

    def ship_show(self):
        if self.ship.image_prep == 'images/ship.png':
            self.ship.blitme()

            """下述代码有待改进"""
        elif self.ship.image_prep == 'images/ban11.png' or self.ship.image_prep == 'images/ban22.png':
            xiamu_last_time2 = time()
            xiamu_last_time1 = self.settings.xiamu_time
            self.settings.wudi_flag = True
            if (xiamu_last_time2 - xiamu_last_time1) < 3:
                xiamu_time1 = self.settings.xiamu_time
                xiamu_time2 = time()
                if (xiamu_time2 - xiamu_time1) < 0.2:
                    self.ship.blitme()
                else:
                    self.ship.image_prep = 'images/ban22.png'
                    self.ship.image = pygame.image.load(self.ship.image_prep)
                    self.ship.blitme()
            else:
                self.settings.wudi_flag = False
                self.ship.image_prep = 'images/ship.png'
                self.ship.image = pygame.image.load(self.ship.image_prep)
                self.ship.blitme()

        elif self.ship.image_prep == 'images/zifaxiangyin.png':
            end = time()
            start = self.ship.bianshen_time
            # print(end-start)
            if end - start < 2:
                self.ship.blitme()
            else:
                self.ship.image_prep = 'images/ship.png'
                self.ship.image = pygame.image.load(self.ship.image_prep)
                self.ship.blitme()
                self.stats.zifa_limit_flag = False

        elif self.ship.image_prep == 'images/jineng3xiangyin.png':
            end = time()
            start = self.ship.suoxiao_time
            # print(end-start)
            if end - start < 2:
                self.ship.blitme()
            else:
                self.ship.image_prep = 'images/ship.png'
                self.ship.image = pygame.image.load(self.ship.image_prep)
                self.ship.blitme()

    def _empty_all(self):
        self.heimao_bulletgroup.empty()
        self.aliens.empty()
        self.bullets.empty()
        self.jineng1.empty()
        self.jineng2_1duan.empty()
        self.jineng2_2duan.empty()
        self.miaobi.empty()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
