#author Sarah Gray
#program version Python 2.7

Rules:
If a dead cell was alive in the last round, it will be alive in the next generation.
If a live cell has less than 2 neighbors, it dies of loneliness.
If a live cell has exactly 2 neighbors, it lives in the next generation.
If any cell, alive or dead, has exactly 3 neighbors -- it is alive in the next generation
If a live cell has more than 3 neighbors, it dies of over crowding.

To play:
Run the play.py file. This file is not intended to be a full-fledged interface for the program, just an easy way for a user to see how it works. 

Notes on writing the program:
I used sets extensively in this project. It was an easy way to remove duplicate values when looking at coordinates. Also, the set data structure allowed me to use union and intersection instead of nested for loops, giving me a Big-Omega advantage on certain methods. You can see these features being used for updating each cell's live neighbor count. 

Also, to minimize the number of n^2 sweeps of the array, I make notes on the live cells present in each new generation. This reduced the number of cells where I needed to update the neighbor count. 
  
