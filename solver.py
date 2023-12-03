"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

#   determines if a placement is valid 
def possible(board, r, c, val, possible_values):
    if isinstance(r, str):
        r = ROW.index(r)
    if isinstance(c, str):
        c = COL.index(c)
    
    for i in range(0,9):
        if board[ROW[r]+COL[i]] == val:
            return False
    
    for i in range(0,9):
        if board[ROW[i]+COL[c]] == val:
            return False

    # check 3x3 squares    
    r0 = (r//3)*3   # (row//3) = the 3x3 square to check, * 3 to get the starting row index of that square
    c0 = (c//3)*3   
    for i in range (0,3):
        for j in range(0,3):
            if board[ROW[r0+i]+COL[c0+j]] == val:
                return False
 
    return True

def update_possible_values(board, row, col, value, possible_values):
    r_idx = ROW.index(row)
    c_idx = COL.index(col)
    
    # Update row
    for c in COL:
        cell = row + c
        if value in possible_values[cell]:
            possible_values[cell].remove(value)
            
    # Update column
    for r in ROW:
        cell = r + col
        if value in possible_values[cell]:
            possible_values[cell].remove(value)
    
    # Update 3x3 square
    r0 = (r_idx // 3) * 3
    c0 = (c_idx // 3) * 3
    for i in range(r0, r0 + 3):
        for j in range(c0, c0 + 3):
            cell = ROW[i] + COL[j]
            if value in possible_values[cell]:
                possible_values[cell].remove(value)
            

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def select_unassigned_variable(board, possible_values):
    min_remaining_values = float('inf')
    best_cell = None
    for r in range(9):
        for c in range(9):
            cell = ROW[r] + COL[c]
            if board[cell] == 0:
                num_possible_values = len(possible_values[cell])
                if num_possible_values < min_remaining_values:
                    min_remaining_values = num_possible_values
                    best_cell = (ROW[r], COL[c])
    return best_cell
    

def backtracking_search(board):
    possible_values = {ROW[r]+COL[c]: list(range(1, 10)) for r in range(9) for c in range(9)}
    return backtracking(board, {}, possible_values)


def is_complete(board):
    return all(board[ROW[r] + COL[c]] != 0 for r in range(9) for c in range(9))


def backtracking(board, assignment, possible_values):
    """Takes a board and returns solved board."""
    # TODO: implement this
    if is_complete(board):
        return board
    
    r, c = select_unassigned_variable(board, possible_values)
    cell = r + c 
    
    original_possible_values = possible_values[cell].copy()

    for value in original_possible_values:
        if possible(board, ROW.index(r), COL.index(c), value, possible_values):
            board[cell] = value
            assignment[cell] = value
            temp_possible_values = {k: v[:] for k, v in possible_values.items()}

            board[cell] = value
            assignment[cell] = value
            update_possible_values(board, r, c, value, possible_values)

            result = backtracking(board, assignment, possible_values)
            if result:
                return result
            
            board[cell] = 0
            del assignment[cell]
            possible_values = temp_possible_values
  
    return None


if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
    
        solved_board = backtracking_search(board)
        if solved_board is not None:
            print(board_to_string(solved_board))
            #print_board(solved_board)
        else:
            print("No solution exists")
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)
            
            solved_board = backtracking_search(board)
           
            # Print solved board. TODO: Comment this out when timing runs.
            print(board_to_string(solved_board))
          
            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
      
           
        print("Finishing all boards in file.")
  