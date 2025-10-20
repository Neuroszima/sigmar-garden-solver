from typing import Optional
from enum import Enum
from random import shuffle, randint


class SigmarMarble(Enum):
    salt = 0
    earth = 1
    fire = 2
    wind = 3
    water = 4
    lead = 16
    tin = 17
    iron = 18
    copper = 19
    silver = 20
    gold = 21
    quicksilver = 32
    mors = 64
    vitae = 65


class SigmarField:
    def __init__(self, marble: int | None, row_index: int, field_index: int,
                 neighbours: Optional[list["SigmarField"]] = None, board_edge_field = False):
        self.marble: int | None = marble
        self.row_index = row_index
        self.field_index = field_index
        self.left_up_neigh: Optional["SigmarField"] = None
        self.right_up_neigh: Optional["SigmarField"] = None
        self.right_neigh: Optional["SigmarField"] = None
        self.right_down_neigh: Optional["SigmarField"] = None
        self.left_down_neigh: Optional["SigmarField"] = None
        self.left_neigh: Optional["SigmarField"] = None
        if isinstance(neighbours, list):
            if all([isinstance(n, type(self)) for n in neighbours]):
                self.update_neighbours(neighbours)
            else:
                raise TypeError("One of the fields passed as neighbour is of invalid type.")
        self.free = False
        self.board_edge_field = board_edge_field

    def __eq__(self, other):
        """This only used for tests."""
        if isinstance(other, self.__class__):
            return (self.marble == other.marble) and (self.row_index == other.row_index) \
                and (self.field_index == other.field_index) and (self.board_edge_field == other.board_edge_field)
        else:
            return NotImplemented

    def update_neighbours(self, neighbours: Optional[list["SigmarField"]]):
        """Assign empty pointers to a real ones for each of the surrounding board fields"""
        self.left_up_neigh = neighbours[0]
        self.right_up_neigh = neighbours[1]
        self.right_neigh = neighbours[2]
        self.right_down_neigh = neighbours[3]
        self.left_down_neigh = neighbours[4]
        self.left_neigh = neighbours[5]

    def get_continuous_neigh_list(self):
        """
        Return a list of fields surrounding this one. Returns a list in counter-clockwise order.
        Returns a list starting from left upper adjacent field.
        """
        return [
            # list wraps up to reflect easier looping of three consecutive values
            self.left_up_neigh,
            self.right_up_neigh,
            self.right_neigh,
            self.right_down_neigh,
            self.left_down_neigh,
            self.left_neigh,
            self.left_up_neigh,
            self.right_up_neigh,
        ]

    def check_and_set_free_status(self, invoke_for_neighbours=True):
        """
        Check if the free status is valid for this board field/cell.
        A cell that is "free" means user is able to interact with it and match other marbles placed on it.
        """
        if self.board_edge_field:
            self.free = True
            return True
        i = 0
        j = 1
        k = 2
        n_list = self.get_continuous_neigh_list()
        if invoke_for_neighbours:
            for neigh in n_list[:6]:
                neigh.check_and_set_free_status(invoke_for_neighbours=False)
        for _ in range(6):
            if n_list[i].marble is None and n_list[j].marble is None and n_list[k].marble is None:
                self.free = True
                return True
            i += 1
            j += 1
            k += 1
        return False

    def update_field(self, marble: int | None):
        """
        Invoke this to recalculate free status when needed, and also
        after an action of taking the marble off this field.
        """
        self.marble = marble
        self.check_and_set_free_status()

    @property
    def enclosed_status(self):
        """Check if all the neighbouring fields are occupied by marbles."""
        counter = 0
        for neigh in self.get_continuous_neigh_list()[:6]:
            if neigh.marble is not None:
                counter += 1
        return counter == 6


class SmallSigmarBoard:
    """
    Small Sigmar Garden board used for application tests.
    Real board is 11-wide map in the diameter, and has more sparse element placement compared to this one
    """
    sigmar_text_encoding = {
        0: "0",  # salt
        1: "e",  # earth
        2: "f",  # fire
        3: "~",  # wind
        4: "w",  # water
        16: "l",  # lead
        17: "t",  # tin
        18: "i",  # iron
        19: "c",  # copper
        20: "s",  # silver
        21: "g",  # gold
        32: "q",  # quicksilver
        64: "m",  # mors
        65: "v",  # vitae
        None: "_"  # empty field
    }

    def __init__(self):
        self.first_element = SigmarMarble.gold
        self.initial_items = [
            (SigmarMarble.quicksilver, SigmarMarble.silver), (SigmarMarble.quicksilver, SigmarMarble.copper),
            (SigmarMarble.earth, SigmarMarble.earth), (SigmarMarble.fire, SigmarMarble.fire),
            (SigmarMarble.wind, SigmarMarble.wind), (SigmarMarble.water, SigmarMarble.water),
            (SigmarMarble.mors, SigmarMarble.vitae), (SigmarMarble.salt, SigmarMarble.salt)
        ]
        self.layout: list[list[SigmarField]] | None = None
        self.init_board_rows()
        self.compose_board_interconnections()
        self.layout_midpoint = 3, 4

    @staticmethod
    def __rand_select_marble_by_index(marble_list_: list):
        if len(marble_list_) < 1:
            raise RuntimeError("Passed list is empty when it should not be.")
        elif len(marble_list_) == 1:
            return 0
        else:
            return randint(0, len(marble_list_)-1)

    def init_board_rows(self):
        # small board only has limited amount of fields compared to the regular layout which has plenty
        # board rows are explained below. the "n" fields will not be seen by "player" or "solver" as it
        # is if there was a solid board edge.
        #  6 -> 7 -> 8 - 9 -> 8 -> 7 -> 6
        #       n - n - n - n - n - n
        #     n - e - e - e - e - e - n
        #   n - e - e - e - e - e - e - n
        # n - e - e - e - e - e - e - e - n
        #   n - e - e - e - e - e - e - n
        #     n - e - e - e - e - e - n
        #       n - n - n - n - n - n
        sizes = [6, 7, 8, 9, 8, 7, 6]
        self.layout: list[list[SigmarField]] = [
            [SigmarField(None, row_idx, field_idx) for field_idx in range(size)]
            for row_idx, size in enumerate(sizes)
        ]
        for field in self.layout[0]:
            field.board_edge_field = True
        for field in self.layout[-1]:
            field.board_edge_field = True
        for layer in self.layout[1:-1]:
            layer[0].board_edge_field = True
            layer[-1].board_edge_field = True

    def compose_board_interconnections(self):
        field: SigmarField
        for row_idx, board_row in enumerate(self.layout[1:4]):
            for field_idx, field in enumerate(board_row[1:-1]):
                field.left_up_neigh = self.layout[row_idx][field_idx]
                field.right_up_neigh = self.layout[row_idx][field_idx+1]
                field.left_neigh = board_row[field_idx]
                field.right_neigh = board_row[field_idx+2]
                if row_idx + 1 < 3:
                    field.left_down_neigh = self.layout[row_idx+2][field_idx+1]
                    field.right_down_neigh = self.layout[row_idx+2][field_idx+2]
                else:
                    field.left_down_neigh = self.layout[row_idx+2][field_idx]
                    field.right_down_neigh = self.layout[row_idx+2][field_idx+1]
        for row_idx, board_row in enumerate(self.layout[4:-1]):
            for field_idx, field in enumerate(board_row[1:-1]):
                field.left_up_neigh = self.layout[3+row_idx][field_idx+1]
                field.right_up_neigh = self.layout[3+row_idx][field_idx+2]
                field.left_neigh = board_row[field_idx]
                field.right_neigh = board_row[field_idx+2]
                field.left_down_neigh = self.layout[3+row_idx+2][field_idx]
                field.right_down_neigh = self.layout[3+row_idx+2][field_idx+1]
        for board_row in self.layout[1:-1]:
            for field in board_row[1:-1]:
                field.check_and_set_free_status()

    def reset_board(self):
        """Return board to empty state for a new game/test."""


    def lay_down_marbles_in_wavefront(self):
        """
        Since original Sigmar Garden game starts from the middle and the first middle element is always the "Gold"
        marble, place it in the middle of the layout. Also, start placing other pairs of marbles, moving out from
        center to the edges, randomly picking the neighbour of the wavefront to propagate outwards.

        Partially tested
        """
        # mid_row = len(self.layout)//2+1
        # mid_element = len(self.layout[mid_row])//2+1
        self.layout[self.layout_midpoint[0]][self.layout_midpoint[1]].update_field(self.first_element.value)
        eligible_wavefront_elements = [self.layout[self.layout_midpoint[0]][self.layout_midpoint[1]]]
        shuffle(self.initial_items)
        for pair in self.initial_items:
            marble: Enum
            for marble in pair:
                success = False
                randomized_wavefront_indexes = [*range(len(eligible_wavefront_elements))]
                # search through available space to place the marble. Do it for each eligible field in the
                for wavefront_sigfield_index in randomized_wavefront_indexes:
                    wavefront_sigmar_field: SigmarField = eligible_wavefront_elements[wavefront_sigfield_index]
                    randomized_neighbours = wavefront_sigmar_field.get_continuous_neigh_list()[:6]
                    shuffle(randomized_neighbours)
                    for neigh in randomized_neighbours:
                        if neigh.marble is None and neigh.free and not neigh.board_edge_field:
                            neigh.update_field(marble.value)  # "value" is a property not a regular method
                            success = True
                        if success:
                            if wavefront_sigmar_field.enclosed_status:
                                eligible_wavefront_elements.pop(wavefront_sigfield_index)
                            eligible_wavefront_elements.append(neigh)
                            break
                    if success:  # on success, break from both loops and pick another marble to place
                        break
                if not success:
                    raise RuntimeError(f"Could not find proper field for {marble=}, aborting.")

    def print_board(self):
        mid_row_idx = len(self.layout)//2-1
        space_count = mid_row_idx*2 + 2
        print(" " * (space_count-2), "/-"+"---"*(len(self.layout[1])-2)+"-\\")
        for idx, row in enumerate(self.layout[1:-1]):
            if idx < mid_row_idx:
                row_txt = " " * (space_count-2) + "/ "
                space_count -= 2
            elif idx == mid_row_idx:
                row_txt = " " * (space_count-1) + "<"
                space_count += 2
            else:
                row_txt = " " * (space_count-2) + "\\ "
                space_count += 2
            field: SigmarField
            row_txt += " - ".join([f"{self.sigmar_text_encoding[field.marble]}" for field in row[1:-1]])
            if idx < mid_row_idx:
                row_txt += " \\"
            elif idx == mid_row_idx:
                row_txt += ">"
            else:
                row_txt += " /"
            print(row_txt)
        print(" " * (space_count-4), "\\-"+"---"*(len(self.layout[1])-2)+"-/")


if __name__ == '__main__':
    smol_board = SmallSigmarBoard()
    smol_board.print_board()
    smol_board.lay_down_marbles_in_wavefront()
    smol_board.print_board()
