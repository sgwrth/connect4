import os
import random
import enum

FIELD_WIDTH = 7
FIELD_HEIGHT = 6
UNDERLINE_LENGTH = 21
BOT_LEVEL = 0.04
MIDDLE_COL = FIELD_WIDTH // 2

PLAYER_1_SYMBOL = "X"
PLAYER_2_SYMBOL = "O"
BOT_NAME = "Bot"
MSG_PROMPT_PLAYER_1_FOR_NAME = "Player 1, what is your name?"
MSG_PROMPT_PLAYER_2_FOR_NAME = "Player 2, what is your name?"
MSG_THANKS_FOR_PLAYING = "Thanks for playing!"
MSG_PROMPT_PLAYER_FOR_MOVE = ", it's your move! Enter the column no. for your token: "
MSG_ENTER_NAME = "Enter name: "
MSG_WELCOME = "Welcome, "
MSG_GOOD_LUCK = "!  And good luck!"
MSG_LETS_PLAY_CONNECT4 = "Let's play Connect 4!"
MSG_HAS_WON = " has won!"
MSG_CHOOSE_MODE = "Select game mode (1 = vs. bot, 2 = two players): "
ERROR_INVALID_COLUMN = "Error!  Invalid column number."
ERROR_COLUMN_FULL = "Error!  Column is full."

class Game_Mode(enum.IntEnum):
    VS_BOT = 1
    TWO_PLAYERS = 2

class Game:
    def __init__(self, active_player):
        self.active_player = active_player
        self.game_won = False
        self.first_move = True
        self.checkmate_cols = -1
        self.tokens_in_cols = [0, 0, 0, 0, 0, 0 ,0]

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

def print_footer():
    for i in range(1, UNDERLINE_LENGTH):
        print("-", end = '')
    print("-")
    for i in range(1, (FIELD_WIDTH + 1)):
        print(" " + str(i) + " ", end = '')
    print("\n")

def check_for_win_horizontal(matrix, game):
    global game_won
    global checkmate_cols
    symbol = game.active_player.token_symbol
    for i in range((FIELD_HEIGHT - 1), -1, -1):
        for j in range(4):
            if matrix[i][j] == symbol:
                if matrix[i][j + 1] == symbol:
                    if matrix[i][j + 2] == symbol:
                        if matrix[i][j + 3] == symbol:
                            print(game.active_player.name + MSG_HAS_WON)
                            game_won = True
                            break
                        elif check_for_3_horizontal_right(matrix, i, j, symbol):
                            checkmate_cols.append(j + 3)
                            if check_for_3_horizontal_left(matrix, i, j, symbol):
                                checkmate_cols.append(j - 1)
                        elif check_for_3_horizontal_left(matrix, i, j, symbol):
                            checkmate_cols.append(j - 1)

def check_for_3_horizontal_right(matrix, i, j, symbol):
    return (
        symbol == player1.token_symbol                  # opponent's symbol
        and matrix[i][j + 3] == ' '                     # and fourth field to the RIGHT empty
        and (                                           # and either:
            i == FIELD_HEIGHT - 1                       # it's on the bottom row
            or (                                        # or:
                    i < FIELD_HEIGHT - 1
                    and matrix[i + 1][j + 3] != ' '     # field beneath fourth not empty
            )
        )
    );

def check_for_3_horizontal_left(matrix, i, j, symbol):
    return (
        symbol == player1.token_symbol                  # opponent's symbol
        and matrix[i][j - 1] == ' '                     # and field LEFT to 3 is empty
        and (                                           # and either:
            i == FIELD_HEIGHT - 1                       # it's on the bottom row
            or (                                        # or:
                i < FIELD_HEIGHT - 1
                and matrix[i + 1][j - 1] != ' '         # and field beneath LEFT to 3 not empty
            )
        )
    );
 
def check_for_win_vertical(matrix, game):
    global game_won
    global checkmate_cols
    symbol = game.active_player.token_symbol
    for i in range((FIELD_HEIGHT - 1), 2, -1):
        for j in range(FIELD_WIDTH - 1):
            if matrix[i][j] == symbol:
                if matrix[i - 1][j] == symbol:
                    if matrix[i - 2][j] == symbol:
                        if matrix[i - 3][j] == symbol:
                            print(game.active_player.name + MSG_HAS_WON)
                            game_won = True
                            break
                        elif check_for_vertical_3(matrix, i, j, symbol):
                            checkmate_cols.append(j)

def check_for_vertical_3(matrix, i, j, symbol):
    return (
        symbol == player1.token_symbol
        and matrix[i - 3][j] == ' '
    );

def check_for_win_diagonal_nw_to_se(matrix, game):
    global game_won
    symbol = game.active_player.token_symbol
    for i in range(3):
        for j in range(4):
            if matrix[i][j] == symbol:
                if matrix[i + 1][j + 1] == symbol:
                    if matrix[i + 2][j + 2] == symbol:
                        if matrix[i + 3][j + 3] == symbol:
                            print(game.active_player.name + MSG_HAS_WON)
                            game_won = True
                            break

def check_for_win_diagonal_sw_to_ne(matrix, game):
    global game_won
    global checkmate_cols
    symbol = game.active_player.token_symbol
    for i in range((FIELD_HEIGHT - 1), 3, -1):
        for j in range(5):
            if matrix[i][j] == symbol:
                if matrix[i - 1][j + 1] == symbol:
                    if matrix[i - 2][j + 2] == symbol:

                        if j < 4 and i > 2:
                            if matrix[i - 3][j + 3] == symbol:
                                print(game.active_player.name + MSG_HAS_WON)
                                game_won = True
                                break
                            elif (
                                    # ne check
                                    matrix[i - 3][j + 3] == ' '
                                    and matrix[i - 2][j + 3] != ' '
                            ):
                                checkmate_cols.append(j + 3)

                        if (
                                # se check
                                (
                                    i < (FIELD_HEIGHT - 1)
                                    and j > 0
                                )
                                and
                                (
                                    matrix[i + 1][j - 1] == ' '
                                    and 
                                            (
                                                i == (FIELD_HEIGHT - 2)
                                                or matrix[i + 2][j - 1] != ' '
                                            )
                                )
                        ):
                            checkmate_cols.append(j - 1)


def check_for_win(matrix, game):
    check_for_win_horizontal(matrix, symbol)
    check_for_win_vertical(matrix, symbol)
    check_for_win_diagonal_nw_to_se(matrix, symbol)
    check_for_win_diagonal_sw_to_ne(matrix, symbol)

def check_for_win_vs_bot(matrix, game):
    check_for_win_horizontal(matrix, game)
    check_for_win_vertical(matrix, game)
    check_for_win_diagonal_nw_to_se(matrix, game)
    check_for_win_diagonal_sw_to_ne(matrix, game)
    if game_won == True:
        wipe_screen()
        print(game.active_player.name + MSG_HAS_WON)
        return True


def wipe_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_matrix(field)
    print_footer()

def toggle_active_player(game):
    if game.active_player == player1:
        game.active_player = player2
    else:
        game.active_player = player1

def place_token(matrix, column, game):
    for i in range((FIELD_HEIGHT - 1), -1, -1):
        if matrix[i][column] == ' ':
            matrix[i][column] = game.active_player.token_symbol
            game.tokens_in_cols[column] += 1
            break

def get_column_from_player(active_player):
    print(active_player.name + MSG_PROMPT_PLAYER_FOR_MOVE, end = '')
    try:
        return int(input()) - 1
    except:
        return -1

def prompt_player_for_move(game):
    while True:
        selected_column = get_column_from_player(game.active_player)
        if FIELD_WIDTH > selected_column > -1:
            if is_col_full(selected_column) == False:
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

def reset_checkmate_cols():
    global checkmate_cols
    for i in range((len(checkmate_cols) - 1), -1, -1):
        print("[removing: ", checkmate_cols[i] + 1, "]")
        checkmate_cols.pop(i)

def print_checkmate_cols(checkmate_cols):
    if 0!= len(checkmate_cols):
        for col in checkmate_cols:
            print(col + 1, " ", end = '')

def print_bots_turn_msg(checkmate_cols):
        if 0 != len(checkmate_cols):
            print("It's Bot's turn now!  (Danger in ", end = '')
            print_checkmate_cols(checkmate_cols)
            print("Will it notice?  Let's see!)  Press ENTER to continue.")
        else:
            print("It's Bot's turn now!  Press ENTER to continue.")
        input()

def select_col_for_bot(checkmate_cols):
    if 0 != len(checkmate_cols):
        for col in checkmate_cols:
            selected_column = col
            break
        reset_checkmate_cols()
        return selected_column
    else:
        while True:
            selected_column = get_random_column_no()
            if is_col_full(selected_column) == False:
                return selected_column

def get_random_column_no():
    return random.randint(0, (FIELD_WIDTH - 1))

def first_move_col(matrix):
    if matrix[(FIELD_HEIGHT - 1)][MIDDLE_COL] == ' ':
        return MIDDLE_COL
    else:
        if random.randint(0, 1) == 0:
            return MIDDLE_COL - 1
        else:
            return MIDDLE_COL + 1

def bot_make_move(matrix, game, checkmate_cols):
    if game.first_move:
        place_token(matrix, first_move_col(matrix), game)
        game.first_move = False
    else:
        place_token(matrix, select_col_for_bot(checkmate_cols), game)

wipe_screen()

print(MSG_LETS_PLAY_CONNECT4 + "\n")

first_move = False
game_won = False
checkmate_cols = []

print(MSG_PROMPT_PLAYER_1_FOR_NAME)
print(MSG_ENTER_NAME, end = '')
name = input()
player1 = Player(name, PLAYER_1_SYMBOL)
print(MSG_WELCOME + player1.name + MSG_GOOD_LUCK + "\n")
game_mode = -1
while game_mode != Game_Mode.VS_BOT and game_mode != Game_Mode.TWO_PLAYERS:
    print(MSG_CHOOSE_MODE)
    try:
        game_mode = int(input())
    except:
        print("[wrong input]")

if game_mode == Game_Mode.TWO_PLAYERS:
    print(MSG_PROMPT_PLAYER_2_FOR_NAME)
    print(MSG_ENTER_NAME, end = '')
    name = input()
    player2 = Player(name, PLAYER_2_SYMBOL)
    print(MSG_WELCOME + player2.name + MSG_GOOD_LUCK + "\n")
    game = Game(player1)
    while game_won != True:
        wipe_screen()
        selected_column = prompt_player_for_move(game)
        place_token(field, selected_column, game)
        print_matrix(field)
        print_footer()
        check_for_win(field, game)
        toggle_active_player(game)
    print(MSG_THANKS_FOR_PLAYING)
elif game_mode == Game_Mode.VS_BOT:
    random.seed()
    player2 = Player(BOT_NAME, PLAYER_2_SYMBOL)
    game = Game(player1)
    print(f"You will play against Bot (v{BOT_LEVEL})!  Press ENTER to continue.")
    input()
    while game_won != True:
        wipe_screen()
        selected_column = prompt_player_for_move(game)
        place_token(field, selected_column, game)
        print_matrix(field)
        print_footer()
        if 1 == check_for_win_vs_bot(field, game):
            break
        toggle_active_player(game)
        wipe_screen()
        print_bots_turn_msg(checkmate_cols)
        bot_make_move(field, game, checkmate_cols)
        print_matrix(field)
        print_footer()
        if 0 == check_for_win_vs_bot(field, game):
            break
        toggle_active_player(game)
    print(MSG_THANKS_FOR_PLAYING)
