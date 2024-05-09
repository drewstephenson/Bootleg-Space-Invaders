import sys
from time import sleep
import pygame
import random
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from messager import Message
from star import Star
from powerup import Powerup


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and its resources."""
        pygame.init()
        self.settings = Settings()

        # Clock to control the game's frame rate
        self.clock = pygame.time.Clock()

        # For a windowed screen
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.full_screen = False

        # For a full screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.full_screen = True

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

        # Used to set the game as inactive on the first startup to wait for the player to press start
        self.first_startup = True

        # Used to set the game as inactive to wait for the player to press a button to continue or end
        self.game_active = False

        # Indicate ship has been hit
        self.ship_down = False

        # Play button
        self.play_button = Button(self, "Play")

        # Continue button
        self.continue_button = Button(self, "Continue")

        # Game over message
        self.game_over = Message(self, "Game Over")

        # Ship hit message
        self.ship_message = Message(self, "ow")

        # Group to store stars
        self.stars = pygame.sprite.Group()
        self._create_stars()

        # Group to store powerups
        self.powerups = pygame.sprite.Group()

        # Triple shot powerup
        self.triple_shot_active = False

        # Piercing bullet powerup
        self.pierce_active = False

        # Powerup messages
        self.message = None

    def run_game(self):
        """Start the main loop for the game."""

        # This loop will run continuously 60 times per second (very fast)
        while True:
            self._check_events()   # check for input (keyboard, mouse)

            if self.game_active and not self.first_startup:
                self.ship.update()  # get ship's position
                self._update_bullets()  # get each bullet position
                self._update_aliens()   # get each alien position
                self._update_powerups()  # get each powerup position
                self._update_stars()  # get each star position

            self._update_screen()  # show changes on screen
            self.clock.tick(60)  # 60 frames per second

            # Redraw screen for each loop
            self.screen.fill(self.settings.background_color)  # background color
            self.ship.blitme()  # ship image

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

            # If the ship is hit, display message for a moment
            elif event.type == pygame.USEREVENT:
                self.ship_down = False

            elif event.type == pygame.USEREVENT + 1:
                self.pierce_active = False   # Pierce timer ends

            elif event.type == pygame.USEREVENT + 2:
                self.triple_shot_active = False  # Triple shot timer ends

            elif event.type == pygame.USEREVENT + 3:
                self.message = None  # Powerup message timer ends

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

        # Adds a keyboard shortcut to start the game 'p'
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        """Responds to a key being released."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Starts a new game when the player clicks the play or continue button."""
        play_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_clicked and self.first_startup:
            self._start_game()

        continue_clicked = self.continue_button.rect.collidepoint(mouse_pos)
        if continue_clicked and not self.game_active:
            self._start_game()

    def _start_game(self):
        """Starts a new game."""
        # Reset stats for a new game
        self.settings.initialize_dynamic_settings()  # reset game speed
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.first_startup = False
        self.game_active = True

        # Clear the screen of any remaining aliens, bullets, and powerups
        self.aliens.empty()
        self.bullets.empty()
        self.powerups.empty()

        # Create new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor when the game is active
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Creates a limited amount of bullets on the screen and adds them to a group."""
        if self.triple_shot_active:
            # Allow 2 bursts of 3 bullets
            self.settings.bullets_allowed = 6

            if len(self.bullets) < self.settings.bullets_allowed:
                # Create 3 bullets in a row
                new_bullet1 = Bullet(self)
                new_bullet2 = Bullet(self)
                new_bullet3 = Bullet(self)

                # Set the position of the 2 additional bullets
                new_bullet2.rect.x += 30
                new_bullet3.rect.x -= 30

                # Add bullets to the group
                self.bullets.add(new_bullet1, new_bullet2, new_bullet3)

        else:
            # Allow 2 bullets on screen at a time
            self.settings.bullets_allowed = 2

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
        if self.pierce_active:
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
            self.settings.bullet_speed = 15.0   # Make bullets travel faster for piercing shot

        else:
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
            self.settings.bullet_speed = 7.5   

        if collisions:
            for alien_hit in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien_hit)
                for alien in alien_hit:
                    self._create_powerup(alien)
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

    def _create_powerup(self, alien):
        """Shooting an alien has a chance to drop a powerup."""
        # 1 percent chance of dropping a powerup
        if random.randint(1, 100) == 1:
            powerup = Powerup(self, alien)
            self.powerups.add(powerup)

    def _update_powerups(self):
        """Update the position of each powerup on the screen."""
        self.powerups.update()

        # Delete any powerups that have gone off-screen
        for powerup in self.powerups.copy():
            if powerup.rect.bottom >= self.settings.screen_height:
                self.powerups.remove(powerup)

        # Check if the powerup has collided with the ship
        self._check_powerup_ship_collisions()

    def _check_powerup_ship_collisions(self):
        """Checks if a powerup has collided with the ship."""
        power_collision = pygame.sprite.spritecollideany(self.ship, self.powerups)
        if power_collision:
            power_collision.apply_power()
            self.powerups.remove(power_collision)

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
        # Vertical spacing is 2 alien heights, stops after making 5 rows of aliens
        # If you are using full screen, the aliens will start lower
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size   # rect.size is a tuple (width, height)

        current_x, current_y = alien_width, alien_height
        if self.full_screen:
            current_y += 7.0 * alien_height

        row = 0
        while row < 5:
            while current_x < (self.settings.screen_width - 4.5 * alien_width):  # 4.5 alien width spacing from the edge
                self._create_alien(current_x, current_y)
                current_x += 2.0 * alien_width  # 2 alien width spacing between aliens

            # Row finished, reset x and increment y value.
            current_x = alien_width
            current_y += 2.0 * alien_height
            row += 1

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

            # Clear any aliens, bullets, and powerups on the screen
            self.aliens.empty()
            self.bullets.empty()
            self.powerups.empty()

            # Display message
            self.ship_down = True
            self.ship_message.prep_ship_msg("ow")
            pygame.time.set_timer(pygame.USEREVENT, 1500)  # 1.5 seconds

            # Recenter the ship, create a new fleet
            self._create_fleet()
            self.ship.center_ship()

            # Pause the game for a moment
            sleep(1.0)

        else:
            self.game_active = False
            pygame.mouse.set_visible(True)   # enable mouse again after game over
            self.game_over.prep_game_msg("Game Over")

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

    def _create_stars(self):
        """Create a group of stars."""
        for _ in range(100):
            star = Star(self)
            self.stars.add(star)

    def _update_stars(self):
        """Update position of current bullets and delete old bullets."""
        # Update star positions
        self.stars.update()

        # Delete stars that have gone off-screen, create new one at top of screen
        for star in self.stars.copy():
            if star.rect.bottom >= self.settings.screen_height:
                self.stars.remove(star)
                new_star = Star(self, 0)
                self.stars.add(new_star)

    def _update_screen(self):
        """Update images on the screen, flip to the new screen."""
        
        # Redraw screen for each loop
        self.screen.fill(self.settings.background_color)  # background color
        for bullet in self.bullets.sprites():   # draw each bullet
            bullet.draw_bullet()
        for powerup in self.powerups.sprites():  # draw each powerup
            powerup.draw_powerup()
        for star in self.stars.sprites():  # draw each star
            star.draw_star()
        self.ship.blitme()   # ship image
        self.aliens.draw(self.screen)   # draw() is the group equivalent of blit()
        self.sb.show_score()

        # Draw powerup messages
        if self.message:
            self.message.draw_game_msg()

        # Draw the play button if the game is inactive
        if self.first_startup:
            self.play_button.draw_button()

        # Draw the continue button instead of the play button after losing, display "Game Over"
        if not self.game_active and not self.first_startup:
            self.continue_button.draw_button()
            self.game_over.draw_game_msg()

        # Draw the ship hit message
        if self.ship_down:
            self.ship_message.draw_ship_msg()

        # Show the most recent drawn screen
        pygame.display.flip()


if __name__ == '__main__':
    # Make the game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
