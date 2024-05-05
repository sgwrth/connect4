import os

FIELD_WIDTH = 7
FIELD_HEIGHT = 6
UNDERLINE_LENGTH = 21

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

def print_footer():
    for i in range(1, UNDERLINE_LENGTH):
        print("-", end = '')
    print("-")
    for i in range(1, (FIELD_WIDTH + 1)):
        print(" " + str(i) + " ", end = '')
    print("\n")

def print_matrix(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i]) - 1):
            print("["+ matrix[i][j]+ "]", end = '')
        print("[" + matrix[i][len(matrix[i]) - 1] + "]")

def check_horizontal(matrix, symbol):
    global game_won
    for i in range((FIELD_HEIGHT - 1), -1, -1):
        for j in range(0, 5):
            if matrix[i][j] == symbol:
                if matrix[i][j + 1] == symbol:
                    if matrix[i][j + 2] == symbol:
                        if matrix[i][j + 3] == symbol:
                            print("won! [h]")
                            game_won = 1
                            break

def check_vertical(matrix, symbol):
    global game_won
    for i in range((FIELD_HEIGHT - 1), 2, -1):
        for j in range(0, (FIELD_WIDTH - 1)):
            if matrix[i][j] == symbol:
                if matrix[i - 1][j] == symbol:
                    if matrix[i - 2][j] == symbol:
                        if matrix[i - 3][j] == symbol:
                            print("won! [v]")
                            game_won = 1
                            break


def check_diagonal_ne_to_sw(matrix, symbol):
    global game_won
    for i in range(0, 4):
        for j in range(0, 4):
            if matrix[i][j] == symbol:
                if matrix[i + 1][j + 1] == symbol:
                    if matrix[i + 2][j + 2] == symbol:
                        if matrix[i + 3][j + 3] == symbol:
                            print("won! [ne2sw]")
                            game_won = 1
                            break

# diagonal SW to NE
def check_diagonal_sw_to_ne(matrix, symbol):
    global game_won
    for i in range((FIELD_HEIGHT - 1), 2, -1):
        for j in range(0, 4):
            if matrix[i][j] == symbol:
                if matrix[i - 1][j + 1] == symbol:
                    if matrix[i - 2][j + 2] == symbol:
                        if matrix[i - 3][j + 3] == symbol:
                            print("won! [sw2ne]")
                            game_won = 1
                            break

def check_for_win(matrix, symbol):
    check_horizontal(matrix, symbol)
    check_vertical(matrix, symbol)
    check_diagonal_ne_to_sw(matrix, symbol)
    check_diagonal_sw_to_ne(matrix, symbol)

print("Let's play Connect 4!\n")

def wipe_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_matrix(field)
    print_footer()

wipe_screen()

print("Player 1, what is your name?")
print("Enter name: ", end = '')
name = input()
player1 = Player(name, "X")
print("Welcome, " + player1.name + "!  And good luck!\n")

print("Player 2, what is your name?")
print("Enter name: ", end = '')
name = input()
player2 = Player(name, "O")
print("Welcome, " + player2.name + "!  And good luck!\n")

active_player = player1

def toggle_active_player():
    global active_player
    if active_player == player1:
        active_player = player2
    else:
        active_player = player1

game_won = 0 

def place_token(matrix, column, player):
    if matrix[0][selected_column] != " ":
        print("Column is full!")
    else:
        for i in range((FIELD_HEIGHT - 1), -1, -1):
            if matrix[i][selected_column] == " ":
                matrix[i][selected_column] = player.token_symbol
                break

toggle_active_player()

while game_won != 1:
    wipe_screen()
    toggle_active_player()
    print(active_player.name + ", it's your move! Enter the column no. for your token: ", end = '')
    selected_column = int(input()) - 1
    place_token(field, selected_column, active_player)
    print_matrix(field)
    check_for_win(field, active_player.token_symbol)

print("Thanks for playing!")
