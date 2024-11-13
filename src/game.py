"""
This module defines the Game class for a 2D game created using the Pygame library.
The game involves a player character interacting with golden snitches, bludgers,
and dementors, each affecting the game state (score, lives, etc.) differently.
The class manages game mechanics such as score tracking, collision detection,
round management, and game rendering. The Game class also handles pausing, restarting,
and displaying a scoreboard at the end of the game.

Modules used:
- random: For randomizing game elements (e.g., selecting a targeted dementor)
- pygame: For creating game windows, handling events, and rendering images and text
- sys: For system-level operations (e.g., exiting the game)

Classes imported from the project:
- Dementor: Represents the enemy objects the player interacts with
- GoldenSnitch: Represents special collectible objects in the game
- Scoreboard: Displays the final score and handles the scoreboard UI
"""

# Import necessary modules
import random
import pygame
import sys
from src.dementor import Dementor
from src.golden_snitch import GoldenSnitch
from src.scoreboard import Scoreboard


# Define the Game class
class Game:
    # Initialize a Game instance
    def __init__(self, window, playground_background_path: str, playground_background_coordinates: tuple,
                 window_margin: int,
                 playground_border_width, text_margin: int, game_fps: int,
                 game_resolution: tuple, bottom_spacing: int, top_spacing: int, game_player, golden_snitch_group,
                 bludger_group, dementor_group, background_music_path: str, game_font_type_path: str,
                 hud_font_color, hud_font_size, main_text_font_size,
                 dementor_images_path: list, list_of_dementor_colors: tuple,
                 dementor_min_speed: int, dementor_max_speed: int, golden_snitch_images_paths: tuple,
                 golden_snitch_min_speed: int, golden_snitch_max_speed: int,
                 scoreboard_title, scoreboard_geometry, scoreboard_icon_path,
                 scoreboard_text_color, scoreboard_button_color, scoreboard_button_hover_color, scoreboard_txt_file_path
                 ):
        # Initialize game window and playground properties
        self.window = window
        self.window_margin = window_margin
        self.playground_border_width = playground_border_width
        self.text_margin = text_margin

        # Load and position the playground background image
        self.playground_bg = pygame.image.load(playground_background_path)
        self.playground_bg_coords = playground_background_coordinates
        self.playground_bg_rect = self.playground_bg.get_rect()
        self.playground_bg_rect.topleft = self.playground_bg_coords

        # Initialize score and round attributes
        self.score = 0
        self.round_number = 0
        # round time
        self.round_time = 0
        self.slow_down_cycle = 0

        # Set game frame rate and resolution
        self.fps = game_fps
        # game resolution and spacing
        self.resolution = game_resolution
        self.bottom_spacing = bottom_spacing
        self.top_spacing = top_spacing

        # Assign player and game object groups
        self.game_player = game_player
        self.golden_snitch_group = golden_snitch_group
        self.bludger_group = bludger_group
        self.dementor_group = dementor_group

        # Initialize golden snitch properties for the game
        self.golden_snitch_images_paths = golden_snitch_images_paths
        self.golden_snitch_min_speed = golden_snitch_min_speed
        self.golden_snitch_max_speed = golden_snitch_max_speed

        # Load and play background music
        pygame.mixer_music.load(background_music_path)
        pygame.mixer_music.play(-1, 0.0)

        # Set up font properties for HUD and main text
        self.hud_game_font = pygame.font.Font(game_font_type_path, hud_font_size)
        self.main_text_font = pygame.font.Font(game_font_type_path, main_text_font_size)
        self.game_font_color = pygame.Color(hud_font_color)

        # Load dementor images for use in the game
        self.dementor_images = []
        self.dementor_paths = dementor_images_path
        for path in self.dementor_paths:
            self.dementor_images.append(pygame.image.load(path))
        self.dementor_colors = list_of_dementor_colors

        # Set speed range for dementors
        self.min_speed = dementor_min_speed
        self.max_speed = dementor_max_speed

        # Choose an initial dementor type to target
        self.targeted_dementor_type = random.randint(0, len(self.dementor_images)-1)
        self.targeted_dementor = self.dementor_images[self.targeted_dementor_type]
        self.targeted_dementor_rect = self.targeted_dementor.get_rect()

        # Scoreboard properties
        self.scoreboard_title = scoreboard_title
        self.scoreboard_geometry = scoreboard_geometry
        self.scoreboard_icon_path = scoreboard_icon_path,
        self.scoreboard_text_color = scoreboard_text_color
        self.scoreboard_button_color = scoreboard_button_color
        self.scoreboard_button_hover_color = scoreboard_button_hover_color
        self.scoreboard_txt_file_path = scoreboard_txt_file_path

    # Update game logic (e.g., time tracking, collision checks)
    def update(self):
        self.slow_down_cycle += 1
        if self.slow_down_cycle == self.fps:
            self.round_time += 1 # Increment the round timer
            self.slow_down_cycle = 0 # Reset the cycle counter

        self.check_collisions() # Check for collisions with game objects

    # Render the game interface, including score, lives, rounds, etc.
    def draw(self, instruction_text: str):

        # Create text surfaces and their positions for game information
        catch_text = self.hud_game_font.render(instruction_text, True, self.game_font_color)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = self.resolution[0]//2
        catch_text_rect.top = self.window_margin

        # Display the score
        score_text = self.hud_game_font.render(f"Score: {self.score}", True, self.game_font_color)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (self.window_margin, self.window_margin)

        # Display remaining lives
        lives_text = self.hud_game_font.render(f"Lives: {self.game_player.lives}",
                                               True, self.game_font_color)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (self.window_margin, score_text_rect.bottom + self.window_margin)

        # Display the current round
        round_text = self.hud_game_font.render(f"Round: {self.round_number}", True, self.game_font_color)
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (self.window_margin, lives_text_rect.bottom + self.window_margin)

        # Display the time elapsed
        time_text = self.hud_game_font.render(f"Time: {self.round_time}", True, self.game_font_color)
        time_text_rect = round_text.get_rect()
        time_text_rect.topright = (self.resolution[0] - time_text.get_width()//2, self.window_margin)

        # Display safe zone entries
        safe_zone_entries_text = self.hud_game_font.render(f"Safe zone: {self.game_player.safe_zone_entries}",
                                                           True, self.game_font_color)
        safe_zone_entries_text_rect = safe_zone_entries_text.get_rect()
        safe_zone_entries_text_rect.topright = (self.resolution[0] - time_text.get_width()//2,
                                                time_text_rect.bottom + self.window_margin)
        # Position the targeted dementor image
        self.targeted_dementor_rect.centerx = self.resolution[0]//2
        self.targeted_dementor_rect.top = catch_text_rect.bottom + self.text_margin

        # Blit (draw) text and targeted dementor image into the window
        self.window.blit(source=catch_text, dest=catch_text_rect)
        self.window.blit(source=score_text, dest=score_text_rect)
        self.window.blit(source=lives_text, dest=lives_text_rect)
        self.window.blit(source=round_text, dest=round_text_rect)
        self.window.blit(source=time_text, dest=time_text_rect)
        self.window.blit(source=safe_zone_entries_text, dest=safe_zone_entries_text_rect)
        self.window.blit(source=self.targeted_dementor, dest=self.targeted_dementor_rect)

        # Draw a border around the playground
        pygame.draw.rect(self.window, self.dementor_colors[self.targeted_dementor_type],
                         (0, self.top_spacing, self.resolution[0],
                          self.resolution[1] - (self.top_spacing + self.bottom_spacing)), self.playground_border_width)

    # Check for collisions between player and game objects
    def check_collisions(self):
        # Check if player collides with a golden snitch
        collided_golden_snitch = pygame.sprite.spritecollideany(self.game_player, self.golden_snitch_group)
        if collided_golden_snitch:
            self.score += 100 * self.round_number
            self.game_player.catch_sound.play()
            self.golden_snitch_group.remove(collided_golden_snitch)
        # Check if player collides with a bludger
        collided_bludger = pygame.sprite.spritecollideany(self.game_player, self.bludger_group)
        if collided_bludger:
            self.score -= 5 * self.round_number
            self.game_player.hit_sound.play()
            self.game_player.starting_position_reset()
        # Check if player collides with a dementor
        collided_dementor = pygame.sprite.spritecollideany(self.game_player, self.dementor_group)
        # Control if collided dementor type is targeted dementor
        if collided_dementor:
            if collided_dementor.type == self.targeted_dementor_type:
                self.score += 10 * self.round_number # Increase score
                collided_dementor.remove(self.dementor_group) # Remove the dementor
                self.game_player.success_sound.play() # Play success sound
                if self.dementor_group:
                    self.choose_new_target() # Choose new dementor to catch
                else:
                    # Reset the player and start new round
                    self.game_player.starting_position_reset()
                    self.game_player.safe_zone_entries += 1
                    self.game_player.lives += 1
                    self.start_new_round()
            else:
                # Play failure sound and decrease lives if wrong dementor is caught
                self.game_player.failure_sound.play()
                self.game_player.lives -= 1
                if self.game_player.lives <= 0:
                    # End game if player has no lives left
                    self.pause_game(f"Final score: {self.score}", "Press Enter to play again!")
                    self.draw_scoreboard()
                    self.reset_game()
                self.game_player.starting_position_reset()

    # Method to start new round, reset time and increase difficulty
    def start_new_round(self):
        # Add and count bonus after the finished round
        self.score += int(100 * (self.round_number / (1 + self.round_time)))

        # Reset round time and increase difficulty
        self.round_time = 0
        self.slow_down_cycle = 0
        self.round_number += 1

        # Clear and refill the golden snitch group
        self.golden_snitch_group.empty()
        # Fill golden_snitch_group
        self.golden_snitch_group.add(GoldenSnitch(self.resolution, self.bottom_spacing,
                                                  self.top_spacing, self.golden_snitch_min_speed,
                                                  self.golden_snitch_max_speed, self.golden_snitch_images_paths))

        # Clear and refill the dementor group with increasing number of dementors
        self.dementor_group.empty()
        # Fill dementor group
        dementor_type = 0
        for path in self.dementor_paths:
            for count in range(self.round_number):
                self.dementor_group.add(Dementor(self.resolution, self.bottom_spacing, self.top_spacing,
                                                 self.min_speed, self.max_speed, (path,), dementor_type))
            dementor_type += 1
        # Choose new dementor to catch
        self.choose_new_target()

    # Method to choose (random) new dementor to catch
    def choose_new_target(self):
        new_targeted_dementor = random.choice(self.dementor_group.sprites())
        self.targeted_dementor_type = new_targeted_dementor.type
        self.targeted_dementor = new_targeted_dementor.image

    # Pause the game with an option to restart
    def pause_game(self, main_text, subheading_text):

        # Create and display main and subheading text on the screen
        main_text_create = self.main_text_font.render(main_text, True, self.game_font_color)
        main_text_create_rect = main_text_create.get_rect()
        main_text_create_rect.center = (self.resolution[0]//2, ((self.resolution[1]//2)-main_text_create.get_height()))

        # Create subheading text
        subheading_text_create = self.main_text_font.render(subheading_text, True, self.game_font_color)
        subheading_text_create_rect = subheading_text_create.get_rect()
        subheading_text_create_rect.center = (self.resolution[0]//2, main_text_create_rect.bottom +
                                              subheading_text_create.get_height() + self.window_margin)

        # Blit the text to the screen
        self.window.fill((0, 0, 0))
        self.window.blit(source=main_text_create, dest=main_text_create_rect)
        self.window.blit(source=subheading_text_create, dest=subheading_text_create_rect)
        pygame.display.update()
        # Pause the game and wait for user input to resume
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        paused = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # Method to reset the game to start from the beginning
    def reset_game(self):
        # Reset score and round, as well as player attributes (lives, safe zone entries)
        self.score = 0
        self.round_number = 0
        self.game_player.player_reset()
        # Restart background music from the beginning
        pygame.mixer_music.rewind()
        # Start a new round after reset
        self.start_new_round()

    # Draw the scoreboard at the end of the game
    def draw_scoreboard(self):
        scoreboard = Scoreboard(self.scoreboard_title, self.scoreboard_geometry,
                                self.scoreboard_icon_path, self.scoreboard_text_color,
                                self.scoreboard_button_color, self.scoreboard_button_hover_color,
                                self.scoreboard_txt_file_path, self.score)
        scoreboard.mainloop()
