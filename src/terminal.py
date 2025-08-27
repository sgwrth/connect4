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

board = Board()
board.wipe_screen()
prnt.welcome()
prnt.prompt_player1_for_name()
player1 = Player(input(), const.PLAYER_1_SYMBOL)
prnt.wish_luck(player1)
game_mode = Game.select_game_mode()

if Game_Mode.TWO_PLAYERS == game_mode:
    prnt.prompt_player2_for_name()
    player2 = Player(input(), const.PLAYER_2_SYMBOL)
    prnt.wish_luck(player2)
    game = Game(player1, game_mode)
    while True != game.game_won:
        board.wipe_screen()
        board.place_token(turns.prompt_player_for_move(game, board), game)
        board.print_board()
        board.check_for_win(game, player1)
        if game.is_tie():
            break
        game.toggle_active_player(player1, player2)
    prnt.thanks_for_playing()

if Game_Mode.VS_BOT == game_mode:
    random.seed()
    player2 = Player(bot.BOT_NAME, const.PLAYER_2_SYMBOL)
    prnt.play_vs_bot()
    input()
    game = Game(player1, game_mode)
    while True:
        board.wipe_screen()
        board.place_token(turns.prompt_player_for_move(game, board), game)
        if game.quit:
            break
        if board.is_win_or_tie(game, player1):
            break
        game.toggle_active_player(player1, player2)
        board.wipe_screen()
        game.print_bots_turn_msg()
        input()
        turns.bot_make_move(game, board)
        if board.is_win_or_tie(game, player2):
            break
        game.toggle_active_player(player1, player2)
    prnt.thanks_for_playing()
