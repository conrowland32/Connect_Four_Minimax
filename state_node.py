import math


class StateNode:
    def __init__(self, previous=None, move=(2, 2), player_turn=1):
        if previous is None:
            self.board = [[0] * 6, [0] * 6, [0] * 6, [0] * 6, [0] * 6, [0] * 6]
        else:
            self.board = previous.board.copy()
        self.board[move[0]][move[1]] = player_turn
        self.move = move
        self.actions = [[None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6]
        self.h1 = None
        self.h2 = None
        
    def calc_h(self, player):
        if player is 1 and self.h1 is not None:
            return self.h1
        if player is 2 and self.h2 is not None:
            return self.h2
        p1_sets = self.find_player_sets(1)
        p2_sets = self.find_player_sets(2)
        if p1_sets == []:
            self.h1 = 1000000
            self.h2 = -1000000
        elif p2_sets == []:
            self.h1 = -1000000
            self.h2 = 1000000
        else:
            self.h1 = 5 * p1_sets[0] - 10 * p2_sets[0] + 3 * p1_sets[1] - 6 * p2_sets[1] + p1_sets[2] - p2_sets[2]
            self.h2 = 5 * p2_sets[0] - 10 * p1_sets[0] + 3 * p2_sets[1] - 6 * p1_sets[1] + p2_sets[2] - p1_sets[2]
        if player is 1:
            return self.h1
        else:
            return self.h2
            

    def find_player_sets(self, player):
        count = [0, 0, 0]
        counted_sets = []
        for y in range(0, 6):
            for x in range(0, 6):

                # Check for terminal node
                if x < 3:
                    if [self.board[x][y], self.board[x+1][y], self.board[x+2][y], self.board[x+3][y]] == [player, player, player, player]:
                        return []
                if y < 3:
                    if [self.board[x][y], self.board[x][y+1], self.board[x][y+2], self.board[x][y+3]] == [player, player, player, player]:
                        return []
                if x < 3 and y < 3:
                    if [self.board[x][y], self.board[x+1][y+1], self.board[x+2][y+2], self.board[x+3][y+3]] == [player, player, player, player]:
                        return []
                if x > 2 and y < 3:
                    if [self.board[x][y], self.board[x-1][y+1], self.board[x-2][y+2], self.board[x-3][y+3]] == [player, player, player, player]:
                        return []

                # Check horizontal 5
                if x < 2:
                    if [self.board[x][y], self.board[x+1][y], self.board[x+2][y], self.board[x+3][y], self.board[x+4][y]] == [0, player, player, player, 0]:
                        count[0] += 1
                        counted_sets.append([(x+1,y), (x+2,y), (x+3,y)])
                        counted_sets.append([(x+1,y), (x+2,y)])
                        counted_sets.append([(x+2,y), (x+3,y)])

                # Check vertical 5
                if y < 2:
                    if [self.board[x][y], self.board[x][y+1], self.board[x][y+2], self.board[x][y+3], self.board[x][y+4]] == [0, player, player, player, 0]:
                        count[0] += 1
                        counted_sets.append([(x,y+1), (x,y+2), x,y+3])
                        counted_sets.append([(x,y+1), (x,y+2)])
                        counted_sets.append([(x,y+2), x,y+3])

                # Check diagonal 5
                if x < 2 and y < 2:
                    if [self.board[x][y], self.board[x+1][y+1], self.board[x+2][y+2], self.board[x+3][y+3], self.board[x+4][y+4]] == [0, player, player, player, 0]:
                        count[0] += 1
                        counted_sets.append([(x+1,y+1), (x+2,y+2), (x+3,y+3)])
                        counted_sets.append([(x+1,y+1), (x+2,y+2)])
                        counted_sets.append([(x+2,y+2), (x+3,y+3)])
                elif x > 3 and y < 2:
                    if [self.board[x][y], self.board[x-1][y+1], self.board[x-2][y+2], self.board[x-3][y+3], self.board[x-4][y+4]] == [0, player, player, player, 0]:
                        count[0] += 1
                        counted_sets.append([(x-1,y+1), (x-2,y+2), (x-3,y+3)])
                        counted_sets.append([(x-1,y+1), (x-2,y+2)])
                        counted_sets.append([(x-2,y+2), (x-3,y+3)])

                # Check horizontal 4
                if x < 3:
                    if [self.board[x][y], self.board[x+1][y], self.board[x+2][y], self.board[x+3][y]] == [0, player, player, player] \
                            and [(x+1,y), (x+2,y), (x+3,y)] not in counted_sets:
                        count[1] += 1
                        counted_sets.append([(x+1,y), (x+2,y), (x+3,y)])
                        counted_sets.append([(x+1,y), (x+2,y)])
                        counted_sets.append([(x+2,y), (x+3,y)])
                    elif [self.board[x][y], self.board[x+1][y], self.board[x+2][y], self.board[x+3][y]] == [player, player, player, 0] \
                            and [(x,y), (x+1,y), (x+2,y)] not in counted_sets:
                        count[1] += 1
                        counted_sets.append([(x,y), (x+1,y), (x+2,y)])
                        counted_sets.append([(x,y), (x+1,y)])
                        counted_sets.append([(x+1,y), (x+2,y)])

                # Check vertical 4
                if y < 3:
                    if [self.board[x][y], self.board[x][y+1], self.board[x][y+2], self.board[x][y+3]] == [0, player, player, player] \
                            and [(x,y+1), (x,y+2), (x,y+3)] not in counted_sets:
                        count[1] += 1
                        counted_sets.append([(x,y+1), (x,y+2), (x,y+3)])
                        counted_sets.append([(x,y+1), (x,y+2)])
                        counted_sets.append([(x,y+2), (x,y+3)])
                    elif [self.board[x][y], self.board[x][y+1], self.board[x][y+2], self.board[x][y+3]] == [player, player, player, 0] \
                            and [(x,y), (x,y+1), (x,y+2)] not in counted_sets:
                        count[1] += 1
                        counted_sets.append([(x,y), (x,y+1), (x,y+2)])
                        counted_sets.append([(x,y), (x,y+1)])
                        counted_sets.append([(x,y+1), (x,y+2)])

                # Check diagonal 4
                if x < 3 and y < 3:
                    if [self.board[x][y], self.board[x+1][y+1], self.board[x+2][y+2], self.board[x+3][y+3]] == [0, player, player, player] \
                            and [(x+1,y+1), (x+2,y+2), (x+3,y+3)] not in counted_sets:
                        count[1] += 1
                        counted_sets.append([(x+1,y+1), (x+2,y+2), (x+3,y+3)])
                        counted_sets.append([(x+1,y+1), (x+2,y+2)])
                        counted_sets.append([(x+2,y+2), (x+3,y+3)])
                    elif [self.board[x][y], self.board[x+1][y+1], self.board[x+2][y+2], self.board[x+3][y+3]] == [player, player, player, 0] \
                            and [(x,y), (x+1,y+1), (x+2,y+2)] not in counted_sets:
                        count[1] += 1
                        counted_sets.append([(x,y), (x+1,y+1), (x+2,y+2)])
                        counted_sets.append([(x,y), (x+1,y+1)])
                        counted_sets.append([(x+1,y+1), (x+2,y+2)])
                elif x > 2 and y < 3:
                    if [self.board[x][y], self.board[x-1][y+1], self.board[x-2][y+2], self.board[x-3][y+3]] == [0, player, player, player] \
                            and [(x-1,y+1), (x-2,y+2), (x-3,y+3)] not in counted_sets:
                        count[1] += 1
                        counted_sets.append([(x-1,y+1), (x-2,y+2), (x-3,y+3)])
                        counted_sets.append([(x-1,y+1), (x-2,y+2)])
                        counted_sets.append([(x-2,y+2), (x-3,y+3)])
                    elif [self.board[x][y], self.board[x-1][y+1], self.board[x-2][y+2], self.board[x-3][y+3]] == [player, player, player, 0] \
                            and [(x,y), (x-1,y+1), (x-2,y+2)] not in counted_sets:
                        count[1] += 1
                        counted_sets.append([(x,y), (x-1,y+1), (x-2,y+2)])
                        counted_sets.append([(x,y), (x-1,y+1)])
                        counted_sets.append([(x-1,y+1), (x-2,y+2)])

                # Check horizontal 3
                if x < 4:
                    if [self.board[x][y], self.board[x+1][y], self.board[x+2][y]] == [0, player, player] \
                            and [(x+1,y), (x+2,y)] not in counted_sets:
                        count[2] += 1
                        counted_sets.append([(x+1,y), (x+2,y)])
                    elif [self.board[x][y], self.board[x+1][y], self.board[x+2][y]] == [player, player, 0] \
                            and [(x,y), (x+1,y)] not in counted_sets:
                        count[2] += 1
                        counted_sets.append([(x,y), (x+1,y)])

                # Check vertical 3
                if y < 4:
                    if [self.board[x][y], self.board[x][y+1], self.board[x][y+2]] == [0, player, player] \
                            and [(x,y+1), (x,y+2)] not in counted_sets:
                        count[2] += 1
                        counted_sets.append([(x,y+1), (x,y+2)])
                    elif [self.board[x][y], self.board[x][y+1], self.board[x][y+2]] == [player, player, 0] \
                            and [(x,y), (x,y+1)] not in counted_sets:
                        count[2] += 1
                        counted_sets.append([(x,y), (x,y+1)])

                # Check diagonal 3
                if x < 4 and y < 4:
                    if [self.board[x][y], self.board[x+1][y+1], self.board[x+2][y+2]] == [0, player, player] \
                            and [(x+1,y+1), (x+2,y+2)] not in counted_sets:
                        count[2] += 1
                        counted_sets.append([(x+1,y+1), (x+2,y+2)])
                    elif [self.board[x][y], self.board[x+1][y+1], self.board[x+2][y+2]] == [player, player, 0] \
                            and [(x,y), (x+1,y+1)] not in counted_sets:
                        count[2] += 1
                        counted_sets.append([(x,y), (x+1,y+1)])
                elif x > 1 and y < 4:
                    if [self.board[x][y], self.board[x-1][y+1], self.board[x-2][y+2]] == [0, player, player] \
                            and [(x-1,y+1), (x-2,y+2)] not in counted_sets:
                        count[2] += 1
                        counted_sets.append([(x-1,y+1), (x-2,y+2)])
                    elif [self.board[x][y], self.board[x-1][y+1], self.board[x-2][y+2]] == [player, player, 0] \
                            and [(x,y), (x-1,y+1)] not in counted_sets:
                        count[2] += 1
                        counted_sets.append([(x,y), (x-1,y+1)])

        del counted_sets
        return count
