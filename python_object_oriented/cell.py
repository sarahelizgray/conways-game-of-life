# author Sarah Gray

class Cell:
    """Cell makes a cell object which contains the size of the board, the liveness of the
    cell, the cell\'s coordinates, the coordinates of this cell\'s neighbors, the number
    of live neighbors of this cell, and if this cell was alive in the last round."""

    def __init__(self, my_coords, board_size):
        self.BOARD_SIZE = board_size
        self.alive = True
        self.my_coords = my_coords
        self.num_live_neighbors = 0
        self.set_of_neighbor_coords = self.find_neighbors_coords(my_coords)
        self.alive_last_round = False

    def kill(self):
        """Sets the cell\'s alive state to False."""

        self.alive = False

    def resurrect(self):
        """Sets the cell\'s alive state to True."""

        self.alive = True

    def is_alive(self):
        """Returns the liveness of the cell."""

        return self.alive

    def set_alive_last_round(self):
        """Given a boolean_value, sets the cell\'s alive_last_round_value to True."""

        self.alive_last_round = True

    def get_alive_last_round(self):
        """Tells whether or not the cell was alive in the last round."""

        return self.alive_last_round

    def find_neighbors_coords(self, my_coords):
        """Returns a list of coordinates for all legal neighbors of the cell."""

        neighbors = set()
        for row in range(my_coords[0] - 1, my_coords[0] + 2):
            for column in range(my_coords[1] - 1, my_coords[1] + 2):
                if row >= 0 and row <= self.BOARD_SIZE - 1 and column >= 0 and column <= self.BOARD_SIZE - 1:
                    neighbors.add((row,column))
        neighbors.remove(my_coords)
        return neighbors

    def set_live_neighbor_count(self, set_of_live_cells):
        """Sets the cell\'s number of live neighbors."""

        live_neighbors = set_of_live_cells.intersection(self.set_of_neighbor_coords)
        self.num_live_neighbors = len(live_neighbors)

    def get_live_neighbor_count(self):
        """Gets the cell\'s live neighbor count."""

        return self.num_live_neighbors

    def get_set_of_neighbor_coords(self):
        """Returns the set of neighbors for this cell."""

        return self.set_of_neighbor_coords

    def get_cell_coords(self):
        """Returns the cell\'s coordinates."""

        return self.my_coords



