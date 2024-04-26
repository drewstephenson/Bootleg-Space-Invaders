import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the player's ship"""

    def __init__(self, game):  # Ship has access to the game instance's resources
        """Initialize the ship and its starting position"""
        super().__init__()  # inherits from Sprite class
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        # Flags to control movement
        self.moving_right = False
        self.moving_left = False

        # Load the ship's image
        self.image = pygame.image.load('si_images/spaceship1.png')

        # Resize the image
        ship_width = game.settings.screen_width // 25
        ship_height = game.settings.screen_height // 15
        self.image = pygame.transform.scale(self.image, (40, 40))

        # Get the resized ship's rect
        self.rect = self.image.get_rect()

        # Start the ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Convert rect to float to store exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship at its current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Re-centers the ship to the mid-bottom of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position by checking the movement flags"""

        # Holding both left and right arrow keys will make the ship stop
        # This will also prevent the ship from going off-screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x
