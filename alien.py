import pygame
from pygame.sprite import Sprite
import random


class Alien(Sprite):
    """Class to represent an alien in the fleet"""

    def __init__(self, game):
        """Initialize the alien's traits and its starting position"""
        super().__init__()  # inherits from Sprite class
        self.screen = game.screen
        self.settings = game.settings

        # List of possible alien images
        self.alien_images = ['si_images/red_bug.png', 'si_images/blue_bug.png', 'si_images/galaga_boss.png']

        # Load random alien image
        self.image = pygame.image.load(random.choice(self.alien_images))

        # Resize the image
        self.image = pygame.transform.scale(self.image, (30, 30))   # apply changes

        # Get the resized alien's rect
        self.rect = self.image.get_rect()

        # Start new aliens at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's horizontal position as a float value
        self.x = float(self.rect.x)

    def update(self):
        """Allows the alien to move."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Returns True when an alien reaches the edge of the screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)



