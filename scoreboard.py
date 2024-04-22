import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """A class to display the player's score."""

    def __init__(self, game):
        """Initialize score-keeping attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # Font settings for score display
        self.text_color = (255, 255, 255)   # white
        self.font = pygame.font.SysFont(None, 36)

        # Prepare the initial score display
        self.prep_score()

        # Prepare high score display
        self.prep_high_score()

        # Prepare level display
        self.prep_level()

        # Prepare lives display
        self.prep_ships()

    def prep_score(self):
        """Turns the score into an image."""
        rounded_score = round(self.stats.score, -1)  # -1 rounds the score to the nearest 10
        score_str = f"Score: {rounded_score:,}"  # adds commas every 3 digits
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.background_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20

    def prep_high_score(self):
        """Turn the high score into an image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"Highest: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                                 self.settings.background_color)

        # Puts the high score at the top center of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx  # aligns high score to center screen
        self.high_score_rect.top = self.score_rect.top  # aligns high score to top of screen

    def check_high_score(self):
        """If the current score is higher than the high score, update the high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw the score on the screen."""
        self.screen.blit(self.score_image, self.score_rect)  # draw current score
        self.screen.blit(self.high_score_image, self.high_score_rect)  # draw high score
        self.screen.blit(self.level_image, self.level_rect)  # draw level
        self.ships.draw(self.screen)  # draw ships

    def prep_level(self):
        """Turn the current level the player is on into an image."""
        level_str = f"Level: {str(self.stats.level)}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.background_color)

        # Position the level below the current score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right  # aligns level to the right of the score
        self.level_rect.top = self.score_rect.bottom + 10   # 10 pixels below the score

    def show_level(self):
        """Draw the level on screen."""
        self.screen.blit(self.level_image, self.level_rect)

    def prep_ships(self):
        """Show how many lives the player has left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)




