import pygame
from pygame.sprite import Sprite
import time


class Gold_Fighter(Sprite):
    """A class to represent a gold fighter"""

    def __init__(self, fg_game):
        """initialize the fighter"""
        super().__init__()
        self.screen = fg_game.screen
        self.settings = fg_game.settings
        self.screen_rect = fg_game.screen.get_rect()
        self.gold_punch_time = fg_game.gold_punch_time
        self.current_time = pygame.time.get_ticks()

        #load initial image for gold fighter
        self.image = pygame.image.load('Gold/Gold_Neutral.bmp')
        self.rect = self.image.get_rect()

        #extra images
        self.base_punch = pygame.image.load('Gold/Gold_Punch.bmp')
        self.low_punch = pygame.image.load('Gold/Gold_Low_Punch.bmp')
        self.base_kick_prep = pygame.image.load('Gold/Gold_Kick_Prep.bmp')
        self.base_kick = pygame.image.load('Gold/Gold_Kick.bmp')
        self.low_kick_prep = pygame.image.load('Gold/Gold_Low_Kick_Prep.bmp')
        self.low_kick = pygame.image.load('Gold/Gold_Low_Kick.bmp')

        # Start each new ship at the bottom right of the screen.
        self.rect.bottomright = self.screen_rect.bottomright

        # store a decimal value for Blue's horizontal and vertical position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # movement flag
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.crouched = False
        self.punch = False
        self.kick = False
        self.attacking = False

    def reset_punch(self):
        if self.crouched:
            self.image = pygame.image.load('Gold/Gold_Crouched.bmp')
            if self.rect.bottom < self.screen_rect.bottom + 20:
                self.y = self.y + 80
            self.attacking = False

        elif self.crouched == False:
            self.image = pygame.image.load('Gold/Gold_Neutral.bmp')
            if self.rect.bottom > self.screen_rect.bottom:
                self.y = self.y - 80
            self.attacking = False

    def reset_kick(self):
        if self.crouched:
            self.image = pygame.image.load('Gold/Gold_Crouched.bmp')
            if self.rect.bottom < self.screen_rect.bottom + 20:
                self.y = self.y + 80
            self.attacking = False


        elif self.crouched == False:
            self.image = pygame.image.load('Gold/Gold_Neutral.bmp')
            if self.rect.bottom > self.screen_rect.bottom:
                self.y = self.y - 80
            self.attacking = False


    def finish_kick(self):
        if self.crouched:
            self.image = self.low_kick
            self.attacking = True
        elif self.crouched == False:
            self.image = self.base_kick
            self.attacking = True


    def update(self):
        """Update the ship's position based on the movement flag."""
        self.screen.blit(self.image, self.rect)
        #update Gold's x and y value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            if self.crouched:
                self.x += self.settings.Gold_crouch_speed
            else:
                self.x += self.settings.Gold_speed
        if self.moving_left and self.rect.left > 0:
            if self.crouched:
                self.x -= self.settings.Gold_crouch_speed
            else:
                self.x -= self.settings.Gold_speed


        # if self.jump == False and self.rect.bottom < self.screen_rect.bottom:
          #  self.y += self.settings.Gold_fall_speed

        # crouch behavior
        if self.crouched and self.punch == False and self.kick == False:
            self.image = pygame.image.load('Gold/Gold_Crouched.bmp')
            if self.rect.bottom < self.screen_rect.bottom + 20:
                self.y = self.y + 80



        elif self.crouched == False and self.punch == False and self.kick == False:
            self.image = pygame.image.load('Gold/Gold_Neutral.bmp')
            if self.rect.bottom > self.screen_rect.bottom:
                self.y = 460.0

        #punch
        if self.punch and self.current_time >= self.gold_punch_time + 15:
            self.attacking = False
        if self.punch and self.current_time >= self.gold_punch_time + 250:
            self.reset_punch()
            self.punch = False

        #kick
        if self.kick and self.current_time >= self.gold_punch_time + 250:
            self.finish_kick()
        if self.kick and self.current_time >= self.gold_punch_time + 265:
            self.attacking = False
        if self.kick and self.current_time >= self.gold_punch_time + 500:
            self.reset_kick()
            self.kick = False


        #update rect object.
        if self.rect.bottom < self.screen_rect.bottom:
            if self.y == 459.99:
                self.y += 460.00 - self.y
            else:
                self.y -= self.settings.Gold_jump_speed

        self.rect.x = self.x
        self.rect.y = self.y

        self.screen.blit(self.image, self.rect)


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
