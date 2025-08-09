from core import constants, errors
from core.board import Board
from core.game import Game
from enums.col_select import Col_Select
from utils import random

def prompt_player_for_move(game: Game, board: Board) -> int:
    while True:
        selected_col = game.active_player.get_col_from_player()
        if selected_col == Col_Select.QUIT_GAME:
            game.quit = True
            return selected_col
        is_valid_col_num = constants.FIELD_WIDTH > selected_col > -1
        if not is_valid_col_num:
            print(errors.INVALID_COL)
            continue
        if board.is_col_full(game, selected_col):
            print(errors.COL_FULL)
            continue
        return selected_col

def select_col_for_bot(game, board: Board) -> int:
    if game.matchpnt_cols:
        return game.matchpnt_cols[0] 
    if game.check_cols:
        selected_col = game.check_cols[0]
        game.reset_check_cols()
        return selected_col
    while True:
        selected_col = random.get_rand_col()
        if not board.is_col_full(game, selected_col):
            return selected_col

def bot_make_move(game, board: Board) -> None:
    if game.first_move:
        board.place_token(board.first_move_col(), game)
        game.first_move = False
    else:
        board.place_token(select_col_for_bot(game, board), game)
