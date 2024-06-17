import pygame
import random


class Player(pygame.sprite.Sprite):

    def __init__(self, game_resolution: tuple, bottom_spacing: int, top_spacing: int,
                 images_paths: tuple, speed: int, lives: int, safe_zone_entries: int,
                 success_sound_path: str, failure_sound_path: str,
                 catch_sound_path: str, hit_sound_path: str):
        super().__init__()
        self.resolution = game_resolution
        # variable to store all image paths
        # (for moving left, left up, left down, right, right up, right down)
        self.images_paths = images_paths
        self.image = pygame.image.load(self.images_paths[0])
        self.bottom_spacing = bottom_spacing
        self.top_spacing = top_spacing
        self.rect = self.image.get_rect()
        self.rect.center = (self.resolution[0]//2, self.resolution[1] - self.image.get_height())
        self.speed = speed
        self.base_lives = lives
        self.lives = lives
        self.base_safe_zone_entries = safe_zone_entries
        self.safe_zone_entries = safe_zone_entries

        self.success_sound = pygame.mixer.Sound(success_sound_path)
        self.success_sound.set_volume(0.1)
        self.failure_sound = pygame.mixer.Sound(failure_sound_path)
        self.failure_sound.set_volume(0.1)
        self.catch_sound = pygame.mixer.Sound(catch_sound_path)
        self.catch_sound.set_volume(0.1)
        self.hit_sound = pygame.mixer.Sound(hit_sound_path)
        self.hit_sound.set_volume(0.1)

        # attribute to store the last direction (left or right) of movement of the player
        self.last_direction = None

    # method to update player
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.image = pygame.image.load(self.images_paths[0])
            self.rect.x -= self.speed
            self.last_direction = "left"
        if keys[pygame.K_RIGHT] and self.rect.right < self.resolution[0]:
            self.image = pygame.image.load(self.images_paths[3])
            self.rect.x += self.speed
            self.last_direction = "right"
        if keys[pygame.K_UP] and self.rect.top > (0 + self.top_spacing):
            self.rect.y -= self.speed
            if keys[pygame.K_UP] and self.last_direction == "left":
                self.image = pygame.image.load(self.images_paths[1])
            if keys[pygame.K_UP] and self.last_direction == "right":
                self.image = pygame.image.load(self.images_paths[4])
            if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                self.image = pygame.image.load(self.images_paths[1])
                self.last_direction = "left"
            if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                self.image = pygame.image.load(self.images_paths[4])
                self.last_direction = "right"
        if keys[pygame.K_DOWN] and self.rect.bottom < (self.resolution[1] - self.bottom_spacing):
            self.rect.y += self.speed
            if keys[pygame.K_DOWN] and self.last_direction == "left":
                self.image = pygame.image.load(self.images_paths[2])
            if keys[pygame.K_DOWN] and self.last_direction == "right":
                self.image = pygame.image.load(self.images_paths[5])
            if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                self.image = pygame.image.load(self.images_paths[2])
                self.last_direction = "left"
            if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                self.image = pygame.image.load(self.images_paths[5])
                self.last_direction = "right"

    # method to go to safe zone
    def back_to_safe_zone(self):
        if self.safe_zone_entries > 0:
            self.safe_zone_entries -= 1
            self.rect.centery = (self.resolution[1] - self.image.get_height())

    # method to move player to safe zone after losing a life or after end of the round
    def starting_position_reset(self):
        self.rect.center = (self.resolution[0]//2, self.resolution[1] - self.image.get_height())

    def player_reset(self):
        self.lives = self.base_lives
        self.safe_zone_entries = self.base_safe_zone_entries
