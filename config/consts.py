# Base game settings
PLAYGROUND_WIDTH = 1200
PLAYGROUND_HEIGHT = 700
GAME_RESOLUTION = (PLAYGROUND_WIDTH, PLAYGROUND_HEIGHT)
GAME_FPS = 60
# The space/gap in pixels between the bottom screen border and the bottom of the game playground
GAME_BOTTOM_SPACING = 100
GAME_TOP_SPACING = 100
SCREEN_MARGIN = 5
PLAYGROUND_BORDER_WIDTH = 5
SCREEN_TITLE = "Harry Potter: The Wizard's fight"
GAME_TITLE = "Harry Potter: The Golden Snitch and The Dementor Clash"
LAUNCH_TEXT = "Press enter to play"

# Fonts, font colors, texts
GAME_FONT = "assets/fonts/Harry.ttf"
FONT_COLOR = "#BAA400"
SCORE_TEXT_FONT_SIZE = 24
MAIN_TEXT_FONT_SIZE = 48
TEXT_MARGIN = 1
INSTRUCTION_TEXT = "Catch this dementor!"


# Background (music and scene)
BG_PATH = "assets/images/backgrounds/bg_hogwarts1.png"
BG_BASE_COORDINATES = (0, 0)
BG_MUSIC = "assets/media/music/bg-music-hp.wav"

# Enemies
DEMENTOR_MIN_SPEED = 1
DEMENTOR_MAX_SPEED = 5
DEMENTOR_PATH_TYPE_0 = ("assets/images/dementors/dementor_blue.png",)
DEMENTOR_PATH_TYPE_1 = ("assets/images/dementors/dementor_green.png",)
DEMENTOR_PATH_TYPE_2 = ("assets/images/dementors/dementor_purple.png",)
DEMENTOR_PATH_TYPE_3 = ("assets/images/dementors/dementor_yellow.png",)
DEMENTOR_IMAGES_PATH = ["assets/images/dementors/dementor_blue.png",
                        "assets/images/dementors/dementor_green.png",
                        "assets/images/dementors/dementor_purple.png",
                        "assets/images/dementors/dementor_yellow.png"]
# enemies colors
BLUE = (21, 31, 217)
GREEN = (24, 194, 38)
PURPLE = (255, 10, 233)
YELLOW = (195, 181, 23)
DEMENTOR_COLORS = (BLUE, GREEN, PURPLE, YELLOW)

# Golden snitch
GOLDEN_SNITCH_BASE_MIN_SPEED = 10
GOLDEN_SNITCH_BASE_MAX_SPEED = 12
GOLDEN_SNITCH_PATH_LEFT = "assets/images/golden_snitch/golden_snitch_small_left.png"
GOLDEN_SNITCH_PATH_RIGHT = "assets/images/golden_snitch/golden_snitch_small_right.png"
GOLDEN_SNITCH_PATHS = (GOLDEN_SNITCH_PATH_LEFT, GOLDEN_SNITCH_PATH_RIGHT)
NUMBER_OF_GOLDEN_SNITCHES = 1

# Bludger
BLUDGER_MIN_SPEED = 8
BLUDGER_MAX_SPEED = 10
BLUDGER_PATH = ("assets/images/bludger/bludger.png", )
NUMBER_OF_BLUDGERS = 2

# Player
PLAYER_SPEED = 8
PLAYER_PATH_LEFT = "assets/images/player/HP_to_left.png"
PLAYER_PATH_LEFT_UP = "assets/images/player/HP_to_left_up.png"
PLAYER_PATH_LEFT_DOWN = "assets/images/player/HP_to_left_down.png"
PLAYER_PATH_RIGHT = "assets/images/player/HP_to_right.png"
PLAYER_PATH_RIGHT_UP = "assets/images/player/HP_to_right_up.png"
PLAYER_PATH_RIGHT_DOWN = "assets/images/player/HP_to_right_down.png"

PLAYER_PATHS = (PLAYER_PATH_LEFT, PLAYER_PATH_LEFT_UP, PLAYER_PATH_LEFT_DOWN,
                PLAYER_PATH_RIGHT, PLAYER_PATH_RIGHT_UP, PLAYER_PATH_RIGHT_DOWN)
PLAYER_LIVES = 5
PLAYER_SAFE_ZONE_ENTRIES = 3
PLAYER_SUCCESS_SOUND = "assets/media/sounds/expecto-patronum.mp3"
PLAYER_FAILURE_SOUND = "assets/media/sounds/wrong.wav"
PLAYER_CATCH_SOUND = "assets/media/sounds/cheers_sound.wav"
PLAYER_HIT_SOUND = "assets/media/sounds/bludger_hit.wav"
