import random
import pygame


class GoldenSnitch(pygame.sprite.Sprite):

    def __init__(self, game_resolution: tuple, bottom_spacing: int, top_spacing: int,
                 images_paths: tuple, min_speed: int, max_speed: int):
        super().__init__()
        self.resolution = game_resolution
        self.bottom_spacing = bottom_spacing
        self.top_spacing = top_spacing
        self.images_paths = images_paths
        self.image = pygame.image.load(random.choice(self.images_paths))
        self.min_speed = min_speed
        self.max_speed = max_speed

        # create rectangle to add golden snitch
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.choice(range(0, self.resolution[0] - self.image.get_width())),
                             random.choice(range(self.top_spacing,
                                                 self.resolution[1] - (self.bottom_spacing + self.image.get_height()))))
        # random choice of the golden snitch direction and speed
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.speed = random.choice(range(self.min_speed, self.max_speed))

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
