def initialise_board(size: int = 8):
    """Returns a new game board with starting pieces in place."""

    # Create empty board
    board = [["None " for i in range(size)] for i in range(size)]

    # Place starting pieces
    board[(size // 2) - 1][(size // 2) - 1] = "Light"
    board[(size // 2)][(size // 2)] = "Light"
    board[(size // 2) - 1][(size // 2)] = "Dark "
    board[(size // 2)][(size // 2) - 1] = "Dark "

    return board


def print_board(board: list[list[str]]):
    """Prints the game board to the console with symbols."""

    for row in board:
        for col in row:
            if col == "None ":
                print("-", end=" ")
            if col == "Light":
                print("●", end=" ")
            if col == "Dark ":
                print("○", end=" ")
        print()


def legal_move(colour: str, coordinate: tuple, board: list[list[str]]):
    """Returns True if placing a piece of the given colour at the given
    coordinate is a legal move on the given board, otherwise returns False."""

    row, col = coordinate
    size = len(board)

    # Cannot play on an occupied square
    if board[row][col] != "None ":
        return False

    opponent = "Dark " if colour == "Light" else "Light"

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

    # Search in all 8 directions
    for row_step, col_step in steps:
        current_row = row + row_step
        current_col = col + col_step

        # While inside the board and the square contains an opponent piece,
        # Check another square in the same direction
        # When a sequence of opponent pieces is found,
        # check for a closing friendly piece

        opponent_sequence_found = False

        while (
            0 <= current_row < size
            and 0 <= current_col < size
            and board[current_row][current_col] == opponent
        ):
            opponent_sequence_found = True
            current_row += row_step
            current_col += col_step

        if (
            opponent_sequence_found
            and 0 <= current_row < size
            and 0 <= current_col < size
            and board[current_row][current_col] == colour
        ):
            return True

    return False


def has_legal_move(board, colour):
    """Returns True if there is at least one legal move for the given
    colour on the given board, otherwise returns False."""

    move_exists = False

    # Check every square on the board for legal moves
    for x in range(len(board)):
        for y in range(len(board[x])):
            if legal_move(colour, (x, y), board):
                move_exists = True

    return move_exists


def flip_pieces(colour: str, coordinate: tuple, board: list[list[str]]):
    """Returns an updated board with opponent pieces flipped as a result
    of placing a piece of the given colour at the given coordinate."""

    row, col = coordinate
    size = len(board)

    opponent = "Dark " if colour == "Light" else "Light"

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

    flipped_any = False

    for row_step, col_step in steps:
        current_row = row + row_step
        current_col = col + col_step
        pieces_to_flip = []

        # Collect opponent pieces in current direction
        while (
            0 <= current_row < size
            and 0 <= current_col < size
            and board[current_row][current_col] == opponent
        ):
            pieces_to_flip.append((current_row, current_col))
            current_row += row_step
            current_col += col_step

        # If the sequence is closed by a friendly piece, flip them
        if (
            pieces_to_flip
            and 0 <= current_row < size
            and 0 <= current_col < size
            and board[current_row][current_col] == colour
        ):
            for r, c in pieces_to_flip:
                board[r][c] = colour
            flipped_any = True

    if flipped_any:
        board[row][col] = colour

    return board


def print_stats(board: list[list[str]]):
    """Prints the end game stats including piece counts and winner."""

    dark_count = 0
    light_count = 0

    for row in board:
        for col in row:
            if col == "Dark ":
                dark_count += 1
            if col == "Light":
                light_count += 1

    print(f"Dark pieces: {dark_count}")
    print(f"Light pieces: {light_count}")

    if dark_count > light_count:
        print("Dark player wins!")
    elif light_count > dark_count:
        print("Light player wins!")
    else:
        print("The game is a draw!")
