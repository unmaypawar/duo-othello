from engine import get_moves


def evaluate_board(board, board_length, player, opponent):
    score = 0

    pieces = evaluate_pieces(board, board_length, player, opponent)
    frontier = evaluate_frontier(board, board_length, player, opponent)
    mobility = evaluate_mobility(board, board_length, player, opponent)
    stability = evaluate_stability(board, board_length, player, opponent)
    corners = evaluate_corners(board, board_length, player, opponent)
    
    score = (3 * mobility) + (2 * frontier) + (pieces) + (500 * stability) + (1000 * corners)

    return score


def evaluate_pieces(board, board_length, player, opponent):
    player_disc = 0
    opponent_disc = 0

    for row in board:
        for cell in row:
            if cell == player:
                player_disc += 1
            elif cell == opponent:
                opponent_disc += 1

    pieces = 100 * (player_disc - opponent_disc) / (player_disc + opponent_disc + 1)

    return pieces


def evaluate_frontier(board, board_length, player, opponent):
    player_frontier = 0
    opponent_frontier = 0

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for row in range(board_length):
        for col in range(board_length):
            if board[row][col] != '.':
                for dr, dc in directions:
                    r = row + dr
                    c = col + dc
                    if 0 <= r < board_length and 0 <= c < board_length:
                        if board[r][c] == '.':
                            if board[row][col] == player:
                                player_frontier += 1
                                break
                            else:
                                opponent_frontier += 1
                                break

    frontier = 100 * (opponent_frontier - player_frontier) / (player_frontier + opponent_frontier + 1)

    return frontier


def evaluate_mobility(board, board_length, player, opponent):
    player_legal_moves = get_moves(board, board_length, player, opponent)
    opponent_legal_moves = get_moves(board, board_length, opponent, player)

    mobility = 100 * (len(player_legal_moves) - len(opponent_legal_moves)) / (len(player_legal_moves) + len(opponent_legal_moves) + 1)

    return mobility


def evaluate_stability(board, board_length, player, opponent):
    player_stable_disc = set()
    opponent_stable_disc = set()

    coordinate = [0, board_length - 1]
    for i in coordinate:
        for j in coordinate:
            if board[i][j] == player:
                r = i
                c = j
                if j == 0:
                    prev_c = board_length - 1
                else:
                    prev_c = 0

                while(0 <= r < board_length and board[r][c] == player):
                    if j == 0:
                        while(0 <= c < board_length and c <= prev_c and board[r][c] == player):
                            player_stable_disc.add((r, c))
                            c += 1
                        prev_c = c - 1

                    else:
                        while(0 <= c < board_length and c >= prev_c and board[r][c] == player):
                            player_stable_disc.add((r, c))
                            c -= 1
                        prev_c = c + 1

                    if i == 0:
                        r += 1
                    else:  
                        r -= 1

                    c = j

    for i in coordinate:
        for j in coordinate:
            if board[i][j] == opponent:
                r = i
                c = j
                if j == 0:
                    prev_c = board_length - 1
                else:
                    prev_c = 0

                while(0 <= r < board_length and board[r][c] == opponent):
                    if j == 0:
                        while(0 <= c < board_length and c <= prev_c and board[r][c] == opponent):
                            opponent_stable_disc.add((r, c))
                            c += 1
                        prev_c = c - 1

                    else:
                        while(0 <= c < board_length and c >= prev_c and board[r][c] == opponent):
                            opponent_stable_disc.add((r, c))
                            c -= 1
                        prev_c = c + 1

                    if i == 0:
                        r += 1
                    else:  
                        r -= 1

                    c = j

    stability = 100 * (len(player_stable_disc) - len(opponent_stable_disc)) / (len(player_stable_disc) + len(opponent_stable_disc) + 1)

    return stability


def evaluate_corners(board, board_length, player, opponent):
    player_corner = 0
    opponent_corner = 0

    coordinate = [0, board_length - 1]

    for i in coordinate:
        for j in coordinate:
            if board[i][j] == player:
                player_corner += 1
            elif board[i][j] == opponent:
                opponent_corner += 1

    corners = 100 * (player_corner - opponent_corner) / (player_corner + opponent_corner + 1)

    return corners