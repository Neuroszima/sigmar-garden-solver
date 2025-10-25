from enum import Enum
from typing import Literal
from itertools import product

from normal_solver.board import SigmarMarble, SigmarField, SmallSigmarBoard


class SmallSigmarGame:
    """Untested class"""
    allowed_combinations = {
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (2, 2), (3, 3), (4, 4),
        (16, 32), (17, 32), (18, 32), (19, 32), (20, 32), (64, 65)
    }
    base_marbles = {0, 1, 2, 3, 4}
    QUICKSILVER = SigmarMarble.quicksilver.value

    def __init__(self):
        self.board = SmallSigmarBoard()
        self.board.lay_down_marbles_in_wavefront()
        self.eligible_fields: list | None = None
        self.eligible_moves: list | None = None
        self.next_metal_to_clear: int = SigmarMarble.lead.value
        self.winning_strategy: list[list] | None = None

    def set_eligible_fields(self):
        self.eligible_fields = []
        for row in self.board.layout[1:-1]:
            for field in row[1:-1]:
                if field.free and field.marble is not None:
                    self.eligible_fields.append(field)

    def set_eligible_moves(self):
        self.eligible_moves = []
        if len(self.eligible_fields) > 0:
            f = [f for f in self.eligible_fields if f.marble != SigmarMarble.gold.value]
            pairs_to_check = product(f, f)
            pair: tuple[SigmarField, SigmarField]
            for pair in pairs_to_check:
                if self.test_eligible_move(pair[0].marble, pair[1].marble):
                    self.eligible_moves.append(pair)

    @staticmethod
    def __convert_to_int(marble: Enum | SigmarMarble | int) -> int:
        if isinstance(marble, int):
            return marble
        elif isinstance(marble, SigmarMarble):
            return marble.value
        elif isinstance(marble, Enum):
            return marble.value
        raise ValueError(f"Improper type of value, is: {marble.__class__}, needs to be int|Enum|SigmarMarble")

    def __increment_metal_to_clear(self):
        """Progressively increment the metal value that should be cleared next"""
        if self.next_metal_to_clear is not None:
            if self.next_metal_to_clear < SigmarMarble.gold.value:
                self.next_metal_to_clear += 1
            else:
                self.next_metal_to_clear = None

    def __decrement_metal_to_clear(self):
        if self.next_metal_to_clear is not None:
            if self.next_metal_to_clear > SigmarMarble.lead.value:
                self.next_metal_to_clear -= 1
        else:
            self.next_metal_to_clear = SigmarMarble.gold.value

    def test_eligible_move(self, marble_1, marble_2) -> bool:
        """
        Tests if two of the chosen marbles from selected fields are eligible for matching and removing from the board.

        Matching rules go as follows:
        1. Earth, Air, Fire, Water (elemental) marbles can only be matched with Salt or its own type.
        2. Salt can only be matched with any element and itself.
        3. Metals can be matched with Quicksilver. However, there needs to be proper order of clearing the board:
            3.1 First metal to clear is Lead, with single unit of Quicksilver.
            3.2 Second metal to clear is Tin, with single unit of Quicksilver.
            3.3 Third metal to clear is Iron, with single unit of Quicksilver.
            3.4 Fourth metal to clear is Copper, with single unit of Quicksilver.
            3.5 Fifth metal to clear is Silver, with single unit of Quicksilver.
            3.6 Lastly, you can remove a free Gold marble, without the use of Quicksilver.
        4. Vitae and Mors can only be paired with the opposite marble
            (only Mors with Vitae, not Mors with Mors, nor Vitae with Vitae)
        :param marble_1: Marble type from field on the board
        :param marble_2: Marble type from field on the board
        :return: True if match is possible, otherwise False.
        """
        marble_type_1 = self.__convert_to_int(marble_1)
        marble_type_2 = self.__convert_to_int(marble_2)

        # allowed combinations
        if (tuple([marble_type_1, marble_type_2]) in self.allowed_combinations) \
            or (tuple([marble_type_2, marble_type_1]) in self.allowed_combinations):
            if marble_type_1 in self.base_marbles:  # base element or salt
                if marble_type_1 != 0:
                    return (marble_type_2 == marble_type_1) or (marble_type_2 == 0)
                return marble_type_2 in self.base_marbles
            elif marble_type_2 in self.base_marbles:
                if marble_type_2 != 0:
                    return (marble_type_1 == marble_type_2) or (marble_type_1 == 0)
                return marble_type_1 in self.base_marbles
            if marble_type_1 == self.QUICKSILVER:  # metal/quicksilver
                if marble_type_2 == self.next_metal_to_clear:
                    return True
                return False
            elif marble_type_2 == self.QUICKSILVER:
                if marble_type_1 == self.next_metal_to_clear:
                    return True
                return False
            if marble_type_1 == 64:
                return marble_type_2 == 65
            elif marble_type_2 == 64:  # vitae/mors
                return marble_type_1 == 65
        return False

    def solve(self, moves_for_victory=9):
        if not self.board.initialized_to_play:
            raise RuntimeError("Board not initialized")

        self.winning_strategy = []
        i = 0
        while not (len(self.winning_strategy) == moves_for_victory) or (i > 140):
            self.set_eligible_fields()
            self.set_eligible_moves()

            i += 1
            break


if __name__ == '__main__':
    from random import seed
    seed(19)
    sigmar_game_smol = SmallSigmarGame()
    sigmar_game_smol.solve()
    sigmar_game_smol.board.print_board()

    print("proper fields:")
    for proper_field in sigmar_game_smol.eligible_fields:
        print(proper_field)
    print("proper moves:")
    for proper_move in sigmar_game_smol.eligible_moves:
        print("Field 1:", str(proper_move[0]))
        print("Field 2:", str(proper_move[1]))
