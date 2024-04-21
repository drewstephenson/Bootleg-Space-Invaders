class GameStats:
    """Track statistics for Bootleg Space Invaders."""

    def __init__(self, game):
        """Initialize the game's statistics."""
        self.settings = game.settings
        self.reset_stats()

        # Keep track of player's high score
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that will to change during the game, gives a value to reset to."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

        