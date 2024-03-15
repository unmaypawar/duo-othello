def read_game(board_length):
    board = []

    with open('input.txt', 'r') as in_file:
        player = in_file.readline().strip()
        if player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        player_time, opponent_time = in_file.readline().strip().split(' ')

        for i in range(board_length):
            row = in_file.readline().strip()
            row = [col for col in row]
            board.append(row)

    return player, opponent, float(player_time), float(opponent_time), board


def get_moves(board, board_length, player, opponent):
    moves = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    for row in range(board_length):
        for col in range(board_length):
            if board[row][col] == '.':
                for dr, dc in directions:
                    r, c = row + dr, col + dc
                    if 0 <= r < board_length and 0 <= c < board_length and board[r][c] == opponent:
                        while 0 <= r < board_length and 0 <= c < board_length and board[r][c] == opponent:
                            r += dr
                            c += dc
                        if 0 <= r < board_length and 0 <= c < board_length and board[r][c] == player:
                            moves.append((row, col))
                            break

    return moves


def update_board(board, board_length, player, move):
    row, col = move
    board[row][col] = player

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    flipped_discs = []

    for dr, dc in directions:
        r, c = row + dr, col + dc 
        discs_to_flip = []

        while 0 <= r < board_length and 0 <= c < board_length and board[r][c] != '.' and board[r][c] != player:
            discs_to_flip.append((r,c))
            r += dr
            c += dc

            if 0 <= r < board_length and 0 <= c < board_length and board[r][c] == player:
                flipped_discs.extend(discs_to_flip)
                break

    for r, c in flipped_discs:
        board[r][c] = player

    return board 
    

def evaluate_pieces(board, board_length, player, opponent):
    player_disc = 0
    opponent_disc = 0

    for row in board:
        for cell in row:
            if cell == player:
                player_disc += 1
            elif cell == opponent:
                opponent_disc += 1

    if player == 'O':
        pieces = 100 * (player_disc - (opponent_disc + 1)) / (player_disc + (opponent_disc + 1) + 1)
    else:
        pieces = 100 * (player_disc - opponent_disc) / (player_disc + opponent_disc + 1)

    return pieces


def evaluate_mobility(board, board_length, player, opponent):
    player_legal_moves = get_moves(board, board_length, player, opponent)
    opponent_legal_moves = get_moves(board, board_length, opponent, player)

    mobility = 100 * (len(player_legal_moves) - len(opponent_legal_moves)) / (len(player_legal_moves) + len(opponent_legal_moves) + 1)

    return mobility


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


def evaluate_weights(board, board_length):
    pieces = 0
    for row in board:
        for cell in row:
            if cell != '.':
                pieces += 1

    return pieces


def evaluate_board(board, board_length, player, opponent):
    score = 0
    weights = evaluate_weights(board, board_length)

    mobility = evaluate_mobility(board, board_length, player, opponent)
    frontier = evaluate_frontier(board, board_length, player, opponent)
    pieces = evaluate_pieces(board, board_length, player, opponent)
    stability = evaluate_stability(board, board_length, player, opponent)
    corners = evaluate_corners(board, board_length, player, opponent)
    
    if weights < 17 and player == 'O':
        score = (3 * mobility) + (3 * pieces) + (500 * stability) + (1000 * corners)

    else:
        score = (3 * mobility) + (2 * frontier) + (pieces) + (500 * stability) + (1000 * corners)

    return score


def killer_move(board, board_length, player, opponent, player_time, opponent_time):
    legal_moves = get_moves(board, board_length, player, opponent)
    
    if player_time < 2:
        return legal_moves[0]

    if len(legal_moves) == 1:
        return legal_moves[0]

    coordinate = [0, board_length - 1]
    for i in coordinate:
        for j in coordinate:
            if (i, j) in legal_moves:
                return (i, j)

    for move in legal_moves:
        new_board = [row[:] for row in board]
        new_board = update_board(new_board, board_length, player, move)
        opponent_legal_moves = []
        opponent_legal_moves = get_moves(new_board, board_length, opponent, player)
        if not opponent_legal_moves:
            return move

    return None


def min_node(board, board_length, depth, alpha, beta, player, opponent):
    min_score = float('inf')
    best_move = None
    legal_moves = get_moves(board, board_length, opponent, player)

    if depth == 0 or not legal_moves:
        return evaluate_board(board, board_length, player, opponent), best_move

    ordered_legal_moves = {}
    for move in legal_moves:
        new_board = [row[:] for row in board]
        new_board = update_board(new_board, board_length, player, move)
        ordered_legal_moves[move] = evaluate_board(new_board, board_length, player, opponent)
    ordered_legal_moves = dict(sorted(ordered_legal_moves.items(), key=lambda item: item[1]))

    for move in ordered_legal_moves:
        new_board = [row[:] for row in board]
        new_board = update_board(new_board, board_length, opponent, move)
        score, local_move = max_node(new_board, board_length, depth - 1, alpha, beta, player, opponent)

        if score < min_score:
            min_score = score
            best_move = move

        beta = min(beta, score)
        if beta <= alpha:
            break

    return min_score, best_move


def max_node(board, board_length, depth, alpha, beta, player, opponent):
    max_score = float('-inf')
    best_move = None
    legal_moves = get_moves(board, board_length, player, opponent)

    if depth == 0 or not legal_moves:
        return evaluate_board(board, board_length, player, opponent), best_move

    ordered_legal_moves = {}
    for move in legal_moves:
        new_board = [row[:] for row in board]
        new_board = update_board(new_board, board_length, player, move)
        ordered_legal_moves[move] = evaluate_board(new_board, board_length, player, opponent)
    ordered_legal_moves = dict(sorted(ordered_legal_moves.items(), key=lambda item: item[1], reverse=True))

    for move in ordered_legal_moves:
        new_board = [row[:] for row in board]
        new_board = update_board(new_board, board_length, player, move)
        score, local_move = min_node(new_board, board_length, depth - 1, alpha, beta, player, opponent)

        if score > max_score:
            max_score = score
            best_move = move

        alpha = max(alpha, score)
        if beta <= alpha:
            break

    return max_score, best_move


def make_move(best_move):
    column_name = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i', 9:'j', 10:'k', 11:'l'}
    row_name = best_move[0] + 1

    with open('output.txt', 'w') as out_file:
        out_file.write(column_name[best_move[1]]+str(row_name))


def main():
    board_length = 12
    depth = 4

    player, opponent, player_time, opponent_time, board = read_game(board_length)
    best_move = killer_move(board, board_length, player, opponent, player_time, opponent_time)
    if best_move == None:
        best_score, best_move = max_node(board, board_length, depth, float('-inf'), float('inf'), player, opponent)
    make_move(best_move)
    
 
if __name__ == "__main__":
    main()