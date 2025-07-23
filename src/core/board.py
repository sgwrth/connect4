import core.messages as msgs
import core.constants as const
from core.constants import FIELD_HEIGHT as HEIGHT
from core.constants import FIELD_WIDTH as WIDTH

class Board:
    def __init__(self):
        self.matrix = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def print_board(self):
        for row in self.matrix:
            print("".join(f"[{cell}]" for cell in row))
        self.print_footer()

    def print_footer(self):
        print("".join("-" for _ in range(const.UNDERLINE_LEN)))
        print("".join(f" {i} " for i in range(1, const.FIELD_WIDTH + 1)))
        print("\n")

    def check_for_win_hori(self, game, player1):
        symbol = game.active_player.token_symbol
        for row in range(const.BOTTOM_ROW, -1, const.GO_UP):
            for col in range(const.FIELD_WIDTH - 2):
                if not self.has_3_hori(row, col, symbol):
                    continue
                if self.is_check_hori_left(row, col, symbol):
                    game.mark_col_as_check_or_matchpnt(col - 1, player1, symbol)
                if col >= const.FIELD_WIDTH - 3:
                    continue
                right_4th_is_symbol = self.matrix[row][col + 3] == symbol
                if right_4th_is_symbol:
                        print(f"{game.active_player.name} {msgs.HAS_WON}")
                        game.game_won = True
                        return
                if self.is_check_hori_right(row, col, symbol):
                    game.mark_col_as_check_or_matchpnt(col + 3, player1, symbol)

    def has_3_hori(self, row, col, symbol):
        return all(self.matrix[row][col + i] == symbol for i in range(3))

    def is_check_hori_right(self, row, col, symbol):
        fourth_on_right_is_empty = self.matrix[row][col + 3] == " "
        below_4th_is_filled = (row == const.BOTTOM_ROW
                               or self.matrix[row + 1][col + 3] != " ")
        return fourth_on_right_is_empty and below_4th_is_filled

    def is_check_hori_left(self, row, col, symbol):
        fourth_on_left_is_empty = self.matrix[row][col - 1] == " "
        below_4th_is_filled = (row == const.BOTTOM_ROW
                               or self.matrix[row + 1][col - 1] != " ")
        return fourth_on_left_is_empty and below_4th_is_filled
