import pygame
import sys
from Settings import Settings
import time

#make rythem game that scores based on proximity from icon center to a position value.


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Rythem Game")

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        #make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_events(self):
        """respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_q:
            sys.exit()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()


            self._update_screen()

if __name__ == '__main__':
    # make a game instance, and run the game.
    rg = Game()
    rg.run_game()






