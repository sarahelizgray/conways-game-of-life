#author Sarah Gray

import cell
import unittest

class test_cell(unittest.TestCase):

    def setUp(self):
        self.testing_cell = cell.Cell((0,0), 5)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_init(self):
        self.assertTrue(self.testing_cell.is_alive())
        self.assertEqual((0,0), self.testing_cell.get_cell_coords())
        self.assertEqual(0, self.testing_cell.get_live_neighbor_count())
        self.assertEqual(set([(0,1), (1,0), (1,1)]), self.testing_cell.get_set_of_neighbor_coords())
        self.assertFalse(False, self.testing_cell.get_alive_last_round())

    def test_kill_and_resurrect(self):
        self.testing_cell.kill()
        self.assertFalse(self.testing_cell.is_alive())
        self.testing_cell.resurrect()
        self.assertTrue(self.testing_cell.is_alive())

    def test_get_and_set_alive_last_round(self):
        self.assertFalse(self.testing_cell.get_alive_last_round())
        self.testing_cell.set_alive_last_round()
        self.assertTrue(self.testing_cell.get_alive_last_round())

    def test_get_set_neighbors_coords(self):
        #top left corner on a 5x5 grid
        top_left = cell.Cell((0,0), 5)
        self.assertEqual(set([(0,1), (1,0), (1,1)]), top_left.get_set_of_neighbor_coords())

        #top right corner on a 5x5 grid
        top_right = cell.Cell((0,4), 5)
        self.assertEqual(set([(0,3), (1,3), (1,4)]), top_right.get_set_of_neighbor_coords())

        #bottom left corner on a 5x5 grid
        bottom_left = cell.Cell((4,0), 5)
        self.assertEqual(set([(4,1), (3,0), (3,1)]), bottom_left.get_set_of_neighbor_coords())

        #bottom right corner on a 5x5 grid
        bottom_right = cell.Cell((4,4), 5)
        self.assertEqual(set([(4,3), (3,4), (3,3)]), bottom_right.get_set_of_neighbor_coords())

        #center on a 5x5 grid
        center = cell.Cell((2,2), 5)
        self.assertEqual(set([(1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3)]), center.get_set_of_neighbor_coords())


    def test_get_and_set_live_neighbor_count(self):
        #using one valid neighbor
        self.testing_cell.set_live_neighbor_count(set([(0,1)]))
        self.assertEqual(1, self.testing_cell.get_live_neighbor_count())

        #using two valid neighbors
        self.testing_cell.set_live_neighbor_count(set([(0,1), (1,0)]))
        self.assertEqual(2, self.testing_cell.get_live_neighbor_count())

        #using three valid neighbors
        self.testing_cell.set_live_neighbor_count(set([(0,1), (1,0), (1,1)]))
        self.assertEqual(3, self.testing_cell.get_live_neighbor_count())

        #using two valid neighbors and two invalid neighbors
        self.testing_cell.set_live_neighbor_count(set([(0,1), (1,1), (4,4), (3,2)]))
        self.assertEqual(2, self.testing_cell.get_live_neighbor_count())

        #using one valid neighbor,two invalid neighbors and cell's location
        self.testing_cell.set_live_neighbor_count(set([(0,0), (1,1), (4,4), (3,2)]))
        self.assertEqual(1, self.testing_cell.get_live_neighbor_count())


if __name__ == '__main__':
    unittest.main()
