import checkers
import gamebot
import pygame, sys
from pygame.locals import *
from time import sleep
##COLORS##
#             R    G    B
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
RED = (255,   0,   0)
BLACK = (0,   0,   0)
GOLD = (255, 215,   0)
HIGH = (160, 190, 255)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"


def main():
    while True:
        game = checkers.Game(loop_mode=False)
        game.setup()
        coca_cola = gamebot.Bot(game, RED, mid_eval='ultima_coca_cola',method='alpha_beta', depth=4)
        sprite = gamebot.Bot(
            game, BLUE, mid_eval='god_slayer_sprite', method='alpha_beta', depth=4)
        while True: 
            if game.turn == BLUE:
                # game.player_turn()
                count_nodes = sprite.step(game.board, True)
                game.update()
            else:
                # game.player_turn()
                count_nodes = coca_cola.step(game.board, True)
                game.update()
            if game.endit:
                break


if __name__ == "__main__":
    main()
    pass
