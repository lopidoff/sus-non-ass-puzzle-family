# sus-ass puzzle v0.1

import colorama

colorama.init()

cell_border = "║"
blank = " "
default_rows = 10
solved = 0

moves = ["/","\\"]                              # movement characters
states = ["*"]                                  # states
command = ["<",">"]                             # break characters

def algebraic(current, new):                    # holds algebraic rules
    return blank

def single_operation(current, new):             # outputs new state & location
    if current == blank:
        return new,0,0
    elif new == blank:
        return current,0,0
    elif current == "\\":
        return new,1,0
    elif current == "/":
        return new,1,1
    elif new == "\\":
        return current,1,0
    elif new == "/":
        return current,1,1
    elif new in states:
        return algebraic(current,new),0,0

def apply_moves(board, action):
    ind = 0
    while ind < len(action):
        k = action[ind]
        if k in (moves + states):
            board.play_action(k,0,0)
            ind += 1
        elif k == ">":
            return ind+1, "c"
        elif k == "<":
            return ind+1, "o"
        else:
            ind += 1
    return ind, "f"

class Board:
    def __init__(self,depth):
        self.state = []                             # storage space for board elts
        for i in range(default_rows):
            new_row = [blank] * (i+1)
            self.state.append(new_row)
        self.depth = depth
    def get_length(self):                           # returns number of rows
        return len(self.state)
    def get_entry(self, row, entry):                # spits out requested entry
        return self.state[row][entry]
    def play_action(self, new, row, entry):         # plays operation on board
        current = self.state[row][entry]
        new_val,row_shift,entry_shift = single_operation(current,new)
        self.state[row][entry] = blank
        if self.state[row+row_shift][entry+entry_shift] == blank:
            self.state[row+row_shift][entry+entry_shift] = new_val
        else:
            self.play_action(new_val, row+row_shift, entry+entry_shift)
    def compose_board(self, board):                 # composes external board
        if self.get_length() == board.get_length():
            num = self.get_length()-1
            for i in range(num,-1,-1):
                for j in range(i+1):
                    self.play_action(board.get_entry(i,j),i,j)
    def __str__(self):
        result = ""
        if self.depth:
            result += "depth = " + str(self.depth) + "\n"
        for i in range(self.get_length()):          # number of rows
            row = ""
            for j in range(i):                      # deficit of spaces in row compared to center
                row += blank
            for j in range(self.get_length()-i):    # number of spaces in the row
                row += cell_border
                row += self.get_entry(-i-1,j)
            row += cell_border
            result += row + "\n"
        return result

def game(overflow,depth=0):
    board = Board(depth)
    saved_index = 0
    while overflow != "":
        ind,end_type = apply_moves(board, overflow)
        saved_index += ind
        if end_type == "c":
            return board, saved_index, overflow[ind:]
        elif end_type == "o":
            new_board,indx,overoverflow = game(overflow[ind:],depth+1)
            board.compose_board(new_board)
            ind += indx
            overflow = overoverflow + overflow[ind:]
        elif end_type == "f":
            overflow = overflow[ind:]
    
    while not solved:
        gap = " " * board.get_length()
        action = input(str(board)+gap)
        print("\033c\033[3J", end='')
        
        while action != "":
            ind,end_type = apply_moves(board, action)
            if end_type == "c":
                return board, saved_index, action[ind:]
            elif end_type == "o":
                new_board,indx,backlash = game(action[ind:],depth+1)
                board.compose_board(new_board)
                ind += indx
                action = backlash + action[ind:]
            elif end_type == "f":
                action = action[ind:]

game("")