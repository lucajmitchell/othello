import random


def count_flips(
    board: list[list[str]], coordinate: tuple, ai_color: str, opponent_color: str
):
    """Counts the number of opponent pieces that would be flipped by placing a piece at the given coordinate."""

    row, col = coordinate
    size = len(board)
    total_flips = 0

    steps = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    for row_step, col_step in steps:
        r, c = row + row_step, col + col_step
        flips_in_direction = 0

        # Keep moving in the direction while we see opponent pieces
        while 0 <= r < size and 0 <= c < size and board[r][c] == opponent_color:
            flips_in_direction += 1
            r += row_step
            c += col_step

        # If we end on AI's own color, the flips are valid
        if 0 <= r < size and 0 <= c < size and board[r][c] == ai_color:
            total_flips += flips_in_direction

    return total_flips


def bot_move(
    board: list[list[str]], ai_color: str = "Light", opponent_color: str = "Dark "
):
    """Determines the AI's move based on maximizing flipped pieces."""

    valid_moves = []

    # Count flips for each empty cell
    for row in range(8):
        for col in range(8):
            if board[row][col] == "None ":
                flips = count_flips(board, (row, col), ai_color, opponent_color)
                if flips > 0:
                    valid_moves.append(((row, col), flips))

    if not valid_moves:
        return None

    # Choose the move that flips the most pieces
    max_flips = max(valid_moves, key=lambda x: x[1])[1]
    best_moves = [move for move, flips in valid_moves if flips == max_flips]

    return random.choice(best_moves)
