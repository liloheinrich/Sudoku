# Sudoku
DPLL SAT solver applied to Sudoku

To run, use `python sudoku.py "filename.txt"`

`filename` is the name of a text file containing a sudoku puzzle, in the following format:
- The first line is the size of the puzzle. For example, if it is 9 x 9 squares then the size is 3 (the square root of 9).
- The second line is the clue dictionary, in this format: 
    - {(row,col): val, (row2,col2): val2, ...}
    - Note: start the row and column indexing at 1

Eight example puzzles are provided. Warning: puzzles 3 and 5 take a very long/undetermined amount of time to run since they are the most difficult.
