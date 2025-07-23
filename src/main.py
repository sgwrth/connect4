import core.bot as bot
import core.constants as const
import enum
import core.errors as errors
import core.messages as messages
import os
import random
from core.board import Board
from core.game import Game
from core.player import Player

class Game_Mode(enum.IntEnum):
    NONE = 0
    VS_BOT = 1
    TWO_PLAYERS = 2

class Column_Select(enum.IntEnum):
    QUIT_GAME = -2
    INVALID_COL = -1

board = Board()

def check_for_win_hori(board, game):
    symbol = game.active_player.token_symbol
    for row in range(const.BOTTOM_ROW, -1, -1):
        for col in range(const.FIELD_WIDTH - 2):

            if not has_3_hori(board, row, col, symbol):
                continue

            if col >= const.FIELD_WIDTH - 3:
                continue

            right_4th_is_symbol = board.matrix[row][col + 3] == symbol

            if right_4th_is_symbol:
                    print(f"{game.active_player.name} {messages.HAS_WON}")
                    game.game_won = True
                    return

            if is_check_hori_right(board, row, col, symbol):
                game.mark_col_as_check_or_matchpnt(col + 3, player1, symbol)

            if is_check_hori_left(board, row, col, symbol):
                game.mark_col_as_check_or_matchpnt(col - 1, player1, symbol)

def has_3_hori(board, row, col, symbol):
    return all(board.matrix[row][col + i] == symbol for i in range(3))

def is_check_hori_right(board, row, col, symbol):
    fourth_on_right_is_empty = board.matrix[row][col + 3] == " "
    below_4th_is_filled = (row == const.BOTTOM_ROW
                           or board.matrix[row + 1][col + 3] != " ")
    return fourth_on_right_is_empty and below_4th_is_filled

def is_check_hori_left(board, row, col, symbol):
    fourth_on_left_is_empty = board.matrix[row][col - 1] == " "
    below_4th_is_filled = (row == const.BOTTOM_ROW
                           or board.matrix[row + 1][col - 1] != " ")
    return fourth_on_left_is_empty and below_4th_is_filled
 
def check_for_win_vert(board, game):
    symbol = game.active_player.token_symbol
    for row in range(const.BOTTOM_ROW, const.THIRD_FROM_TOP, const.GO_UP):
        for col in range(const.FIELD_WIDTH):

            if not has_3_vert(board, row, col, symbol):
                continue

            if board.matrix[row - 3][col] == symbol:
                print(f"{game.active_player.name} {messages.HAS_WON}")
                game.game_won = True
                return

            if vert_4th_empty(board, row, col):
                game.mark_col_as_check_or_matchpnt(col, player1, symbol)

def has_3_vert(board, row, col, symbol):
    return all(board.matrix[row - i][col] == symbol for i in range(3))

def vert_4th_empty(board, row, col):
    return board.matrix[row - 3][col] == " "

def check_for_win_diagonal_nw_to_se(board, game):
    symbol = game.active_player.token_symbol
    for row in range(const.FIELD_HEIGHT - 2):
        for col in range(const.FIELD_WIDTH - 2):

            enough_se_space_for_4 = (row < const.FIELD_HEIGHT - 3
                                     and col < const.FIELD_WIDTH - 3)

            if not has_3_diagonal_nw_to_se(board, row, col, symbol):
                continue

            nw_4th_is_empty = board.matrix[row - 1][col - 1] == ' '
            below_nw_4th_is_filled = board.matrix[row][col - 1] != ' '

            if row > 0 and col > 0 and nw_4th_is_empty and below_nw_4th_is_filled:
                game.mark_col_as_check_or_matchpnt(col - 1, player1, symbol)

            if not enough_se_space_for_4:
                continue

            if board.matrix[row + 3][col + 3] == symbol:
                print(f"{game.active_player.name} {messages.HAS_WON}")
                game.game_won = True
                return

            se_4th_is_empty = board.matrix[row + 3][col + 3] == ' '
            below_se_4th_is_filled = (row + 3 == const.BOTTOM_ROW
                                      or board.matrix[row + 4][col + 3] != ' ')

            if se_4th_is_empty and below_se_4th_is_filled:
                game.mark_col_as_check_or_matchpnt(col + 3, player1, symbol)

def has_3_diagonal_nw_to_se(board, row, col, symbol):
    return all(board.matrix[row + i][col + i] == symbol for i in range(3))

def check_for_win_diagonal_sw_to_ne(board, game):
    symbol = game.active_player.token_symbol
    for row in range(const.BOTTOM_ROW, const.THIRD_FROM_TOP, const.GO_UP):
        for col in range(const.SECOND_FROM_RIGHT):

            if not has_3_diagonal_sw_to_ne(board, row, col, symbol):
                continue

            enough_ne_space_for_4th = col < 4 and row > 2 # Magic numbers.

            if not enough_ne_space_for_4th:
                continue

            ne_4th_is_symbol = board.matrix[row - 3][col + 3] == symbol

            if ne_4th_is_symbol:
                print(f"{game.active_player.name} {messages.HAS_WON}") 
                game.game_won = True
                return

            ne_4th_is_empty = board.matrix[row - 3][col + 3] == " "
            below_ne_4th_is_filled = board.matrix[row - 2][col + 3] != " "

            if ne_4th_is_empty and below_ne_4th_is_filled:
                game.mark_col_as_check_or_matchpnt(col + 3, player1, symbol)

            sw_cell_exists = row < const.BOTTOM_ROW and col > 0

            if not sw_cell_exists:
                continue

            sw_4th_is_empty = board.matrix[row + 1][col - 1] == " "
            below_sw_4th_is_filled = (row == const.ROW_ABOVE_BOTTOM_ROW
                                      or board.matrix[row + 2][col - 1] != " ")

            if sw_4th_is_empty and below_sw_4th_is_filled:
                game.mark_col_as_check_or_matchpnt(col - 1, player1, symbol)

def has_3_diagonal_sw_to_ne(board, row, col, symbol):
    return all(board.matrix[row - i][col + i] == symbol for i in range(3))

def check_for_win(board, game):
    check_for_win_hori(board, game)
    check_for_win_vert(board, game)
    check_for_win_diagonal_nw_to_se(board, game)
    check_for_win_diagonal_sw_to_ne(board, game)

def check_for_win_vs_bot(board, game):
    reset_matchpnt_cols(game)
    check_for_win(board, game)
    if not game.game_won:
        return False
    wipe_screen(board)
    print(f"{game.active_player.name} {messages.HAS_WON}")
    return True

def wipe_screen(board):
    os.system("cls" if os.name == "nt" else "clear")
    board.print_board()

def place_token(board, col, game):

    if col == Column_Select.QUIT_GAME:
        return

    for row in range(const.BOTTOM_ROW, -1, const.GO_UP):
        if cell_is_empty(board, row, col):
            board.matrix[row][col] = game.active_player.token_symbol
            game.tokens_in_cols[col] += 1
            game.moves_left -= 1
            return

def cell_is_empty(board, row, col):
    return board.matrix[row][col] == " "

def get_col_from_player(active_player):
    print(active_player.name + messages.PROMPT_PLAYER_FOR_MOVE, end = "")
    user_input = input()
    if user_input == const.KEY_TO_QUIT:
        return Column_Select.QUIT_GAME 
    else:
        try:
            return int(user_input) - 1
        except:
            return Column_Select.INVALID_COL

def prompt_player_for_move(game):
    while True:
        selected_col = get_col_from_player(game.active_player)

        if selected_col == Column_Select.QUIT_GAME:
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

def reset_check_cols(game):
    for i in range(len(game.check_cols) - 1, -1, -1):
        game.check_cols.pop(i)

def reset_matchpnt_cols(game):
    for i in range(len(game.matchpnt_cols) - 1, -1, -1):
        game.matchpnt_cols.pop(i)

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
        reset_check_cols(game)
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
        place_token(board, first_move_col(board), game)
        game.first_move = False
    else:
        place_token(board, select_col_for_bot(game), game)

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
    return True if check_for_win_vs_bot(board, game) or is_tie(game) else False

wipe_screen(board)

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
        wipe_screen(board)
        place_token(board, prompt_player_for_move(game), game)
        board.print_board()
        check_for_win(board, game)
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
        wipe_screen(board)
        place_token(board, prompt_player_for_move(game), game)
        if game.quit:
            break
        board.print_board()
        if is_win_or_tie(board, game):
            break
        game.toggle_active_player(player1, player2)
        wipe_screen(board)
        check_for_win(board, game)
        print_bots_turn_msg(game)
        bot_make_move(board, game)
        board.print_board()
        if is_win_or_tie(board, game):
            break
        game.toggle_active_player(player1, player2)
    print(f"{messages.THANKS_FOR_PLAYING}")
