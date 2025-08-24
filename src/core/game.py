from typing import Union
import core.constants as const
import output.print as prnt
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
            return
        self.matchpnt_cols.append(col)

    def toggle_active_player(self, player1: Player, player2: Player) -> None:
        self.active_player = player1 if self.active_player == player2 else player2

    def reset_check_cols(self) -> None:
        [self.check_cols.pop(i) for i in range((len(self.check_cols) - 1), -1, -1)]

    def reset_matchpnt_cols(self) -> None:
        [self.matchpnt_cols.pop(i)
            for i in range((len(self.matchpnt_cols) - 1), -1, -1)]


    def is_tie(self) -> bool:
        if 1 > self.moves_left:
            prnt.tie_game()
            return True
        return False

    @staticmethod
    def select_game_mode() -> int:
        game_mode = Game_Mode.NONE
        while True:
            prnt.choose_mode()
            try:
                game_mode = int(input())
            except:
                prnt.illegal_input()
                continue
            if game_mode == Game_Mode.VS_BOT or game_mode == Game_Mode.TWO_PLAYERS:
                return game_mode
            prnt.illegal_input()

    def check_cols_to_str(self) -> Union[str, None]:
        return (" ".join(f"{col + 1}"
            for col in self.check_cols) if self.check_cols else None)

    def matchpnt_cols_to_str(self) -> Union[str, None]:
        return (" ".join(f"{col + 1}"
            for col in self.matchpnt_cols) if self.matchpnt_cols else None)

    def print_bots_turn_msg(self) -> None:
            if self.matchpnt_cols:
                prnt.will_bot_notice_matchpnts(self)
            if self.check_cols:
                prnt.will_bot_notice_danger(self)
            else:
                prnt.bots_turn()

