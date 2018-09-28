import sys
import math
from state_node import StateNode


def minimax(current_node, current_depth, max_depth, max_step, player_turn, searching_player):
    if current_depth == max_depth or abs(current_node.calc_h(searching_player)) == 1000000:
        return current_node.calc_h(searching_player)
    if max_step is True:
        current_max_val = -10000
        moves = current_node.get_valid_moves(player_turn)
        for next_move in moves:
            if player_turn == 1:
                min_node_val = minimax(next_move, current_depth+1,
                                       max_depth, False, 2, searching_player)
            else:
                min_node_val = minimax(next_move, current_depth+1,
                                       max_depth, False, 1, searching_player)
            if min_node_val > current_max_val:
                current_max_val = min_node_val
            if current_depth == 0:
                current_node.actions[next_move.move[0]
                                     ][next_move.move[1]] = min_node_val
        return current_max_val
    else:
        current_min_val = 10000
        moves = current_node.get_valid_moves(player_turn)
        for next_move in moves:
            if player_turn == 1:
                max_node_val = minimax(next_move, current_depth+1,
                                       max_depth, True, 2, searching_player)
            else:
                max_node_val = minimax(next_move, current_depth+1,
                                       max_depth, True, 1, searching_player)
            if max_node_val < current_min_val:
                current_min_val = max_node_val
        return current_min_val


def player1_turn(current_state):
    value = minimax(current_state, 0, 2, True, 1, 1)
    chosen_action = None
    for y in range(0, 6):
        for x in range(0, 6):
            if current_state.actions[x][y] is None:
                continue
            if current_state.actions[x][y] == value and chosen_action is None:
                chosen_action = StateNode(current_state, (x, y), 1)
            elif current_state.actions[x][y] == value:
                if (abs(2.5 - x) + abs(2.5 - y)) < chosen_action.calc_middle_distance():
                    chosen_action = StateNode(current_state, (x, y), 1)
    return chosen_action


def player2_turn(current_state):
    value = minimax(current_state, 0, 4, True, 2, 2)
    chosen_action = None
    for y in range(0, 6):
        for x in range(0, 6):
            if current_state.actions[x][y] is None:
                continue
            if current_state.actions[x][y] == value and chosen_action is None:
                chosen_action = StateNode(current_state, (x, y), 2)
            elif current_state.actions[x][y] == value:
                if (abs(2.5 - x) + abs(2.5 - y)) < chosen_action.calc_middle_distance():
                    chosen_action = StateNode(current_state, (x, y), 2)
    return chosen_action


def main():
    current_state = StateNode()
    print(current_state.board, current_state.calc_h(1), current_state.calc_h(2))
    while True:
        print('Player 2 taking turn...')
        current_state = player2_turn(current_state)
        print(current_state.board, current_state.calc_h(
            1), current_state.calc_h(2))
        if abs(current_state.calc_h(1)) == 1000000:
            sys.exit()

        print('Player 1 taking turn...')
        current_state = player1_turn(current_state)
        print(current_state.board, current_state.calc_h(
            1), current_state.calc_h(2))
        if abs(current_state.calc_h(1)) == 1000000:
            sys.exit()


if __name__ == '__main__':
    main()
