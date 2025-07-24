import core.constants as const

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


