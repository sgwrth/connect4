from core import errors, messages
import core.constants as const
from core.player import Player
from enums.game_mode import Game_Mode

class Game:
    def __init__(self, active_player: Player, game_mode: int):
        self.active_player = active_player
        self.game_mode = game_mode
        self.game_won = False
        self.first_move = True
        self.check_cols = []
        self.matchpnt_cols = []
        self.tokens_in_cols = [0, 0, 0, 0, 0, 0 ,0]
        self.moves_left = const.MAX_MOVES
        self.quit = False

    def mark_col_as_check_or_matchpnt(self, col: int, player1: Player, symbol: str) -> None:
        if symbol == player1.token_symbol:
            self.check_cols.append(col)
        else:
            self.matchpnt_cols.append(col)

    def toggle_active_player(self, player1: Player, player2: Player) -> None:
        self.active_player = player1 if self.active_player == player2 else player2

    def reset_check_cols(self) -> None:
        for i in range(len(self.check_cols) - 1, -1, -1):
            self.check_cols.pop(i)

    def reset_matchpnt_cols(self) -> None:
        for i in range(len(self.matchpnt_cols) - 1, -1, -1):
            self.matchpnt_cols.pop(i)


    def is_tie(self) -> bool:
        if 1 > self.moves_left:
            print(messages.TIE_GAME)
            return True
        else:
            return False

    @staticmethod
    def select_game_mode() -> int:
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
            
    def check_cols_to_str(self) -> str | None:
        if self.check_cols:
            return " ".join(f"{col + 1}" for col in self.check_cols)
        else:
            return None

    def matchpnt_cols_to_str(self) -> str | None:
        if self.matchpnt_cols:
            return " ".join(f"{col + 1}" for col in self.matchpnt_cols)
        else:
            return None

    def print_bots_turn_msg(self) -> None:
            if self.matchpnt_cols:
                print(f"{messages.MATCHPNTS_IN} {self.matchpnt_cols_to_str()}")
                print(f"{messages.WILL_IT_NOTICE}  {messages.PRESS_ENTER}")
            if self.check_cols:
                print(f"{messages.BOT_TURN}")
                print(f"{messages.DANGER_IN} {self.check_cols_to_str()}")
                print(f"{messages.WILL_IT_NOTICE}  {messages.PRESS_ENTER}")
            else:
                print(f"{messages.BOT_TURN}  {messages.PRESS_ENTER}")
            input()

