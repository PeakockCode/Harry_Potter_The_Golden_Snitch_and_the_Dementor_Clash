# Import the Enemy class from the src.enemy module
from src.enemy import Enemy


# Define the Dementor class, which inherits from the Enemy class
class Dementor(Enemy):

    # Initialize a new Dementor instance
    def __init__(self, game_resolution, bottom_spacing, top_spacing,
                 min_speed, max_speed, images_paths, dementor_type: int):
        # Call the parent class (Enemy) initializer with the provided parameters
        super().__init__(game_resolution, bottom_spacing, top_spacing, min_speed, max_speed, images_paths)

        # Assign a specific type to the Dementor instance
        self.type = dementor_type
