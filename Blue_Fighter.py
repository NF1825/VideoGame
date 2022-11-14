import pygame
from pygame.sprite import Sprite

class Blue_Fighter(Sprite):
    """A class to represent a blue fighter"""

    def __init__(self, fg_game):
        """initialize the fighter"""
        super().__init__()
        self.screen = fg_game.screen
        self.settings = fg_game.settings
        self.screen.rect = fg_game.screen.get_rect()

        

