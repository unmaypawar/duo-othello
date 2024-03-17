def start_game(board_length):
    board = []
    for i in range(board_length):
        row = []
        for j in range(board_length):
            row.append('.')
        board.append(row)

    board[2][3] = 'B'
    board[3][2] = 'B'
    board[8][9] = 'B'
    board[9][8] = 'B'
    board[2][2] = 'W'
    board[3][3] = 'W'
    board[8][8] = 'W'
    board[9][9] = 'W'

    return board


def is_game_over(board, board_length):
    flag = 0
    for i in range(board_length):
        for j in range(board_length):
            if board[i][j] == '.':
                flag = 1
                break

    if not flag:
        return 1

    ai_moves = get_moves(board, board_length, 'W', 'B')
    if ai_moves:
        return 0

    player_moves = get_moves(board, board_length, 'B', 'W')
    if player_moves:
        return 0

    return 1


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


def killer_move(board, board_length, player, opponent):
    legal_moves = get_moves(board, board_length, player, opponent)

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


def make_move(best_move, player_moves, board, board_length, root):
    col = best_move.x // 60
    row = best_move.y // 60
    print('here')
    if (row, col) in player_moves:
        board = update_board(board, board_length, 'B', (row, col))
        root.destroy()
        return board

    return 0