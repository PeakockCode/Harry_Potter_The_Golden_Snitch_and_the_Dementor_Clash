# Import necessary modules
import pygame
import random
from src.enemy import Enemy

# Define the GoldenSnitch class, which inherits from the Enemy class
class GoldenSnitch(Enemy):

    # Initialize a GoldenSnitch instance
    def __init__(self, game_resolution, bottom_spacing, top_spacing,
                 min_speed, max_speed, images_paths):
        # Call the parent class (Enemy) initializer with the provided parameters
        super().__init__(game_resolution, bottom_spacing, top_spacing,
                         min_speed, max_speed, images_paths)

    # Method to update the movement and behavior of the golden snitch
    def update(self):
        # Change the image based on the direction of movement
        if self.direction_x == -1:
            self.image = pygame.image.load(self.images_paths[0])
        else:
            self.image = pygame.image.load(self.images_paths[1])

        # Update the position of the golden snitch based on its direction and speed
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
        # Ensure the golden snitch stays within the screen boundaries and changes direction if needed
        if self.rect.left < 0 or self.rect.right > self.resolution[0]:
            self.direction_x = -1 * self.direction_x
            # Adjust the position to move it within the speed range after changing direction
            self.rect.x += self.direction_x * random.choice(range(self.min_speed, self.max_speed))

        if self.rect.top < self.top_spacing or self.rect.bottom > (self.resolution[1] - self.bottom_spacing):
            self.direction_y = -1 * self.direction_y
            # Adjust the position to move it within the speed range after changing direction
            self.rect.x += self.direction_x * random.choice(range(self.min_speed, self.max_speed))
