#author Sarah Gray

import board
import unittest

class test_board(unittest.TestCase):

    def setUp(self):
        self.BOARD_SIZE = 5
        self.test_set_of_coords = set([(1,1), (0,0), (0,1), (4,4), (3,2)])
        self.test_array_object = board.Board(self.BOARD_SIZE, self.test_set_of_coords)
        self.test_array = self.test_array_object.array

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_init(self):
        set_of_live_cell_coords = set()
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if self.test_array[row][column].is_alive():
                    set_of_live_cell_coords.add(self.test_array[row][column].get_cell_coords())
        self.assertEqual(set_of_live_cell_coords, self.test_set_of_coords)

    def test_remove_illegal_coords(self):
        new_set_of_coords = set([(4,4), (3,3), (5,5), (-1,-1), (-1,0), (-1,5), (-1,4), (5, 1)])
        legal_coords = self.test_array_object.remove_illegal_coords(new_set_of_coords)
        self.assertEqual(set([(4,4), (3,3)]), legal_coords)

    def test_convert_coords_to_cells(self):
        set_of_cells = self.test_array_object.convert_coords_to_cells(self.test_set_of_coords)
        set_of_live_cell_coords = set()
        for cell in set_of_cells:
            set_of_live_cell_coords.add(cell.get_cell_coords())
        self.assertEqual(self.test_set_of_coords, set_of_live_cell_coords)

    def test_convert_cells_to_coords(self):
        set_of_cells = self.test_array_object.convert_coords_to_cells(self.test_set_of_coords)
        set_of_live_cell_coords = self.test_array_object.convert_cells_to_coords(set_of_cells)
        self.assertEqual(self.test_set_of_coords, set_of_live_cell_coords)

    def test_update_live_neighbor_count(self):
        cell_coords = set([(2,2), (0,0), (1,0)])
        blank_array = self.test_array_object.make_array()
        one_cell = self.test_array_object.convert_coords_to_cells(cell_coords)
        populated_array = self.test_array_object.place_cells_on_array(one_cell, blank_array)
        updated_array = self.test_array_object.update_live_neighbor_count(one_cell, populated_array)
        expected_result = [[1,2,0,0,0], [1,3,1,1,0], [1,2,0,1,0], [0,1,1,1,0], [0,0,0,0,0]]
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                self.assertEqual(expected_result[row][column], updated_array[row][column].get_live_neighbor_count())

    def test_place_cells_on_array(self):
        cell_coords = set([(2,2)])
        blank_array = self.test_array_object.make_array()
        one_cell = self.test_array_object.convert_coords_to_cells(cell_coords)
        populated_array = self.test_array_object.place_cells_on_array(one_cell, blank_array)
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if populated_array[row][column].is_alive():
                    self.assertEqual(row, 2)
                    self.assertEqual(column,2)

    def test_make_array(self):
        blank_array = self.test_array_object.make_array()
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                self.assertFalse(blank_array[row][column].is_alive())

    def test_apply_rules_die_of_loneliness(self):
        cell_coords = set([(2,2)])
        blank_array = self.test_array_object.make_array()
        one_cell_set = self.test_array_object.convert_coords_to_cells(cell_coords)
        populated_array = self.test_array_object.place_cells_on_array(one_cell_set, blank_array)
        (new_live_cell_set, new_array) = self.test_array_object.apply_rules(populated_array)
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                self.assertFalse(new_array[row][column].is_alive())
        self.assertEqual(set([]), new_live_cell_set)

    def test_apply_rules_resurrect_if_alive_last_round(self):
        cell_coords = set([(2,2)])
        blank_array = self.test_array_object.make_array()
        one_cell_set = self.test_array_object.convert_coords_to_cells(cell_coords)
        for cell in one_cell_set:
            cell.kill()
            cell.set_alive_last_round()
        populated_array = self.test_array_object.place_cells_on_array(one_cell_set, blank_array)
        (new_live_cell_set, new_array) = self.test_array_object.apply_rules(populated_array)
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if new_array[row][column].is_alive():
                    self.assertEqual(row, 2)
                    self.assertEqual(column,2)

    def test_apply_rules_just_right_live(self):
        cell_coords = set([(2,0), (3,0), (2,1)])
        blank_array = self.test_array_object.make_array()
        cell_set = self.test_array_object.convert_coords_to_cells(cell_coords)
        populated_array = self.test_array_object.place_cells_on_array(cell_set, blank_array)
        updated_array = self.test_array_object.update_live_neighbor_count(cell_set, populated_array)
        (new_live_cell_coords, new_array) = self.test_array_object.apply_rules(populated_array)
        self.assertTrue(new_array[2][0].is_alive())
        self.assertTrue(new_array[3][0].is_alive())
        self.assertTrue(new_array[2][1].is_alive())

    def test_apply_rules_grow_based_on_neighbor_count(self):
        cell_coords = set([(2,0), (3,0), (2,1)])
        blank_array = self.test_array_object.make_array()
        cell_set = self.test_array_object.convert_coords_to_cells(cell_coords)
        populated_array = self.test_array_object.place_cells_on_array(cell_set, blank_array)
        updated_array = self.test_array_object.update_live_neighbor_count(cell_set, populated_array)
        (new_live_cell_set, new_array) = self.test_array_object.apply_rules(populated_array)
        self.assertTrue(new_array[3][1].is_alive())

    def test_apply_rules_grow_whole_board(self):
        cell_coords = set([(2,2), (2,1), (2,0), (1,2), (1,1)])
        expected_result_coords = set([(1,0), (2,0), (1,2), (2,2), (3,1)])
        blank_array = self.test_array_object.make_array()
        cell_set = self.test_array_object.convert_coords_to_cells(cell_coords)
        populated_array = self.test_array_object.place_cells_on_array(cell_set, blank_array)
        updated_array = self.test_array_object.update_live_neighbor_count(cell_set, populated_array)
        (new_live_cell_coords, new_array) = self.test_array_object.apply_rules(populated_array)
        self.assertEqual(new_live_cell_coords,expected_result_coords)

    def test_evolve_one_generation(self):
        array = self.test_array
        result_array = self.test_array_object.evolve(array, 1)
        self.assertEqual(array, result_array)

    def test_evolve_two_generations(self):
        array = self.test_array
        result_array = self.test_array_object.evolve(array, 2)
        expected_cell_coords = set([(1,0), (0,0), (1,1),(0,1)])
        result_coords = set()
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if result_array[row][column].is_alive():
                    result_coords.add(result_array[row][column].get_cell_coords())
        self.assertEqual(result_coords, expected_cell_coords)

    def test_evolve_three_generations(self):
         array = self.test_array
         result_array = self.test_array_object.evolve(array, 3)
         expected_cell_coords = set([(0,0), (0,1), (1,1), (1,0), (3,2), (4,4)])
         result_coords = set()
         for row in range(self.BOARD_SIZE):
             for column in range(self.BOARD_SIZE):
                 if result_array[row][column].is_alive():
                     result_coords.add(result_array[row][column].get_cell_coords())
         self.assertEqual(result_coords, expected_cell_coords)


if __name__ == '__main__':
    unittest.main()



#unittest.main()