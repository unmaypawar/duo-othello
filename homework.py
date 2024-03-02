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
    

def min_node(board, board_length, depth, alpha, beta, player, opponent):
    min_score = float('inf')
    best_move = None
    legal_moves = get_moves(board, board_length, opponent, player)

    if depth == 0 or not legal_moves:
        return evaluate_board(board, player, opponent), best_move

    for move in legal_moves:
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
        return evaluate_board(board, player, opponent), best_move

    for move in legal_moves:
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


def evaluate_board(board, player, opponent):
    score = 0
    for row in board:
        for cell in row:
            if cell == player:
                score += 1
            elif cell == opponent:
                score -= 1

    return score


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
    best_score, best_move = max_node(board, board_length, depth, float('-inf'), float('inf'), player, opponent)
    game_debug(board, board_length, player, opponent, best_move, player_time, opponent_time)
    make_move(best_move)
    
 
if __name__ == "__main__":
    main()