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
        small_game = SmallSigmarGame("small")
        small_board_layout_sizes = [6, 7, 8, 9, 8, 7, 6]
        for expected_size, row in zip(small_board_layout_sizes, self.small_game.board.layout):
            self.assertEqual(expected_size, len(row))
            for field in row:
                self.assertIsInstance(field, SigmarField)

        self.assertIsNone(self.small_game.eligible_fields)
        self.assertEqual(SigmarMarble.lead.value, self.small_game.next_metal_to_clear)

