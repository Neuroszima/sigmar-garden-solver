from typing import Literal

from board import SigmarField, SmallSigmarBoard


class SmallSigmarGame:

    def __init__(self, board_type: Literal["small", "normal"]):
        if board_type == "small":
            self.board = SmallSigmarBoard()
            self.board.lay_down_marbles_in_wavefront()
        else:
            raise ValueError("No other type of initialization is possible. Use: 'small'")
        self.eligible_moves: list | None = None

    def get_eligible_moves(self):
        self.eligible_moves = []
        for row in self.board.layout[1:-1]:
            for field in row[1:-1]:
                if field.free and field.marble is not None:
                    self.eligible_moves.append(field)
