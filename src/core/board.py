import os
import core.constants as const
import output.print as prnt
from core.constants import FIELD_HEIGHT as HEIGHT
from core.constants import FIELD_WIDTH as WIDTH
from core.game import Game
from core.player import Player
from enums.col_select import Col_Select
from utils import random

class Board:
    def __init__(self, matrix=None):
        if not matrix:
            self.matrix = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
        else:
            self.matrix = matrix

    def print_board(self) -> None:
        [[print("".join(f"[{cell}]" for cell in row))] for row in self.matrix]
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
                    prnt.player_has_won(game)
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
        not_col_1 = col > 0
        fourth_on_left_is_empty = self.matrix[row][col - 1] == " "
        below_4th_is_filled = (row == const.BOTTOM_ROW
                               or self.matrix[row + 1][col - 1] != " ")
        return not_col_1 and fourth_on_left_is_empty and below_4th_is_filled

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
                    prnt.player_has_won(game)
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
                if self.nw_4th_is_empty_and_ready(row, col):
                    game.mark_col_as_check_or_matchpnt(col - 1, player1, symbol)
                if not self.enough_se_space_for_4th(row, col):
                    continue
                if self.matrix[row + 3][col + 3] == symbol:
                    prnt.player_has_won(game)
                    game.game_won = True
                    return
                if self.se_4th_is_empty_and_ready(row, col):
                    game.mark_col_as_check_or_matchpnt(col + 3, player1, symbol)

    def nw_4th_is_empty_and_ready(self, row: int, col: int) -> bool:
        nw_4th_is_empty = self.matrix[row - 1][col - 1] == ' '
        below_nw_4th_filled = self.matrix[row][col - 1] != ' '
        return row > 0 and col > 0 and nw_4th_is_empty and below_nw_4th_filled

    def enough_se_space_for_4th(self, row: int, col: int) -> bool:
        return row < const.FIELD_HEIGHT - 3 and col < const.FIELD_WIDTH - 3

    def se_4th_is_empty_and_ready(self, row: int, col: int) -> bool:
        se_4th_is_empty = self.matrix[row + 3][col + 3] == ' '
        below_se_4th_filled = (row + 3 == const.BOTTOM_ROW
                               or self.matrix[row + 4][col + 3] != ' ')
        return se_4th_is_empty and below_se_4th_filled

    def has_3_diagonal_nw_to_se(self, row: int, col: int, symbol: str) -> bool:
        return all(self.matrix[row + i][col + i] == symbol for i in range(3))

    def check_for_win_diagonal_sw_to_ne(self, game: Game, player1: Player) -> None:
        symbol = game.active_player.token_symbol
        for row in range(const.BOTTOM_ROW, const.THIRD_FROM_TOP, const.GO_UP):
            for col in range(const.SECOND_FROM_RIGHT):
                if not self.has_3_diagonal_sw_to_ne(row, col, symbol):
                    continue
                if not self.enough_ne_space_for_4th(row, col):
                    continue
                if self.ne_to_sw_win(row, col, symbol):
                    prnt.player_has_won(game)
                    game.game_won = True
                    return
                if self.ne_4th_empty_and_ready(row, col):
                    game.mark_col_as_check_or_matchpnt(col + 3, player1, symbol)
                if not self.sw_cell_exists(row, col):
                    continue
                if self.sw_4th_empty_and_ready(row, col):
                    game.mark_col_as_check_or_matchpnt(col - 1, player1, symbol)

    def enough_ne_space_for_4th(self, row: int, col: int) -> bool:
        return col < 4 and row > 2 # Magic numbers.

    def ne_to_sw_win(self, row, col, symbol: str) -> None:
        return self.matrix[row - 3][col + 3] == symbol

    def ne_4th_empty_and_ready(self, row: int, col: int) -> bool:
        ne_4th_is_empty = self.matrix[row - 3][col + 3] == " "
        below_ne_4th_filled = self.matrix[row - 2][col + 3] != " "
        return ne_4th_is_empty and below_ne_4th_filled

    def sw_cell_exists(self, row: int, col: int) -> bool:
        return row < const.BOTTOM_ROW and col > 0

    def sw_4th_empty_and_ready(self, row: int, col: int) -> bool:
        sw_4th_is_empty = self.matrix[row + 1][col - 1] == " "
        below_sw_4th_filled = (row == const.ROW_ABOVE_BOTTOM_ROW
                               or self.matrix[row + 2][col - 1] != " ")
        return sw_4th_is_empty and below_sw_4th_filled

    def has_3_diagonal_sw_to_ne(self, row: int, col: int, symbol: str) -> bool:
        return all(self.matrix[row - i][col + i] == symbol for i in range(3))

    def check_for_win(self, game: Game, player: Player) -> None:
        self.check_for_win_hori(game, player)
        self.check_for_win_vert(game, player)
        self.check_for_win_diagonal_nw_to_se(game, player)
        self.check_for_win_diagonal_sw_to_ne(game, player)

    def check_for_win_vs_bot(self, game: Game, player: Player) -> bool:
        game.reset_matchpnt_cols()
        self.check_for_win(game, player)
        if not game.game_won:
            return False
        self.wipe_screen()
        prnt.player_has_won(game)
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
