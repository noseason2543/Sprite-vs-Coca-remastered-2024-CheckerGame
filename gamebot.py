import pygame
import sys
from pygame.locals import *
import random
from copy import deepcopy
import math
from time import sleep

from checkers import Game
pygame.font.init()


WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
RED = (255,   0,   0)
BLACK = (0,   0,   0)
GOLD = (255, 215,   0)
HIGH = (160, 190, 255)

NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"


class Bot:
    def __init__(self, game, color, method='alpha_beta', mid_eval=None, depth=1):
        self.method = method
        if mid_eval == 'god_slayer_sprite':
            self._mid_eval = self._god_slayer_sprite
        elif mid_eval == 'ultima_coca_cola':
            self._mid_eval = self._ultima_coca_cola
        self.depth = depth
        self.game = game
        self.color = color
        self.eval_color = color
        if self.color == BLUE:
            self.adversary_color = RED
        else:
            self.adversary_color = BLUE
        self._current_eval = self._mid_eval
        self._count_nodes = 0

    def step(self, board, return_count_nodes=False):
        self._count_nodes = 0
        if self.method == 'alpha_beta':
            self._alpha_beta_step(board)
        if return_count_nodes:
            return self._count_nodes

    def _action(self, current_pos, final_pos, board):
        try:
            if current_pos is None:
                self.game.end_turn()
            if self.game.hop == False:
                if board.location(final_pos[0], final_pos[1]).occupant != None and board.location(final_pos[0], final_pos[1]).occupant.color == self.game.turn:
                    current_pos = final_pos

                elif current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):
                    a = board.location(current_pos[0],current_pos[1]).occupant.king
                    board.move_piece(current_pos[0], current_pos[1], final_pos[0], final_pos[1])
                    if final_pos not in board.adjacent(current_pos[0], current_pos[1]) and board.location(final_pos[0],final_pos[1]).occupant.king == False:
                        if final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] < 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                        elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] < 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                        elif final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] > 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                        elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] > 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                        self.game.hop = True
                        current_pos = final_pos
                    elif final_pos in board.get_king_kill_move() and board.location(final_pos[0],final_pos[1]).occupant.king == True:
                        if final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] < 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                        elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] < 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                        elif final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] > 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                        elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] > 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                        self.game.hop = True
                        current_pos = final_pos
                    elif a == False and board.location(final_pos[0],final_pos[1]).occupant.king == True:
                        if final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] < 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                        elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] < 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                        elif final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] > 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                        elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] > 0:
                            board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                        self.game.end_turn()
                    final_pos = board.legal_moves(current_pos[0], current_pos[1], True)
                    if final_pos != []:
                        self._action(current_pos, final_pos[0], board)
                    self.game.end_turn()

            if self.game.hop == True:
                if current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1], self.game.hop):
                    board.move_piece(current_pos[0], current_pos[1], final_pos[0], final_pos[1])
                    if final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))



                if board.legal_moves(final_pos[0], final_pos[1], self.game.hop) == []:
                    self.game.end_turn()
                else:
                    current_pos = final_pos
                    final_pos = board.legal_moves(
                        current_pos[0], current_pos[1], True)
                    if final_pos != []:
                        self._action(current_pos, final_pos[0], board)
                    self.game.end_turn()
            if self.game.hop != True:
                self.game.turn = self.adversary_color
        except TypeError :
            print ('Finish')
            self.game.terminate_game()
    
    def _action_on_board(self, board, current_pos, final_pos, hop=False):
        if hop == False:
            if board.location(final_pos[0], final_pos[1]).occupant != None and board.location(final_pos[0], final_pos[1]).occupant.color == self.game.turn:
                current_pos = final_pos

            elif current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):
                a = board.location(current_pos[0],current_pos[1]).occupant.king
                board.move_piece(current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                if final_pos not in board.adjacent(current_pos[0], current_pos[1]) and board.location(final_pos[0],final_pos[1]).occupant.king == False:
                    if final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                    hop = True
                    current_pos = final_pos
                elif final_pos in board.get_king_kill_move() and board.location(final_pos[0],final_pos[1]).occupant.king == True:
                    if final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                    hop = True
                    current_pos = final_pos
                elif a == False and board.location(final_pos[0],final_pos[1]).occupant.king == True:
                    if final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                    elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))

                final_pos = board.legal_moves(current_pos[0], current_pos[1], True)
                if final_pos != []:
                    self._action_on_board(board, current_pos, final_pos[0],hop=True)
        else:
            if current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1], hop):
                board.move_piece(current_pos[0], current_pos[1], final_pos[0], final_pos[1])
                if final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] < 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] - (abs(current_pos[1]-final_pos[1]) - 1)))))
                elif final_pos[0]-current_pos[0] < 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] - (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))
                elif final_pos[0]-current_pos[0] > 0 and final_pos[1]-current_pos[1] > 0:
                        board.remove_piece((final_pos[0]-(final_pos[0] - (current_pos[0] + (abs(current_pos[0]-final_pos[0]) - 1)))) , (final_pos[1]-(final_pos[1] - (current_pos[1] + (abs(current_pos[1]-final_pos[1]) - 1)))))


            if board.legal_moves(final_pos[0], final_pos[1], self.game.hop) == []:
                return
            else:
                current_pos = final_pos
                final_pos = board.legal_moves(current_pos[0], current_pos[1], True)
                if final_pos != []:
                    self._action_on_board(board, current_pos, final_pos[0],hop=True)

    def _generate_move(self, board):
        for i in range(8):
            for j in range(8):
                if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
                    yield (i, j, board.legal_moves(i, j, self.game.hop))

    def _alpha_beta_step(self, board):
        random_move, random_choice, _ = self._alpha_beta(self.depth - 1, board, 'max', alpha=-float('inf'), beta=float('inf'))
        self._action(random_move, random_choice, board)
        return

    def _alpha_beta(self, depth, board, fn, alpha, beta):
        if depth == 0:
            if fn == 'max':
                max_value = -float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._count_nodes += 1
                        self._action_on_board(board_clone, pos, action)
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        if step_value > max_value:
                            max_value = step_value
                            best_pos = pos
                            best_action = (action[0], action[1])
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        if(step_value == -float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        alpha = max(alpha, max_value)
                        if beta < alpha:
                            break
                    if beta < alpha:
                        break
                return best_pos, best_action, max_value
            else:
                min_value = float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        self._count_nodes += 1
                        step_value = self._current_eval(board_clone)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        if(step_value == float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        beta = min(beta, min_value)
                        if beta < alpha:
                            break
                    if beta < alpha:
                        break
                return best_pos, best_action, min_value
        else:
            if fn == 'max':
                max_value = -float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._action_on_board(board_clone, pos, action)
                        self._count_nodes += 1
                        if self._check_for_endgame(board_clone):
                            step_value = float("inf")
                        else:
                            _, _, step_value = self._alpha_beta(depth - 1, board_clone, 'min', alpha, beta)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        if(step_value is None):
                            continue
                        if step_value > max_value:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                        elif step_value == max_value and random.random() <= 0.5:
                            max_value = step_value
                            best_pos = pos
                            best_action = action
                        if(step_value == -float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        alpha = max(alpha, max_value)
                        if beta <= alpha:
                            break
                    if beta < alpha:
                        break
                return best_pos, best_action, max_value
            else:
                min_value = float("inf")
                best_pos = None
                best_action = None
                for pos in self._generate_move(board):
                    for action in pos[2]:
                        board_clone = deepcopy(board)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        self._count_nodes += 1
                        self._action_on_board(board_clone, pos, action)
                        if self._check_for_endgame(board_clone):
                            step_value = -float("inf")
                        else:
                            _, _, step_value = self._alpha_beta( depth - 1, board_clone, 'max', alpha, beta)
                        self.color, self.adversary_color = self.adversary_color, self.color
                        self.game.turn = self.color
                        if(step_value is None):
                            continue
                        if step_value < min_value:
                            min_value = step_value
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        elif step_value == min_value and random.random() <= 0.5:
                            min_value = step_value
                            best_pos = pos
                            best_action = action
                        if(step_value == float("inf") and best_pos is  None):
                            best_pos = (pos[0], pos[1])
                            best_action = (action[0], action[1])
                        beta = min(beta, min_value)
                        if beta < alpha:
                            break
                    if beta < alpha:
                        break
                return best_pos, best_action, min_value

    def _god_slayer_sprite(self, board):
        score = 0
        for i in range(8):
            for j in range(8):
                occupant = board.location(i, j).occupant
                if(occupant is not None):
                    if occupant.color == self.eval_color:
                        score += 5 + (8 - j) + 2 * (occupant.king + 1)
                    else:
                        score -= 5 + j + 2 * (occupant.king + 2)
        return score

    def _ultima_coca_cola(self, board):
        score = 0
        num_pieces = 0
        for i in range(8):
            for j in range(8):
                occupant = board.location(i, j).occupant
                if(occupant is not None):
                    num_pieces += 1
                    if occupant.color == self.eval_color and occupant.king:
                        score += 12
                    elif occupant.color != self.eval_color and occupant.king:
                        score -= 12
                    elif occupant.color == self.eval_color and j < 4:
                        score += 5
                    elif occupant.color != self.eval_color and j < 4:
                        score -= 7
                    elif occupant.color == self.eval_color and j >= 4:
                        score += 7
                    elif occupant.color != self.eval_color and j >= 4:
                        score -= 5
        return score

    def _check_for_endgame(self, board):
        for x in range(8):
            for y in range(8):
                if board.location(x, y).color == BLACK and board.location(x, y).occupant != None and board.location(x, y).occupant.color == self.game.turn:
                    if board.legal_moves(x, y) != []:
                        return False
        return True