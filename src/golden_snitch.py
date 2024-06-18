import pygame
import random
from src.enemy import Enemy


class GoldenSnitch(Enemy):

    def __init__(self, game_resolution, bottom_spacing, top_spacing,
                 min_speed, max_speed, images_paths):
        super().__init__(game_resolution, bottom_spacing, top_spacing,
                         min_speed, max_speed, images_paths)

    # method to update movement of the golden snitch
    def update(self):
        if self.direction_x == -1:
            self.image = pygame.image.load(self.images_paths[0])
        else:
            self.image = pygame.image.load(self.images_paths[1])
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
    # borders not to move behind
        if self.rect.left < 0 or self.rect.right > self.resolution[0]:
            self.direction_x = -1 * self.direction_x
            self.rect.x += self.direction_x * random.choice(range(self.min_speed, self.max_speed))
        if self.rect.top < self.top_spacing or self.rect.bottom > (self.resolution[1] - self.bottom_spacing):
            self.direction_y = -1 * self.direction_y
            self.rect.x += self.direction_x * random.choice(range(self.min_speed, self.max_speed))
