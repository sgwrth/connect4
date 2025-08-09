from core import errors, messages
import core.constants as const
from enums.col_select import Col_Select
from enums.game_mode import Game_Mode
from utils.random import get_rand_col

class Game:
    def __init__(self, active_player, game_mode):
        self.active_player = active_player
        self.game_mode = game_mode
        self.game_won = False
        self.first_move = True
        self.check_cols = []
        self.matchpnt_cols = []
        self.tokens_in_cols = [0, 0, 0, 0, 0, 0 ,0]
        self.moves_left = const.MAX_MOVES
        self.quit = False

    def mark_col_as_check_or_matchpnt(self, col, player1, symbol):
        if symbol == player1.token_symbol:
            self.check_cols.append(col)
        else:
            self.matchpnt_cols.append(col)

    def toggle_active_player(self, player1, player2):
        self.active_player = player1 if self.active_player == player2 else player2

    def reset_check_cols(self):
        for i in range(len(self.check_cols) - 1, -1, -1):
            self.check_cols.pop(i)

    def reset_matchpnt_cols(self):
        for i in range(len(self.matchpnt_cols) - 1, -1, -1):
            self.matchpnt_cols.pop(i)

    def prompt_player_for_move(self, board):
        while True:
            selected_col = self.active_player.get_col_from_player()
            if selected_col == Col_Select.QUIT_GAME:
                self.quit = True
                return selected_col
            is_valid_col_num = const.FIELD_WIDTH > selected_col > -1
            if not is_valid_col_num:
                print(errors.INVALID_COL)
                continue
            if board.is_col_full(self, selected_col):
                print(errors.COL_FULL)
                continue
            return selected_col

    def is_tie(self):
        if 1 > self.moves_left:
            print(messages.TIE_GAME)
            return True
        else:
            return False

    def is_win_or_tie(self, board, player1):
        return True if board.check_for_win_vs_bot(self, player1) or self.is_tie() else False

    def select_col_for_bot(self, board):
        if self.matchpnt_cols:
            return self.matchpnt_cols[0] 
        if self.check_cols:
            selected_col = self.check_cols[0]
            self.reset_check_cols()
            return selected_col
        while True:
            selected_col = get_rand_col()
            if not board.is_col_full(self, selected_col):
                return selected_col

    @staticmethod
    def select_game_mode():
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
            
    def check_cols_to_str(self):
        if self.check_cols:
            return " ".join(f"{col + 1}" for col in self.check_cols)

    def matchpnt_cols_to_str(self):
        if self.matchpnt_cols:
            return " ".join(f"{col + 1}" for col in self.matchpnt_cols)

    def print_bots_turn_msg(self):
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

    def bot_make_move(self, board):
        if self.first_move:
            board.place_token(board.first_move_col(), self)
            self.first_move = False
        else:
            board.place_token(self.select_col_for_bot(board), self)
