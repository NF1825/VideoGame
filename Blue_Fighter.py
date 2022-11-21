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

        #extra images
        self.base_punch = pygame.image.load('Blue/Blue_Punch2.bmp')
        self.low_punch = pygame.image.load('Blue/Blue_Low_Punch.bmp')

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value for Blue's horizontal and vertical position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # movement flag
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.crouched = False
        self.punch = False
        self.attacking = False


    def update(self):
        """Update the ship's position based on the movement flag."""
        #update Blue's x and y value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            if self.crouched:
                self.x += self.settings.Blue_crouch_speed
            else:
                self.x += self.settings.Blue_speed
        if self.moving_left and self.rect.left > 0:
            if self.crouched:
                self.x -= self.settings.Blue_crouch_speed
            else:
                self.x -= self.settings.Blue_speed

        #Jumping
        if self.jump and self.crouched == False and self.rect.bottom > self.screen_rect.bottom-15:
            self.jump = False
            for x in range(0,150):
                self.y -= self.settings.Blue_jump_speed
        elif self.jump and self.rect.bottom < self.screen_rect.bottom-10:
            self.jump = False

        if self.jump == False and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.Blue_fall_speed

        #crouch behavior
        if self.crouched:
            self.image = pygame.image.load('Blue/Blue_Crouch.bmp')
            if self.rect.bottom < self.screen_rect.bottom+20:
                self.y = self.y + 80

        elif self.crouched == False:
            self.image = pygame.image.load('Blue/Blue_Neutral.bmp')
            if self.rect.bottom > self.screen_rect.bottom:
                self.y = self.y - 80

        #punch
        if self.punch:
            print(self.image)
            if self.crouched == False:
                self.image = self.base_punch
                print(self.image)
            elif self.crouched:
                self.image = self.low_punch
            self.screen.blit(self.image, self.rect)
            initial = pygame.time.get_ticks()
            current = pygame.time.get_ticks()
            while current < initial+500:
                self.screen.blit(self.image, self.rect)
                current = pygame.time.get_ticks()
            self.reset_punch()






        #update rect object.
        self.rect.x = self.x
        self.rect.y = self.y

        self.screen.blit(self.image, self.rect)

    def reset_punch(self):
        self.punch = False
        self.blitme()

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
