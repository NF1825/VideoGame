import pygame
from pygame.sprite import Sprite
import time


class Blue_Fighter(Sprite):
    """A class to represent a blue fighter"""

    def __init__(self, fg_game):
        """initialize the fighter"""
        super().__init__()
        self.screen = fg_game.screen
        self.settings = fg_game.settings
        self.screen_rect = fg_game.screen.get_rect()

        #load initial image for blue fighter
        self.image =pygame.image.load('Blue/Blue_Neutral.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value for Blue's horizontal and vertical position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # movement flag
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.moving_down = False


    def update(self):
        """Update the ship's position based on the movement flag."""
        #update Blue's x and y value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.Blue_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.Blue_speed
        if self.jump and self.rect.bottom > self.screen_rect.bottom-15:
            self.jump = False
            for x in range(0,150):
                self.y -= self.settings.Blue_jump_speed
        elif self.jump and self.rect.bottom < self.screen_rect.bottom-10:
            self.jump = False

        if self.jump == False and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.Blue_fall_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.Blue_speed

        #update rect object.
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
