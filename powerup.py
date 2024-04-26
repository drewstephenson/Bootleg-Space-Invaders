import pygame
from pygame.sprite import Sprite
import random
from messager import Message


class Powerup(Sprite):
    """A class to represent a powerup the player can collect in game."""
    def __init__(self, game, alien):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game

        # Create the powerup's rect and set its position
        self.rect = pygame.Rect(0, 0, self.settings.powerup_width, self.settings.powerup_height)
        self.rect.center = alien.rect.center

        # Powerup color
        self.color = (255, 0, 0)  # red

        # Store y value as a float
        self.y = float(self.rect.y)

        # List of possible powerups
        self.powers = ["extra_life", "pierce", "triple_shot", "nuke"]
        self.power = random.choice(self.powers)

    def update(self):
        """Update the powerup's position."""
        self.y += self.settings.powerup_speed
        self.rect.y = self.y

    def draw_powerup(self):
        """Draw the powerup on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def apply_power(self):
        """Apply the powerup to the game."""
        if self.power == "extra_life":
            # Increase life, update scoreboard picture
            self.game.stats.ships_left += 1
            self.game.sb.prep_ships()
            self.game.message = Message(self.game, "Extra life!!")
            self.game.message.draw_game_msg()

        if self.power == "pierce":
            self.game.pierce_active = True
            pygame.time.set_timer(pygame.USEREVENT + 1, self.game.settings.powerup_duration)
            self.game.message = Message(self.game, "Piercing shot!!")
            self.game.message.draw_game_msg()

        if self.power == "triple_shot":
            self.game.triple_shot_active = True
            pygame.time.set_timer(pygame.USEREVENT + 2, self.game.settings.powerup_duration)
            self.game.message = Message(self.game, "Triple shot!!")
            self.game.message.draw_game_msg()

        if self.power == "nuke":
            for _ in self.game.aliens.sprites():
                self.game.stats.score += self.game.settings.alien_points
                self.game.sb.prep_score()
                self.game.sb.check_high_score()

            self.game.aliens.empty()
            self.game.message = Message(self.game, "Boom!!")
            self.game.message.draw_game_msg()

        # Set a timer for each powerup message
        pygame.time.set_timer(pygame.USEREVENT + 3, 2000)







