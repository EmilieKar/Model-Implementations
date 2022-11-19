import numpy as np 
import random

class RuleBased:
    def __init__(self):
        self.ai_sign = "X"
        self.p_sign = "O"

    def move(self, grid, sign):
        if sign == "O":
            self.ai_sign = "O"
            self.p_sign = "X"

        # If able choose middle
        if grid[1,1] == "":
            return 1,1
        
        # If you can win in one move do so
        r,c = self.check_next_win(self.ai_sign, grid)
        if r != -1: 
            return r,c
        
        # If opponent can win in one move prevent them 
        r,c = self.check_next_win(self.p_sign, grid)
        if r != -1: 
            return r,c
        
        # If a corner is available
        corners = [[0,0],[0,2],[2,0],[2,2]]
        for c in corners:
            if grid[c[0]][c[1]] == "":
                return c[0], c[1]
        
        # Pick random remaining
        while True:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            if grid[i][j] == "":
                break
        return i, j

        
    def check_next_win(self, sign, grid):
        for i in range(3):
            if (grid[i][0] == grid[i][1] == sign) and (grid[i][2] == ""):
                return i, 2
            if (grid[i][1] == grid[i][2] == sign) and (grid[i][0] == ""):
                return i, 0
            if (grid[i][0] == grid[i][2] == sign) and (grid[i][1] == ""):
                return i, 1

            if (grid[0][i] == grid[1][i] == sign) and (grid[2][i] == ""):
                return 2, i
            if (grid[1][i] == grid[2][i] == sign) and (grid[0][i] == ""):
                return 0, i
            if (grid[0][i] == grid[2][i] == sign) and (grid[1][i] == ""):
                return 1, i
            
        if (grid[0][0] == grid[1][1] == sign) and (grid[2][2] == ""):
            return 2, 2
        if (grid[1][1] == grid[2][2] == sign) and (grid[0][0] == ""):
            return 0,0
        if (grid[0][0] == grid[2][2] == sign) and(grid[1][1] == ""):
            return 1,1

        if (grid[0][2] == grid[1][1] == sign) and (grid[2][0] == ""):
            return 2, 0
        if (grid[1][1] == grid[2][0] == sign) and (grid[0][2] == ""):
            return 0,2
        if (grid[0][2] == grid[2][0] == sign) and (grid[1][1] == ""):
            return 1,1

        return -1,-1