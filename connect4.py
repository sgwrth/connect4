import os

FIELD_WIDTH = 7
FIELD_HEIGHT = 6
UNDERLINE_LENGTH = 21

PLAYER_1_SYMBOL = "X"
PLAYER_2_SYMBOL = "O"
MSG_PROMPT_PLAYER_1_FOR_NAME = "Player 1, what is your name?"
MSG_PROMPT_PLAYER_2_FOR_NAME = "Player 2, what is your name?"
MSG_THANKS_FOR_PLAYING = "Thanks for playing!"
MSG_PROMPT_PLAYER_FOR_MOVE = ", it's your move! Enter the column no. for your token: "
MSG_ENTER_NAME = "Enter name: "
MSG_WELCOME = "Welcome, "
MSG_GOOD_LUCK = "!  And good luck!"
MSG_LETS_PLAY_CONNECT4 = "Let's play Connect 4!"
MSG_HAS_WON = " has won!"
ERROR_INVALID_COLUMN = "Error! Invalid column number."

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
    for i in range((FIELD_HEIGHT - 1), -1, -1):
        for j in range(4):
            if matrix[i][j] == symbol:
                if matrix[i][j + 1] == symbol:
                    if matrix[i][j + 2] == symbol:
                        if matrix[i][j + 3] == symbol:
                            print(active_player.name + MSG_HAS_WON)
                            game_won = 1
                            break

def check_for_win_vertical(matrix, symbol):
    global game_won
    for i in range((FIELD_HEIGHT - 1), 2, -1):
        for j in range(FIELD_WIDTH - 1):
            if matrix[i][j] == symbol:
                if matrix[i - 1][j] == symbol:
                    if matrix[i - 2][j] == symbol:
                        if matrix[i - 3][j] == symbol:
                            print(active_player.name + MSG_HAS_WON)
                            game_won = 1
                            break

def check_for_win_diagonal_nw_to_se(matrix, symbol):
    global game_won
    for i in range(3):
        for j in range(4):
            if matrix[i][j] == symbol:
                if matrix[i + 1][j + 1] == symbol:
                    if matrix[i + 2][j + 2] == symbol:
                        if matrix[i + 3][j + 3] == symbol:
                            print(active_player.name + MSG_HAS_WON)
                            game_won = 1
                            break

def check_for_win_diagonal_sw_to_ne(matrix, symbol):
    global game_won
    for i in range((FIELD_HEIGHT - 1), 2, -1):
        for j in range(4):
            if matrix[i][j] == symbol:
                if matrix[i - 1][j + 1] == symbol:
                    if matrix[i - 2][j + 2] == symbol:
                        if matrix[i - 3][j + 3] == symbol:
                            print(active_player.name + MSG_HAS_WON)
                            game_won = 1
                            break

def check_for_win(matrix, symbol):
    check_for_win_horizontal(matrix, symbol)
    check_for_win_vertical(matrix, symbol)
    check_for_win_diagonal_nw_to_se(matrix, symbol)
    check_for_win_diagonal_sw_to_ne(matrix, symbol)

print(MSG_LETS_PLAY_CONNECT4 + "\n")

def wipe_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_matrix(field)
    print_footer()

wipe_screen()

print(MSG_PROMPT_PLAYER_1_FOR_NAME)
print(MSG_ENTER_NAME, end = '')
name = input()
player1 = Player(name, PLAYER_1_SYMBOL)
print(MSG_WELCOME + player1.name + MSG_GOOD_LUCK + "\n")

print(MSG_PROMPT_PLAYER_2_FOR_NAME)
print(MSG_ENTER_NAME, end = '')
name = input()
player2 = Player(name, PLAYER_2_SYMBOL)
print(MSG_WELCOME + player2.name + MSG_GOOD_LUCK + "\n")

active_player = player1

def toggle_active_player():
    global active_player
    if active_player == player1:
        active_player = player2
    else:
        active_player = player1

game_won = 0 

def place_token(matrix, column, player):
    for i in range((FIELD_HEIGHT - 1), -1, -1):
        if matrix[i][selected_column] == " ":
            matrix[i][selected_column] = player.token_symbol
            break

def get_column_from_player():
    print(active_player.name + MSG_PROMPT_PLAYER_FOR_MOVE, end = '')
    column_as_string = input()
    try:
        column_as_int = int(column_as_string) - 1
        return column_as_int
    except:
        return -1

def prompt_player_for_move():
    global selected_column
    while True:
        selected_column = get_column_from_player()
        if selected_column > -1 and selected_column < FIELD_WIDTH:
            break
        else:
            print(ERROR_INVALID_COLUMN)

while game_won != 1:
    wipe_screen()
    prompt_player_for_move()
    place_token(field, selected_column, active_player)
    print_matrix(field)
    check_for_win(field, active_player.token_symbol)
    toggle_active_player()

print(MSG_THANKS_FOR_PLAYING)
