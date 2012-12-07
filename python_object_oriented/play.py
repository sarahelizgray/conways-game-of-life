#author Sarah Gray

import board

print "Welcome to Conway\'s Game of Life"
print
print "With each generation, the following rules will be applied:"
print
print "If a dead cell was alive in the last round, it will be alive in the next generation"
print "If a live cell has less than 2 neighbors -- it dies of loneliness" 
print "If a live cell has exactly 2 neighbors -- it is alive in the next generation"
print "If any cell, alive or dead, has exactly 3 neighbors -- it is alive in the next generation"
print "If a live cell has more than 3 neighbors -- it dies of over crowding" 
print
print "Let's play!"
print
#select the baord size
board_size = 0
while board_size < 1 or board_size > 25 or type(board_size) != int:
    board_size = input("Please enter a board size, between 1 and 25:")
    
#select number of generations
generations = 0
print
while generations < 1 or generations >10 or type(generations) != int:
    generations = input("Please enter the number of generations, between 1 and 10:")
    
#get the live cell placement
print
print "Please enter the coordinates of the live cells, enter -1 to quit entering cells"
set_of_live_cell_coords = set()
ok_to_run = True
while ok_to_run:
    print
    x = -1
    while x < 0 or x > board_size - 1 or type(x) != int:
        x = input("Please enter an x coordinate:")
        if x == -1:
            ok_to_run = False
            break
    y = -1 
    while y < 0 or y > board_size - 1 or type(y) != int:
        y = input("Please enter a y coordinate:")
        if y == -1:
            okay_to_run = False
            break
            
    set_of_live_cell_coords.add((x,y))

my_board = board.Board(board_size, set_of_live_cell_coords)
my_board.evolve(my_board.array, generations)