import numpy as np 
import random
from CheckWin import checkWin

class RandomSearch:
    def __init__(self, iterations = 1000):
        self.iterations = iterations
        self.ai_sign = "X"
        self.p_sign = "O"


    def move(self, grid, sign):
        moves = np.array([[[0,1],[0,1],[0,1]],[[0,1],[0,1],[0,1]],[[0,1],[0,1],[0,1]]])
        if sign == "O":
            self.ai_sign = "O"
            self.p_sign = "X"

        for x in range(self.iterations):
            #selection(random)
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if grid[row,col] == "":
                    moves[row,col][0] += self.aiMoved(row,col, grid.copy())
                    moves[row,col][1] += 1
            else:
                    moves[row,col][0] = -999999
                    moves[row,col][1] += 1
        score = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(3):
            for j in range(3):
                N = moves[i,j][1]
                V = moves[i,j][0]
                score[i][j] = V/N
        score = np.array(score)
        row,col = np.unravel_index(score.argmax(), score.shape)
        return row,col

    def aiMoved(self,row,col, grid):
        grid[row,col] = self.ai_sign
        if checkWin(grid) == self.p_sign:
            return -1
        if checkWin(grid) == self.ai_sign:
            return 1
        #selection for nodes
        i = 0
        j = 0
        while True:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            if grid[i][j] == "":
                break
        return self.playerMoved(i,j, grid.copy())
    
    def playerMoved(self,row,col, grid):
        grid[row,col] = self.p_sign
        if checkWin(grid) == self.p_sign:
            return -1
        if checkWin(grid) == self.ai_sign:
            return 1
        #selection for nodes
        i = 0
        j = 0
        while True:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            if grid[i][j] == "":
                break
        return self.aiMoved(i,j, grid.copy())

