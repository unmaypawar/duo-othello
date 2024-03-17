from engine import get_moves, update_board
from evaluate import evaluate_board


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