import copy
import dpll_solve
import sys
import os
import ast 

def clue_clauses(n, s, clues, clauses):
    """ Creates clauses to enforce the given sudoku clues. 
    
    inputs
        n: the size of the sudoku puzzle
        s: 3D array, maps each (row, col, val) combination to a unique integer identifier
        clues: dictionary of sudoku puzzle clues as (x,y)-locations mapped to z-values
        clauses: 2D array of clauses with literals represented by integers
    """

    # assigns the variable corresponding to each location + value to true, then
    # assigns the rest of the variables corresponding to that location to false
    for (x,y),z in clues.items():
        for i in range(n*n):
            if i == z-1:
                clauses.append([s[x-1][y-1][i]])
            else:
                clauses.append([-s[x-1][y-1][i]])

def filled_clauses(n, s, clauses):
    """ Creates clauses to ensure there is at least one number in each location. 

    inputs
        n: the size of the sudoku puzzle
        s: 3D array, maps each (row, col, val) combination to a unique integer identifier
        clauses: 2D array of clauses with literals represented by integers
    """

    # at least one value has to be true for each location to ensure the puzzle is filled out
    for x in range(n*n):
        for y in range(n*n):
            long_clause = []
            for z in range(n*n):
                long_clause.append(s[x][y][z])
            clauses.append(long_clause)

def rowcol_clauses(n, s, clauses):
    """ Creates clauses to ensure each number appears at most once in each row & column. 

    inputs
        n: the size of the sudoku puzzle
        s: 3D array, maps each (row, col, val) combination to a unique integer identifier
        clauses: 2D array of clauses with literals represented by integers
    """

    # if a value z shows up twice in column y, the clause will not be satisfied
    for x in range(n*n-1):
        for y in range(n*n):
            for z in range(n*n):
                for i in range(x+1,n*n):
                    clauses.append([-s[x][y][z], -s[i][y][z]])

    # if a value z shows up twice in row x, the clause will not be satisfied
    for x in range(n*n):
        for y in range(n*n-1):
            for z in range(n*n):
                for i in range(y+1,n*n):
                    clauses.append([-s[x][y][z], -s[x][i][z]])

def box_clauses(n, s, clauses):
    """ Creates clauses to ensure each number appears only once in each sub-grid. 

    inputs
        n: the size of the sudoku puzzle
        s: 3D array, maps each (row, col, val) combination to a unique integer identifier
        clauses: 2D array of clauses with literals represented by integers
    """

    # clauses that check values in the same row & box but in neighboring columns
    for x in range(n):
        for y in range(n):
            for z in range(n*n):
                for i in range(n):
                    for j in range(n):
                        for k in range(y+1, n):
                            clauses.append([-s[n*i+x][n*j+y][z], -s[n*i+x][n*j+k][z]])

    # clauses that check values in the same column & box but in neighboring rows, 
    # as well as values that are in the same box but in a different row & column
    for x in range(n):
        for y in range(n):
            for z in range(n*n):
                for i in range(n):
                    for j in range(n):
                        for k in range(x+1, n):
                            for l in range(n):
                                clauses.append([-s[n*i+x][n*j+y][z], -s[n*i+k][n*j+l][z]])

def read_puzzle():
    """ Reads in the sudoku puzzle information from the given file, handles errors.

    returns 
        n: the size of the sudoku puzzle
        clues: dictionary of sudoku puzzle clues as (x,y)-locations mapped to z-values
    """

    # check that they provided a filename, give detailed file spec
    arg_len = len(sys.argv)
    if arg_len == 1:
        print("Please provide the filename of a text file containing a sudoku puzzle, in the following format:")
        print("The first line is the size of the puzzle. For example, if it is 9 x 9 squares then the size is 3 (sqr root of 9).")
        print("The second line is the clue dictionary, in this format: {(row,col): val, (row2,col2): val2, ...}")
        print("Note: start the row and column indexing at 1.")
        exit(1)

    # check the file exists
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print("Invalid filename.")

    # read in the info and return it
    with open(filename) as f:
        first_line = f.readline()
        n = int(first_line)
        data = f.read() 
        clues = ast.literal_eval(data) 
        return n, clues

def print_puzzle(n, clues):
    """ Prints out the puzzle before it is solved. 

    inputs
        n: the size of the sudoku puzzle
        clues: dictionary of sudoku puzzle clues as (x,y)-locations mapped to z-values
    """
    for x in range(n*n):
        for y in range(n*n):
            if (x+1,y+1) in clues:
                print(clues[(x+1,y+1)], end=" ")
            else:
                print(" ", end=" ")
            if (y+1) % n == 0 and y+1 != n*n:
                    print("|", end=" ")
        if (x+1) % n == 0 and x+1 != n*n:
            print()
            for i in range(2*n*n+2*n-3):
                print("-", end="")
        print()
    print()

def solve_puzzle(n, s, clues, clauses):
    """ Creates the necessary clauses and runs the dpll solver.
    
    inputs
        n: the size of the sudoku puzzle
        s: 3D array, maps each (row, col, val) combination to a unique integer identifier
        clues: dictionary of sudoku puzzle clues as (x,y)-locations mapped to z-values
        clauses: 2D array of clauses with literals represented by integers
    
    returns
        sat: boolean that is true if the puzzle is satisfiable, false otherwise
        assm: dictionary of literals to their satisfying assignments
    """
    clue_clauses(n, s, clues, clauses)
    filled_clauses(n, s, clauses)
    rowcol_clauses(n, s, clauses)
    box_clauses(n, s, clauses)

    # solver returns boolean satisfiability and final variable assignments
    return dpll_solve.dpll(clauses)

def print_solution(n, s, assm):
    """ Prints the final puzzle solution using the assignments given by the dpll solver.
    
    inputs
        n: the size of the sudoku puzzle
        s: 3D array, maps each (row, col, val) combination to a unique integer identifier
        assm: dictionary of literal assignments

    returns
        sudoku_sol: dictionary of (x,y)-locations to z-values, a concise encoding of the puzzle solution
    """
    sudoku_sol = dict()
    for x in range(n*n):
        for y in range(n*n):
            for z in range(n*n):
                if assm[s[x][y][z]]:
                    print(z+1, end=" ")
                    sudoku_sol[(x+1,y+1)] = z+1
            if (y+1) % n == 0 and y+1 != n*n:
                print("|", end=" ")
        if (x+1) % n == 0 and x+1 != n*n:
            print()
            for i in range(2*n*n+2*n-3):
                print("-", end="")
        print()
    return sudoku_sol


n, clues = read_puzzle()
print_puzzle(n, clues)

# maps each (row, col, val) combination to a unique integer identifier
s = [[[(n*n*n*n*x) + (n*n*y) + z + 1 for x in range(n*n)] for y in range(n*n)] for z in range(n*n)]
clauses = []

sat, assm = solve_puzzle(n, s, clues, clauses)
print("Solvable?", sat)
print()

if sat:
    sudoku_sol = print_solution(n, s, assm)