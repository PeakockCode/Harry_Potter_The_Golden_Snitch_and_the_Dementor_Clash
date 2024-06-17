import pygame
import sys

from config import consts
from src.game import Game
from src.dementor import Dementor
from src.player import Player
from src.golden_snitch import GoldenSnitch
from src.bludger import Bludger


if __name__ == "__main__":

    # game init
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(consts.GAME_RESOLUTION)
    pygame.display.set_caption(consts.SCREEN_TITLE)

    # add dementor group
    dementor_group = pygame.sprite.Group()
    for _ in range(len(consts.DEMENTOR_IMAGES_PATH)):
        dementor = Dementor(consts.GAME_RESOLUTION,
                            consts.GAME_BOTTOM_SPACING, consts.GAME_TOP_SPACING,
                            consts.DEMENTOR_IMAGES_PATH[_],
                            consts.DEMENTOR_MIN_SPEED, consts.DEMENTOR_MAX_SPEED,
                            _)
        dementor_group.add(dementor)

    # add golden_snitch
    golden_snitch_group = pygame.sprite.Group()
    for _ in range(consts.NUMBER_OF_GOLDEN_SNITCHES):
        golden_snitch = GoldenSnitch(consts.GAME_RESOLUTION, consts.GAME_BOTTOM_SPACING,
                                     consts.GAME_TOP_SPACING, consts.GOLDEN_SNITCH_PATHS,
                                     consts.GOLDEN_SNITCH_BASE_MIN_SPEED, consts.GOLDEN_SNITCH_BASE_MAX_SPEED)
        golden_snitch_group.add(golden_snitch)

    # add bludger
    bludger_group = pygame.sprite.Group()
    for _ in range(consts.NUMBER_OF_BLUDGERS):
        bludger = Bludger(consts.GAME_RESOLUTION, consts.GAME_BOTTOM_SPACING,
                          consts.GAME_TOP_SPACING, consts.BLUDGER_PATH,
                          consts.BLUDGER_MIN_SPEED, consts.BLUDGER_MAX_SPEED)
        bludger_group.add(bludger)

    # add player
    player_group = pygame.sprite.Group()
    player = Player(consts.GAME_RESOLUTION, consts.GAME_BOTTOM_SPACING, consts.GAME_TOP_SPACING,
                    consts.PLAYER_PATHS, consts.PLAYER_SPEED,
                    consts.PLAYER_LIVES, consts.PLAYER_SAFE_ZONE_ENTRIES,
                    consts.PLAYER_SUCCESS_SOUND, consts.PLAYER_FAILURE_SOUND,
                    consts.PLAYER_CATCH_SOUND, consts.PLAYER_HIT_SOUND)
    player_group.add(player)

    # init the game
    my_game = Game(screen, consts.BG_PATH, consts.BG_BASE_COORDINATES,
                   consts.SCREEN_MARGIN, consts.PLAYGROUND_BORDER_WIDTH,
                   consts.TEXT_MARGIN, consts.GAME_FPS, consts.GAME_RESOLUTION,
                   consts.GAME_BOTTOM_SPACING, consts.GAME_TOP_SPACING, player, golden_snitch_group, bludger_group,
                   dementor_group, consts.BG_MUSIC, consts.GAME_FONT, consts.FONT_COLOR,
                   consts.SCORE_TEXT_FONT_SIZE, consts.MAIN_TEXT_FONT_SIZE, consts.DEMENTOR_IMAGES_PATH,
                   consts.DEMENTOR_COLORS, consts.DEMENTOR_MIN_SPEED, consts.DEMENTOR_MAX_SPEED,
                   consts.GOLDEN_SNITCH_PATHS, consts.GOLDEN_SNITCH_BASE_MIN_SPEED, consts.GOLDEN_SNITCH_BASE_MAX_SPEED)

    # main game cycle
    running = True
    my_game.pause_game(consts.GAME_TITLE, consts.LAUNCH_TEXT)
    my_game.start_new_round()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.back_to_safe_zone()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.blit(my_game.playground_bg, my_game.playground_bg_rect.topleft)

        # dementor and player draw
        dementor_group.draw(screen)
        golden_snitch_group.draw(screen)
        bludger_group.draw(screen)
        player_group.draw(screen)

        # dementor and player update
        dementor_group.update()
        golden_snitch_group.update()
        bludger_group.update()
        player_group.update()

        # game update
        my_game.update()
        my_game.draw(consts.INSTRUCTION_TEXT)

        pygame.display.flip()
        clock.tick(consts.GAME_FPS)
