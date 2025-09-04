import core.bot as bot
import core.constants as const
import core.messages as messages
import core.turns as turns
import output.print as prnt
import random
from core import turns
from core.board import Board
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
    print(request_body["message"])
    if "board" not in request_body:
        return jsonify({
            "board": board.matrix,
            "active_player": 1 if game.active_player == player1 else 2,
            "first_move": game.first_move,
            "check_cols": game.check_cols,
            "matchpnt_cols": game.matchpnt_cols,
            "game_won": game.game_won,
            "tokens_in_cols": game.tokens_in_cols,
            "moves_left": game.moves_left,
            "quit": game.quit,
            "move": None
        })
    board = Board(None, None, request_json["board"])
    game = Game(None, None, request_json)


"""
while True:
    board.place_token(turns.prompt_player_for_move(game, board), game)
    if game.quit:
        break
    if board.is_win_or_tie(game, player1):
        break
    game.toggle_active_player(player1, player2)
    turns.bot_make_move(game, board)
    if board.is_win_or_tie(game, player2):
        break
    game.toggle_active_player(player1, player2)
"""

if __name__ == "__main__":
    app.run(debug=True)
