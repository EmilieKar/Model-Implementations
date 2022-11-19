import constants as c
import numpy as np
import random
import timeit

class NormalPlayer: 
    def __init__(self, name):
        self.name = name

    def move(self, grid, sign):
        # TODO: Add illegal move check for safety
        print(f"{self.name}s turn! You are {sign}s")
        print(f"State is: \n {grid}")
        print("State your move start with which row 0 to 2")
        row = int(input())
        print("state what column 0 to 2")
        col = int(input())
        return row, col

class AiPlayer: 
    
    def __init__(self, clf):
        self.clf = clf
        self.movecount = 0
        self.tot_time = 0

    def move(self, grid, sign):
        start_time = timeit.default_timer()
        r,c = self.clf.move(grid, sign)
        elapsed_time = timeit.default_timer() - start_time
        self.movecount += 1
        self.tot_time += elapsed_time
        return r,c

    def avg_time(self):
        return self.tot_time/self.movecount

        
class Game:
    def __init__(self, player1, player2, ifprint = True):
        self.grid = np.array(["","","","","","","","",""]).reshape((3, 3)) # Note this could also be represented as a simple list.
        self.players = [player1, player2]
        self.ifprint = ifprint
        # Not exactly turn but used to select which player should do the next move
        self.turn = 0
        
    
    def start(self):
        self.grid = np.array(["","","","","","","","",""]).reshape((3, 3))
        # Randomize who starts the game
        if random.uniform(0, 1) > 0.5:
            self.turn = 0
            if self.ifprint: print(f"Starting player is {c.SIGNS[self.turn]}")
        else:
            self.turn = 1
            if self.ifprint: print(f"Starting player is {c.SIGNS[self.turn]}")
        
        while self.checkWinner() == 0 :
            player_idx = self.turn % 2
            row, col = self.players[player_idx].move(self.grid, c.SIGNS[player_idx])
            self.grid[row][col] = c.SIGNS[player_idx]
            self.turn += 1

            # Check if board is full
            if self.turn >= 9: 
                if "" not in self.grid:
                    if self.ifprint: 
                        print("Game is a tie")
                        print(self.grid)
                    return 2

        winner = self.checkWinner()
        if self.ifprint: 
            print(f"Winner is {winner}")
            print(self.grid)
        return c.SIGNS.index(winner)
            

    def checkWinner(self):
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != "":
                return self.grid[i][0]
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != "":
                return self.grid[0][i]

        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != "") or (self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ""):
                return self.grid[1][1]

        return 0

import seaborn as sns

def comparePlayers(player1, player2, iterations, ifprint = False):

    tictac = Game(player1, player2, ifprint = ifprint)
    score = [0,0,0]
    for i in range(iterations):
        if ifprint : print(f"Starting game {i+1}/{iterations}:")
        win = tictac.start()
        score[win] += 1

    # score = [x/iterations for x in score]
    # plt = sns.barplot(x=["Player1 Win", "Player2 Win", "Tie"], y=score)
    # plt.set_ylabel("Percentage")
    return score