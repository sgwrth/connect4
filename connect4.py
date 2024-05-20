import os
import random

FIELD_WIDTH = 7
FIELD_HEIGHT = 6
UNDERLINE_LENGTH = 21
BOT_LEVEL = 0.03

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
ERROR_INVALID_COLUMN = "Error! Invalid column number."

class Game:
    def __init__(self, active_player, game_won, first_move, checkmate_col):
        self.active_player = active_player
        self.game_won = game_won
        self.first_move = first_move
        self.checkmate_col = checkmate_col
        self.tokens_in_cols = [0, 0, 0, 0, 0 ,0 ,0]

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

def check_for_win_horizontal(matrix, symbol):
    global game_won
    global checkmate_col
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
                            checkmate_col.append(j + 3)
                            if check_for_3_horizontal_left(matrix, i, j, symbol):
                                checkmate_col.append(j - 1)
                        elif check_for_3_horizontal_left(matrix, i, j, symbol):
                            checkmate_col.append(j - 1)

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
 
def check_for_win_vertical(matrix, symbol):
    global game_won
    global checkmate_col
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
                            checkmate_col.append(j)

def check_for_vertical_3(matrix, i, j, symbol):
    return (
        symbol == player1.token_symbol
        and matrix[i - 3][j] == ' '
    );

def check_for_win_diagonal_nw_to_se(matrix, symbol):
    global game_won
    for i in range(3):
        for j in range(4):
            if matrix[i][j] == symbol:
                if matrix[i + 1][j + 1] == symbol:
                    if matrix[i + 2][j + 2] == symbol:
                        if matrix[i + 3][j + 3] == symbol:
                            print(game.active_player.name + MSG_HAS_WON)
                            game_won = True
                            break

def check_for_win_diagonal_sw_to_ne(matrix, symbol):
    global game_won
    global checkmate_col
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
                                checkmate_col.append(j + 3)

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
                            checkmate_col.append(j - 1)


def check_for_win(matrix, symbol):
    check_for_win_horizontal(matrix, symbol)
    check_for_win_vertical(matrix, symbol)
    check_for_win_diagonal_nw_to_se(matrix, symbol)
    check_for_win_diagonal_sw_to_ne(matrix, symbol)

def check_for_win_vs_bot(matrix, symbol):
    check_for_win_horizontal(matrix, symbol)
    check_for_win_vertical(matrix, symbol)
    check_for_win_diagonal_nw_to_se(matrix, symbol)
    check_for_win_diagonal_sw_to_ne(matrix, symbol)
    if game_won == True:
        return True


def wipe_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_matrix(field)
    print_footer()

def toggle_active_player():
    # global active_player
    if game.active_player == player1:
        game.active_player = player2
    else:
        game.active_player = player1

def place_token(matrix, column, player):
    for i in range((FIELD_HEIGHT - 1), -1, -1):
        if matrix[i][selected_column] == " ":
            matrix[i][selected_column] = player.token_symbol
            break

def get_column_from_player(active_player):
    print(active_player.name + MSG_PROMPT_PLAYER_FOR_MOVE, end = '')
    column_as_string = input()
    try:
        column_as_int = int(column_as_string) - 1
        return column_as_int
    except:
        return -1

def prompt_player_for_move(active_player):
    global selected_column
    while True:
        selected_column = get_column_from_player(active_player)
        if selected_column > -1 and selected_column < FIELD_WIDTH:
            break
        else:
            print(ERROR_INVALID_COLUMN)

def reset_checkmate_col():
    global checkmate_col
    for i in range((len(checkmate_col) - 1), -1, -1):
        print("[removing: ", checkmate_col[i] + 1, "]")
        checkmate_col.pop(i)

# wipe_screen()
print_matrix(field)
print_footer()

print(MSG_LETS_PLAY_CONNECT4 + "\n")

first_move = False
game_won = False
checkmate_col = []
# bot_level = 0.02

print(MSG_PROMPT_PLAYER_1_FOR_NAME)
print(MSG_ENTER_NAME, end = '')
name = input()
player1 = Player(name, PLAYER_1_SYMBOL)
print(MSG_WELCOME + player1.name + MSG_GOOD_LUCK + "\n")
print(MSG_CHOOSE_MODE)
game_mode = input()

def get_random_column_no():
    return random.randint(0, (FIELD_WIDTH - 1))

if game_mode == "2":
    print(MSG_PROMPT_PLAYER_2_FOR_NAME)
    print(MSG_ENTER_NAME, end = '')
    name = input()
    player2 = Player(name, PLAYER_2_SYMBOL)
    print(MSG_WELCOME + player2.name + MSG_GOOD_LUCK + "\n")
    game = Game(player1, False, True, -1)
    # active_player = player1
    while game_won != True:
        # wipe_screen()
        prompt_player_for_move(game.active_player)
        place_token(field, selected_column, game.active_player)
        print_matrix(field)
        print_footer()
        check_for_win(field, game.active_player.token_symbol)
        toggle_active_player()
    print(MSG_THANKS_FOR_PLAYING)
elif game_mode == "1":
    random.seed()
    player2 = Player(BOT_NAME, PLAYER_2_SYMBOL)
    game = Game(player1, False, True, -1)
    print(f"You will play against Bot (v{BOT_LEVEL})!  Press ENTER to continue.")
    input()
    # active_player = player1
    while game_won != True:
        # wipe_screen()
        prompt_player_for_move(game.active_player)
        place_token(field, selected_column, game.active_player)
        print_matrix(field)
        print_footer()
        if 1 == check_for_win_vs_bot(field, game.active_player.token_symbol):
            break
        if 0!= len(checkmate_col):
            print("[checkmate cols: ", end = '')
        for col in checkmate_col:
            print(col + 1, " ", end = '')
        if 0!= len(checkmate_col):
            print(']\n')
        toggle_active_player()
        # wipe_screen()
        if 0 != len(checkmate_col):
            print("It's Bot's turn now!  (Will it notice?  Let's see!)  Press ENTER to continue.")
        else:
            print("It's Bot's turn now!  Press ENTER to continue.")
        input()
        if 0 != len(checkmate_col):
            for col in checkmate_col:
                selected_column = col
                # checkmate_col.remove(col)
                break
            reset_checkmate_col()
        else:
            selected_column = get_random_column_no()
        place_token(field, selected_column, game.active_player)
        print_matrix(field)
        print_footer()
        if 0 == check_for_win_vs_bot(field, game.active_player.token_symbol):
            break
        toggle_active_player()
    print(MSG_THANKS_FOR_PLAYING)
