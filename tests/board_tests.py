from random import randint, choice
from typing import Literal
from unittest import TestCase

from normal_solver.board import SmallSigmarBoard, SigmarMarble, SigmarField


class SigmarFieldTests(TestCase):
    def setUp(self):
        self.randrow_idx = randint(2000, 4000)
        self.randfield_idx = randint(2000, 4000)
        self.random_marble = self.__get_rand_marble()
        self.test_marble = SigmarMarble(self.random_marble)
        self.test_field = SigmarField(
            self.test_marble.value, self.randrow_idx, self.randfield_idx)
        self.test_field_edge = SigmarField(
            self.test_marble.value, self.randrow_idx, self.randfield_idx, board_edge_field=True)

    def __get_rand_marble(self):
        return choice([0, 1, 2, 3, 4, 16, 17, 18, 19, 20, 21, 32, 64, 65])

    def test_init(self):
        """Test SigmarField class initialization path (basic)."""
        self.assertEqual(self.random_marble, self.test_marble.value)
        self.assertEqual(self.random_marble, self.test_field.marble)
        self.assertEqual(self.randrow_idx, self.test_field.row_index)
        self.assertEqual(self.randfield_idx, self.test_field.field_index)
        self.assertEqual(self.random_marble, self.test_field_edge.marble)
        self.assertEqual(self.randrow_idx, self.test_field_edge.row_index)
        self.assertEqual(self.randfield_idx, self.test_field_edge.field_index)
        self.assertTrue(self.test_field_edge.board_edge_field)
        self.assertFalse(self.test_field.board_edge_field)

    def test_update_neighbours(self):
        """
        Test neighbour updating for the SigmarField class. Test this during init as well as post-init
        through dedicated method.
        """
        other_fields_list = [SigmarField(
            self.__get_rand_marble(), randint(1, 1000), randint(1, 1000)
        ) for _ in range(6)]

        for i, attr_ in enumerate([
            "left_up_neigh", "right_up_neigh", "right_neigh",
            "right_down_neigh", "left_down_neigh", "left_neigh",
        ]):
            neighbouring_field_pointer = getattr(self.test_field, attr_)
            self.assertIsNone(neighbouring_field_pointer)

        self.test_field.update_neighbours(other_fields_list)

        for i, attr_ in enumerate([
            "left_up_neigh", "right_up_neigh", "right_neigh",
            "right_down_neigh", "left_down_neigh", "left_neigh",
        ]):
            neighbouring_field_pointer = getattr(self.test_field, attr_)
            self.assertEqual(other_fields_list[i], neighbouring_field_pointer)
            self.assertIs(other_fields_list[i], neighbouring_field_pointer)

        field_with_neigh_initialization = SigmarField(
            self.__get_rand_marble(), randint(1, 1000), randint(1, 1000),
            neighbours=other_fields_list,
        )

        for i, attr_ in enumerate([
            "left_up_neigh", "right_up_neigh", "right_neigh",
            "right_down_neigh", "left_down_neigh", "left_neigh",
        ]):
            neighbouring_field_pointer = getattr(field_with_neigh_initialization, attr_)
            self.assertEqual(other_fields_list[i], neighbouring_field_pointer)
            self.assertIs(other_fields_list[i], neighbouring_field_pointer)

    def test_check_and_set_free_status(self):
        """
        Test checking if marble placed on the given field will be marked correctly as "free to interact with"
        by the method or not.

        Example:

        Looking at the specific field present on the board, the layout could resemble something like this:

                u   u
                 \ /
              o - m - u
                 / \
                o   o

        Where, when looked at the field in the middle (denoted as "m" above), looking at hexagonal layout around,
        the field could be surrounded by other marbles. Considering layout above as "resembling hexagonal", and
        noting "u" cells that are "unoccupied" (not containing a marble), and "o" as "occupied" by a marble, we
        say that layout presents a case where marble is "free to interact with".

        It is said so because we can see that 3 of the surrounding fields form a consecutive block of unoccupied fields.
        A consecutive block would be an arrangement of fields that surrounds a given one, when for each consecutive
        field in it holds a relation of "unoccupied" or "occupied". The minimum number of spaces around the given field,
        for that field to be considered "free" is 3 and each field of a block must be unoccupied.

        Examples of layout arrangements, that middle field in it is NOT considered as free:

                 o   u          u   o          u   u          o   u
                  \ /            \ /            \ /            \ /
               u - m - u      o - m - u      o - m - o      u - m - u
                  / \            / \            / \            / \
                 u   o          o   o          o   o          o   o

        The property o "free" for a given field means that, when there is marble on it, a user can interact with this
        field and match other marbles with the one placed in a "free" field. In other words - it is "free to interact
        with" by the user.
        """
        # all fields are filled with random marbles
        other_fields_list = [SigmarField(
            self.__get_rand_marble(), randint(1, 1000), randint(1, 1000)
        ) for _ in range(6)]

        self.test_field.update_neighbours(other_fields_list)
        self.test_field.check_and_set_free_status(invoke_for_neighbours=False)  # invoke only for this cell/field
        self.assertFalse(self.test_field.free, "Field is free even if all neighbours are full.")

        # 3 neighbouring fields are emptied, setting an "arc/block of 3 unoccupied fields",
        # making test field selectable.
        start_idx = randint(0, 2)
        for i in range(3):
            other_fields_list[start_idx+i].marble = None

        self.test_field.check_and_set_free_status(invoke_for_neighbours=False)  # invoke only for this cell/field
        self.assertTrue(
            self.test_field.free,
            "Field is not free, even when there is an arc of empty cells neighbouring the main field."
        )

    def test_update_field(self):
        """
        The "visual explanation" of the setup for this test:

                o   o   o
                 \ / \ /
              o - o - o - o
                 / \ / \
                o   o   o

        This "micro board" serves as a setup for testing if correct "free" flagging is triggered when a field is
        updated. This arrangement is initialized as follows:
        1. Initialize the 3rd field of the second row with a marble, and make it "free", by having 3 neighbouring
            fields empty, and other 3 filled. The surrounding field are laid out in the hexagonal pattern, just
            like in real Sigmar Garden game.
        2. The 2nd field of the second row will serve as the blocked field, having 4 filled neighbouring fields, and
            only 2 upper fields, that are going to be initialized with it, will be free.

        During the test, the 3rd field from second row is updated as "None" -> emptying that field. Then the
        neighbouring "closed" field (2nd field from second row) should have 3 "consecutive" empty neighbours, being
        marked as "free" during the process.

        Test also partially checks if there is no sideeffect for "enclosed status" property for both of these fields.
        """
        # test init step 1.
        updated_field_neighbours = [
            SigmarField(None, randint(1, 1000), randint(1, 1000), board_edge_field=True)
            for _ in range(3)
        ] + [
            SigmarField(self.__get_rand_marble(), randint(1, 1000), randint(1, 1000), board_edge_field=True)
            for _ in range(3)
        ]
        self.test_field.update_neighbours(updated_field_neighbours)

        # test init step 2
        nonfree_field = updated_field_neighbours[-1]
        nonfree_field.board_edge_field = False
        enclosed_field_neighbours = [
            SigmarField(None, randint(1, 1000), randint(1, 1000), board_edge_field=True),
            updated_field_neighbours[1], self.test_field, updated_field_neighbours[-2],
            SigmarField(self.__get_rand_marble(), randint(1, 1000), randint(1, 1000), board_edge_field=True),
            SigmarField(self.__get_rand_marble(), randint(1, 1000), randint(1, 1000), board_edge_field=True),
        ]
        nonfree_field.update_neighbours(enclosed_field_neighbours)

        # test execution
        self.test_field.check_and_set_free_status()
        self.assertTrue(self.test_field.free)
        self.assertFalse(self.test_field.enclosed_status)
        nonfree_field.check_and_set_free_status()
        self.assertFalse(nonfree_field.free)
        self.assertFalse(nonfree_field.enclosed_status)

        self.test_field.update_field(None)
        self.assertIsNone(self.test_field.marble)
        self.assertTrue(self.test_field.free)
        self.assertTrue(nonfree_field.free)
        self.assertFalse(self.test_field.enclosed_status)
        self.assertFalse(nonfree_field.enclosed_status)


class BoardTest(TestCase):
    def setUp(self):
        self.mini_board = SmallSigmarBoard()

    @staticmethod
    def __rand_select_by_index(list_: list):
        if len(list_) < 1:
            raise RuntimeError("Passed list is empty when it should not be.")
        elif len(list_) == 1:
            return 0
        else:
            return randint(0, len(list_) - 1)

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
        game field also has an instance of the "pointee" -> in our example if "right-down" instance field of
        has original game field as a pointer. Thus, we check if neighbouring game fields see each other in each
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
        """Test layout initialization as empty mini-board"""
        borad_rows_length = [6, 7, 8, 9, 8, 7, 6]
        for row_idx, row in enumerate(self.mini_board.layout):
            self.assertEqual(borad_rows_length[row_idx], len(row))
            for field_idx, field in enumerate(row):
                self.assertIsInstance(field, SigmarField)
                self.assertIsNone(field.marble)

    def test_board_reset(self):
        self.mini_board.lay_down_marbles_in_wavefront()
        for row in self.mini_board.layout:
            for field in row:
                self.assertIsNone(field.marble)
                self.assertTrue(field.free)
                self.assertFalse(field.enclosed_status)

    def test_board_adjacent_field_check(self):
        """
        Test if, during initialization of board layout, each meaningful element (that is - the ones that do not
        act as an edge) see each other properly (have each other as neighbours in their respective object instances).

        This is crucial for "free" checks for the main game to function.
        """
        field: SigmarField
        for row_idx, row in enumerate(self.mini_board.layout):
            for field_idx, field in enumerate(row):
                if field.board_edge_field:
                    continue
                err_field = f"{row_idx=} {field_idx=}"
                self.assertReciprocity(0, field, field.left_up_neigh, err_field)
                self.assertReciprocity(1, field, field.right_up_neigh, err_field)
                self.assertReciprocity(2, field, field.right_neigh, err_field)
                self.assertReciprocity(3, field, field.right_down_neigh, err_field)
                self.assertReciprocity(4, field, field.left_down_neigh, err_field)
                self.assertReciprocity(5, field, field.left_neigh, err_field)
                self.assertTrue(field.free, f"Field that is not free: {err_field}")

    def test_board_wavefront_layout(self):
        """
        Test if the wavefront layout method works as intended.
        Test if marbles are not associated to fields on the edge and if all marbles are laid out.
        """
        field: SigmarField
        self.mini_board.lay_down_marbles_in_wavefront()
        elements_to_lay_down = [
            self.mini_board.first_element.value,
            *[pair[0].value for pair in self.mini_board.initial_items],
            *[pair[1].value for pair in self.mini_board.initial_items],
        ]

        elements_laid_down = []
        # we now check full layout, not only the main board fields. This means edges are checked for errors
        for row in self.mini_board.layout:
            for field in row:
                if field.marble is None:
                    continue
                else:
                    self.assertFalse(
                        field.board_edge_field,
                        "Marble placed on Sigmar Field that serves as board edge"
                    )
                    elements_laid_down.append(field.marble)
        elements_to_clear = len(elements_to_lay_down)
        while elements_to_clear > 0:
            elem_idx = self.__rand_select_by_index(elements_to_lay_down)
            marble_selected = elements_to_lay_down[elem_idx]
            for i in range(len(elements_laid_down)):
                if marble_selected == elements_laid_down[i]:
                    elements_laid_down.pop(i)
                    elements_to_lay_down.pop(elem_idx)
                    break
            elements_to_clear -= 1

        self.assertEqual(
            [], elements_laid_down,
            f"Not all elements have been laid down: {elements_laid_down}"
        )
        self.assertEqual(
            [], elements_to_lay_down,
            f"Not all elements have been laid down: {elements_laid_down}"
        )


if __name__ == '__main__':
    from unittest.main import main
    main()
