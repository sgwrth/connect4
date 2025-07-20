import constants as const

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
