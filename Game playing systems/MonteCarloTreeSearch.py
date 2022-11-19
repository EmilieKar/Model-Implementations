import numpy as np
import random

from CheckWin import checkWin
from CheckDraw import checkDraw
from Node import Node
from RuleBased import RuleBased

class MonteCarloTreeSearch:
    def __init__(self, iterations = 100, rollout = 'random'):
        self.iterations = iterations
        self.ai_sign = "X"
        self.p_sign = "O"
        if rollout == 'rules':
            self.rollout = self.rollout_rules
            print('Using rollout_rules')
        else: 
            self.rollout = self.rollout_random
        self.ruleclf = RuleBased()

    def move(self, grid, sign):
        if sign == "O":
            self.ai_sign = "O"
            self.p_sign = "X"

        root = Node(grid.copy(),self.p_sign,None, "max")
        
        for x in range(self.iterations):
            # select by ucb1
            newNode = root.findUcbMax()
            # rollout on selected
            value = self.rollout(newNode.state.copy(), newNode.sign)
            # update all parent nodes
            newNode.backProg(value)
        
        #picks child with highest number of visits
        maxVisits = 0
        row = 0
        col = 0
        for i in range(3):
            for j in range(3):
                if root.edges[i,j] is not None:
                    if root.edges[i,j].n > maxVisits:
                        maxVisits = root.edges[i,j].n
                        row = i
                        col = j                
        return row,col

    # plays out randomly
    def rollout_random(self,grid, sign):
        if checkWin(grid) == self.p_sign:
            return -20
        if checkWin(grid) == self.ai_sign:
            return 10
        if checkDraw(grid):
            return 0
        # selection for nodes, random for now, a more sofisticated method to chose i and j like a neural network trained on
        # old games at first and then ai vs ai game here would make for a great model.
        #i,j = findOptimal(grid)
        i = 0
        j = 0
        while True:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            if grid[i][j] == "":
                break
        grid[i,j] = sign
        if sign == "X":
            return self.rollout(grid.copy(), "O")
        else:
            return self.rollout(grid.copy(), "X")

    #Plays out according to pre defined rules
    def rollout_rules(self, grid, sign):
        if checkWin(grid) == self.p_sign:
            return -20
        if checkWin(grid) == self.ai_sign:
            return 10
        if checkDraw(grid):
            return 0

        i, j = self.ruleclf.move(grid, sign)
        grid[i,j] = sign
        if sign == "X":
            return self.rollout(grid.copy(), "O")
        else:
            return self.rollout(grid.copy(), "X")