from core.game import Game
import core.messages as msgs
import core.constants as const
import os
from core.constants import FIELD_HEIGHT as HEIGHT
from core.constants import FIELD_WIDTH as WIDTH
from core.player import Player
from enums.col_select import Col_Select
from utils import random

class Board:
    def __init__(self):
        self.matrix = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def print_board(self) -> None:
        for row in self.matrix:
            print("".join(f"[{cell}]" for cell in row))
        self.print_footer()

    def print_footer(self) -> None:
        print("".join("-" for _ in range(const.UNDERLINE_LEN)))
        print("".join(f" {i} " for i in range(1, const.FIELD_WIDTH + 1)))
        print("\n")

    def check_for_win_hori(self, game: Game, player1: Player) -> None:
        symbol = game.active_player.token_symbol
        for row in range(const.BOTTOM_ROW, -1, const.GO_UP):
            for col in range(const.FIELD_WIDTH - 2):
                if not self.has_3_hori(row, col, symbol):
                    continue
                if self.is_check_hori_left(row, col):
                    game.mark_col_as_check_or_matchpnt(col - 1, player1, symbol)
                if col >= const.FIELD_WIDTH - 3:
                    continue
                right_4th_is_symbol = self.matrix[row][col + 3] == symbol
                if right_4th_is_symbol:
                    print(f"{game.active_player.name} {msgs.HAS_WON}")
                    game.game_won = True
                    return
                if self.is_check_hori_right(row, col):
                    game.mark_col_as_check_or_matchpnt(col + 3, player1, symbol)

    def has_3_hori(self, row: int, col: int, symbol: str) -> bool:
        return all(self.matrix[row][col + i] == symbol for i in range(3))

    def is_check_hori_right(self, row: int, col: int) -> bool:
        fourth_on_right_is_empty = self.matrix[row][col + 3] == " "
        below_4th_is_filled = (row == const.BOTTOM_ROW
                               or self.matrix[row + 1][col + 3] != " ")
        return fourth_on_right_is_empty and below_4th_is_filled

    def is_check_hori_left(self, row: int, col: int) -> bool:
        fourth_on_left_is_empty = self.matrix[row][col - 1] == " "
        below_4th_is_filled = (row == const.BOTTOM_ROW
                               or self.matrix[row + 1][col - 1] != " ")
        return fourth_on_left_is_empty and below_4th_is_filled

    def place_token(self, col: int, game: Game) -> None:
        if col == Col_Select.QUIT_GAME:
            return
        for row in range(const.BOTTOM_ROW, -1, const.GO_UP):
            if self.cell_is_empty(row, col):
                self.matrix[row][col] = game.active_player.token_symbol
                game.tokens_in_cols[col] += 1
                game.moves_left -= 1
                return

    def cell_is_empty(self, row: int, col: int) -> bool:
        return self.matrix[row][col] == " "

    def check_for_win_vert(self, game: Game, player1: Player) -> None:
        symbol = game.active_player.token_symbol
        for row in range(const.BOTTOM_ROW, const.THIRD_FROM_TOP, const.GO_UP):
            for col in range(const.FIELD_WIDTH):
                if not self.has_3_vert(row, col, symbol):
                    continue
                if self.matrix[row - 3][col] == symbol:
                    print(f"{game.active_player.name} {msgs.HAS_WON}")
                    game.game_won = True
                    return
                if self.vert_4th_empty(row, col):
                    game.mark_col_as_check_or_matchpnt(col, player1, symbol)

    def has_3_vert(self, row: int, col: int, symbol: str) -> bool:
        return all(self.matrix[row - i][col] == symbol for i in range(3))

    def vert_4th_empty(self, row: int, col: int) -> bool:
        return self.matrix[row - 3][col] == " "

    def check_for_win_diagonal_nw_to_se(self, game: Game, player1: Player) -> None:
        symbol = game.active_player.token_symbol
        for row in range(const.FIELD_HEIGHT - 2):
            for col in range(const.FIELD_WIDTH - 2):

                if not self.has_3_diagonal_nw_to_se(row, col, symbol):
                    continue

                nw_4th_is_empty = self.matrix[row - 1][col - 1] == ' '
                below_nw_4th_filled = self.matrix[row][col - 1] != ' '
                if row > 0 and col > 0 and nw_4th_is_empty and below_nw_4th_filled:
                    game.mark_col_as_check_or_matchpnt(col - 1, player1, symbol)

                enough_se_space_for_4 = (row < const.FIELD_HEIGHT - 3
                                         and col < const.FIELD_WIDTH - 3)
                if not enough_se_space_for_4:
                    continue

                if self.matrix[row + 3][col + 3] == symbol:
                    print(f"{game.active_player.name} {msgs.HAS_WON}")
                    game.game_won = True
                    return

                se_4th_is_empty = self.matrix[row + 3][col + 3] == ' '
                below_se_4th_filled = (row + 3 == const.BOTTOM_ROW
                                       or self.matrix[row + 4][col + 3] != ' ')
                if se_4th_is_empty and below_se_4th_filled:
                    game.mark_col_as_check_or_matchpnt(col + 3, player1, symbol)

    def has_3_diagonal_nw_to_se(self, row: int, col: int, symbol: str) -> bool:
        return all(self.matrix[row + i][col + i] == symbol for i in range(3))

    def check_for_win_diagonal_sw_to_ne(self, game: Game, player1: Player) -> None:
        symbol = game.active_player.token_symbol
        for row in range(const.BOTTOM_ROW, const.THIRD_FROM_TOP, const.GO_UP):
            for col in range(const.SECOND_FROM_RIGHT):

                if not self.has_3_diagonal_sw_to_ne(row, col, symbol):
                    continue

                enough_ne_space_for_4th = col < 4 and row > 2 # Magic numbers.
                if not enough_ne_space_for_4th:
                    continue

                ne_4th_is_symbol = self.matrix[row - 3][col + 3] == symbol
                if ne_4th_is_symbol:
                    print(f"{game.active_player.name} {msgs.HAS_WON}") 
                    game.game_won = True
                    return

                ne_4th_is_empty = self.matrix[row - 3][col + 3] == " "
                below_ne_4th_filled = self.matrix[row - 2][col + 3] != " "
                if ne_4th_is_empty and below_ne_4th_filled:
                    game.mark_col_as_check_or_matchpnt(col + 3, player1, symbol)

                sw_cell_exists = row < const.BOTTOM_ROW and col > 0
                if not sw_cell_exists:
                    continue

                sw_4th_is_empty = self.matrix[row + 1][col - 1] == " "
                below_sw_4th_filled = (row == const.ROW_ABOVE_BOTTOM_ROW
                                       or self.matrix[row + 2][col - 1] != " ")
                if sw_4th_is_empty and below_sw_4th_filled:
                    game.mark_col_as_check_or_matchpnt(col - 1, player1, symbol)

    def has_3_diagonal_sw_to_ne(self, row: int, col: int, symbol: str) -> bool:
        return all(self.matrix[row - i][col + i] == symbol for i in range(3))

    def check_for_win(self, game: Game, player1: Player) -> None:
        self.check_for_win_hori(game, player1)
        self.check_for_win_vert(game, player1)
        self.check_for_win_diagonal_nw_to_se(game, player1)
        self.check_for_win_diagonal_sw_to_ne(game, player1)

    def check_for_win_vs_bot(self, game: Game, player1: Player) -> bool:
        game.reset_matchpnt_cols()
        self.check_for_win(game, player1)
        if not game.game_won:
            return False
        self.wipe_screen()
        print(f"{game.active_player.name} {msgs.HAS_WON}")
        return True

    def wipe_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        self.print_board()

    def is_col_full(self, game: Game, col: int) -> bool:
        return False if game.tokens_in_cols[col] < const.FIELD_HEIGHT else True

    def first_move_col(self) -> int:
        if self.matrix[const.BOTTOM_ROW][const.MIDDLE_COL] == ' ':
            return const.MIDDLE_COL
        if random.coin_toss():
            return const.MIDDLE_COL - 1
        return const.MIDDLE_COL + 1

    def is_win_or_tie(self, game: Game, player1: Player) -> bool:
        return True if self.check_for_win_vs_bot(game, player1) or game.is_tie() else False
