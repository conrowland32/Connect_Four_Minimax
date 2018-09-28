import sys
import math
from state_node import StateNode


# def minimax(current_node, current_depth, max_depth, max_step, player_turn, searching_player):
#     if current_depth is max_depth or abs(current_node.calc_h(searching_player)) is 1000000:
#         return current_node.calc_h(searching_player)
#     if max_step is True:
#         current_max = -10000
#         moves = current_node.get_valid_moves(player_turn)
#         for i, move in enumerate(moves):
#             if player_turn is 1:
#                 min_node = minimax(move, current_depth+1,
#                                    max_depth, False, 2, searching_player)
#             else:
#                 min_node = minimax(move, current_depth+1,
#                                    max_depth, False, 1, searching_player)
#             if min_node > current_max:
#                 current_max = min_node
#             if current_depth is 0:
#                 current_node.actions[move.move] = min_node
#         return current_max
#     else:
#         current_min = 10000
#         moves = current_node.get_valid_moves(player_turn)
#         for move in moves:
#             if player_turn is 1:
#                 max_node = minimax(move, current_depth+1,
#                                    max_depth, True, 2, searching_player)
#                 if max_node < current_min:
#                     current_min = max_node
#             else:
#                 max_node = minimax(move, current_depth+1,
#                                    max_depth, True, 1, searching_player)
#                 if max_node < current_min:
#                     current_min = max_node
#         return current_min


# def player1_turn(current_state):
#     value = minimax(current_state, 0, 2, True, 1, 1)
#     print(value, current_state.actions)


def player2_turn(current_state):
    value = minimax(current_state, 0, 3, True, 2, 2)
    print(value, current_state.actions)
    return current_state


def main():
    current_state = StateNode()
    print(current_state.board, current_state.calc_h(1), current_state.calc_h(2))
    # while True:
    print('Player 2 taking turn...')
    current_state = player2_turn(current_state)
    print(current_state.board, current_state.calc_h(1), current_state.calc_h(2))


if __name__ == '__main__':
    main()
