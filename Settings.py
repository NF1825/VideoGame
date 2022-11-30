import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        # Blue settings
        self.Blue_health = 1000.0
        self.Blue_speed = 5
        self.Blue_jump_speed = 1
        self.Blue_fall_speed = 5
        self.Blue_crouch_speed = 2

        # Gold settings
        self.Gold_health = 1000.0
        self.Gold_speed = 5
        self.Gold_jump_speed = 1
        self.Gold_fall_speed = 5
        self.Gold_crouch_speed = 2

        #timer
        self.timer_length = 60.0
        #seconds
        self.dt = 0