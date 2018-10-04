import sys
import math
import time
import random
from state_node import StateNode

nodes_expanded = 0

# Minimax algorithm


def minimax(current_node, current_depth, max_depth, max_step, player_turn, searching_player, alpha, beta):
    global nodes_expanded

    # If terminal node
    if current_depth == max_depth or abs(current_node.calc_h(searching_player)) == 10000:
        return current_node.calc_h(searching_player)

    # If current node is a max node
    if max_step is True:
        current_max_val = -1000000
        moves = current_node.get_valid_moves(player_turn)
        nodes_expanded += len(moves)
        for next_move in moves:
            if player_turn == 1:
                min_node_val = minimax(
                    next_move, current_depth+1, max_depth, False, 2, searching_player, alpha, beta)
            else:
                min_node_val = minimax(
                    next_move, current_depth+1, max_depth, False, 1, searching_player, alpha, beta)
            if min_node_val > current_max_val:
                current_max_val = min_node_val
            if current_max_val > alpha:
                alpha = current_max_val
            if beta < alpha:
                break
            if current_depth == 0:
                current_node.actions[next_move.move[0]
                                     ][next_move.move[1]] = min_node_val
        return current_max_val

    # If current node is a min node
    else:
        current_min_val = 1000000
        moves = current_node.get_valid_moves(player_turn)
        nodes_expanded += len(moves)
        for next_move in moves:
            if player_turn == 1:
                max_node_val = minimax(
                    next_move, current_depth+1, max_depth, True, 2, searching_player, alpha, beta)
            else:
                max_node_val = minimax(
                    next_move, current_depth+1, max_depth, True, 1, searching_player, alpha, beta)
            if max_node_val < current_min_val:
                current_min_val = max_node_val
            if current_min_val < beta:
                beta = current_min_val
            if beta < alpha:
                break
        return current_min_val


# Handle player 1 turn
def player1_turn(current_state):
    # Minimax search to depth 2 (2-ply)
    value = minimax(current_state, 0, 2, True, 1, 1, -1000000, 1000000)
    chosen_action = None
    same_distances = []
    print(current_state.actions)

    # Select best action and return as new state
    for y in range(0, 6):
        for x in range(0, 6):
            if current_state.actions[x][y] is None:
                continue
            if current_state.actions[x][y] == value and chosen_action is None:
                chosen_action = StateNode(current_state, (x, y), 1)
                same_distances = [chosen_action]
            elif current_state.actions[x][y] == value:
                if math.sqrt((2.5 - x)**2 + (2.5 - y)**2) < chosen_action.calc_middle_distance():
                    chosen_action = StateNode(current_state, (x, y), 1)
                    same_distances = [chosen_action]
                elif math.sqrt((2.5 - x)**2 + (2.5 - y)**2) == chosen_action.calc_middle_distance():
                    same_distances.append(StateNode(current_state, (x, y), 1))

    # If there are ties, randomly select location
    if len(same_distances) > 1:
        return random.choice(same_distances)
    return chosen_action


# Handle player 2 turn
def player2_turn(current_state):
    # Minimax search with depth 4 (4-ply)
    value = minimax(current_state, 0, 4, True, 2, 2, -1000000, 1000000)
    chosen_action = None
    same_distances = []
    print(current_state.actions)

    # Select best action and return as new state
    for y in range(0, 6):
        for x in range(0, 6):
            if current_state.actions[x][y] is None:
                continue
            if current_state.actions[x][y] == value and chosen_action is None:
                chosen_action = StateNode(current_state, (x, y), 2)
                same_distances = [chosen_action]
            elif current_state.actions[x][y] == value:
                if math.sqrt((2.5 - x)**2 + (2.5 - y)**2) < chosen_action.calc_middle_distance():
                    chosen_action = StateNode(current_state, (x, y), 2)
                    same_distances = [chosen_action]
                elif math.sqrt((2.5 - x)**2 + (2.5 - y)**2) == chosen_action.calc_middle_distance():
                    same_distances.append(StateNode(current_state, (x, y), 2))

    # If there are ties, randomly select location
    if len(same_distances) > 1:
        return random.choice(same_distances)
    return chosen_action


def main():
    global nodes_expanded
    metadata = open("output2/metadata.txt", "w")
    player1_wins = 0
    player2_wins = 0
    num_draws = 0

    # Play 20 games
    for game in range(0, 20):
        # Initial game setup
        game_start = time.time()
        game_over = False
        game_output = open("output2/game" + str(game+1) + ".txt", "w")
        turns_taken = 1
        print('Player 2 taking turn...')
        game_output.write('Player 2 taking turn...\n')
        current_state = StateNode()
        for x in range(0, 6):
            print(current_state.board[x])
            game_output.write(str(current_state.board[x]) + '\n')
        print('')
        game_output.write('\n\n')

        # Play until board is full or a player wins
        while turns_taken < 36 and not game_over:

            # Player 1 takes turn
            print('Player 1 taking turn...')
            game_output.write('Player 1 taking turn...\n')
            start = time.time()
            nodes_expanded = 0
            current_state = player1_turn(current_state)
            end = time.time()
            turns_taken += 1
            for x in range(0, 6):
                print(current_state.board[x])
                game_output.write(str(current_state.board[x]) + '\n')
            print(current_state.calc_h(1), ' ', current_state.calc_h(
                2), ' ', nodes_expanded, ' ', end-start, '\n')
            game_output.write(str(current_state.calc_h(1)) + '  ' + str(current_state.calc_h(
                2)) + '  ' + str(nodes_expanded) + ' ' + str(end-start) + '\n\n')

            # Check if player 1 won on this turn
            if current_state.calc_h(1) == 10000:
                game_end = time.time()
                game_over = True
                player1_wins += 1
                print('Player 1 wins!')
                game_output.write('Player 1 wins!\n')
                metadata.write('Player 1 wins game ' + str(game+1) + '! Total wins: ' + str(player1_wins) + ' : ' + str(player2_wins) + '  (' + str(
                    num_draws) + ' draws) Game time: ' + str(game_end-game_start) + '\n')
                break

            # If board is full, game ends in draw
            if turns_taken == 36:
                break

            # Player 2 takes turn
            print('Player 2 taking turn...')
            game_output.write('Player 2 taking turn...\n')
            start = time.time()
            nodes_expanded = 0
            current_state = player2_turn(current_state)
            end = time.time()
            turns_taken += 1
            for x in range(0, 6):
                print(current_state.board[x])
                game_output.write(str(current_state.board[x]) + '\n')
            print(current_state.calc_h(1), ' ', current_state.calc_h(
                2), ' ', nodes_expanded, ' ', end-start, '\n')
            game_output.write(str(current_state.calc_h(1)) + '  ' + str(current_state.calc_h(
                2)) + '  ' + str(nodes_expanded) + ' ' + str(end-start) + '\n\n')

            # Check if player 2 won on this turn
            if current_state.calc_h(2) == 10000:
                game_end = time.time()
                game_over = True
                player2_wins += 1
                print('Player 2 wins!')
                game_output.write('Player 2 wins!\n')
                metadata.write('Player 2 wins game ' + str(game+1) + '! Total wins: ' + str(player1_wins) + ' : ' + str(player2_wins) + '  (' + str(
                    num_draws) + ' draws) Game time: ' + str(game_end-game_start) + '\n')
                break

        # If board is full and no player won, the games ends in a draw
        if not game_over:
            game_end = time.time()
            num_draws += 1
            print('Draw.')
            game_output.write('Draw.\n')
            metadata.write('Draw for game ' + str(game+1) + '. Total wins: ' + str(player1_wins) + ' : ' + str(player2_wins) + '  (' + str(
                num_draws) + ' draws) Game time: ' + str(game_end-game_start) + '\n')


if __name__ == '__main__':
    main()
