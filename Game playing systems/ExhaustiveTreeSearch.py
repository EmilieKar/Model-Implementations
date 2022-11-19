import numpy as np 
import random
from CheckWin import checkWin
from CheckDraw import checkDraw

class ExhaustiveTreeSearch:
    def __init__(self):
        self.ai_sign = "X"
        self.p_sign = "O"

    def move(self, grid, sign):
        # Init
        moves = np.array([[0,0,0],[0,0,0],[0,0,0]])
        if sign == "O":
            self.ai_sign = "O"
            self.p_sign = "X"

        for row in range(3):
            for col in range(3):
                if grid[row,col] == "":
                    moves[row,col] = self.aiMoved(row,col, grid.copy())
                else:
                    moves[row,col] = -999999 # Move is unavailble
        #print(moves)
        row,col = np.unravel_index(moves.argmax(), moves.shape)
        return row,col

    def aiMoved(self,row, col, grid):
        # Make move
        grid[row ,col ] = self.ai_sign

        # Check for end states
        if checkWin(grid) == self.ai_sign:
            return 1

        if checkWin(grid) == self.p_sign:
            return -1
        
        if checkDraw(grid):
            return 0

        sum = 0

        for i in range(3):
            for j in range(3):
                if grid[i,j] == "":
                    # Test all possible moves
                    sum += self.playerMoved(i,j, grid.copy())
        return sum
    
    def playerMoved(self,row, col, grid):
        grid[row,col] = self.p_sign
        if checkWin(grid) == self.p_sign:
            return -1
        if checkWin(grid) == self.ai_sign:
            return 1
        if checkDraw(grid):
            return 0
        
        sum = 0
        for i in range(3):
            for j in range(3):
                if grid[i,j] == "":
                    sum += self.aiMoved(i,j, grid.copy())
        return sum