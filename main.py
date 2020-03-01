#!/usr/bin/python

import numpy as np
from dataclasses import dataclass
import random
import pygame
from pprint import pprint
import graphics
import graphicsAk

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
        if (isValid(x+1,y)):
            playboard[x+1,y].numIdentMines+=1
            playboard[x+1,y].numHidden-=1
        if (isValid(x+1,y+1)):
            playboard[x+1,y+1].numIdentMines+=1
            playboard[x+1,y+1].numHidden-=1
        if (isValid(x,y+1)):
            playboard[x,y+1].numIdentMines+=1
            playboard[x,y+1].numHidden-=1
        if (isValid(x-1,y+1)):
            playboard[x-1,y+1].numIdentMines+=1
            playboard[x-1,y+1].numHidden-=1
        if(isValid(x-1,y)):
            playboard[x-1,y].numIdentMines+=1
            playboard[x-1,y].numHidden-=1
        if (isValid(x-1,y-1)):
            playboard[x-1,y-1].numIdentMines+=1
            playboard[x-1,y-1].numHidden-=1
        if (isValid(x,y-1)):
            playboard[x,y-1].numIdentMines+=1
            playboard[x,y-1].numHidden-=1
        if (isValid(x+1,y-1)):
            playboard[x+1,y-1].numIdentMines+=1
            playboard[x+1,y-1].numHidden-=1
    else:
        playboard[x,y].mine = 2
        playboard[x,y].num = matrix[x,y]
        if (isValid(x+1,y)):
            playboard[x+1,y].numSafe+=1
            playboard[x+1,y].numHidden-=1
            if(matrix[x+1,y] == 0):
                playboard[x+1,y].mine = 2
                playboard[x+1,y].num = matrix[x+1,y]
        if (isValid(x+1,y+1)):
            playboard[x+1,y+1].numSafe+=1
            playboard[x+1,y+1].numHidden-=1
            if(matrix[x+1,y+1] == 0):
                playboard[x+1,y+1].mine = 2
                playboard[x+1,y+1].num = matrix[x+1,y+1]
        if (isValid(x,y+1)):
            playboard[x,y+1].numSafe+=1
            playboard[x,y+1].numHidden-=1
            if(matrix[x,y+1] == 0):
                playboard[x,y+1].mine = 2
                playboard[x,y+1].num = matrix[x,y+1]
        if (isValid(x-1,y+1)):
            playboard[x-1,y+1].numSafe+=1
            playboard[x-1,y+1].numHidden-=1
            if(matrix[x-1,y+1] == 0):
                playboard[x-1,y+1].mine = 2
                playboard[x-1,y+1].num = matrix[x-1,y+1]
        if(isValid(x-1,y)):
            playboard[x-1,y].numSafe+=1
            playboard[x-1,y].numHidden-=1
            if(matrix[x-1,y] == 0):
                playboard[x-1,y].mine = 2
                playboard[x-1,y].num = matrix[x-1,y]
        if (isValid(x-1,y-1)):
            playboard[x-1,y-1].numSafe+=1
            playboard[x-1,y-1].numHidden-=1
            if(matrix[x-1,y-1] == 0):
                playboard[x-1,y-1].mine = 2
                playboard[x-1,y-1].num = matrix[x-1,y-1]
        if (isValid(x,y-1)):
            playboard[x,y-1].numSafe+=1
            playboard[x,y-1].numHidden-=1
            if(matrix[x,y-1] == 0):
                playboard[x,y-1].mine = 2
                playboard[x,y-1].num = matrix[x,y-1]
        if (isValid(x+1,y-1)):
            playboard[x+1,y-1].numSafe+=1
            playboard[x+1,y-1].numHidden-=1
            if(matrix[x+1,y-1] == 0):
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
            if (x,y) in set_of_coords:
                set_of_coords.remove((x,y))
            if (isValid(x+1,y)):
                if (matrix[x+1,y] == 0):
                    queue.append((x+1,y))
                playboard[x+1,y].num = matrix[x+1,y]

            if (isValid(x+1,y+1)):
                if (matrix[x+1,y+1] == 0):
                    queue.append((x+1,y+1))
                playboard[x+1,y+1].num = matrix[x+1,y+1]

            if (isValid(x,y+1)):
                if (matrix[x,y+1] == 0):
                    queue.append((x,y+1))
                playboard[x,y+1].num = matrix[x,y+1]

            if (isValid(x-1,y+1)):
                if (matrix[x-1,y+1] == 0):
                    queue.append((x-1,y+1))
                playboard[x-1,y+1].num = matrix[x-1,y+1]

            if(isValid(x-1,y)):
                if (matrix[x-1,y] == 0):
                    queue.append((x-1,y))
                playboard[x-1,y].num = matrix[x-1,y]

            if (isValid(x-1,y-1)):
                if (matrix[x-1,y-1] == 0):
                    queue.append((x-1,y-1))
                playboard[x-1,y-1].num = matrix[x-1,y-1]

            if (isValid(x,y-1)):
                if (matrix[x,y-1] == 0):
                    queue.append((x,y-1))
                playboard[x,y-1].num = matrix[x,y-1]

            if (isValid(x+1,y-1)):
                if (matrix[x+1,y-1] == 0):
                    queue.append((x+1,y-1))
                playboard[x+1,y-1].num = matrix[x+1,y-1]

    return playboard

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

def mark_as_flags(x,y):
    if (isValid(x+1,y)):
        if(playboard[x+1,y].mine == 0):
            playboard[x+1,y].mine = 3
            if (x+1,y) in set_of_coords:
                set_of_coords.remove((x+1,y))
    if (isValid(x+1,y+1)):
        if(playboard[x+1,y+1].mine == 0):
            playboard[x+1,y+1].mine = 3
            if (x+1,y+1) in set_of_coords:
                set_of_coords.remove((x+1,y+1))
    if (isValid(x,y+1)):
        if(playboard[x,y+1].mine == 0):
            playboard[x,y+1].mine = 3
            if (x,y+1) in set_of_coords:
                set_of_coords.remove((x,y+1))
    if (isValid(x-1,y+1)):
        if(playboard[x-1,y+1].mine == 0):
            playboard[x-1,y+1].mine = 3
            if (x-1,y+1) in set_of_coords:
                set_of_coords.remove((x-1,y+1))
    if(isValid(x-1,y)):
        if(playboard[x-1,y].mine == 0):
            playboard[x-1,y].mine = 3
            if (x-1,y) in set_of_coords:
                set_of_coords.remove((x-1,y))
    if (isValid(x-1,y-1)):
        if(playboard[x-1,y-1].mine == 0):
            playboard[x-1,y-1].mine = 3
            if (x-1,y-1) in set_of_coords:
                set_of_coords.remove((x-1,y-1))
    if (isValid(x,y-1)):
        if(playboard[x,y-1].mine == 0):
            playboard[x,y-1].mine = 3
            if (x,y-1) in set_of_coords:
                set_of_coords.remove((x,y-1))
    if (isValid(x+1,y-1)):
        if(playboard[x+1,y-1].mine == 0):
            playboard[x+1,y-1].mine = 3
            if (x+1,y-1) in set_of_coords:
                set_of_coords.remove((x+1,y-1))

def set_hidden_to_safe(x,y):
    if (isValid(x+1,y)):
        if(playboard[x+1,y].mine == 0):
            playboard[x+1,y].mine = 2
    if (isValid(x+1,y+1)):
        if(playboard[x+1,y+1].mine == 0):
            playboard[x+1,y+1].mine = 2
    if (isValid(x,y+1)):
        if(playboard[x,y+1].mine == 0):
            playboard[x,y+1].mine = 2
    if (isValid(x-1,y+1)):
        if(playboard[x-1,y+1].mine == 0):
            playboard[x-1,y+1].mine = 2
    if(isValid(x-1,y)):
        if(playboard[x-1,y].mine == 0):
            playboard[x-1,y].mine = 2
    if (isValid(x-1,y-1)):
        if(playboard[x-1,y-1].mine == 0):
            playboard[x-1,y-1].mine = 2
    if (isValid(x,y-1)):
        if(playboard[x,y-1].mine == 0):
            playboard[x,y-1].mine = 2
    if (isValid(x+1,y-1)):
        if(playboard[x+1,y-1].mine == 0):
            playboard[x+1,y-1].mine = 2

matrix = createMine()
print(matrix)

def isValid(i, j):
    if(i>=0 and i<dim and j>=0 and j<dim):
        return True
    return False

#count mines around a specific index
def countMines(x, y, matrix):
    #get all 8 coordinates around a specific x,y coordinate and increment if it is a mine
    num_mines_around=0
    if(isValid(x+1, y)):
        if(matrix[x+1][y]==9):
            num_mines_around+=1
    if(isValid(x+1, y+1)):
        if(matrix[x+1][y+1]==9):
            num_mines_around+=1
    if(isValid(x, y+1)):
        if(matrix[x][y+1]==9):
            num_mines_around+=1
    if(isValid(x-1, y+1)):
        if(matrix[x-1][y+1]==9):
            num_mines_around+=1
    if(isValid(x-1, y)):
        if(matrix[x-1][y]==9):
            num_mines_around+=1
    if(isValid(x-1, y-1)):
        if(matrix[x-1][y-1]==9):
            num_mines_around+=1
    if(isValid(x, y-1)):
        if(matrix[x][y-1]==9):
            num_mines_around+=1
    if(isValid(x+1, y-1)):
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

set_of_coords = set()
for i in range(0, dim):
    for j in range(0, dim):
        set_of_coords.add((i,j))

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
    updateKB((v,w))
else:
    playboard[v,w].mine = 2
print((v,w))
# ans_board[v,w] = matrix[v,w]
while(matrix[v,w] != 0):
    v = random.randint(0,dim-1)
    w = random.randint(0,dim-1)
    playboard[v,w].num = matrix[v,w]
    print((v,w))

playboard = bfs_from_0(playboard,(v,w))



prev_len = -1
#while set size changes
bullshit = set_of_coords
for coords in set_of_coords:
    bullshit.add(coords)
while(len(set_of_coords)>=0):
    prev_len = len(set_of_coords)
    for coords in bullshit:
        x = coords[0]
        y = coords[1]
        if(playboard[x,y].mine == 2):
            if (playboard[x,y].num - playboard[x,y].numIdentMines == playboard[x,y].numHidden):
                updateKB((x,y))
                #make all numHidden as flag and remove flags from set_coords
                mark_as_flags(x,y)
                if (x,y) in set_of_coords:
                    set_of_coords.remove((x,y))
            if(playboard[x,y].num == playboard[x,y].numIdentMines):
                updateKB((x,y))
                #mark hidden neighbors as safe
                set_hidden_to_safe(x,y)
                if (x,y) in set_of_coords:
                    set_of_coords.remove((x,y))

                #check if any of the neighbors are 0
                if (isValid(x+1,y)):
                    if(playboard[x+1,y].num == 0):
                        bfs_from_0(playboard, ((x+1,y)))
                if (isValid(x+1,y+1)):
                    if(playboard[x+1,y+1].num == 0):
                        bfs_from_0(playboard, ((x+1,y+1)))
                if (isValid(x,y+1)):
                    if(playboard[x,y+1].num == 0):
                        bfs_from_0(playboard, ((x,y+1)))
                if (isValid(x-1,y+1)):
                    if(playboard[x-1,y+1].num == 0):
                        bfs_from_0(playboard, ((x-1,y+1)))
                if(isValid(x-1,y)):
                    if(playboard[x-1,y].num == 0):
                        bfs_from_0(playboard, ((x-1,y)))
                if (isValid(x-1,y-1)):
                    if(playboard[x-1,y-1].num == 0):
                        bfs_from_0(playboard, ((x-1,y-1)))
                if (isValid(x,y-1)):
                    if(playboard[x,y-1].num == 0):
                        bfs_from_0(playboard, ((x,y-1)))
                if (isValid(x+1,y-1)):
                    if(playboard[x+1,y-1].num == 0):
                        bfs_from_0(playboard, ((x+1,y-1)))

    bullshit = set()
    for coords in set_of_coords:
        bullshit.add(coords)
    #check for size of set if same
    if(prev_len == len(set_of_coords)):
        #generate a new random number
        randCoord = set_of_coords.pop()
        set_of_coords.add(randCoord)

        v = randCoord[0]
        w = randCoord[1]
        playboard[v,w].num = matrix[v,w]
        while (v,w) not in set_of_coords:
            randCoord = set_of_coords.pop()
            set_of_coords.add(randCoord)
            v = randCoord[0]
            w = randCoord[1]
            playboard[v,w].num = matrix[v,w]
            #print((v,w))
            updateKB((v,w))




graphics.display_graphics(playboard, dim)

print(playboard)
