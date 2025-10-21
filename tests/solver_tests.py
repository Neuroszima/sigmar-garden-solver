from random import randint, choice, choices
from string import ascii_letters
from typing import Literal
from unittest import TestCase

from normal_solver.board import SmallSigmarBoard, SigmarMarble, SigmarField
from normal_solver.solver import SmallSigmarGame


class SmallSigmarGameTest(TestCase):
    def setUp(self):
        self.small_game = SmallSigmarGame("small")

    def test_game_init(self):
        rand_gametype = "".join(choices(ascii_letters, k=randint(10, 15)))
        with self.assertRaises(ValueError):
            SmallSigmarGame(rand_gametype)
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


if __name__ == '__main__':
    from unittest import main
    main()
