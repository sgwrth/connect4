import bot
import constants as const
import enum
import errors
import messages
import os
import random
from game import Game
from player import Player

class Game_Mode(enum.IntEnum):
    NONE = 0
    VS_BOT = 1
    TWO_PLAYERS = 2

class Column_Select(enum.IntEnum):
    QUIT_GAME = -2
    INVALID_COLUMN = -1


field = (
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "]
    )

def print_matrix(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[row]) - 1):
            print("["+ matrix[row][col]+ "]", end = '')
        print("[" + matrix[row][len(matrix[row]) - 1] + "]")
    print_footer()

def print_footer():
    for i in range(1, const.UNDERLINE_LEN):
        print("-", end = '')
    print("-")
    for i in range(1, (const.FIELD_WIDTH + 1)):
        print(" " + str(i) + " ", end = '')
    print("\n")

def check_for_win_hori(matrix, game):
    symbol = game.active_player.token_symbol
    for row in range(const.BOTTOM_ROW, -1, -1):
        for col in range(const.FIELD_WIDTH - 2):
            if has_3_hori(matrix, row, col, symbol):
                if col < (const.FIELD_WIDTH - 3) and matrix[row][col + 3] == symbol:
                    print(game.active_player.name + messages.HAS_WON)
                    game.game_won = True
                    break
                elif (col < const.FIELD_WIDTH - 3
                        and is_check_hori_right(matrix, row, col, symbol)):
                    mark_col_as_check_or_matchpnt(col + 3, symbol)
                    if is_check_hori_left(matrix, row, col, symbol):
                        mark_col_as_check_or_matchpnt(col - 1, symbol)
                elif is_check_hori_left(matrix, row, col, symbol):
                    mark_col_as_check_or_matchpnt(col - 1, symbol)

def mark_col_as_check_or_matchpnt(column, symbol):
    if symbol == player1.token_symbol:
        game.check_cols.append(column)
    else:
        game.matchpnt_cols.append(column)

def has_3_hori(matrix, row, col, symbol):
    return (matrix[row][col] == symbol
            and matrix[row][col + 1] == symbol
            and matrix[row][col + 2] == symbol)

def is_check_hori_right(matrix, row, col, symbol):
    return (matrix[row][col + 3] == ' '
            and (
                    is_bottom_row(row)
                    or (row < const.BOTTOM_ROW and matrix[row + 1][col + 3] != ' '))
            );

def is_bottom_row(row):
    return row == const.BOTTOM_ROW

def is_check_hori_left(matrix, row, col, symbol):
    return (matrix[row][col - 1] == ' '
            and (is_bottom_row(row)
                or (row < const.BOTTOM_ROW and matrix[row + 1][col - 1] != ' ')));
 
def check_for_win_vert(matrix, game):
    symbol = game.active_player.token_symbol
    for row in range(const.BOTTOM_ROW, 2, -1):
        for col in range(const.FIELD_WIDTH):
            if has_3_vert(matrix, row, col, symbol):
                if matrix[row - 3][col] == symbol:
                    game.game_won = True
                    break
                elif vert_empty(matrix, row, col):
                    mark_col_as_check_or_matchpnt(col, symbol)

def has_3_vert(matrix, row, col, symbol):
    return (matrix[row][col] == symbol
            and matrix[row - 1][col] == symbol
            and matrix[row - 2][col] == symbol)

def vert_empty(matrix, row, col):
    return matrix[row - 3][col] == ' '

def check_for_win_diagonal_nw_to_se(matrix, game):
    symbol = game.active_player.token_symbol
    for row in range(const.FIELD_WIDTH - 2):
        for col in range(const.FIELD_WIDTH - 2):
            if ((const.FIELD_HEIGHT - 2) > row > 0 and (const.FIELD_WIDTH - 2) > col > 0
                    and has_3_diagonal_nw_to_se(matrix, row, col, symbol)
                    and matrix[row - 1][col - 1] == ' '
                    and matrix[row][col - 1] != ' '):
                mark_col_as_check_or_matchpnt(col - 1, symbol)
            if row < (const.FIELD_HEIGHT - 3) and col < (const.FIELD_WIDTH - 3):
                if has_3_diagonal_nw_to_se(matrix, row, col, symbol):
                    if matrix[row + 3][col + 3] == symbol:
                        print(game.active_player.name + messages.HAS_WON)
                        game.game_won = True
                        break
                    if (matrix[row + 3][col + 3] == ' '
                        and (is_bottom_row(row + 3)
                                or matrix[row + 4][col + 3] != ' ')):
                        mark_col_as_check_or_matchpnt(col + 3, symbol)

def has_3_diagonal_nw_to_se(matrix, row, col, symbol):
    return (matrix[row][col] == symbol
            and matrix[row + 1][col + 1] == symbol
            and matrix[row + 2][col + 2] == symbol)

def check_for_win_diagonal_sw_to_ne(matrix, game):
    symbol = game.active_player.token_symbol
    for row in range(const.BOTTOM_ROW, 2, -1):
        for col in range(5): # Magic number.
            if has_3_diagonal_sw_to_ne(matrix, row, col, symbol):
                if col < 4 and row > 2: # Magic numbers.
                    if matrix[row - 3][col + 3] == symbol:
                        print(game.active_player.name + messages.HAS_WON) 
                        game.game_won = True
                        break
                    elif (matrix[row - 3][col + 3] == ' '
                            and matrix[row - 2][col + 3] != ' '):
                        mark_col_as_check_or_matchpnt(col + 3, symbol)
                if (row < const.BOTTOM_ROW and col > 0
                        and (matrix[row + 1][col - 1] == ' '
                        and (row == const.FIELD_HEIGHT - 2
                                or matrix[row + 2][col - 1] != ' '))):
                    mark_col_as_check_or_matchpnt(col - 1, symbol)

def has_3_diagonal_sw_to_ne(matrix, row, col, symbol):
    return (matrix[row][col] == symbol
            and matrix[row - 1][col + 1] == symbol
            and matrix[row - 2][col + 2] == symbol)

def check_for_win(matrix, game):
    check_for_win_hori(matrix, game)
    check_for_win_vert(matrix, game)
    check_for_win_diagonal_nw_to_se(matrix, game)
    check_for_win_diagonal_sw_to_ne(matrix, game)

def check_for_win_vs_bot(matrix, game):
    reset_matchpnt_cols(game)
    check_for_win(matrix, game)
    if game.game_won:
        wipe_screen()
        print(game.active_player.name + messages.HAS_WON)
        return True

def wipe_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_matrix(field)

def toggle_active_player(game):
    game.active_player = player1 if game.active_player == player2 else player2

def place_token(matrix, column, game):
    if Column_Select.QUIT_GAME != column:
        for row in range(const.BOTTOM_ROW, -1, -1):
            if matrix[row][column] == ' ':
                matrix[row][column] = game.active_player.token_symbol
                game.tokens_in_cols[column] += 1
                game.moves_left -= 1
                break

def get_column_from_player(active_player):
    print(active_player.name + messages.PROMPT_PLAYER_FOR_MOVE, end = '')
    user_input = input()
    if user_input == const.KEY_TO_QUIT:
        return Column_Select.QUIT_GAME 
    else:
        try:
            return int(user_input) - 1
        except:
            return Column_Select.INVALID_COLUMN

def prompt_player_for_move(game):
    while True:
        selected_column = get_column_from_player(game.active_player)
        if Column_Select.QUIT_GAME is selected_column:
            game.quit = True
            return selected_column
        if const.FIELD_WIDTH > selected_column > -1:
            if False == is_col_full(selected_column):
                return selected_column
            else:
                print(errors.COLUMN_FULL)
        else:
            print(errors.INVALID_COLUMN)

def is_col_full(col):
    return False if game.tokens_in_cols[col] < const.FIELD_HEIGHT else True

def reset_check_cols(game):
    for i in range(len(game.check_cols) - 1, -1, -1):
        game.check_cols.pop(i)

def reset_matchpnt_cols(game):
    for i in range(len(game.matchpnt_cols) - 1, -1, -1):
        game.matchpnt_cols.pop(i)

def print_check_cols(game):
    if game.check_cols:
        for col in game.check_cols:
            print(col + 1, " ", end = '')

def print_bots_turn_msg(game):
        if game.matchpnt_cols:
            print(messages.matchpntS_IN, end = '')
            for col in game.matchpnt_cols:
                print(col + 1, " ", end = '')
            print(messages.WILL_IT_NOTICE, messages.PRESS_ENTER)
        if game.check_cols:
            print(messages.BOT_TURN)
            print(messages.DANGER_IN, end = '')
            print_check_cols(game)
            print(messages.WILL_IT_NOTICE, messages.PRESS_ENTER)
        else:
            print(messages.BOT_TURN, messages.PRESS_ENTER)
        input()

def select_col_for_bot(game):
    if game.matchpnt_cols:
        for col in game.matchpnt_cols:
            selected_column = col
            break
        return selected_column
    if game.check_cols:
        for col in game.check_cols:
            selected_column = col
            break
        reset_check_cols(game)
        return selected_column
    else:
        while True:
            selected_column = get_rand_col()
            if False == is_col_full(selected_column):
                return selected_column

def get_rand_col():
    return random.randint(0, (const.FIELD_WIDTH - 1))

def first_move_col(matrix):
    if matrix[const.BOTTOM_ROW][const.MIDDLE_COL] == ' ':
        return const.MIDDLE_COL
    else:
        if random.randint(0, 1) == 0:
            return const.MIDDLE_COL - 1
        else:
            return const.MIDDLE_COL + 1

def bot_make_move(matrix, game):
    if game.first_move:
        place_token(matrix, first_move_col(matrix), game)
        game.first_move = False
    else:
        place_token(matrix, select_col_for_bot(game), game)

def select_game_mode():
    game_mode = Game_Mode.NONE
    while True:
        print(messages.CHOOSE_MODE, end = '')
        try:
            game_mode = int(input())
        except:
            print(errors.ILLEGAL_INPUT)
            continue
        if game_mode == Game_Mode.VS_BOT:
            return game_mode
        elif game_mode == Game_Mode.TWO_PLAYERS:
            return game_mode
        else:
            print(errors.ILLEGAL_INPUT)

def is_tie(game):
    if 1 > game.moves_left:
        print(messages.TIE_GAME)
        return True
    else:
        return False

def is_win_or_tie(matrix, game):
    return True if check_for_win_vs_bot(field, game) or is_tie(game) else False

wipe_screen()

print(messages.LETS_PLAY_CONNECT4 + "\n")
print(messages.PROMPT_PLAYER_1_FOR_NAME)
print(messages.ENTER_NAME, end = '')
player1 = Player(input(), const.PLAYER_1_SYMBOL)
print(messages.WELCOME + player1.name + messages.GOOD_LUCK + "\n")

game_mode = select_game_mode()

if Game_Mode.TWO_PLAYERS == game_mode:
    print(messages.PROMPT_PLAYER_2_FOR_NAME)
    print(messages.ENTER_NAME, end = '')
    player2 = Player(input(), const.PLAYER_2_SYMBOL)
    print(messages.WELCOME + player2.name + messages.GOOD_LUCK + "\n")
    game = Game(player1, game_mode)
    while True != game.game_won:
        wipe_screen()
        place_token(field, prompt_player_for_move(game), game)
        print_matrix(field)
        check_for_win(field, game)
        if is_tie(game):
            break
        toggle_active_player(game)
    print(messages.THANKS_FOR_PLAYING)
elif Game_Mode.VS_BOT == game_mode:
    random.seed()
    player2 = Player(bot.BOT_NAME, const.PLAYER_2_SYMBOL)
    game = Game(player1, game_mode)
    print(messages.PLAY_VS_BOT)
    input()
    while True:
        wipe_screen()
        place_token(field, prompt_player_for_move(game), game)
        if game.quit:
            break
        print_matrix(field)
        if is_win_or_tie(field, game):
            break
        toggle_active_player(game)
        wipe_screen()
        check_for_win(field, game)
        print_bots_turn_msg(game)
        bot_make_move(field, game)
        print_matrix(field)
        if is_win_or_tie(field, game):
            break
        toggle_active_player(game)
    print(messages.THANKS_FOR_PLAYING)
