# Import necessary modules
import pygame
import sys

# Import game configuration constants and classes
from config import consts
from src.game import Game
from src.dementor import Dementor
from src.player import Player
from src.golden_snitch import GoldenSnitch
from src.enemy import Enemy

# Main entry point of the game
if __name__ == "__main__":

    # game init and set up Pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(consts.GAME_RESOLUTION)
    pygame.display.set_caption(consts.SCREEN_TITLE)

    # Create and add Dementors to the game
    dementor_group = pygame.sprite.Group()
    for _ in range(len(consts.DEMENTOR_IMAGES_PATH)):
        dementor = Dementor(consts.GAME_RESOLUTION,
                            consts.GAME_BOTTOM_SPACING, consts.GAME_TOP_SPACING,
                            consts.DEMENTOR_MIN_SPEED, consts.DEMENTOR_MAX_SPEED,
                            (consts.DEMENTOR_IMAGES_PATH[_],), _)
        dementor_group.add(dementor)

    # Create and add Golden Snitches to the game
    golden_snitch_group = pygame.sprite.Group()
    for _ in range(consts.NUMBER_OF_GOLDEN_SNITCHES):
        golden_snitch = GoldenSnitch(consts.GAME_RESOLUTION, consts.GAME_BOTTOM_SPACING,
                                     consts.GAME_TOP_SPACING, consts.GOLDEN_SNITCH_BASE_MIN_SPEED,
                                     consts.GOLDEN_SNITCH_BASE_MAX_SPEED, consts.GOLDEN_SNITCH_PATHS)
        golden_snitch_group.add(golden_snitch)

    # Create and add Bludgers to the game
    bludger_group = pygame.sprite.Group()
    for _ in range(consts.NUMBER_OF_BLUDGERS):
        bludger = Enemy(consts.GAME_RESOLUTION, consts.GAME_BOTTOM_SPACING,
                        consts.GAME_TOP_SPACING, consts.BLUDGER_MIN_SPEED,
                        consts.BLUDGER_MAX_SPEED, consts.BLUDGER_PATH)
        bludger_group.add(bludger)

    # Create and add the player to the game
    player_group = pygame.sprite.Group()
    player = Player(consts.GAME_RESOLUTION, consts.GAME_BOTTOM_SPACING, consts.GAME_TOP_SPACING,
                    consts.PLAYER_PATHS, consts.PLAYER_SPEED,
                    consts.PLAYER_LIVES, consts.PLAYER_SAFE_ZONE_ENTRIES,
                    consts.PLAYER_SUCCESS_SOUND, consts.PLAYER_FAILURE_SOUND,
                    consts.PLAYER_CATCH_SOUND, consts.PLAYER_HIT_SOUND)
    player_group.add(player)

    # Initialize the main game object with required configurations and components
    my_game = Game(screen, consts.BG_PATH, consts.BG_BASE_COORDINATES,
                   consts.SCREEN_MARGIN, consts.PLAYGROUND_BORDER_WIDTH,
                   consts.TEXT_MARGIN, consts.GAME_FPS, consts.GAME_RESOLUTION,
                   consts.GAME_BOTTOM_SPACING, consts.GAME_TOP_SPACING, player, golden_snitch_group, bludger_group,
                   dementor_group, consts.BG_MUSIC, consts.GAME_FONT, consts.FONT_COLOR,
                   consts.SCORE_TEXT_FONT_SIZE, consts.MAIN_TEXT_FONT_SIZE, consts.DEMENTOR_IMAGES_PATH,
                   consts.DEMENTOR_COLORS, consts.DEMENTOR_MIN_SPEED, consts.DEMENTOR_MAX_SPEED,
                   consts.GOLDEN_SNITCH_PATHS, consts.GOLDEN_SNITCH_BASE_MIN_SPEED, consts.GOLDEN_SNITCH_BASE_MAX_SPEED,
                   consts.SCOREBOARD_TITLE, consts.SCOREBOARD_GEOMETRY, consts.SCOREBOARD_ICON,
                   consts.SCOREBOARD_TEXT_COLOR, consts.SCOREBOARD_BUTTON_COLOR,
                   consts.SCOREBOARD_HOVER_COLOR, consts.SCOREBOARD_TXT_FILE_PATH)

    # Main game loop
    running = True
    my_game.pause_game(consts.GAME_TITLE, consts.LAUNCH_TEXT) # Display initial pause screen with game title and launch text
    my_game.start_new_round() # Start the first round of the game
    while running:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.back_to_safe_zone() # Move player back to the safe zone when space is pressed
            if event.type == pygame.QUIT:
                running = False # Exit the game loop if the quit event is detected
                pygame.quit() # Close the Pygame window
                sys.exit() # Terminate the program

        # Draw the background for the playground
        screen.blit(my_game.playground_bg, my_game.playground_bg_rect.topleft)

        # Draw game elements: Dementors, Golden Snitches, Bludgers, and the Player
        dementor_group.draw(screen)
        golden_snitch_group.draw(screen)
        bludger_group.draw(screen)
        player_group.draw(screen)

        # Update game elements' state
        dementor_group.update()
        golden_snitch_group.update()
        bludger_group.update()
        player_group.update()

        # Update the game state and draw additional elements (e.g., instructions)
        my_game.update()
        my_game.draw(consts.INSTRUCTION_TEXT)

        # Refresh the display to show the updated frame
        pygame.display.flip()
        # Control the frame rate of the game
        clock.tick(consts.GAME_FPS)
