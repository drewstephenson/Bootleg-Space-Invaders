import pygame
from pygame.sprite import Sprite  # Sprite allows grouping related elements in the game


class Bullet(Sprite):
    """A class allows the ship to shoot bullets"""

    def __init__(self, game):
        """Create a bullet at the ship's position"""
        super().__init__()  # inherits from Sprite class
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # Create the bullet's rect at (0, 0), correct its position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """Update the position of the bullet going up the screen"""
        # Precise update of the bullet's position
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draws the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)  # fills the rect space with the color on screen
