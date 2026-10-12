from flask import Flask, render_template, request, jsonify
from components import *
from bot import bot_move


app = Flask(__name__)


@app.route("/")
def home():
    """Renders the main game page and initializes game state."""

    # Intitialise game state
    global board, player, move_counter
    board = initialise_board()
    move_counter = 60
    player = "Dark "

    # Render the main game page
    return render_template("index.html")


def get_win_stats():
    """Returns the winner and piece counts."""

    dark_count = 0
    light_count = 0
    for row in board:
        for col in row:
            if col == "Dark ":
                dark_count += 1
            elif col == "Light":
                light_count += 1

    if dark_count > light_count:
        winner = "Dark"
    elif light_count > dark_count:
        winner = "Light"
    else:
        winner = "Tie"

    return winner, dark_count, light_count


# Called when a player makes a move
@app.route("/make_move", methods=["POST"])
def make_move():
    """Flask route to handle a player's move and return the updated game state."""

    global player, board, move_counter

    # Recieve move from frontend
    data = request.get_json()
    row = int(data["row"])
    col = int(data["col"])

    # Validate move
    if not legal_move(player, (row, col), board):
        return jsonify({"status": "invalid move"})

    # Update game state
    board = flip_pieces(player, (row, col), board)
    player = "Dark " if player == "Light" else "Light"
    move_counter -= 1

    # Check for game over
    if (
        move_counter == 0
        or not has_legal_move(board, "Dark ")
        and not has_legal_move(board, "Light")
    ):
        winner, dark_count, light_count = get_win_stats()
        return jsonify(
            {
                "status": "game over",
                "winner": winner,
                "dark_count": dark_count,
                "light_count": light_count,
            }
        )

    # Send updated game state to frontend
    return jsonify({"status": "success", "board": board, "next_player": player})


@app.route("/get_game_state")
def get_game_state():
    """Flask route to get the current game state."""

    global board, player, move_counter
    return jsonify({"board": board, "player": player, "move_counter": move_counter})


@app.route("/load_game_state", methods=["POST"])
def load_game_state():
    """Flask route to load a saved game state."""

    global board, player, move_counter

    data = request.get_json()
    board = data["board"]
    player = data["player"]
    move_counter = data["move_counter"]

    return jsonify({"status": "success"})


@app.route("/get_ai_move", methods=["POST"])
def get_ai_move():
    """Flask route to return the AI's move."""

    global board

    data = request.get_json()
    board = data["board"]

    # AI couldn't make a move, game over
    if bot_move(board) is None:
        winner, dark_count, light_count = get_win_stats()
        return jsonify(
            {
                "status": "game over",
                "winner": winner,
                "dark_count": dark_count,
                "light_count": light_count,
            }
        )

    row, col = bot_move(board)

    return jsonify({"status": "success", "row": row, "col": col})


if __name__ == "__main__":
    app.run(debug=True)
