import pygame
import sys
from Settings import Settings
from Blue_Fighter import Blue_Fighter
import time
import multiprocessing

#make fighting game


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Fighter")
        self.blue_punch_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()

        self.blue = Blue_Fighter(self)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.blue.blitme()

        #make the most recently drawn screen visible.
        pygame.display.flip()
        

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
        elif event.key == pygame.K_a:
            # Move blue to the left.
            self.blue.moving_left = True
        elif event.key == pygame.K_w:
            #Make blue jump
            self.blue.jump = True
        elif event.key == pygame.K_s:
            #move blue down
            self.blue.crouched = True
        elif event.key == pygame.K_1:
            self.punch("blue")
            self.blue.blue_punch_time = pygame.time.get_ticks()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.blue.moving_right = False
        elif event.key == pygame.K_a:
            self.blue.moving_left = False
        elif event.key == pygame.K_s:
            self.blue.crouched = False

    def punch(self,color):
        if color == "blue":
            self.blue.punch = True
            print(self.blue.image)
            if self.blue.crouched == False:
                self.blue.image = self.blue.base_punch
                print(self.blue.image)
            elif self.blue.crouched:
                self.blue.image = self.blue.low_punch




    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.current_time = pygame.time.get_ticks()
            self.blue.current_time = self.current_time
            self._check_events()
            self.blue.update()


            self._update_screen()


if __name__ == '__main__':
    # make a game instance, and run the game.
    fg = Game()
    fg.run_game()






