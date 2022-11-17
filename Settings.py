import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # Blue settings
        self.Blue_speed = 1
        self.Blue_jump_speed = 1.25
        self.Blue_fall_speed = 1.5