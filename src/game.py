import random
import pygame
import sys
from src.dementor import Dementor
from src.golden_snitch import GoldenSnitch


class Game:

    def __init__(self, window, playground_background_path: str, playground_background_coordinates: tuple,
                 window_margin: int,
                 playground_border_width, text_margin: int, game_fps: int,
                 game_resolution: tuple, bottom_spacing: int, top_spacing: int, game_player, golden_snitch_group,
                 bludger_group, dementor_group, background_music_path: str, game_font_type_path: str,
                 hud_font_color, hud_font_size, main_text_font_size,
                 dementor_images_path: list, list_of_dementor_colors: tuple,
                 dementor_min_speed: int, dementor_max_speed: int, golden_snitch_images_paths: tuple,
                 golden_snitch_min_speed: int, golden_snitch_max_speed: int):
        # screen and text settings
        self.window = window
        self.window_margin = window_margin
        self.playground_border_width = playground_border_width
        self.text_margin = text_margin
        # playground background
        self.playground_bg = pygame.image.load(playground_background_path)
        self.playground_bg_coords = playground_background_coordinates
        self.playground_bg_rect = self.playground_bg.get_rect()
        self.playground_bg_rect.topleft = self.playground_bg_coords

        # base score and base round
        self.score = 0
        self.round_number = 0
        # round time
        self.round_time = 0
        self.slow_down_cycle = 0
        # game fps
        self.fps = game_fps
        # game resolution and spacing
        self.resolution = game_resolution
        self.bottom_spacing = bottom_spacing
        self.top_spacing = top_spacing
        # player, golden_snitch, dementor and bludger
        self.game_player = game_player
        self.golden_snitch_group = golden_snitch_group
        self.bludger_group = bludger_group
        self.dementor_group = dementor_group

        # information to renew golden snitch in the game
        self.golden_snitch_images_paths = golden_snitch_images_paths
        self.golden_snitch_min_speed = golden_snitch_min_speed
        self.golden_snitch_max_speed = golden_snitch_max_speed

        # music
        pygame.mixer_music.load(background_music_path)
        pygame.mixer_music.play(-1, 0.0)
        # fonts
        self.hud_game_font = pygame.font.Font(game_font_type_path, hud_font_size)
        self.main_text_font = pygame.font.Font(game_font_type_path, main_text_font_size)
        self.game_font_color = pygame.Color(hud_font_color)

        # dementor images
        self.dementor_images = []
        self.dementor_paths = dementor_images_path
        for path in self.dementor_paths:
            self.dementor_images.append(pygame.image.load(path))
        self.dementor_colors = list_of_dementor_colors
        # dementor speed
        self.min_speed = dementor_min_speed
        self.max_speed = dementor_max_speed
        # selected dementor
        self.targeted_dementor_type = random.randint(0, len(self.dementor_images)-1)
        self.targeted_dementor = self.dementor_images[self.targeted_dementor_type]
        self.targeted_dementor_rect = self.targeted_dementor.get_rect()

    # method to update game
    def update(self):
        self.slow_down_cycle += 1
        if self.slow_down_cycle == self.fps:
            self.round_time += 1
            self.slow_down_cycle = 0

        self.check_collisions()

    # method to generate texts, count score, safe zone, etc
    def draw(self, instruction_text: str):

        # fonts and text settings
        # instructions
        catch_text = self.hud_game_font.render(instruction_text, True, self.game_font_color)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = self.resolution[0]//2
        catch_text_rect.top = self.window_margin

        # score
        score_text = self.hud_game_font.render(f"Score: {self.score}", True, self.game_font_color)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (self.window_margin, self.window_margin)

        # lives
        lives_text = self.hud_game_font.render(f"Lives: {self.game_player.lives}",
                                               True, self.game_font_color)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (self.window_margin, score_text_rect.bottom + self.window_margin)

        # rounds
        round_text = self.hud_game_font.render(f"Round: {self.round_number}", True, self.game_font_color)
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (self.window_margin, lives_text_rect.bottom + self.window_margin)

        # time
        time_text = self.hud_game_font.render(f"Time: {self.round_time}", True, self.game_font_color)
        time_text_rect = round_text.get_rect()
        time_text_rect.topright = (self.resolution[0] - time_text.get_width()//2, self.window_margin)

        # safe zone text
        safe_zone_entries_text = self.hud_game_font.render(f"Safe zone: {self.game_player.safe_zone_entries}",
                                                           True, self.game_font_color)
        safe_zone_entries_text_rect = safe_zone_entries_text.get_rect()
        safe_zone_entries_text_rect.topright = (self.resolution[0] - time_text.get_width()//2,
                                                time_text_rect.bottom + self.window_margin)
        # targeted dementor draw
        self.targeted_dementor_rect.centerx = self.resolution[0]//2
        self.targeted_dementor_rect.top = catch_text_rect.bottom + self.text_margin

        # blitting texts
        self.window.blit(source=catch_text, dest=catch_text_rect)
        self.window.blit(source=score_text, dest=score_text_rect)
        self.window.blit(source=lives_text, dest=lives_text_rect)
        self.window.blit(source=round_text, dest=round_text_rect)
        self.window.blit(source=time_text, dest=time_text_rect)
        self.window.blit(source=safe_zone_entries_text, dest=safe_zone_entries_text_rect)
        self.window.blit(source=self.targeted_dementor, dest=self.targeted_dementor_rect)

        # border of the playground
        pygame.draw.rect(self.window, self.dementor_colors[self.targeted_dementor_type],
                         (0, self.top_spacing, self.resolution[0],
                          self.resolution[1] - (self.top_spacing + self.bottom_spacing)), self.playground_border_width)

    # method to check collisions between player and dementors
    def check_collisions(self):
        # create collided golden_snitch
        collided_golden_snitch = pygame.sprite.spritecollideany(self.game_player, self.golden_snitch_group)
        if collided_golden_snitch:
            self.score += 100 * self.round_number
            self.game_player.catch_sound.play()
            self.golden_snitch_group.remove(collided_golden_snitch)
        # create collided bludger
        collided_bludger = pygame.sprite.spritecollideany(self.game_player, self.bludger_group)
        if collided_bludger:
            self.score -= 5 * self.round_number
            self.game_player.hit_sound.play()
            self.game_player.starting_position_reset()
        # create collided dementor
        collided_dementor = pygame.sprite.spritecollideany(self.game_player, self.dementor_group)
        # control if collided dementor type is targeted dementor
        if collided_dementor:
            if collided_dementor.type == self.targeted_dementor_type:
                self.score += 10 * self.round_number
                collided_dementor.remove(self.dementor_group)
                self.game_player.success_sound.play()
                if self.dementor_group:
                    self.choose_new_target()
                else:
                    self.game_player.starting_position_reset()
                    self.game_player.safe_zone_entries += 1
                    self.game_player.lives += 1
                    self.start_new_round()
            else:
                self.game_player.failure_sound.play()
                self.game_player.lives -= 1
                if self.game_player.lives <= 0:
                    self.pause_game(f"Final score: {self.score}", "Press Enter to play again!")
                    self.reset_game()
                self.game_player.starting_position_reset()

    # method to start new round
    def start_new_round(self):
        # bonus after the finished round
        self.score += int(100 * (self.round_number / (1 + self.round_time)))

        # reset time, slow_down_cycle plus increase round number and safe zone entries
        self.round_time = 0
        self.slow_down_cycle = 0
        self.round_number += 1

        # clear golden_snitch_group
        self.golden_snitch_group.empty()
        # filling golden_snitch_group
        self.golden_snitch_group.add(GoldenSnitch(self.resolution, self.bottom_spacing,
                                                  self.top_spacing, self.golden_snitch_images_paths,
                                                  self.golden_snitch_min_speed, self.golden_snitch_max_speed))

        # clear dementor group to enter new amount of dementors
        self.dementor_group.empty()
        # filling dementor group
        dementor_type = 0
        for path in self.dementor_paths:
            for count in range(self.round_number):
                self.dementor_group.add(Dementor(self.resolution, self.bottom_spacing, self.top_spacing,
                                                 path, self.min_speed, self.max_speed, dementor_type))
            dementor_type += 1
        # new dementor to catch
        self.choose_new_target()

    # method to random choose new dementor to catch
    def choose_new_target(self):
        new_targeted_dementor = random.choice(self.dementor_group.sprites())
        self.targeted_dementor_type = new_targeted_dementor.type
        self.targeted_dementor = new_targeted_dementor.image

    # method to pause game (before start of the new game and before the very first game
    def pause_game(self, main_text, subheading_text):

        # creating main text
        main_text_create = self.main_text_font.render(main_text, True, self.game_font_color)
        main_text_create_rect = main_text_create.get_rect()
        main_text_create_rect.center = (self.resolution[0]//2, ((self.resolution[1]//2)-main_text_create.get_height()))

        # creating subheading text
        subheading_text_create = self.main_text_font.render(subheading_text, True, self.game_font_color)
        subheading_text_create_rect = subheading_text_create.get_rect()
        subheading_text_create_rect.center = (self.resolution[0]//2, main_text_create_rect.bottom +
                                              subheading_text_create.get_height() + self.window_margin)

        # blitting text
        self.window.fill((0, 0, 0))
        self.window.blit(source=main_text_create, dest=main_text_create_rect)
        self.window.blit(source=subheading_text_create, dest=subheading_text_create_rect)
        pygame.display.update()

        # pause_game
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        paused = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # method to reset the game to start from the beginning
    def reset_game(self):
        # the game reset (score, rounds) and the player reset (lives and safe zone entries)
        self.score = 0
        self.round_number = 0
        self.game_player.player_reset()
        # music reset to play background music from the beginning
        pygame.mixer_music.rewind()
        # call start new round method to start the game
        self.start_new_round()
