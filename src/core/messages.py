import core.bot as bot
import core.constants as const

PROMPT_PLAYER_1_FOR_NAME = "Player 1, what is your name?"
PROMPT_PLAYER_2_FOR_NAME = "Player 2, what is your name?"
THANKS_FOR_PLAYING = "Thanks for playing!"
PROMPT_PLAYER_FOR_MOVE = (
        ", it's your move!\n"
        f"Enter the column no. for your token (or {const.KEY_TO_QUIT} to quit): "
        )
ENTER_NAME = "Enter name: "
WELCOME = "Welcome, "
GOOD_LUCK = "!  And good luck!"
LETS_PLAY_CONNECT4 = "Let's play Connect 4!"
HAS_WON = "has won!"
CHOOSE_MODE = "Select game mode (1 = vs. bot, 2 = two players): "
PRESS_ENTER = "Press ENTER to continue."
PLAY_VS_BOT = (
        f"You will play against Bot (v{bot.BOT_LEVEL})!  {PRESS_ENTER}"
        )
TIE_GAME = "Wow! It's a tie game!"
BOT_TURN = "It's Bot's turn now!"
MATCHPOINTS_IN = "Matchpoint(s) in "
WILL_IT_NOTICE = "\nWill it notice?  Let's see!"
DANGER_IN = "Danger in "
