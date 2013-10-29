__author__ = 'Antifrize'

class Grid:
    grid = 0

    def setGridBySize(self,N,K):
        self.grid = []
        for tau in range(K):
            self.grid.append([0 for x in N])

    def outputGrid(self):
        for line in self.grid:
            for num in line:
                print(str(num)+" ")

    def getLineByTime(self,n):
        return self.grid[n]

    def getLineByPos(self,n):
        return [line[n] for line in self.grid]