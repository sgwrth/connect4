import output.print as prnt
from core import constants
from enums.col_select import Col_Select


class Player:
    def __init__(self, name, token_symbol):
        self.name = name
        self.token_symbol = token_symbol

    def get_col_from_player(self) -> int:
        prnt.prompt_player_for_move(self)
        user_input = input()
        if user_input == constants.KEY_TO_QUIT:
            return Col_Select.QUIT_GAME 
        try:
            return int(user_input) - 1
        except:
            return Col_Select.INVALID_COL
