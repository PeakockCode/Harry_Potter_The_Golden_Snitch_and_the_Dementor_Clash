from src.enemy import Enemy


class Dementor(Enemy):

    def __init__(self, game_resolution, bottom_spacing, top_spacing,
                 min_speed, max_speed, images_paths, dementor_type: int):
        super().__init__(game_resolution, bottom_spacing, top_spacing, min_speed, max_speed, images_paths)
        self.type = dementor_type
