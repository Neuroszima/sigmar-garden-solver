from enum import Enum
from typing import Literal

from normal_solver.board import SigmarMarble, SigmarField, SmallSigmarBoard


class SmallSigmarGame:
    """Untested class"""
    allowed_combinations = {
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (2, 2), (3, 3), (4, 4),
        (16, 32), (17, 32), (18, 32), (19, 32), (20, 32), (64, 65)
    }
    QUICKSILVER = SigmarMarble.quicksilver.value

    def __init__(self, board_type: Literal["small", "normal"]):
        if board_type == "small":
            self.board = SmallSigmarBoard()
            self.board.lay_down_marbles_in_wavefront()
        else:
            raise ValueError("No other type of initialization is possible. Use: 'small'")
        self.eligible_fields: list | None = None
        self.next_metal_to_clear: int = SigmarMarble.lead.value

    def set_eligible_fields(self):
        self.eligible_fields = []
        for row in self.board.layout[1:-1]:
            for field in row[1:-1]:
                if field.free and field.marble is not None:
                    self.eligible_fields.append(field)

    @staticmethod
    def __convert_to_int(marble: Enum | SigmarMarble | int) -> int:
        if isinstance(marble, int):
            return marble
        elif isinstance(marble, SigmarMarble):
            return marble.value
        elif isinstance(marble, Enum):
            return marble.value
        raise ValueError(f"Improper type of value, is: {marble.__class__}, needs to be int|Enum|SigmarMarble")

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

        # allowed combination
        if tuple([marble_type_1, marble_type_2]) in self.allowed_combinations \
            or tuple([marble_type_2, marble_type_1]) in self.allowed_combinations:
            # metal-quicksilver combination
            if marble_type_1 == self.QUICKSILVER:
                if marble_type_2 == self.next_metal_to_clear:
                    return True
                return False
            elif marble_type_2 == self.QUICKSILVER:
                if marble_type_1 == self.next_metal_to_clear:
                    return True
                return False
        return False