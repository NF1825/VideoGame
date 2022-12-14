import pygame
import sys
from Settings import Settings
from Blue_Fighter import Blue_Fighter
from Gold_Fighter import Gold_Fighter
from button import Button
import time
import multiprocessing
import random

# make fighting game


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.fps = pygame.time.Clock()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Plebe Boxing")
        self.blue_punch_time = pygame.time.get_ticks()
        self.gold_punch_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()
        self.win_condition = False
        self.game_start = False
        self.bg_color2 = (255, 255, 255)

        self.pregame = pygame.image.load("Gold/PreGame.bmp")

        self.font = pygame.font.Font(None, 40)
        self.color_blue = pygame.Color(0, 0, 255)
        self.color_gold = pygame.Color(255, 215, 0)
        self.color_black = pygame.Color(0, 0, 0)

        self.play_button =Button(self, "Play")

        self.blue = Blue_Fighter(self)
        self.gold = Gold_Fighter(self)
        self.display_time = (self.settings.timer_length / 60.0)

        self.txt = self.font.render(str(self.display_time), True, self.color_black, self.color_blue)

        # Music
        self.bg_music = pygame.mixer.music.load("Gold/'Magic Spear I' - Ace Combat 7.mp3")

    def reset_game(self):
        self.win_condition = False
        self.blue.remove()
        self.gold.remove()

        self.blue = Blue_Fighter(self)
        self.gold = Gold_Fighter(self)

        self.settings.Blue_health = 1000.0
        self.settings.Gold_health = 1000.0

        self.settings.timer_length = 3600




    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.

        # draw the play button if the game is inactive.
        if not self.game_start:
            self.screen.blit(self.pregame, (0, 0))
            self.play_button.draw_button()
            pygame.display.flip()

        elif self.game_start:

            if not self.win_condition:
                self.screen.fill(self.settings.bg_color)
                self.screen.blit(pygame.image.load("Blue/ring2.bmp"), (0, 0))
                self.blue.blitme()
                self.gold.blitme()
                self.screen.blit(self.txt, self.blue.screen_rect.midtop)
                self.update_healthbar()
                pygame.display.flip()
                self.fps.tick(60)

            elif self.win_condition:
                self.screen.fill(self.bg_color2)
                self.screen.blit(self.txt, ((self.blue.screen_rect.centerx - 50), self.blue.screen_rect.centery))
                pygame.display.flip()
                time.sleep(4)
                self.reset_game()
                pygame.mouse.set_visible(True)
                self.game_start = False

            # make the most recently drawn screen visible.

    def gravity_update(self):
        self.settings.Blue_jump_speed -= self.settings.gravity
        self.settings.Gold_jump_speed -= self.settings.gravity

    def _check_events(self):
        """respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_d:
            # Move blue to the right.
            self.blue.moving_right = True
        elif event.key == pygame.K_QUOTE:
            # Move gold to the right
            self.gold.moving_right = True

        elif event.key == pygame.K_a:
            # Move blue to the left.
            self.blue.moving_left = True
        elif event.key == pygame.K_l:
            # Move Gold to the left.
            self.gold.moving_left = True

        elif event.key == pygame.K_w:
            # Make blue jump
            if self.blue.rect.bottom >= self.blue.screen_rect.bottom:
                #self.blue.rect.bottom = self.blue.screen_rect.bottom
                self.settings.Blue_jump_speed = 9
                self.blue.y -= self.settings.Blue_jump_speed

        elif event.key == pygame.K_p:
            # Make Gold Jump
            if self.gold.rect.bottom >= self.gold.screen_rect.bottom:
                # self.blue.rect.bottom = self.blue.screen_rect.bottom
                self.settings.Gold_jump_speed = 9
                self.gold.y -= self.settings.Gold_jump_speed

        elif event.key == pygame.K_s:
            # move blue down
            self.blue.crouched = True
        elif event.key == pygame.K_SEMICOLON:
            # Make gold crouch
            self.gold.crouched = True

        elif event.key == pygame.K_BACKQUOTE and not self.blue.kick:
            self.punch("blue")
            self.blue.blue_punch_time = pygame.time.get_ticks()
        elif event.key == pygame.K_m and not self.gold.kick:
            self.punch("gold")
            self.gold.gold_punch_time = pygame.time.get_ticks()

        elif event.key == pygame.K_1 and not self.blue.punch:
            self.kick("blue")
            self.blue.blue_punch_time = pygame.time.get_ticks()
        elif event.key == pygame.K_COMMA and not self.gold.punch:
            self.kick("gold")
            self.gold.gold_punch_time = pygame.time.get_ticks()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.blue.moving_right = False
        elif event.key == pygame.K_QUOTE:
            self.gold.moving_right = False
        elif event.key == pygame.K_a:
            self.blue.moving_left = False
        elif event.key == pygame.K_l:
            self.gold.moving_left = False
        elif event.key == pygame.K_s:
            self.blue.crouched = False
        elif event.key == pygame.K_SEMICOLON:
            self.gold.crouched = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_start:
            #Start the game
            self.game_start = True

            #hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def punch(self, color):
        if color == "blue":
            self.blue.punch = True
            self.blue.attacking = True
            if not self.blue.crouched:
                self.blue.image = self.blue.base_punch
            elif self.blue.crouched:
                self.blue.image = self.blue.low_punch
        elif color == "gold":
            self.gold.punch = True
            self.gold.attacking = True
            if not self.gold.crouched:
                self.gold.image = self.gold.base_punch
            elif self.gold.crouched:
                self.gold.image = self.gold.low_punch

    def kick(self, color):
        if color == "blue":
            self.blue.kick = True
            if not self.blue.crouched:
                self.blue.image = self.blue.base_kick_prep
            elif self.blue.crouched:
                self.blue.image = self.blue.low_kick_prep
        elif color == "gold":
            self.gold.kick = True
            if not self.gold.crouched:
                self.gold.image = self.gold.base_kick_prep
            elif self.gold.crouched:
                self.gold.image = self.gold.low_kick_prep

    def check_collisions(self):
        # check if a collision between the fighter sprites occurs
        collisions = pygame.sprite.collide_rect(self.blue, self.gold)

        if collisions and not self.blue.attacking and not self.gold.attacking:
            self.blue.moving_right = False
            self.gold.moving_left = False

        if collisions and self.blue.attacking:
            # Dylan helped me design the block feature
            if self.blue.kick and not self.blue.crouched and self.gold.crouched:
                if self.gold.rect.right <= self.gold.screen_rect.right - 150:
                    self.gold.x += 150
            elif self.blue.punch and not self.blue.crouched and self.gold.crouched:
                if self.gold.rect.right <= self.gold.screen_rect.right - 75:
                    self.gold.x += 75

            elif self.blue.kick and not self.blue.crouched and not self.gold.crouched:
                self.settings.Gold_health -= 25
                pygame.mixer.Sound.play(self.gold.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.gold.rect.right <= self.gold.screen_rect.right - 300:
                    self.gold.x += 300
            elif self.blue.punch and not self.blue.crouched and not self.gold.crouched:
                self.settings.Gold_health -= 15
                pygame.mixer.Sound.play(self.gold.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.gold.rect.right <= self.gold.screen_rect.right - 150:
                    self.gold.x += 150

            elif self.blue.kick and self.blue.crouched and self.gold.crouched:
                self.settings.Gold_health -= 25
                pygame.mixer.Sound.play(self.gold.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.gold.rect.right <= self.gold.screen_rect.right - 250:
                    self.gold.x += 250

            elif self.blue.punch and self.blue.crouched and self.gold.crouched:
                self.settings.Gold_health -= 15
                pygame.mixer.Sound.play(self.gold.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.gold.rect.right <= self.gold.screen_rect.right - 125:
                    self.gold.x += 125

            elif self.blue.kick and self.blue.crouched and not self.gold.crouched:
                self.settings.Gold_health -= 15
                pygame.mixer.Sound.play(self.gold.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.gold.rect.right <= self.gold.screen_rect.right - 150:
                    self.gold.x += 150

            elif self.blue.punch and self.blue.crouched and not self.gold.crouched:
                self.settings.Gold_health -= 5
                pygame.mixer.Sound.play(self.gold.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.gold.rect.right <= self.gold.screen_rect.right - 75:
                    self.gold.x += 75
        # gold attacks
        if collisions and self.gold.attacking:
            if self.gold.kick and not self.gold.crouched and self.blue.crouched:
                if self.blue.rect.left >= self.blue.screen_rect.left + 150:
                    self.blue.x -= 150
            elif self.gold.punch and not self.gold.crouched and self.blue.crouched:
                if self.blue.rect.left >= self.blue.screen_rect.left + 75:
                    self.blue.x -= 75

            elif self.gold.kick and not self.gold.crouched and not self.blue.crouched:
                self.settings.Blue_health -= 25
                pygame.mixer.Sound.play(self.blue.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.blue.rect.left >= self.blue.screen_rect.left + 300:
                    self.blue.x -= 300
            elif self.gold.punch and not self.gold.crouched and not self.blue.crouched:
                self.settings.Blue_health -= 15
                pygame.mixer.Sound.play(self.blue.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.blue.rect.left >= self.blue.screen_rect.left + 150:
                    self.blue.x -= 150
            elif self.gold.kick and self.gold.crouched and self.blue.crouched:
                self.settings.Blue_health -= 25
                pygame.mixer.Sound.play(self.blue.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.blue.rect.left >= self.blue.screen_rect.left + 250:
                    self.blue.x -= 250
            elif self.gold.punch and self.gold.crouched and self.blue.crouched:
                self.settings.Blue_health -= 15
                pygame.mixer.Sound.play(self.blue.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.blue.rect.left >= self.blue.screen_rect.left + 125:
                    self.blue.x -= 125
            elif self.gold.kick and self.gold.crouched and not self.blue.crouched:
                self.settings.Blue_health -= 15
                pygame.mixer.Sound.play(self.blue.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.blue.rect.left >= self.blue.screen_rect.left + 150:
                    self.blue.x -= 150
            elif self.gold.punch and self.gold.crouched and not self.blue.crouched:
                self.settings.Gold_health -= 5
                pygame.mixer.Sound.play(self.blue.hurt, loops=0, maxtime=3000, fade_ms=0)
                if self.blue.rect.left >= self.blue.screen_rect.left + 75:
                    self.blue.x -= 75

    def run_timer(self):
        if self.settings.timer_length > 0.0 and not self.win_condition:
            self.settings.timer_length -= self.settings.dt
            self.txt = self.font.render(str(round(self.settings.timer_length / 60)), True, self.color_black)
        elif self.settings.timer_length == 0 and not self.win_condition:
            self.win_condition = True
            self.settings.timer_length -= self.settings.dt
            self.temp = random.randint(0,1)
            if self.temp == 0:
                self.txt = self.font.render('Blue Wins!', True, self.color_blue)
            elif self.temp == 1:
                self.txt = self.font.render('Gold Wins!', True, self.color_gold)
        elif self.win_condition:
            if self.settings.Blue_health == 0:
                self.txt = self.font.render('Gold Wins!', True, self.color_gold)

    def update_healthbar(self):
        """update healthbars based on health"""
        if self.settings.Gold_health == 0 or self.settings.Blue_health == 0:
            if self.settings.Gold_health == 0:
                self.txt = self.txt = self.font.render('Blue Wins!', True, self.color_blue)
            elif self.settings.Blue_health == 0:
                self. txt = self.txt = self.font.render('Gold Wins!', True, self.color_gold)
            self.win_condition = True
        pygame.draw.rect(self.screen, self.color_black, ((self.blue.screen_rect.left, self.blue.screen_rect.top), (500, 50)))
        pygame.draw.rect(self.screen, self.color_blue, ((self.blue.screen_rect.left, self.blue.screen_rect.top), ((self.settings.Blue_health / 2), 50)))
        pygame.draw.rect(self.screen, self.color_black, (((self.blue.screen_rect.right - 500), self.blue.screen_rect.top), (500, 50)))
        pygame.draw.rect(self.screen, self.color_gold, (((self.gold.screen_rect.right - (self.settings.Gold_health / 2)), self.gold.screen_rect.top), ((self.settings.Gold_health / 2), 50)))

    def run_game(self):
        """Start the main loop for the game."""
        pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)
        while True:
            self.current_time = pygame.time.get_ticks()
            self.blue.current_time = self.current_time
            self.gold.current_time = self.current_time
            self.gravity_update()
            self._check_events()

            self.blue.update()
            self.gold.update()
            self.check_collisions()

            if self.settings.timer_length >= 0:
                self.run_timer()

            self._update_screen()


if __name__ == '__main__':
    # make a game instance, and run the game.
    fg = Game()
    fg.run_game()
