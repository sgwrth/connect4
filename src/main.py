from core import turns
import core.bot as bot
import core.constants as const
import core.messages as messages
import core.turns as turns
import random
from core.board import Board
from core.game import Game
from core.player import Player
from enums.game_mode import Game_Mode

board = Board()
board.wipe_screen()

print(f"{messages.LETS_PLAY_CONNECT4}")
print(f"{messages.PROMPT_PLAYER_1_FOR_NAME}")
print(messages.ENTER_NAME, end = "")

player1 = Player(input(), const.PLAYER_1_SYMBOL)

print(f"{messages.WELCOME}, {player1.name}!  {messages.GOOD_LUCK}\n")

game_mode = Game.select_game_mode()

if Game_Mode.TWO_PLAYERS == game_mode:
    print(f"{messages.PROMPT_PLAYER_2_FOR_NAME}")
    print(messages.ENTER_NAME, end = "")
    player2 = Player(input(), const.PLAYER_2_SYMBOL)
    print(f"{messages.WELCOME}, {player2.name}!  {messages.GOOD_LUCK}\n")
    game = Game(player1, game_mode)
    while True != game.game_won:
        board.wipe_screen()
        board.place_token(turns.prompt_player_for_move(game, board), game)
        board.print_board()
        board.check_for_win(game, player1)
        if game.is_tie():
            break
        game.toggle_active_player(player1, player2)
    print(f"{messages.THANKS_FOR_PLAYING}")

if Game_Mode.VS_BOT == game_mode:
    random.seed()
    player2 = Player(bot.BOT_NAME, const.PLAYER_2_SYMBOL)
    game = Game(player1, game_mode)
    print(f"{messages.PLAY_VS_BOT}")
    input()
    while True:
        board.wipe_screen()
        board.place_token(turns.prompt_player_for_move(game, board), game)
        if game.quit:
            break
        board.print_board()
        if board.is_win_or_tie(game, player1):
            break
        game.toggle_active_player(player1, player2)
        board.wipe_screen()
        board.check_for_win(game, player1)
        game.print_bots_turn_msg()
        turns.bot_make_move(game, board)
        board.print_board()
        if board.is_win_or_tie(game, player1):
            break
        game.toggle_active_player(player1, player2)
    print(f"{messages.THANKS_FOR_PLAYING}")
