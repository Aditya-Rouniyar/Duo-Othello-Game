# Homework 2
# Duo-Othello

# import time

# Reading the input
MAX_DEPTH = 3
BOARD_SIZE = 12
CORNER = [(0, 0), (0, 11), (11, 0), (11, 11)]
EDGE = [(0, i) for i in range(1, 11)] + [(11, i) for i in range(1, 11)] + \
    [(i, 0) for i in range(1, 11)] + [(i, 11) for i in range(1, 11)]
MOBILITY_WEIGHT = 2.0  # Weight for mobility
CORNER_WEIGHT = 5.0  # Weight for corner control
EDGE_WEIGHT = 1.0  # Weight for edge control


def read_input(file_name):
    # Open the file
    with open(file_name, "r") as file:

        # Read the Player Data
        # Color
        player = file.readline().strip()
        opponent = 'O' if player == 'X' else 'X'
        time = file.readline().strip()

        # Board
        board_state = []
        for _ in range(12):
            row = file.readline().strip()
            board_state.append(row)

    return player, opponent, board_state


def find_valid_moves_and_evaluate(row, col, player, board):
    # Directions   down downright right  upright     up     upleft      left   downleft
    directions = [(0, 1), (1, 1), (1, 0), (1, -1),
                  (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    # Determine opponent's symbol
    opponent = 'O' if player == 'X' else 'X'
    total_captured = 0
    valid_move = False
    converted_opponents = set()
    converted_possibilities = []
    for cr, cc in directions:  # cr = change in row and cc = change in col
        opponent_found = False
        r, c = row+cr, col+cc  # Checking the directions by adding with the given direction
        captured_pieces = 0
        converted_possibilities = []

        # if r or c is within the bound and board location has opponent then move further in that direction
        while 0 <= r < 12 and 0 <= c < 12 and board[r][c] == opponent:
            opponent_found = True
            converted_possibilities.append((r, c))
            r += cr
            c += cc
            captured_pieces += 1

        # Traversing through r and c, opponent is found then board at the end have the player that means we can capture it
        if opponent_found and 0 <= r < 12 and 0 <= c < 12 and board[r][c] == player:
            total_captured += captured_pieces
            valid_move = True
            for point in converted_possibilities:
                converted_opponents.add(point)

    return valid_move, total_captured, converted_opponents

# Find out the moves that are possible


def print_board(board, mes):
    print(mes + '\n')
    print('\n'.join([''.join(i) for i in board]))


def get_legal_moves(player, board):
    valid_moves = []
    possible_converted_opponents = {}
    for row in range(12):
        for col in range(12):
            if board[row][col] == '.':
                is_valid, _, possible_converted_opponents[(row, col)] = find_valid_moves_and_evaluate(
                    row, col, player, board)
                # possible_converted_opponents[(row, col)] = converted_opponents
                if is_valid:
                    valid_moves.append((row, col))
    return valid_moves, possible_converted_opponents

# Evaluate the utility of the current state


def evaluate(board, player, move):
    player_count = 0
    opponent_count = 0
    corner_player = 0
    corner_opponent = 0
    edge_player = 0
    edge_opponent = 0
    stability_player = 0
    stability_opponent = 0
    mobility_player = 0
    mobility_opponent = 0
    coin_parity = 0  # Coin Parity heuristic

    # Define weights for different heuristics
    weight_pieces_count = 1
    weight_corner = 5
    weight_edge = 2
    weight_stability = 3
    weight_mobility = 1
    weight_coin_parity = 2  # Adjust weight according to preference

    opponent = 'O' if player == 'X' else 'X'

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == player:
                player_count += 1
                if (i, j) in CORNER:
                    corner_player += 1
                if i == 0 or i == BOARD_SIZE - 1 or j == 0 or j == BOARD_SIZE - 1:
                    edge_player += 1
                # Calculate stability
                if (i == 0 or i == BOARD_SIZE - 1 or j == 0 or j == BOARD_SIZE - 1 or
                        board[i-1][j] == player or board[i+1][j] == player or
                        board[i][j-1] == player or board[i][j+1] == player):
                    stability_player += 1

            elif board[i][j] == opponent:
                opponent_count += 1
                if (i, j) in CORNER:
                    corner_opponent += 1
                if i == 0 or i == BOARD_SIZE - 1 or j == 0 or j == BOARD_SIZE - 1:
                    edge_opponent += 1
                # Calculate stability
                if (i == 0 or i == BOARD_SIZE - 1 or j == 0 or j == BOARD_SIZE - 1 or
                        board[i-1][j] == opponent or board[i+1][j] == opponent or
                        board[i][j-1] == opponent or board[i][j+1] == opponent):
                    stability_opponent += 1

    # Calculate mobility
    player_moves, _ = get_legal_moves(player, board)
    opponent_moves, _ = get_legal_moves(opponent, board)
    mobility_player = len(player_moves)
    mobility_opponent = len(opponent_moves)

    # Calculate coin parity
    coin_parity = (player_count - opponent_count) / \
        (player_count + opponent_count)

    # Calculate total score
    score = (weight_pieces_count * (player_count - opponent_count) +
             weight_corner * (corner_player - corner_opponent) +
             weight_edge * (edge_player - edge_opponent) +
             weight_stability * (stability_player - stability_opponent) +
             weight_mobility * (mobility_player - mobility_opponent) +
             weight_coin_parity * coin_parity)

    return score

    # count = 0
    # count_enemy = 0
    # corner_player = 0
    # corner_opponent = 0
    # corner_point = 0
    # edge_player = 0
    # edge_opponent = 0
    # mobility_player = 0
    # mobility_opponent = 0
    # i = 0
    # j = 0
    # opponent = 'O' if player == 'X' else 'X'
    # # print_board(board, "eval")
    # for row in board:
    #     for cell in row:

    #         if cell == player:
    #             count += 1
    #             if (i, j) in CORNER:
    #                 corner_player += 1
    #             elif i == 0 or i == 11 or j == 0 or j == 11:
    #                 edge_player += 1

    #         elif cell == opponent:
    #             count_enemy += 1
    #             if (i, j) in CORNER:
    #                 corner_opponent += 1
    #             elif i == 0 or i == 11 or j == 0 or j == 11:
    #                 edge_opponent += 1
    #         j += 1
    #     i += 1

    # # count_enemy = 0
    # # for row in board:
    # #     for cell in row:
    # #         if cell == opponent:
    # #             count_enemy += 1
    # #             if (i, j) in CORNER:
    # #                 corner_opponent += 1
    # #             elif i == 0 or i == 11 or j == 0 or j == 11:
    # #                 edge_opponent += 1
    # #         j += 1
    # #     i += 1
    # if move in CORNER:
    #     corner_point = 0.5
    # # print_board(board, "evaluate")
    # # return count
    # O_score = 1 if player == 'O' else 0
    # # - corner_opponent)/max(1, (corner_player + corner_opponent))
    # return count + corner_player*3 + edge_player*0.5

# Making a move against the opponent


def make_move(board, move, current_player, converted_opponents):
    row, col = move
    new_board = [list(row) for row in board]
    new_board[row][col] = current_player
    for i in range(12):
        for j in range(12):
            if (i, j) in converted_opponents:
                new_board[i][j] = current_player
    return new_board

# Minimax algorithm


# def minimaxX(board, depth, player, alpha, beta):
#     legal_moves = get_legal_moves(player, board)

#     # Terminal state or reached maximum depth
#     if depth == 0 or len(legal_moves) == 0:
#         # Evaluate the utility of the current board state
#         return evaluate(board, player), None

#     best_move = None

#     if player == 'X':  # Maximizing player
#         max_utility = float('-inf')
#         for move in legal_moves:
#             new_board = make_move(board, move, 'X')
#             utility, _ = minimaxX(new_board, depth - 1, 'O', alpha, beta)
#             if utility > max_utility:
#                 max_utility = utility
#                 best_move = move
#             alpha = max(alpha, max_utility)
#             if alpha >= beta:
#                 break
#         return max_utility, best_move
#     else:  # Minimizing player
#         min_utility = float('inf')
#         for move in legal_moves:
#             new_board = make_move(board, move, 'O')
#             utility, _ = minimaxX(new_board, depth - 1, 'X', alpha, beta)
#             if utility < min_utility:
#                 min_utility = utility
#                 best_move = move
#             beta = min(beta, min_utility)
#             if alpha >= beta:
#                 break
#         return min_utility, best_move


def minimaxO(board, depth, player, opponent, alpha, beta, our_turn, move=None):
    legal_moves, all_converted_opponents = get_legal_moves(player, board)
    # print(f'legal moves: {legal_moves}')
    # Terminal state or reached maximum depth
    if depth == 1 or len(legal_moves) == 0:
        # Evaluate the utility of the current board state
        if our_turn:
            return (1/(depth))*evaluate(board, opponent, move), None
        else:
            return (1/(depth))*evaluate(board, player, move), None
    elif depth != MAX_DEPTH:
        if our_turn:
            utility = (1/(depth))*evaluate(board, opponent, move)
        else:
            utility = (1/(depth))*evaluate(board, player, move)
    else:
        utility = 0

    best_move = None

    if our_turn:  # Maximizing player
        max_utility = float('-inf')
        for move in legal_moves:

            new_board = make_move(board, move, player,
                                  all_converted_opponents[move])
            # print_board(new_board, "Player Board")

            utility_temp, _ = minimaxO(new_board, depth - 1,
                                       player, opponent, alpha, beta, False, move)
            utility += utility_temp
            if utility > max_utility:
                max_utility = utility
                best_move = move

            alpha = max(alpha, max_utility)
            if alpha >= beta:
                break

        return max_utility, best_move
    else:  # Minimizing player
        min_utility = float('inf')
        for move in legal_moves:
            new_board = make_move(board, move, opponent,
                                  all_converted_opponents[move])
            # print_board(new_board, 'New board oppponent')

            utility_temp, _ = minimaxO(new_board, depth - 1,
                                       player, opponent, alpha, beta, True, move)
            utility += utility_temp
            if utility < min_utility:
                min_utility = utility
                best_move = move

            beta = min(beta, min_utility)
            if alpha >= beta:
                break

        return min_utility, best_move


# Writing an output to the file
def write_output(file, move):
    with open(file, 'w') as file:
        file.write(move)


def main():
    # start_time = time.time()

    # Reading the input in the file
    player, opponent, board = read_input("input.txt")

    # Printing the input data
    # print(player)
    # for x in range(12):
    #    print(board[x])

    # Get the legal moves
    # legal_moves = get_legal_moves(player, board)
    # print(legal_moves)

    # legal_moves = get_legal_moves(player, board)

    # if player == 'X':
    #     _, selected_move = minimaxX(
    #         board, 12, player, float('-inf'), float('-inf'))
    # else:
    _, selected_move = minimaxO(
        board, MAX_DEPTH + 1, player, opponent, float('-inf'), float('inf'), True)
    # print(selected_move)

    move_to_be_printed = chr(
        selected_move[1] + ord('a')) + str(selected_move[0] + 1)
    # print(move_to_be_printed)

    # Writing the ouput to the file
    write_output("output.txt", move_to_be_printed)

    # print("Execution time:", time.time() - start_time)


if __name__ == "__main__":
    main()
