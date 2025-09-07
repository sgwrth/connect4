import random
from core import constants

def get_rand_col():
    return random.randint(0, (constants.FIELD_WIDTH - 1))

def coin_toss():
    return random.randint(0, 1) == 0
