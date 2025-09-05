import core.bot as bot
import core.constants as const
import core.messages as messages
import core.turns as turns
import output.print as prnt
import random
from core import turns
from core.board import Board
from core.constants import FIELD_HEIGHT as HEIGHT
from core.constants import FIELD_WIDTH as WIDTH
from core.game import Game
from core.player import Player
from enums.game_mode import Game_Mode
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

board = Board()
player1 = Player("Player", const.PLAYER_1_SYMBOL)
player2 = Player(bot.BOT_NAME, const.PLAYER_2_SYMBOL)
active_player = 1
game = Game(player1, Game_Mode.VS_BOT)
random.seed()

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def home():
    global game
    global board
    request_body = request.json
    if "board" not in request_body:
        return jsonify({
            "board": [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)],            "check_cols": game.check_cols,
            "matchpnt_cols": [],
            "game_won": False,
            "tokens_in_cols": [0, 0, 0, 0, 0, 0, 0],
            "moves_left": 42,
            "quit": False,
            "move": None
        })
    board = Board(request_body["board"])
    game = Game(request_body)
    player1 = Player("Player", const.PLAYER_1_SYMBOL)
    player2 = Player(bot.BOT_NAME, const.PLAYER_2_SYMBOL)
    game.active_player = player1
    board.place_token(request_body["move"], game)
    game.active_player = player2
    turns.bot_make_move(game, board)
    return jsonify({
        "board": board.matrix,
        "check_cols": game.check_cols,
        "matchpnt_cols": game.matchpnt_cols,
        "game_won": game.game_won,
        "tokens_in_cols": game.tokens_in_cols,
        "moves_left": game.moves_left,
        "quit": game.quit,
        "move": None
    })

"""
while True:
    if game.quit:
        break
    if board.is_win_or_tie(game, player1):
        break
    if board.is_win_or_tie(game, player2):
        break
"""

if __name__ == "__main__":
    app.run(debug=True)
