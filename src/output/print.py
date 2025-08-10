import core.errors as errors
from core import messages as msgs
from core.game import Game
from core.player import Player

def welcome() -> None:
    print(f"{msgs.LETS_PLAY_CONNECT4}")

def prompt_player1_for_name() -> None:
    print(f"{msgs.PROMPT_PLAYER_1_FOR_NAME}")
    print(msgs.ENTER_NAME, end = "")

def prompt_player2_for_name() -> None:
    print(f"{msgs.PROMPT_PLAYER_2_FOR_NAME}")
    print(msgs.ENTER_NAME, end = "")

def wish_luck(player: Player) -> None:
    print(f"{msgs.WELCOME}, {player.name}!  {msgs.GOOD_LUCK}\n")

def thanks_for_playing() -> None:
    print(f"{msgs.THANKS_FOR_PLAYING}")

def play_vs_bot():
    print(f"{msgs.PLAY_VS_BOT}")
    input() # A 'Press any key to continue' type situation.

def player_has_won(game: Game) -> None:
    print(f"{game.active_player.name} {msgs.HAS_WON}")

def tie_game() -> None:
    print(msgs.TIE_GAME)

def choose_mode() -> None:
    print(msgs.CHOOSE_MODE, end = "")

def illegal_input() -> None:
    print(errors.ILLEGAL_INPUT)

def will_bot_notice_matchpnts(game: Game) -> None:
    print(f"{msgs.MATCHPNTS_IN} {game.matchpnt_cols_to_str()}")
    print(f"{msgs.WILL_IT_NOTICE}  {msgs.PRESS_ENTER}")

def will_bot_notice_danger(game: Game) -> None:
    print(f"{msgs.BOT_TURN}")
    print(f"{msgs.DANGER_IN} {game.check_cols_to_str()}")
    print(f"{msgs.WILL_IT_NOTICE}  {msgs.PRESS_ENTER}")

def bots_turn() -> None:
    print(f"{msgs.BOT_TURN}  {msgs.PRESS_ENTER}")

def prompt_player_for_move(player: Player) -> None:
    print(player.name + msgs.PROMPT_PLAYER_FOR_MOVE, end = "")