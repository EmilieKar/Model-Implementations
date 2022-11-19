def checkWin(grid):
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != "":
            return grid[i][0]
        if grid[0][i] == grid[1][i] == grid[2][i] != "":
            return grid[0][i]

    if (grid[0][0] == grid[1][1] == grid[2][2] != "") or (grid[0][2] == grid[1][1] == grid[2][0] != ""):
            return grid[1][1]

    return 0