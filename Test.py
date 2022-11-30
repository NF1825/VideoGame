import pygame
import sys
from Settings import Settings
from Blue_Fighter import Blue_Fighter
from Gold_Fighter import Gold_Fighter
import time
import multiprocessing
import random

#make fighting game


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.fps = pygame.time.Clock()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Fighter")
        self.blue_punch_time = pygame.time.get_ticks()
        self.gold_punch_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()

        self.font = pygame.font.Font(None, 40)
        self.color_blue = pygame.Color(0,0,255)
        self.color_gold = pygame.Color(255,215,0)
        self.color_white = pygame.Color(255,255,255)

        self.blue = Blue_Fighter(self)
        self.gold = Gold_Fighter(self)

        #self.txt = self.font.render(str(self.settings.timer_length), True, self.color_white)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.blue.blitme()
        self.gold.blitme()
        #self.screen.blit(self.txt, self.blue.screen_rect.midtop)

        #make the most recently drawn screen visible.
        pygame.display.flip()
        self.fps.tick(60)


    def _check_events(self):
        """respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

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
            #Make blue jump
            self.blue.jump = True
        elif event.key == pygame.K_p:
            # Make Gold Jump
            self.gold.jump = True

        elif event.key == pygame.K_s:
            #move blue down
            self.blue.crouched = True
        elif event.key == pygame.K_SEMICOLON:
            #Make gold crouch
            self.gold.crouched = True

        elif event.key == pygame.K_1 and self.blue.kick == False:
            self.punch("blue")
            self.blue.blue_punch_time = pygame.time.get_ticks()
        elif event.key == pygame.K_m and self.gold.kick == False:
            self.punch("gold")
            self.gold.gold_punch_time = pygame.time.get_ticks()

        elif event.key == pygame.K_2 and self.blue.punch == False:
            self.kick("blue")
            self.blue.blue_punch_time = pygame.time.get_ticks()
        elif event.key == pygame.K_COMMA and self.gold.punch == False:
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

    def punch(self,color):
        if color == "blue":
            self.blue.punch = True
            self.blue.attacking = True
            if self.blue.crouched == False:
                self.blue.image = self.blue.base_punch
            elif self.blue.crouched:
                self.blue.image = self.blue.low_punch
        elif color == "gold":
            self.gold.punch = True
            self.gold.attacking = True
            if self.gold.crouched == False:
                self.gold.image = self.gold.base_punch
            elif self.gold.crouched:
                self.gold.image = self.gold.low_punch

    def kick(self, color):
        if color == "blue":
            self.blue.kick = True
            if self.blue.crouched == False:
                self.blue.image = self.blue.base_kick_prep
            elif self.blue.crouched:
                self.blue.image = self.blue.low_kick_prep
        elif color == "gold":
            self.gold.kick = True
            if self.gold.crouched == False:
                self.gold.image = self.gold.base_kick_prep
            elif self.gold.crouched:
                self.gold.image = self.gold.low_kick_prep



    def check_collisions(self):
        #check if a collision between the fighter sprites occurs
        collisions = pygame.sprite.collide_rect(self.blue, self.gold)

        if collisions and self.blue.attacking == False and self.gold.attacking == False:
            self.blue.moving_right = False
            self.gold.moving_left = False

        if collisions and self.blue.attacking == True:
            if self.blue.kick and self.blue.crouched == False and self.gold.crouched:
                if self.gold.rect.right <= self.gold.screen_rect.right - 150:
                    self.gold.x += 150
            elif self.blue.punch and self.blue.crouched == False and self.gold.crouched:
                if self.gold.rect.right <= self.gold.screen_rect.right - 75:
                    self.gold.x += 75
            elif self.blue.kick and self.blue.crouched == False and self.gold.crouched == False:
                self.settings.Gold_health -= 2
                if self.gold.rect.right <= self.gold.screen_rect.right - 300:
                    self.gold.x += 300
            elif self.blue.punch and self.blue.crouched == False and self.gold.crouched == False:
                self.settings.Gold_health -= 1
                if self.gold.rect.right <= self.gold.screen_rect.right -150:
                    self.gold.x += 150
            elif self.blue.kick and self.blue.crouched and self.gold.crouched:
                self.settings.Gold_health -= 2
                if self.gold.rect.right <= self.gold.screen_rect.right - 250:
                    self.gold.x += 250
            elif self.blue.punch and self.blue.crouched and self.gold.crouched:
                self.settings.Gold_health -= 1
                if self.gold.rect.right <= self.gold.screen_rect.right -125:
                    self.gold.x += 125
            elif self.blue.kick and self.blue.crouched and self.gold.crouched == False:
                self.settings.Gold_health -= 1
                if self.gold.rect.right <= self.gold.screen_rect.right -150:
                    self.gold.x += 150
            elif self.blue.punch and self.blue.crouched and self.gold.crouched == False:
                self.settings.Gold_health -= 0.5
                if self.gold.rect.right <= self.gold.screen_rect.right -75:
                    self.gold.x += 75

        if collisions and self.gold.attacking == True:
            if self.gold.kick and self.gold.crouched == False and self.blue.crouched:
                if self.blue.rect.left >= self.blue.screen_rect.left + 150:
                    self.blue.x -= 150
            elif self.gold.punch and self.gold.crouched == False and self.blue.crouched:
                if self.blue.rect.left >= self.blue.screen_rect.left + 75:
                    self.blue.x -= 75
            elif self.gold.kick and self.gold.crouched == False and self.blue.crouched == False:
                self.settings.Blue_health -= 2
                if self.blue.rect.left >= self.blue.screen_rect.left + 300:
                    self.blue.x -= 300
            elif self.gold.punch and self.gold.crouched == False and self.blue.crouched == False:
                self.settings.Blue_health -= 1
                if self.blue.rect.left >= self.blue.screen_rect.left + 150:
                    self.blue.x -= 150
            elif self.gold.kick and self.gold.crouched and self.blue.crouched:
                self.settings.Blue_health -= 2
                if self.blue.rect.left >= self.blue.screen_rect.left + 250:
                    self.blue.x -= 250
            elif self.gold.punch and self.gold.crouched and self.blue.crouched:
                self.settings.Blue_health -= 1
                if self.blue.rect.left >= self.blue.screen_rect.left + 125:
                    self.blue.x -= 125
            elif self.gold.kick and self.gold.crouched and self.blue.crouched == False:
                self.settings.Blue_health -= 1
                if self.blue.rect.left >= self.blue.screen_rect.left + 150:
                    self.blue.x -= 150
            elif self.gold.punch and self.gold.crouched and self.blue.crouched == False:
                self.settings.Gold_health -= 0.5
                if self.blue.rect.left >= self.blue.screen_rect.left + 75:
                    self.blue.x -= 75



    #def run_timer(self):
       #while self.settings.timer_length >= 0.0:
            #self.settings.timer_length -= self.settings.dt
            #self.txt = self.font.render(str(self.settings.timer_length), True, self.color_white)
        #self.temp = random.randint(0,1)
        #if self.temp == 0:
            #self.txt = self.font.render('Blue Wins!',True, self.color_blue)
        #elif self.temp == 1:
            #self.txt = self.font.render('Gold Wins!',True, self.color_gold)



    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.current_time = pygame.time.get_ticks()
            self.blue.current_time = self.current_time
            self.gold.current_time = self.current_time
            self._check_events()
            self.blue.update()
            self.gold.update()
            self.check_collisions()
            self.run_timer()



            self._update_screen()


if __name__ == '__main__':
    # make a game instance, and run the game.
    fg = Game()
    fg.run_game()






