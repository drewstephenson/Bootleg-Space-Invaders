import json

class GameStats:
    """Track statistics for Bootleg Space Invaders."""

    def __init__(self, game):
        """Initialize the game's statistics."""
        self.settings = game.settings
        self.reset_stats()

        # Keep track of player's high score
        self.high_score = self.load_high_score()

    def reset_stats(self):
        """Initialize statistics that will to change during the game, gives a value to reset to."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        """Load the high score from the JSON file."""
        try:
            with open('high_score.json') as f:
                high_score = json.load(f)

        except FileNotFoundError:
            high_score = 0

        return high_score

    def save_high_score(self):
        """Save the high score to the JSON file."""
        with open('high_score.json', 'w') as f:
            json.dump(self.high_score, f)

        