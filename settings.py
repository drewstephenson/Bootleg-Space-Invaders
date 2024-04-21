class Settings:
    """A class to store the static settings in Bootleg Space Invaders"""

    def __init__(self):
        """Initialize the game's settings"""

        # Screen settings
        self.screen_width = 800
        self.screen_height = 475
        self.background_color = (0, 0, 45)   # dark blue

        # Ship settings
        self.ship_limit = 3  # number of lives

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 25
        self.bullet_color = (255, 255, 0)  # yellow
        self.bullets_allowed = 2   # bullet limit to prevent spamming

        # Alien settings
        self.fleet_drop_speed = 20  # y speed
        self.fleet_direction = 1   # 1 means going right, -1 means going left

        # Difficulty settings
        self.speedup_scale = 1.1  # rate of game speed increase

        # Score settings
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the dynamic settings in the game."""
        # Ship settings
        self.ship_speed = 3.25

        # Bullet settings
        self.bullet_speed = 7.5

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_direction = 1   # 1 means going right, -1 means going left
        self.alien_points = 50

    def increase_speed(self):
        """Apply increases to speed."""
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)