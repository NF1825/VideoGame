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
        self.blue_punch_time = fg_game.blue_punch_time
        self.current_time = pygame.time.get_ticks()

        #load initial image for blue fighter
        self.image = pygame.image.load('Blue/Blue_Neutral.bmp')
        self.rect = self.image.get_rect()

        # load soundfiles
        self.hurt = pygame.mixer.Sound("Gold/roblox-death-sound_1.mp3")

        #extra images
        self.base_punch = pygame.image.load('Blue/Blue_Punch2.bmp')
        self.low_punch = pygame.image.load('Blue/Blue_Low_Punch.bmp')
        self.base_kick_prep = pygame.image.load('Blue/Blue_High_Kick_Prep_2.bmp')
        self.base_kick = pygame.image.load('Blue/Blue_High_Kick.bmp')
        self.low_kick_prep = pygame.image.load('Blue/Blue_Low_Kick_Prep.bmp')
        self.low_kick = pygame.image.load('Blue/Blue_Low_Kick.bmp')

        # Start each new blue fighter at the bottom left of the screen.
        self.rect.bottomleft = self.screen_rect.bottomleft

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
            self.image = pygame.image.load('Blue/Blue_Crouch.bmp')
            if self.rect.bottom < self.screen_rect.bottom + 20:
                self.y = self.y + 80
            self.attacking = False

        elif self.crouched == False:
            self.image = pygame.image.load('Blue/Blue_Neutral.bmp')
            if self.rect.bottom > self.screen_rect.bottom:
                self.y = self.y - 80
            self.attacking = False

    def reset_kick(self):
        if self.crouched:
            self.image = pygame.image.load('Blue/Blue_Crouch.bmp')
            if self.rect.bottom < self.screen_rect.bottom + 20:
                self.y = self.y + 80
            self.attacking = False


        elif self.crouched == False:
            self.image = pygame.image.load('Blue/Blue_Neutral.bmp')
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


        #if self.jump == False and self.rect.bottom < self.screen_rect.bottom:
            #self.y += self.settings.Blue_fall_speed

        #crouch behavior
        if self.crouched and self.punch == False and self.kick == False:
            self.image = pygame.image.load('Blue/Blue_Crouch.bmp')
            if self.rect.bottom < self.screen_rect.bottom+20:
                self.y = self.y + 80





        elif self.crouched == False and self.punch == False and self.kick == False:
            self.image = pygame.image.load('Blue/Blue_Neutral.bmp')
            if self.rect.bottom > self.screen_rect.bottom:
                self.y = 440.00


        #punch
        if self.punch and self.current_time >= self.blue_punch_time + 15:
            self.attacking = False
        if self.punch and self.current_time >= self.blue_punch_time + 250:
            self.reset_punch()
            self.punch = False

        #kick
        if self.kick and self.current_time >= self.blue_punch_time + 250:
            self.finish_kick()
        if self.kick and self.current_time >= self.blue_punch_time + 265:
            self.attacking = False
        if self.kick and self.current_time >= self.blue_punch_time + 500:
            self.reset_kick()
            self.kick = False



        #update rect object.
        if self.rect.bottom < self.screen_rect.bottom:
            if self.y == 439.99:
                self.y += 440.00 - self.y
            else:
                self.y -= self.settings.Blue_jump_speed
        #print(self.y)

        self.rect.x = self.x
        self.rect.y = self.y

        self.screen.blit(self.image, self.rect)


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
