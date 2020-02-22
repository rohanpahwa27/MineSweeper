#!/usr/bin/python

import numpy as np
from dataclasses import dataclass



@dataclass
class KB():
    mine: bool #1 if it is a mine, 0 if it is safe, 2 if it is hidden
    numMines: int #num of surrounding mines
    numSafe: int #num of surrounding safe squares (should =
    numIdentMines: int #num of identified mines (should be <= numMines)
    numHidden: int #num of hidden squares

dim = 10
num_mines = 5
#fills a matrix of size dim*dim with num_mines many mines
def createMine():

    #random_matrix = np.random.randint(1,size=(dim,dim))
    random_matrix = np.zeros((dim, dim), dtype=np.int)
    mine_location = set()
    #for i in range(0, num_mines):
    while len(mine_location)!= num_mines:
        value = np.random.randint(dim*dim)
        if(value not in mine_location):
            mine_location.add(value)
            x = int(value%dim)
            y = int(value/dim)
            random_matrix[x][y] = 1

    print(random_matrix)

createMine()


kb1 = KB(True,0,0,0,0)
print(kb1)
