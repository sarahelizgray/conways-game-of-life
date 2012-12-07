#author Sarah Gray

import cell

class Board:
    """Board makes a board object which contains a board size and an array of
    cell objects. The board class contains methods for evolving the array based
    on Conway's rules."""
                
    def __init__(self, array_size, set_of_live_cell_coords):
        self.BOARD_SIZE = array_size
        live_cell_coords = self.remove_illegal_coords(set_of_live_cell_coords)
        set_of_live_cells = self.convert_coords_to_cells(live_cell_coords)
        array = self.make_array()
        self.place_cells_on_array(set_of_live_cells, array)
        #self.array only to be used for testing
        self.array = self.update_live_neighbor_count(set_of_live_cells, array)
        
        
    def print_array(self, array):
        """Prints the array to the console."""
        
        spacing = " " * 2
        for row in range(self.BOARD_SIZE):
            value_collector = ""
            for column in range(self.BOARD_SIZE):
                if array[row][column].is_alive():
                    cell = 'x'
                else:
                    cell = '.'
                value_collector = value_collector + cell + spacing
            print value_collector

    def remove_illegal_coords(self, set_of_points):
        """Removes duplicate and invalid points for cells 
        based on array size. Returns corrected set of cells."""
        
        good_points = set()
        for (x, y) in set_of_points:
            if x >= 0 and x <= self.BOARD_SIZE - 1 and y >= 0 and y <= self.BOARD_SIZE - 1:
                good_points.add((x,y))      
        return good_points  
        
    def convert_coords_to_cells(self, set_of_live_cell_coords):
        """Given a set of coordinate tuples, returns a set of 
        cell objects containing those coordinates."""
        
        set_of_live_cells = set()
        for (row,column) in set_of_live_cell_coords:
            new_cell = cell.Cell((row,column), self.BOARD_SIZE)
            set_of_live_cells.add(new_cell)
        return set_of_live_cells    
    
    def convert_cells_to_coords(self, set_of_cells):
        """Given a set of cell objects, returns a set of tuples 
        representing the cell\'s coordinates."""
        
        set_of_cell_coords = set()
        for cell in set_of_cells:
            set_of_cell_coords.add(cell.get_cell_coords())
        return set_of_cell_coords
        
    def update_live_neighbor_count(self, set_of_live_cells, array):
        """Uses the set of live cells to update the live_neighbor_count 
        on the array. Returns updated array."""
        
        #get all coords of neighbors of live cells
        all_neighbor_coords = set()
        for cell in set_of_live_cells:
            all_neighbor_coords = all_neighbor_coords.union(cell.get_set_of_neighbor_coords())
            
        #get the coords of all the live cells
        set_of_live_cell_coords = self.convert_cells_to_coords(set_of_live_cells)
        
        #combine live cells with their neighbors
        all_coords_to_update = set_of_live_cell_coords.union(all_neighbor_coords)

        #now update the neighbor count on the array for the live cells and their neighbors 
        for (x,y) in all_coords_to_update:
            array[x][y].set_live_neighbor_count(set_of_live_cell_coords)
        
        return array
        
    def place_cells_on_array(self, set_of_cells, array):
        """Places cells on array based on the coordinates 
        contained in each cell. Returns array with cells."""
        
        for cell in set_of_cells:
            (x,y) = cell.get_cell_coords()
            array[x][y] = cell
        return array                


    def make_array(self):
        """Returns a container array of size array_size x array_size 
        containing only dead cells."""
        
        new_array = [] 
        
        for row in range(self.BOARD_SIZE):
            new_row = []
            for column in range(self.BOARD_SIZE):
                    new_cell = cell.Cell((row,column), self.BOARD_SIZE)
                    new_cell.kill()
                    new_row.append(new_cell)
            new_array.append(new_row)

        return new_array


    def apply_rules (self, array):
        """Creates a new array and set of live cells for next generation based on current 
        array. Returns new array representing the next generation and the list of live 
        cells present in the new array. """
        
        new_live_cell_set = set()
        temp_array = self.make_array()
        
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                neighbor_count = array[row][column].get_live_neighbor_count()
                
                #die of over-crowding
                if neighbor_count > 3 and array[row][column].is_alive():
                    temp_array[row][column].kill()
                    temp_array[row][column].set_alive_last_round()
                
                #grow
                if neighbor_count == 3:
                    temp_array[row][column].resurrect()
                    new_live_cell_set.add((row,column))
                
                #just right, so get to live on in next round
                elif neighbor_count == 2 and array[row][column].is_alive():
                    temp_array[row][column].resurrect()
                    new_live_cell_set.add((row,column))
                
                #die of loneliness
                elif neighbor_count < 2 and array[row][column].is_alive():
                    temp_array[row][column].kill()
                    temp_array[row][column].set_alive_last_round()
                
                #resurrect if alive last round
                elif array[row][column].get_alive_last_round():
                    temp_array[row][column].resurrect()
                    new_live_cell_set.add((row,column))     
        return (new_live_cell_set, temp_array)
        
        
    def evolve(self, array, generations):
        """"Evaluates the array according to Conway\'s rules generation number of times. 
        Print the evaluated array to the console after each generation."""

        print
        print ("_____Generation_____")
        self.print_array(array)
        

        if generations == 1:
            return array
            

        else:
            (set_of_live_cell_coords, temp_array) = self.apply_rules(array)
            set_of_live_cells = self.convert_coords_to_cells(set_of_live_cell_coords)
            temp_array = self.update_live_neighbor_count(set_of_live_cells, temp_array)
            return self.evolve(temp_array, generations - 1)