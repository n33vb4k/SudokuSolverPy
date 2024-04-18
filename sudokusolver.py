import numpy as np

#100% works for sudoku puzzles with only 1 solution
def sudoku_solver(sudoku):
    """
    Input
        sudoku : 9x9 numpy array - empty cells are designated by 0.

    Output
        9x9 numpy array of integers with solution, or array of -1s if no solution
    """
    
    #checks input the board follows the rules of sudoku
    def check_input_board(board):
        for r in range(9):
            for c in range(9):
                if not check_valid(board, board[r][c], r, c) and board[r][c] != 0:
                    return False
        return True
    
    #checks the position of a number is valid and follows the rules
    def check_valid(board, num, row, col):
        #check none same in row
        for c in range(9):
            if board[row][c] == num and c != col:
                return False
        #check none same in col
        for r in range(9):
            if board[r][col] == num and r != row:
                return False
        #check none same in 3x3
        box_row = row // 3
        box_col = col // 3
        for r in range(box_row * 3, box_row * 3 + 3):
            for c in range (box_col * 3, box_col*3 + 3):
                if board[r][c] == num and r != row and c != col:
                    return False
                
        return True
        
    
    #gets the possible values for an empty space, removing ones that it definitely cannot be
    def possible_values(board, row, col):
        vals = set(range(1, 10))
        # Remove values in the same row
        vals -= set(board[row, :])
        # Remove values in the same column
        vals -= set(board[:, col])
        # Remove values in the same 3x3 box
        box_row = row // 3
        box_col = col // 3
        box_vals = board[box_row*3:(box_row+1)*3, box_col*3:(box_col+1)*3].flatten()
        vals -= set(box_vals)
        return list(vals) 
    
    #checks if the board is complete by checking there are no 0s remaining
    def check_solved(board):
        if not np.all(board):
            return False
        return True
    
    #builds a dictionary mapping empty spaces to the possible values for that space
    def build_possible_values_dict(board):
        pvals = {}
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    pvals[(r,c)] = possible_values(board, r, c)
        return pvals
    
    #returns a list of cells which do not yet have a set value and are affected by a change
    def affected_cells(row, col, pvals):
        affected = []
        # Add cells in the same row
        affected.extend([(row, c) for c in range(9) if c != col and (row,c) in pvals])
        # Add cells in the same column
        affected.extend([(r, col) for r in range(9) if r != row and (r, col) in pvals])
        # Add cells in the same 3x3 box
        box_row = row // 3
        box_col = col // 3
        affected.extend([(r, c) for r in range(box_row * 3, box_row * 3 + 3) for c in range(box_col * 3, box_col * 3 + 3) if (r, c) != (row, col) and (r,c) in pvals])
        # Remove duplicates and return the list
        return list(set(affected))
    
    #recursive depth first search with backtracking
    def solve(board, pvals):
        #terminating case for recursion
        if check_solved(board):
            return board
        #gets the position of the cell with the least number of possible values
        r, c = min(pvals, key=lambda k: len(pvals[k]))
        values = pvals[(r, c)]
        for value in values:
            if check_valid(board, value, r, c):
                board[r][c] = value
                next_pvals = pvals.copy()
                next_pvals.pop((r,c))
                # Update next_pvals only for affected cells
                for cell in affected_cells(r, c, pvals):
                    next_pvals[cell] = possible_values(board, cell[0], cell[1])
                # Recursive call to solve
                next_state = solve(board, next_pvals)
                if check_solved(next_state):
                    return next_state
                # If not solved, discard the assignment and next_pvals and continue with the next value
                board[r][c] = 0

        return board
                

    #checks if the inputted board follows the rules of sudoku, before attempting to solve
    if not check_input_board(sudoku):
        return np.full((9, 9), -1)
    
    #builds pvals dictionary for the input board
    pvals = build_possible_values_dict(sudoku)
   
    maybe_solved = solve(sudoku, pvals)
    if not check_solved(maybe_solved):
        return np.full((9, 9), -1)
    else:
        solved_sudoku = maybe_solved
    
    return solved_sudoku

hardtest = np.array(
[[0, 2, 0, 0, 0, 6, 9, 0, 0],
 [0, 0, 0, 0, 5, 0, 0, 2, 0],
 [6, 0, 0, 3, 0, 0, 0, 0, 0],
 [9, 4, 0, 0, 0, 7, 0, 0, 0],
 [0, 0, 0, 4, 0, 0, 7, 0, 0],
 [0, 3, 0, 2, 0, 0, 0, 8, 0],
 [0, 0, 9, 0, 4, 0, 0, 0, 0],
 [3, 0, 0, 9, 0, 2, 0, 1, 7],
 [0, 0, 8, 0, 0, 0, 0, 0, 2]])

print(hardtest)
print("\n")
print(sudoku_solver(hardtest))
print("\n")
