from src.enemy import Enemy


class Bludger(Enemy):

    def __init__(self, game_resolution, bottom_spacing, top_spacing,
                 min_speed, max_speed, images_paths):
        super().__init__(game_resolution, bottom_spacing, top_spacing,
                         min_speed, max_speed, images_paths)
