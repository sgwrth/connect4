import asyncio
import core.bot as bot
import core.constants as const
import core.messages as messages
import core.turns as turns
import output.print as prnt
import json
import random
import time
from core import turns
from core.board import Board
from core.game import Game
from core.player import Player
from enums.game_mode import Game_Mode
from websockets.asyncio.server import serve

async def hello(websocket):
    response = {"data": None, "message": "Please enter your name"}
    await websocket.send(json.dumps(response))
    player_name = await websocket.recv()
    board = Board()
    player1 = Player(player_name, const.PLAYER_1_SYMBOL)
    player2 = Player(bot.BOT_NAME, const.PLAYER_2_SYMBOL)
    random.seed()
    game = Game(player1, Game_Mode.VS_BOT)
    response["message"] = f"Please place your token, {player_name}"
    response["data"] = board.matrix
    await websocket.send(json.dumps(response))

    while True:
        col_str = await websocket.recv()
        col = int(col_str) - 1
        board.place_token(col, game)
        if board.is_win_or_tie(game, player1):
            message = "You have won!" if game.game_won else "It's a tie!"
        else:
            message = f"It's Bot's turn now.  Waiting..."
        response = {"data": board.matrix, "message": message}

        await websocket.send(json.dumps(response))

        time.sleep(2)

        game.toggle_active_player(player1, player2)
        turns.bot_make_move(game, board)
        if board.is_win_or_tie(game, player2):
            message = "Bot has won!" if game.game_won else "It's a tie!"
        else:
            message = "Please place your token"
        game.toggle_active_player(player1, player2)
        response = {"data": board.matrix, "message": message}
        await websocket.send(json.dumps(response))
        if game.game_won:
            break

async def main():
    async with serve(hello, "0.0.0.0", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
