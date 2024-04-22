import pygame.font


class Message:
    """Class for creating messages to display in game."""

    def __init__(self, game, msg):
        """Initialize the message's attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.ship = game.ship

        # Set the dimensions of the message, adjusting it to the screen size
        self.width, self.height = 200, 50
        self.message_color = (255, 255, 255)  # white
        self.font = pygame.font.SysFont(None, 36)

        # Prep game message
        self.prep_game_msg(msg)

        # Prep ship message
        self.prep_ship_msg(msg)

    def prep_game_msg(self, msg):
        """Turn given message into an image and display it above the center of the screen."""
        self.game_msg_image = self.font.render(msg, True, self.message_color)
        self.game_msg_rect = self.game_msg_image.get_rect()
        self.game_msg_rect.centerx = self.screen_rect.centerx
        self.game_msg_rect.top = self.screen_rect.top + 50

    def draw_game_msg(self):
        """Draw the game message on screen."""
        self.screen.blit(self.game_msg_image, self.game_msg_rect)

    def prep_ship_msg(self, msg):
        """Turn given message into an image and display it above the ship."""
        self.ship_msg_image = self.font.render(msg, True, self.message_color)
        self.ship_msg_rect = self.ship_msg_image.get_rect()
        self.ship_msg_rect.midbottom = (self.ship.rect.midtop[0], self.ship.rect.midtop[1] - 10)  # aligns message slightly above the ship

    def draw_ship_msg(self):
        """Draw the message on screen above the ship."""
        self.screen.blit(self.ship_msg_image, self.ship_msg_rect)

