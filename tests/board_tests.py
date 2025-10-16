from typing import Literal
from unittest import TestCase

from normal_solver.board import SmallSigmarBoard, SigmarMarble, SigmarField


class BoardTest(TestCase):
    def setUp(self):
        self.mini_board = SmallSigmarBoard()

    def assertReciprocity(
        self, field_to_check: Literal[0, 1, 2, 3, 4, 5],
        original_field_reference: SigmarField, reciprocal_field_reference: SigmarField,
        err_field: str
    ):
        """
        Check, if for each possible pair of neighbouring pairs, both fields do see each other in
        layout fields. If not, trigger AssertionError.

        Reciprocity test checks if, by taking any field instance of the board from any particular row,
        by taking for example the "left-upper" connection of hexagonal layout, the instance of the pointed
        gamefield also has an instance of the "pointee" -> in our example if "right-down" instance field of
        has original gamefield as a pointer. Thus, we check if neighbouring gamefields see each other in each
        respective instance, having pointers set to each other correctly.
        """
        err_msg = f"reciprocity assertion failed at {err_field}, {field_to_check=}"
        field: SigmarField = original_field_reference
        if field_to_check == 0:
            if not field.left_up_neigh.board_edge_field:
                self.assertIs(field.left_up_neigh, reciprocal_field_reference, err_msg)
                self.assertIs(reciprocal_field_reference.right_down_neigh, field, err_msg)
        elif field_to_check == 1:
            if not field.right_up_neigh.board_edge_field:
                self.assertIs(field.right_up_neigh, reciprocal_field_reference, err_msg)
                self.assertIs(reciprocal_field_reference.left_down_neigh, field, err_msg)
        elif field_to_check == 2:
            if not field.right_neigh.board_edge_field:
                self.assertIs(field.right_neigh, reciprocal_field_reference, err_msg)
                self.assertIs(reciprocal_field_reference.left_neigh, field, err_msg)
        elif field_to_check == 3:
            if not field.right_down_neigh.board_edge_field:
                self.assertIs(field.right_down_neigh, reciprocal_field_reference, err_msg)
                self.assertIs(reciprocal_field_reference.left_up_neigh, field, err_msg)
        elif field_to_check == 4:
            if not field.left_down_neigh.board_edge_field:
                self.assertIs(field.left_down_neigh, reciprocal_field_reference, err_msg)
                self.assertIs(reciprocal_field_reference.right_up_neigh, field, err_msg)
        elif field_to_check == 5:
            if not field.left_neigh.board_edge_field:
                self.assertIs(field.left_neigh, reciprocal_field_reference, err_msg)
                self.assertIs(reciprocal_field_reference.right_neigh, field, err_msg)

    def test_layout(self):
        for row_idx, row in enumerate(self.mini_board.layout):
            for field_idx, field in enumerate(row):
                self.assertIsInstance(field, SigmarField)
                self.assertIsNone(field.marble)

    def test_board_adjecent_field_check(self):
        for row_idx, row in enumerate(self.mini_board.layout):
            for field_idx, field in enumerate(row):
                if field.board_edge_field:
                    continue
                field: SigmarField
                err_field = f"{row_idx=} {field_idx=}"
                self.assertReciprocity(0, field, field.left_up_neigh, err_field)
                self.assertReciprocity(1, field, field.right_up_neigh, err_field)
                self.assertReciprocity(2, field, field.right_neigh, err_field)
                self.assertReciprocity(3, field, field.right_down_neigh, err_field)
                self.assertReciprocity(4, field, field.left_down_neigh, err_field)
                self.assertReciprocity(5, field, field.left_neigh, err_field)
