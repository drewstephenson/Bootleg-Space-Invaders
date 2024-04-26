import pygame
import random
from pygame.sprite import Sprite


class Star(Sprite):
    """Class to represent a star in the game's background."""
    def __init__(self, game, y=None):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Set the star's width and height, place it randomly on the screen
        self.rect = pygame.Rect(0, 0, self.settings.star_width, self.settings.star_height)  # 2x2 pixel stars
        self.rect.x = random.randint(0, game.settings.screen_width)

        # If y value is passed, use that value. Otherwise, place star with random y value.
        if y is not None:
            self.rect.y = y
        else:
            self.rect.y = random.randint(0, game.settings.screen_height)

        # Store y value as a float for precision
        self.y = float(self.rect.y)

        # Color
        self.color = (255, 255, 255)  # white

    def draw_star(self):
        """Draw the star on screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        """Update the star's position."""
        self.y += self.settings.star_speed
        self.rect.y = self.y

