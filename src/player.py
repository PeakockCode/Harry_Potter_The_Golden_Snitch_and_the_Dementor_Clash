# Import necessary modules
import pygame


# Define the Player class, which inherits from pygame's Sprite class for game object management
class Player(pygame.sprite.Sprite):

    # Initialize a Player instance
    def __init__(self, game_resolution: tuple, bottom_spacing: int, top_spacing: int,
                 images_paths: tuple, speed: int, lives: int, safe_zone_entries: int,
                 success_sound_path: str, failure_sound_path: str,
                 catch_sound_path: str, hit_sound_path: str):
        # Call the parent class (Sprite) initializer
        super().__init__()
        self.resolution = game_resolution

        # Store all image paths for different movement directions
        # (left, left up, left down, right, right up, right down)
        self.images_paths = images_paths
        self.image = pygame.image.load(self.images_paths[0])  # Load initial image
        self.bottom_spacing = bottom_spacing
        self.top_spacing = top_spacing

        # Create a rectangle for the player and set its starting position
        self.rect = self.image.get_rect()
        self.rect.center = (self.resolution[0] // 2, self.resolution[1] - self.image.get_height())

        # Initialize movement speed, lives, and safe zone entry limits
        self.speed = speed
        self.base_lives = lives
        self.lives = lives
        self.base_safe_zone_entries = safe_zone_entries
        self.safe_zone_entries = safe_zone_entries

        # Load and set the volume for sound effects
        self.success_sound = pygame.mixer.Sound(success_sound_path)
        self.success_sound.set_volume(0.1)
        self.failure_sound = pygame.mixer.Sound(failure_sound_path)
        self.failure_sound.set_volume(0.1)
        self.catch_sound = pygame.mixer.Sound(catch_sound_path)
        self.catch_sound.set_volume(0.1)
        self.hit_sound = pygame.mixer.Sound(hit_sound_path)
        self.hit_sound.set_volume(0.1)

        # Attribute to store the last direction of movement (left or right)
        self.last_direction = None

    # Method to update the player's movement based on key presses
    def update(self):
        keys = pygame.key.get_pressed()  # Check which keys are currently pressed

        # Move left if the left arrow key is pressed and the player is within screen bounds
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.image = pygame.image.load(self.images_paths[0])  # Load image for moving left
            self.rect.x -= self.speed
            self.last_direction = "left"

        # Move right if the right arrow key is pressed and the player is within screen bounds
        if keys[pygame.K_RIGHT] and self.rect.right < self.resolution[0]:
            self.image = pygame.image.load(self.images_paths[3])  # Load image for moving right
            self.rect.x += self.speed
            self.last_direction = "right"

        # Move up if the up arrow key is pressed and the player is above the top spacing
        if keys[pygame.K_UP] and self.rect.top > (0 + self.top_spacing):
            self.rect.y -= self.speed
            # Load appropriate image based on current direction
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

        # Move down if the down arrow key is pressed and the player is below the bottom spacing
        if keys[pygame.K_DOWN] and self.rect.bottom < (self.resolution[1] - self.bottom_spacing):
            self.rect.y += self.speed
            # Load appropriate image based on current direction
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

    # Method to move the player to a safe zone
    def back_to_safe_zone(self):
        if self.safe_zone_entries > 0:  # Check if the player has remaining safe zone entries
            self.safe_zone_entries -= 1
            self.rect.centery = (self.resolution[1] - self.image.get_height())  # Move to the bottom of the screen

    # Method to reset the player's position after losing a life or at the end of a round
    def starting_position_reset(self):
        self.rect.center = (self.resolution[0] // 2, self.resolution[1] - self.image.get_height())  # Center the player

    # Method to reset the player's lives and safe zone entries to their base values
    def player_reset(self):
        self.lives = self.base_lives
        self.safe_zone_entries = self.base_safe_zone_entries