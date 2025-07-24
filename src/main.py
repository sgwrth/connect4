import core.bot as bot
import core.constants as const
import enum
import core.errors as errors
import core.messages as messages
import random
from core.board import Board
from core.game import Game
from core.player import Player
from enums.col_select import Col_Select
from enums.game_mode import Game_Mode

board = Board()

def get_col_from_player(active_player):
    print(active_player.name + messages.PROMPT_PLAYER_FOR_MOVE, end = "")
    user_input = input()
    if user_input == const.KEY_TO_QUIT:
        return Col_Select.QUIT_GAME 
    else:
        try:
            return int(user_input) - 1
        except:
            return Col_Select.INVALID_COL

def prompt_player_for_move(game):
    while True:
        selected_col = get_col_from_player(game.active_player)
        if selected_col == Col_Select.QUIT_GAME:
            game.quit = True
            return selected_col
        is_valid_col_num = const.FIELD_WIDTH > selected_col > -1
        if not is_valid_col_num:
            print(errors.INVALID_COL)
            continue
        if is_col_full(selected_col):
            print(errors.COL_FULL)
            continue
        return selected_col

def is_col_full(col):
    return False if game.tokens_in_cols[col] < const.FIELD_HEIGHT else True

def check_cols_to_str(game):
    if game.check_cols:
        return " ".join(f"{col + 1}" for col in game.check_cols)

def matchpnt_cols_to_str(game):
    if game.matchpnt_cols:
        return " ".join(f"{col + 1}" for col in game.matchpnt_cols)

def print_bots_turn_msg(game):
        if game.matchpnt_cols:
            print(f"{messages.MATCHPNTS_IN} {matchpnt_cols_to_str(game)}")
            print(f"{messages.WILL_IT_NOTICE}  {messages.PRESS_ENTER}")
        if game.check_cols:
            print(f"{messages.BOT_TURN}")
            print(f"{messages.DANGER_IN} {check_cols_to_str(game)}")
            print(f"{messages.WILL_IT_NOTICE}  {messages.PRESS_ENTER}")
        else:
            print(f"{messages.BOT_TURN}  {messages.PRESS_ENTER}")
        input()

def select_col_for_bot(game):
    if game.matchpnt_cols:
        return game.matchpnt_cols[0] 
    if game.check_cols:
        selected_col = game.check_cols[0]
        game.reset_check_cols()
        return selected_col
    while True:
        selected_col = get_rand_col()
        if not is_col_full(selected_col):
            return selected_col

def get_rand_col():
    return random.randint(0, (const.FIELD_WIDTH - 1))

def first_move_col(board):
    if board.matrix[const.BOTTOM_ROW][const.MIDDLE_COL] == ' ':
        return const.MIDDLE_COL
    if random.randint(0, 1) == 0:
        return const.MIDDLE_COL - 1
    return const.MIDDLE_COL + 1

def bot_make_move(board, game):
    if game.first_move:
        board.place_token(first_move_col(board), game)
        game.first_move = False
    else:
        board.place_token(select_col_for_bot(game), game)

def select_game_mode():
    game_mode = Game_Mode.NONE
    while True:
        print(messages.CHOOSE_MODE, end = "")
        try:
            game_mode = int(input())
        except:
            print(errors.ILLEGAL_INPUT)
            continue
        if game_mode == Game_Mode.VS_BOT or game_mode == Game_Mode.TWO_PLAYERS:
            return game_mode
        print(errors.ILLEGAL_INPUT)

def is_tie(game):
    if 1 > game.moves_left:
        print(messages.TIE_GAME)
        return True
    else:
        return False

def is_win_or_tie(board, game):
    return True if board.check_for_win_vs_bot(game, player1) or is_tie(game) else False

board.wipe_screen()

print(f"{messages.LETS_PLAY_CONNECT4}")
print(f"{messages.PROMPT_PLAYER_1_FOR_NAME}")
print(messages.ENTER_NAME, end = "")
player1 = Player(input(), const.PLAYER_1_SYMBOL)
print(f"{messages.WELCOME}, {player1.name}!  {messages.GOOD_LUCK}\n")

game_mode = select_game_mode()

if Game_Mode.TWO_PLAYERS == game_mode:
    print(f"{messages.PROMPT_PLAYER_2_FOR_NAME}")
    print(messages.ENTER_NAME, end = "")
    player2 = Player(input(), const.PLAYER_2_SYMBOL)
    print(f"{messages.WELCOME}, {player2.name}!  {messages.GOOD_LUCK}\n")
    game = Game(player1, game_mode)
    while True != game.game_won:
        board.wipe_screen()
        board.place_token(prompt_player_for_move(game), game)
        board.print_board()
        board.check_for_win(game, player1)
        if is_tie(game):
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
        board.place_token(prompt_player_for_move(game), game)
        if game.quit:
            break
        board.print_board()
        if is_win_or_tie(board, game):
            break
        game.toggle_active_player(player1, player2)
        board.wipe_screen()
        board.check_for_win(game, player1)
        print_bots_turn_msg(game)
        bot_make_move(board, game)
        board.print_board()
        if is_win_or_tie(board, game):
            break
        game.toggle_active_player(player1, player2)
    print(f"{messages.THANKS_FOR_PLAYING}")
