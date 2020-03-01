#!/usr/bin/python

import numpy as np
from dataclasses import dataclass
import random
import pygame
from pprint import pprint
import graphics
import graphicsAk
import agent2
from func import isValid

@dataclass
class KB():
    mine: int #0 if hidden, 1 if mine, 2 if safe, 3 if flag
    num: int #num of surrounding mines
    numSafe: int #num of surrounding safe squares
    numIdentMines: int #num of identified mines (should be <= num)
    numHidden: int #num of hidden squares

dim = 10
num_mines = 10
#fills a matrix of size dim*dim with num_mines many mines

def setHidden(playboard):
    for i in range(1,dim-1):
        for j in range(1,dim-1):
            playboard[i,j].numHidden = 8

    playboard[0,0].numHidden = 3
    playboard[0,dim-1].numHidden = 3
    playboard[dim-1,0].numHidden = 3
    playboard[dim-1,dim-1].numHidden = 3

    for i in range(1,dim-1):
        playboard[0,i].numHidden = 5
        playboard[i,0].numHidden = 5
        playboard[dim-1,i].numHidden = 5
        playboard[i,dim-1].numHidden = 5


def updateKB(coord):
    x = coord[0]
    y = coord[1]
    if (matrix[x,y] == 9):
        playboard[x,y].mine = 1
        if (isValid(x+1,y,dim)):
            playboard[x+1,y].numIdentMines+=1
            playboard[x+1,y].numHidden-=1
        if (isValid(x+1,y+1,dim)):
            playboard[x+1,y+1].numIdentMines+=1
            playboard[x+1,y+1].numHidden-=1
        if (isValid(x,y+1,dim)):
            playboard[x,y+1].numIdentMines+=1
            playboard[x,y+1].numHidden-=1
        if (isValid(x-1,y+1,dim)):
            playboard[x-1,y+1].numIdentMines+=1
            playboard[x-1,y+1].numHidden-=1
        if(isValid(x-1,y,dim)):
            playboard[x-1,y].numIdentMines+=1
            playboard[x-1,y].numHidden-=1
        if (isValid(x-1,y-1,dim)):
            playboard[x-1,y-1].numIdentMines+=1
            playboard[x-1,y-1].numHidden-=1
        if (isValid(x,y-1,dim)):
            playboard[x,y-1].numIdentMines+=1
            playboard[x,y-1].numHidden-=1
        if (isValid(x+1,y-1,dim)):
            playboard[x+1,y-1].numIdentMines+=1
            playboard[x+1,y-1].numHidden-=1
    else:
        playboard[x,y].mine = 2
        playboard[x,y].num = matrix[x,y]
        if (isValid(x+1,y,dim)):
            playboard[x+1,y].numSafe+=1
            playboard[x+1,y].numHidden-=1
            playboard[x+1,y].mine = 2
            playboard[x+1,y].num = matrix[x+1,y]
        if (isValid(x+1,y+1,dim)):
            playboard[x+1,y+1].numSafe+=1
            playboard[x+1,y+1].numHidden-=1
            playboard[x+1,y+1].mine = 2
            playboard[x+1,y+1].num = matrix[x+1,y+1]
        if (isValid(x,y+1,dim)):
            playboard[x,y+1].numSafe+=1
            playboard[x,y+1].numHidden-=1
            playboard[x,y+1].mine = 2
            playboard[x,y+1].num = matrix[x,y+1]
        if (isValid(x-1,y+1,dim)):
            playboard[x-1,y+1].numSafe+=1
            playboard[x-1,y+1].numHidden-=1
            playboard[x-1,y+1].mine = 2
            playboard[x-1,y+1].num = matrix[x-1,y+1]
        if(isValid(x-1,y,dim)):
            playboard[x-1,y].numSafe+=1
            playboard[x-1,y].numHidden-=1
            playboard[x-1,y].mine = 2
            playboard[x-1,y].num = matrix[x-1,y]
        if (isValid(x-1,y-1,dim)):
            playboard[x-1,y-1].numSafe+=1
            playboard[x-1,y-1].numHidden-=1
            playboard[x-1,y-1].mine = 2
            playboard[x-1,y-1].num = matrix[x-1,y-1]
        if (isValid(x,y-1,dim)):
            playboard[x,y-1].numSafe+=1
            playboard[x,y-1].numHidden-=1
            playboard[x,y-1].mine = 2
            playboard[x,y-1].num = matrix[x,y-1]
        if (isValid(x+1,y-1,dim)):
            playboard[x+1,y-1].numSafe+=1
            playboard[x+1,y-1].numHidden-=1
            playboard[x+1,y-1].mine = 2
            playboard[x+1,y-1].num = matrix[x+1,y-1]




def bfs_from_0(playboard, start): #start has to be in format (i,j) as a tuple
    explored = set()
    queue = [start]
    
    while queue:
        node = queue.pop(0)
        x = node[0]
        y = node[1]
        if node not in explored:
            updateKB((x,y))
            explored.add(node)
            if (isValid(x+1,y,dim)):
                if (matrix[x+1,y] == 0):
                    queue.append((x+1,y))
                playboard[x+1,y].num = matrix[x+1,y]
        
            if (isValid(x+1,y+1,dim)):
                if (matrix[x+1,y+1] == 0):
                    queue.append((x+1,y+1))
                playboard[x+1,y+1].num = matrix[x+1,y+1]
            
            if (isValid(x,y+1,dim)):
                if (matrix[x,y+1] == 0):
                    queue.append((x,y+1))
                playboard[x,y+1].num = matrix[x,y+1]
            
            if (isValid(x-1,y+1,dim)):
                if (matrix[x-1,y+1] == 0):
                    queue.append((x-1,y+1))
                playboard[x-1,y+1].num = matrix[x-1,y+1]
            
            if(isValid(x-1,y,dim)):
                if (matrix[x-1,y] == 0):
                    queue.append((x-1,y))
                playboard[x-1,y].num = matrix[x-1,y]
            
            if (isValid(x-1,y-1,dim)):
                if (matrix[x-1,y-1] == 0):
                    queue.append((x-1,y-1))
                playboard[x-1,y-1].num = matrix[x-1,y-1]
            
            if (isValid(x,y-1,dim)):
                if (matrix[x,y-1] == 0):
                    queue.append((x,y-1))
                playboard[x,y-1].num = matrix[x,y-1]
            
            if (isValid(x+1,y-1,dim)):
                if (matrix[x+1,y-1] == 0):
                    queue.append((x+1,y-1))
                playboard[x+1,y-1].num = matrix[x+1,y-1]

    return playboard,explored


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
            random_matrix[x,y] = 9 #numerical representation of mine

    return random_matrix

matrix = createMine()
print(matrix)

#count mines around a specific index
def countMines(x, y, matrix):
    #get all 8 coordinates around a specific x,y coordinate and increment if it is a mine
    num_mines_around=0
    if(isValid(x+1, y,dim)):
        if(matrix[x+1][y]==9):
            num_mines_around+=1
    if(isValid(x+1, y+1,dim)):
        if(matrix[x+1][y+1]==9):
            num_mines_around+=1
    if(isValid(x, y+1,dim)):
        if(matrix[x][y+1]==9):
            num_mines_around+=1
    if(isValid(x-1, y+1,dim)):
        if(matrix[x-1][y+1]==9):
            num_mines_around+=1
    if(isValid(x-1, y,dim)):
        if(matrix[x-1][y]==9):
            num_mines_around+=1
    if(isValid(x-1, y-1,dim)):
        if(matrix[x-1][y-1]==9):
            num_mines_around+=1
    if(isValid(x, y-1,dim)):
        if(matrix[x][y-1]==9):
            num_mines_around+=1
    if(isValid(x+1, y-1,dim)):
        if(matrix[x+1][y-1]==9):
            num_mines_around+=1
    return num_mines_around

for i in range(0, dim):
    for j in range(0, dim):
        if(matrix[i,j]!=9):
            mine_num = countMines(i,j,matrix)
            matrix[i, j] = mine_num

print("---------ANSWER-----------KEY--------------------")
print(matrix)

# START game
# MAKE AN ARRAY OF EMPTY KBS THAT THE AI USES

playboard = np.empty(shape=(dim,dim), dtype=object)
for o in range(0, dim):
    for p in range(0, dim):
        KBTemp= KB(0,-1,0,0,0)
        playboard[o][p]= KBTemp
setHidden(playboard)
v = random.randint(0,dim-1)
w = random.randint(0,dim-1)
playboard[v,w].num = matrix[v,w]
if (matrix[v,w] == 9):
    playboard[v,w].mine = 1
else:
    playboard[v,w].mine = 2
print((v,w))
# ans_board[v,w] = matrix[v,w]
while(matrix[v,w] != 0):
    v = random.randint(0,dim-1)
    w = random.randint(0,dim-1)
    playboard[v,w].num = matrix[v,w]
    print((v,w))

playboard,explored = bfs_from_0(playboard,(v,w))

print(agent2.populateEQMap(dim,playboard,explored))

graphics.display_graphics(playboard, dim)

print(playboard)

#what did beatrice do to main? see below:
#changed bfs function to also return explored
#added agent2 at the bottom
#changed all isValid methods bc moved to func.py and then added dim as parameter
#note: PLS FIX SET IT NOT WORK
