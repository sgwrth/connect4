import os
import random
import enum

FIELD_WIDTH = 7
FIELD_HEIGHT = 6
UNDERLINE_LENGTH = 21
BOT_LEVEL = 0.065
MIDDLE_COL = FIELD_WIDTH // 2
MAX_MOVES = FIELD_WIDTH * FIELD_HEIGHT

PLAYER_1_SYMBOL = "X"
PLAYER_2_SYMBOL = "O"
BOT_NAME = "Bot"
KEY_TO_QUIT = "x"

MSG_PROMPT_PLAYER_1_FOR_NAME = "Player 1, what is your name?"
MSG_PROMPT_PLAYER_2_FOR_NAME = "Player 2, what is your name?"
MSG_THANKS_FOR_PLAYING = "Thanks for playing!"
MSG_PROMPT_PLAYER_FOR_MOVE = (
        ", it's your move!\n"
        f"Enter the column no. for your token (or {KEY_TO_QUIT} to quit): "
        )
MSG_ENTER_NAME = "Enter name: "
MSG_WELCOME = "Welcome, "
MSG_GOOD_LUCK = "!  And good luck!"
MSG_LETS_PLAY_CONNECT4 = "Let's play Connect 4!"
MSG_HAS_WON = " has won!"
MSG_CHOOSE_MODE = "Select game mode (1 = vs. bot, 2 = two players): "
MSG_PRESS_ENTER = "Press ENTER to continue."
MSG_PLAY_VS_BOT = (
        f"You will play against Bot (v{BOT_LEVEL})!  {MSG_PRESS_ENTER}"
        )
MSG_TIE_GAME = "Wow! It's a tie game!"
MSG_BOT_TURN = "It's Bot's turn now!"
MSG_MATCHPOINTS_IN = "Matchpoint(s) in "
MSG_WILL_IT_NOTICE = "\nWill it notice?  Let's see!"
MSG_DANGER_IN = "Danger in "
ERROR_INVALID_COLUMN = "Error!  Invalid column number."
ERROR_COLUMN_FULL = "Error!  Column is full."
ERROR_ILLEGAL_INPUT = "Error!  Illegal input."

class Game_Mode(enum.IntEnum):
    NONE = 0
    VS_BOT = 1
    TWO_PLAYERS = 2

class Column_Select(enum.IntEnum):
    QUIT_GAME = -2
    INVALID_COLUMN = -1

class Game:
    def __init__(self, active_player, game_mode):
        self.active_player = active_player
        self.game_mode = game_mode
        self.game_won = False
        self.first_move = True
        self.checkmate_cols = []
        self.matchpoint_cols = []
        self.tokens_in_cols = [0, 0, 0, 0, 0, 0 ,0]
        self.moves_left = MAX_MOVES
        self.quit = False

class Player:
    def __init__(self, name, token_symbol):
        self.name = name
        self.token_symbol = token_symbol

field = (
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "]
    )

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i]) - 1):
            print("["+ matrix[i][j]+ "]", end = '')
        print("[" + matrix[i][len(matrix[i]) - 1] + "]")
    print_footer()

def print_footer():
    for i in range(1, UNDERLINE_LENGTH):
        print("-", end = '')
    print("-")
    for i in range(1, (FIELD_WIDTH + 1)):
        print(" " + str(i) + " ", end = '')
    print("\n")

def check_for_win_horizontal(matrix, game):
    symbol = game.active_player.token_symbol
    for i in range(FIELD_HEIGHT - 1, -1, -1):
        for j in range(FIELD_WIDTH - 2):
            if has_3_horizontal(matrix, i, j, symbol):
                if j < (FIELD_WIDTH - 3) and matrix[i][j + 3] == symbol:
                    print(game.active_player.name + MSG_HAS_WON)
                    game.game_won = True
                    break
                elif (j < FIELD_WIDTH - 3
                        and is_checkmate_horizontal_right(matrix, i, j, symbol)):
                    mark_col_as_checkmate_or_matchpoint(j + 3, symbol)
                    if is_checkmate_horizontal_left(matrix, i, j, symbol):
                        mark_col_as_checkmate_or_matchpoint(j - 1, symbol)
                elif is_checkmate_horizontal_left(matrix, i, j, symbol):
                    mark_col_as_checkmate_or_matchpoint(j - 1, symbol)

def mark_col_as_checkmate_or_matchpoint(column, symbol):
    if symbol == player1.token_symbol:
        game.checkmate_cols.append(column)
    else:
        game.matchpoint_cols.append(column)

def has_3_horizontal(matrix, i, j, symbol):
    return (matrix[i][j] == symbol
            and matrix[i][j + 1] == symbol
            and matrix[i][j + 2] == symbol)

def is_checkmate_horizontal_right(matrix, i, j, symbol):
    return (matrix[i][j + 3] == ' '
            and (is_bottom_row(i)
                    or (i < FIELD_HEIGHT - 1 and matrix[i + 1][j + 3] != ' ')));

def is_bottom_row(row):
    return row == FIELD_HEIGHT - 1

def is_checkmate_horizontal_left(matrix, i, j, symbol):
    return (matrix[i][j - 1] == ' '
            and (i == FIELD_HEIGHT - 1
                    or (i < FIELD_HEIGHT - 1 and matrix[i + 1][j - 1] != ' ')));
 
def check_for_win_vertical(matrix, game):
    symbol = game.active_player.token_symbol
    for i in range(FIELD_HEIGHT - 1, 2, -1):
        for j in range(FIELD_WIDTH):
            if has_3_vertical(matrix, i, j, symbol):
                if matrix[i - 3][j] == symbol:
                    game.game_won = True
                    break
                elif vertical_empty(matrix, i, j):
                    mark_col_as_checkmate_or_matchpoint(j, symbol)

def has_3_vertical(matrix, i, j, symbol):
    return (matrix[i][j] == symbol
            and matrix[i - 1][j] == symbol
            and matrix[i - 2][j] == symbol)

def vertical_empty(matrix, i, j):
    return matrix[i - 3][j] == ' '

def check_for_win_diagonal_nw_to_se(matrix, game):
    symbol = game.active_player.token_symbol
    for i in range(FIELD_WIDTH - 2):
        for j in range(FIELD_WIDTH - 2):
            if ((FIELD_HEIGHT - 2) > i > 0 and (FIELD_WIDTH - 2) > j > 0
                    and has_3_diagonal_nw_to_se(matrix, i, j, symbol)
                    and matrix[i - 1][j - 1] == ' '
                    and matrix[i][j - 1] != ' '):
                mark_col_as_checkmate_or_matchpoint(j - 1, symbol)
            if i < (FIELD_HEIGHT - 3) and j < (FIELD_WIDTH - 3):
                if has_3_diagonal_nw_to_se(matrix, i, j, symbol):
                    if matrix[i + 3][j + 3] == symbol:
                        print(game.active_player.name + MSG_HAS_WON)
                        game.game_won = True
                        break
                    if (matrix[i + 3][j + 3] == ' '
                        and (is_bottom_row(i + 3)
                                or matrix[i + 4][j + 3] != ' ')):
                        mark_col_as_checkmate_or_matchpoint(j + 3, symbol)

def has_3_diagonal_nw_to_se(matrix, i, j, symbol):
    return (matrix[i][j] == symbol
            and matrix[i + 1][j + 1] == symbol
            and matrix[i + 2][j + 2] == symbol)

def check_for_win_diagonal_sw_to_ne(matrix, game):
    symbol = game.active_player.token_symbol
    for i in range(FIELD_HEIGHT - 1, 2, -1):
        for j in range(5):
            if has_3_diagonal_sw_to_ne(matrix, i, j, symbol):
                if j < 4 and i > 2:
                    if matrix[i - 3][j + 3] == symbol:
                        print(game.active_player.name + MSG_HAS_WON) 
                        game.game_won = True
                        break
                    elif (matrix[i - 3][j + 3] == ' '
                            and matrix[i - 2][j + 3] != ' '):
                        mark_col_as_checkmate_or_matchpoint(j + 3, symbol)
                if (i < FIELD_HEIGHT - 1 and j > 0
                        and (matrix[i + 1][j - 1] == ' '
                        and (i == FIELD_HEIGHT - 2
                                or matrix[i + 2][j - 1] != ' '))):
                    mark_col_as_checkmate_or_matchpoint(j - 1, symbol)

def has_3_diagonal_sw_to_ne(matrix, i, j, symbol):
    return (matrix[i][j] == symbol
            and matrix[i - 1][j + 1] == symbol
            and matrix[i - 2][j + 2] == symbol)

def check_for_win(matrix, game):
    check_for_win_horizontal(matrix, game)
    check_for_win_vertical(matrix, game)
    check_for_win_diagonal_nw_to_se(matrix, game)
    check_for_win_diagonal_sw_to_ne(matrix, game)

def check_for_win_vs_bot(matrix, game):
    reset_matchpoint_cols(game)
    check_for_win(matrix, game)
    if game.game_won:
        wipe_screen()
        print(game.active_player.name + MSG_HAS_WON)
        return True

def wipe_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_matrix(field)

def toggle_active_player(game):
    if game.active_player == player1:
        game.active_player = player2
    else:
        game.active_player = player1

def place_token(matrix, column, game):
    if Column_Select.QUIT_GAME != column:
        for i in range(FIELD_HEIGHT - 1, -1, -1):
            if matrix[i][column] == ' ':
                matrix[i][column] = game.active_player.token_symbol
                game.tokens_in_cols[column] += 1
                game.moves_left -= 1
                break

def get_column_from_player(active_player):
    print(active_player.name + MSG_PROMPT_PLAYER_FOR_MOVE, end = '')
    user_input = input()
    if user_input == KEY_TO_QUIT:
        return Column_Select.QUIT_GAME 
    else:
        try:
            return int(user_input) - 1
        except:
            return Column_Select.INVALID_COLUMN

def prompt_player_for_move(game):
    while True:
        selected_column = get_column_from_player(game.active_player)
        if Column_Select.QUIT_GAME == selected_column:
            game.quit = True
            return selected_column
        if FIELD_WIDTH > selected_column > -1:
            if False == is_col_full(selected_column):
                return selected_column
            else:
                print(ERROR_COLUMN_FULL)
        else:
            print(ERROR_INVALID_COLUMN)

def is_col_full(col):
    if game.tokens_in_cols[col] < FIELD_HEIGHT:
        return False
    else:
        return True

def reset_checkmate_cols(game):
    for i in range(len(game.checkmate_cols) - 1, -1, -1):
        game.checkmate_cols.pop(i)

def reset_matchpoint_cols(game):
    for i in range(len(game.matchpoint_cols) - 1, -1, -1):
        game.matchpoint_cols.pop(i)

def print_checkmate_cols(game):
    if game.checkmate_cols:
        for col in game.checkmate_cols:
            print(col + 1, " ", end = '')

def print_bots_turn_msg(game):
        if game.matchpoint_cols:
            print(MSG_MATCHPOINTS_IN, end = '')
            for col in game.matchpoint_cols:
                print(col + 1, " ", end = '')
            print(MSG_WILL_IT_NOTICE, MSG_PRESS_ENTER)
        if game.checkmate_cols:
            print(MSG_BOT_TURN)
            print(MSG_DANGER_IN, end = '')
            print_checkmate_cols(game)
            print(MSG_WILL_IT_NOTICE, MSG_PRESS_ENTER)
        else:
            print(MSG_BOT_TURN, MSG_PRESS_ENTER)
        input()

def select_col_for_bot(game):
    if game.matchpoint_cols:
        for col in game.matchpoint_cols:
            selected_column = col
            break
        return selected_column
    if game.checkmate_cols:
        for col in game.checkmate_cols:
            selected_column = col
            break
        reset_checkmate_cols(game)
        return selected_column
    else:
        while True:
            selected_column = get_random_column_no()
            if False == is_col_full(selected_column):
                return selected_column

def get_random_column_no():
    return random.randint(0, (FIELD_WIDTH - 1))

def first_move_col(matrix):
    if matrix[FIELD_HEIGHT - 1][MIDDLE_COL] == ' ':
        return MIDDLE_COL
    else:
        if random.randint(0, 1) == 0:
            return MIDDLE_COL - 1
        else:
            return MIDDLE_COL + 1

def bot_make_move(matrix, game):
    if game.first_move:
        place_token(matrix, first_move_col(matrix), game)
        game.first_move = False
    else:
        place_token(matrix, select_col_for_bot(game), game)

def select_game_mode():
    game_mode = Game_Mode.NONE
    while True:
        print(MSG_CHOOSE_MODE, end = '')
        try:
            game_mode = int(input())
        except:
            print(ERROR_ILLEGAL_INPUT)
            continue
        if game_mode == Game_Mode.VS_BOT:
            return game_mode
        elif game_mode == Game_Mode.TWO_PLAYERS:
            return game_mode
        else:
            print(ERROR_ILLEGAL_INPUT)

def is_tie(game):
    if 1 > game.moves_left:
        print(MSG_TIE_GAME)
        return True
    else:
        return False

def is_win_or_tie(matrix, game):
    if check_for_win_vs_bot(field, game) or is_tie(game):
        return True
    else:
        return False

wipe_screen()

print(MSG_LETS_PLAY_CONNECT4 + "\n")
print(MSG_PROMPT_PLAYER_1_FOR_NAME)
print(MSG_ENTER_NAME, end = '')
player1 = Player(input(), PLAYER_1_SYMBOL)
print(MSG_WELCOME + player1.name + MSG_GOOD_LUCK + "\n")

game_mode = select_game_mode()

if Game_Mode.TWO_PLAYERS == game_mode:
    print(MSG_PROMPT_PLAYER_2_FOR_NAME)
    print(MSG_ENTER_NAME, end = '')
    player2 = Player(input(), PLAYER_2_SYMBOL)
    print(MSG_WELCOME + player2.name + MSG_GOOD_LUCK + "\n")
    game = Game(player1, game_mode)
    while True != game.game_won:
        wipe_screen()
        place_token(field, prompt_player_for_move(game), game)
        print_matrix(field)
        check_for_win(field, game)
        if is_tie(game):
            break
        toggle_active_player(game)
    print(MSG_THANKS_FOR_PLAYING)
elif Game_Mode.VS_BOT == game_mode:
    random.seed()
    player2 = Player(BOT_NAME, PLAYER_2_SYMBOL)
    game = Game(player1, game_mode)
    print(MSG_PLAY_VS_BOT)
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
    print(MSG_THANKS_FOR_PLAYING)
