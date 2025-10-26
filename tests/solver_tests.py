from random import randint, choice, choices, seed
from string import ascii_letters
from typing import Literal
from unittest import TestCase

from normal_solver.board import SmallSigmarBoard, SigmarMarble, SigmarField
from normal_solver.solver import SmallSigmarGame


class SmallSigmarGameTest(TestCase):
    def setUp(self):
        seed(19)
        self.small_game = SmallSigmarGame()

    def test_game_init(self):
        small_board_layout_sizes = [6, 7, 8, 9, 8, 7, 6]
        for expected_size, row in zip(small_board_layout_sizes, self.small_game.board.layout):
            self.assertEqual(expected_size, len(row))
            for field in row:
                self.assertIsInstance(field, SigmarField)

        self.assertIsNone(self.small_game.eligible_fields)
        self.assertEqual(SigmarMarble.lead.value, self.small_game.next_metal_to_clear)

    def test_marble_matching(self):
        """
        For each pair of good or bad marble combinations that would or would not match (respectively), check
        if the function to match marbles works correctly, according to game rules.
        Do that for regular numeric values as well.
        """
        good_pairs = [
            (SigmarMarble.water, SigmarMarble.water), (SigmarMarble.fire, SigmarMarble.fire),
            (SigmarMarble.earth, SigmarMarble.earth), (SigmarMarble.wind, SigmarMarble.wind),
            (SigmarMarble.salt, SigmarMarble.salt), (SigmarMarble.salt, SigmarMarble.water),
            (SigmarMarble.salt, SigmarMarble.wind), (SigmarMarble.salt, SigmarMarble.fire),
            (SigmarMarble.salt, SigmarMarble.earth), (SigmarMarble.vitae, SigmarMarble.mors)
        ]
        good_pairs = good_pairs + [(pair[0].value, pair[1].value) for pair in good_pairs]
        bad_pairs = [
            (SigmarMarble.water, SigmarMarble.earth), (SigmarMarble.quicksilver, SigmarMarble.earth),
            (SigmarMarble.vitae, SigmarMarble.fire), (SigmarMarble.salt, SigmarMarble.vitae),
            (SigmarMarble.silver, SigmarMarble.earth), (SigmarMarble.silver, SigmarMarble.water)
        ]
        bad_pairs = bad_pairs + [(pair[0].value, pair[1].value) for pair in bad_pairs]

        for pair in good_pairs:
            msg = f"Not true for pair {pair[0]} {pair[1]}"
            self.assertTrue(self.small_game.test_eligible_move(*pair), msg)
        for pair in bad_pairs:
            msg = f"Not false for pair {pair[0]} {pair[1]}"
            self.assertFalse(self.small_game.test_eligible_move(*pair), msg)

    def test_possible_marbles_set(self):
        """
        Test if board has marbles actually correctly set as free or not free (by neighbourhood rules), and also
        if solver picks upon that layout and chooses correct
        """
        free_coords_for_seed_19 = {(1, 2), (1, 4), (2, 5), (3, 2), (4, 2), (4, 5), (5, 3), (5, 4)}
        for row in self.small_game.board.layout[1:-1]:
            for field in row[1:-1]:
                if field.marble is not None:
                    msg = f"{field}" + " is {}free "
                    if tuple([field.row_index, field.field_index]) in free_coords_for_seed_19:
                        print(field)
                        self.assertTrue(field.free, msg.format("not ") + "when it should be")
                    else:
                        self.assertFalse(field.free, msg.format("") + "when it should not be")
        self.small_game.set_eligible_fields()
        self.assertEqual(len(free_coords_for_seed_19), len(self.small_game.eligible_fields))
        for field in self.small_game.eligible_fields:
            field: SigmarField
            correct_element_position: tuple[int, int] = tuple([field.row_index, field.field_index])  # noqa
            if correct_element_position in free_coords_for_seed_19:
                free_coords_for_seed_19.remove(correct_element_position)  # remove raises errors when something is wrong
        self.assertEqual(0, len(free_coords_for_seed_19))

    def test_possible_moves_set(self):
        """
        Check if only necessary moves are present in the list of all possible moves.
        There should be no duplicates (like permutations of pairs that represent the same pair on the board), as
        well as there should be no cases of metal-quicksilver pairs that are only available later (for example
        copper-quicksilver that is "free", but the next metal to clear is lead, and not copper).
        """
        self.small_game.print_board()
        eligible_moves_for_seed_19 = {
            ((2, 5), (5, 3),),  # mors-vitae pair
            ((1, 4), (4, 2),),  # wind-wind pair
            ((1, 4), (3, 2),),  # wind-salt pair
            ((3, 2), (4, 2),),  # wind-salt pair
        }

        self.small_game.set_eligible_fields()
        self.small_game.set_eligible_moves()
        self.assertEqual(len(eligible_moves_for_seed_19), len(self.small_game.eligible_moves))
        for fields_pair in self.small_game.eligible_moves:
            fields_pair: tuple[SigmarField, SigmarField]
            field_coords_1 = tuple([
                tuple([fields_pair[0].row_index, fields_pair[0].field_index]),
                tuple([fields_pair[1].row_index, fields_pair[1].field_index]),
            ])
            field_coords_2 = tuple([
                tuple([fields_pair[1].row_index, fields_pair[1].field_index]),
                tuple([fields_pair[0].row_index, fields_pair[0].field_index]),
            ])
            if field_coords_1 in eligible_moves_for_seed_19:
                eligible_moves_for_seed_19.remove(field_coords_1)  # noqa
            elif field_coords_2 in eligible_moves_for_seed_19:
                eligible_moves_for_seed_19.remove(field_coords_2)  # noqa
            else:
                raise AssertionError(
                    "Field configuration should not be present as a possible move in collection of available moves.")
        # after loop all cases should be cleared
        self.assertEqual(0, eligible_moves_for_seed_19)


if __name__ == '__main__':
    from unittest import main

    main()
