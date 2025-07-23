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
