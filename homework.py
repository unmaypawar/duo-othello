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

    return player, opponent, player_time, opponent_time, board


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
    

def evaluate_disc_diff(board, board_length, player, opponent):
    player_disc = 0
    opponent_disc = 0

    for row in board:
        for cell in row:
            if cell == player:
                player_disc += 1
            elif cell == opponent:
                opponent_disc += 1

    disc_diff = 100 * (player_disc - opponent_disc) / (player_disc + opponent_disc)

    return disc_diff


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


def evaluate_board(board, board_length, player, opponent):
    score = 0
    
    disc_diff = evaluate_disc_diff(board, board_length, player, opponent)
    mobility = evaluate_mobility(board, board_length, player, opponent)
    corners = evaluate_corners(board, board_length, player, opponent)

    score = disc_diff + (2 * mobility) + (1000 * corners)

    return score


def killer_move(board, board_length, player, opponent, player_time, opponent_time):
    legal_moves = get_moves(board, board_length, player, opponent)
    
    if len(legal_moves) == 1:
        return legal_moves[0]

    corners = [(0, 0), (0, board_length - 1), (board_length - 1, 0), (board_length - 1, board_length - 1)]
    for corner in corners:
        if corner in legal_moves:
            return corner

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


def game_debug(board, board_length, player, opponent, best_move, player_time, opponent_time):
    print(best_move)
    if best_move != None:
        board = update_board(board, board_length, player, best_move)
    time = player_time + ' ' + opponent_time
    with open('input.txt', 'w') as in_file:
        in_file.writelines(opponent)
        in_file.writelines('\n')
        in_file.writelines(time)
        in_file.writelines('\n')
        for i in range(board_length):
            in_file.writelines(board[i])
            in_file.writelines('\n')


def main():
    board_length = 12
    depth = 4

    player, opponent, player_time, opponent_time, board = read_game(board_length)
    best_move = killer_move(board, board_length, player, opponent, player_time, opponent_time)
    if best_move == None:
        best_score, best_move = max_node(board, board_length, depth, float('-inf'), float('inf'), player, opponent)

    game_debug(board, board_length, player, opponent, best_move, player_time, opponent_time)
    make_move(best_move)
    
 
if __name__ == "__main__":
    main()