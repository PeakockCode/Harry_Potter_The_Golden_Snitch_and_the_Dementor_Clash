# Import necessary modules
import pygame
import random

# Define the Enemy class, which inherits from pygame's Sprite class for game object management
class Enemy(pygame.sprite.Sprite):
    # Initialize an Enemy instance
    def __init__(self, game_resolution: tuple, bottom_spacing: int, top_spacing: int,
                 min_speed: int, max_speed: int, images_paths):
        # Call the parent class (Sprite) initializer
        super().__init__()
        # Set game resolution and spacing properties
        self.resolution = game_resolution
        self.bottom_spacing = bottom_spacing
        self.top_spacing = top_spacing
        self.images_paths = images_paths
        self.min_speed = min_speed
        self.max_speed = max_speed
        # Load a random image for the enemy from the provided image paths
        self.image = pygame.image.load(random.choice(self.images_paths))
        # create a rectangle representing the enemy and set its initial position at random coordinates
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.choice(range(0, self.resolution[0]-self.image.get_width())),
                             random.choice(range(self.top_spacing,
                                                 self.resolution[1]-(self.bottom_spacing+self.image.get_height()))))
        # Choose random direction and speed for the enemy's movement
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.speed = random.choice(range(self.min_speed, self.max_speed))

    # Method to update the enemy's position on the screen
    def update(self):
        # Update the position of the enemy based on its direction and speed
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
        # Prevent the enemy from moving outside the screen boundaries and change direction if necessary
        if self.rect.left < 0 or self.rect.right > self.resolution[0]:
            self.direction_x = -1 * self.direction_x
        if self.rect.top < self.top_spacing or self.rect.bottom > (self.resolution[1] - self.bottom_spacing):
            self.direction_y = -1 * self.direction_y
