from core import constants, messages
from enums.col_select import Col_Select


class Player:
    def __init__(self, name, token_symbol):
        self.name = name
        self.token_symbol = token_symbol

    def get_col_from_player(self):
        print(self.name + messages.PROMPT_PLAYER_FOR_MOVE, end = "")
        user_input = input()
        if user_input == constants.KEY_TO_QUIT:
            return Col_Select.QUIT_GAME 
        else:
            try:
                return int(user_input) - 1
            except:
                return Col_Select.INVALID_COL
