import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and its resources."""
        pygame.init()
        self.settings = Settings()

        # Clock to control the game's frame rate
        self.clock = pygame.time.Clock()

        # For a windowed screen
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # For a full screen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # Title
        pygame.display.set_caption("Bootleg Space Invaders")

        # Instance to store stats
        self.stats = GameStats(self)

        # Scoreboard instance
        self.sb = Scoreboard(self)

        # Ship instance
        self.ship = Ship(self)

        # Group to store bullets
        self.bullets = pygame.sprite.Group()  # Group is like a list with extra functions

        # Group to store aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Clock to control the game's frame rate
        self.clock = pygame.time.Clock()

        # Used to set the game as inactive to wait for the player to press a continue button
        self.game_active = False

        # Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""

        # This loop will run continuously 60 times per second (very fast)
        while True:
            self._check_events()   # check for input (keyboard, mouse)

            if self.game_active:
                self.ship.update()  # get ship's position
                self._update_bullets()  # get each bullet position
                self._update_aliens()   # get each alien position

            self._update_screen()  # show changes on screen
            self.clock.tick(60)  # 60 frames per second

            # Redraw screen for each loop
            self.screen.fill(self.settings.background_color)  # background color
            self.ship.blitme()  # ship image

            # Show the most recent drawn screen
            pygame.display.flip()

    def _check_events(self):
        """Responds to key presses and mouse clicks."""
        for event in pygame.event.get():
            # If the window's close button is clicked, the game will exit
            if event.type == pygame.QUIT:
                sys.exit()

            # If key is held down, the ship will move
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            # If key is released, the ship will stop moving
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            # If the mouse clicks the play button, the game will start
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Responds to a key being pressed down."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        # Adds a keyboard shortcut to quit the game 'q'
        elif event.key == pygame.K_q:
            sys.exit()

        # Shoots a bullet when the space bar is pressed
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        # Adds a keyboard shortcut to start the game 'Enter'
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        """Responds to a key being released."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Starts a new game when the player clicks the play button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()

    def _start_game(self):
        """Starts a new game."""
        # Reset stats for a new game
        self.settings.initialize_dynamic_settings()  # reset game speed
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True

        # Clear the screen of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor when the game is active
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Creates a limited amount of bullets on the screen and adds them to a group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)   # add() is the group equivalent of append()

    def _update_bullets(self):
        """Update position of current bullets and delete old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Delete bullets that have gone off-screen to save memory
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Checks for any alien-bullet collisions, deleting both if detected."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()

        # When all aliens are destroyed, create a new fleet, increase difficulty
        if not self.aliens:
            self.bullets.empty()  # clear out any remaining bullets
            self._create_fleet()  # create new fleet
            self.settings.increase_speed()  # increase game speed

            # Increase level display
            self.stats.level += 1
            self.sb.prep_level()

        # Potential power up: piercing bullet
        # collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)

    def _create_alien(self, x_position, y_position):
        """Creates an alien and places it in a row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Creates aliens in a row until there is no more space
        # Each alien is 2 alien widths apart, aliens on end of row are 1.5 alien widths from the edge
        # Vertical spacing is 2 alien heights, stops 6 alien heights from the bottom of the screen
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size   # rect.size is a tuple (width, height)

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 4.5 * alien_width):  # 4.5 alien width spacing from the edge
                self._create_alien(current_x, current_y)
                current_x += 2.0 * alien_width  # 2 alien width spacing between aliens

            # Row finished, reset x and increment y value.
            current_x = alien_width
            current_y += 2.0 * alien_height

    def _update_aliens(self):
        """Update the position of each alien in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Check if alien hit the ship
        self._check_ship_alien_collisions()

        # Check if alien hit bottom of the screen
        self._check_aliens_bottom()

    def _check_ship_alien_collisions(self):
        """Checks for any ship-alien collisions."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  # looks for collision with the alien group and ship
            self._ship_hit()

    def _ship_hit(self):
        """Handles the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Lose a life, decrement the number of ships left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Clear any aliens and bullets on the screen
            self.aliens.empty()
            self.bullets.empty()

            # Recenter the ship, create a new fleet
            self._create_fleet()
            self.ship.center_ship()

            # Pause the game to allow the player to recover
            sleep(1.0)  # 1.0 second pause

        else:
            self.game_active = False
            pygame.mouse.set_visible(True)   # enable mouse again after game over

    def _check_aliens_bottom(self):
        """Checks if any aliens have reached the bottom of the screen, treating it like losing a ship."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Executes _change_fleet_direction() at the appropriate time. """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Allows the fleet to move down and change direction after hitting the edge of the screen."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed   # drops aliens the same distance as fleet drop speed
        self.settings.fleet_direction *= -1   # alternates between moving left and right after hitting edge

    def _update_screen(self):
        """Update images on the screen, flip to the new screen."""
        
        # Redraw screen for each loop
        self.screen.fill(self.settings.background_color)  # background color
        for bullet in self.bullets.sprites():   # each bullet
            bullet.draw_bullet()
        self.ship.blitme()   # ship image
        self.aliens.draw(self.screen)   # draw() is the group equivalent of blit()
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # Show the most recent drawn screen
        pygame.display.flip()


if __name__ == '__main__':
    # Make the game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
