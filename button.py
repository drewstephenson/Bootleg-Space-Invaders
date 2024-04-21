import pygame.font   # Allows Pygame to render text to the screen


class Button:
    """Class for creating buttons in pygame."""

    def __init__(self, game, msg):
        """Initialize the button's attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions of the button, adjusting it to the screen size
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)  # green
        self.text_color = (255, 255, 255)  # white
        self.font = pygame.font.SysFont(None, 48)   # None makes it a default font, 48 is the size
        # Create button's rect and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Message for the button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn given message into a rendered image and center it on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)  # draws the text
        self.msg_image_rect = self.msg_image.get_rect()  # gets its rect
        self.msg_image_rect.center = self.rect.center  # centers it on the button

    def draw_button(self):
        """Draw the button and then the message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


