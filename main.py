#!/usr/bin/python
import time
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

#fills a matrix of size dim*dim with num_mines many mines
dim = 10
num_mines = 20

#returns a list of all valid neighbors around a specific coordinate
def getValidNeighbors(coord):
    x = coord[0]
    y = coord[1]
    list = []
    if (isValid(dim,x+1,y)):
        list.append((x+1,y))
    if (isValid(dim,x+1,y+1)):
        list.append((x+1,y+1))
    if (isValid(dim,x,y+1)):
        list.append((x,y+1))
    if (isValid(dim,x-1,y+1)):
        list.append((x-1,y+1))
    if(isValid(dim,x-1,y)):
        list.append((x-1,y))
    if (isValid(dim,x-1,y-1)):
        list.append((x-1,y-1))
    if (isValid(dim,x,y-1)):
        list.append((x,y-1))
    if (isValid(dim,x+1,y-1)):
        list.append((x+1,y-1))
    return list

#initialize knowledge base with number of hidden squares in each coordinate of board
def setHidden(playboard):
    #coordinates that are not corner and edge have 8 hidden spots around them
    for i in range(1,dim-1):
        for j in range(1,dim-1):
            playboard[i,j].numHidden = 8

    #corner coordinates have 3 hidden spots around them
    playboard[0,0].numHidden = 3
    playboard[0,dim-1].numHidden = 3
    playboard[dim-1,0].numHidden = 3
    playboard[dim-1,dim-1].numHidden = 3

    #edge coordinates have 5 hidden spots around them
    for i in range(1,dim-1):
        playboard[0,i].numHidden = 5
        playboard[i,0].numHidden = 5
        playboard[dim-1,i].numHidden = 5
        playboard[i,dim-1].numHidden = 5

#updates knowledge base
def updateKB(playboard, coord):
    x = coord[0]
    y = coord[1]
    #if coordinate is a 9 means a mine, so increase all identified mines by 1, and decrease hidden by 1 of neighbors
    if (matrix[x,y] == 9):
        if (playboard[x,y].mine != 3):
            playboard[x,y].mine = 1
        list = getValidNeighbors((x,y))
        for coords in list:
            x = coords[0]
            y = coords[1]
            playboard[x,y].numIdentMines+=1
            playboard[x,y].numHidden-=1

    else:
    #if coordinate is not a mine increase neighbors safe and decrease neighbors hidden
        playboard[x,y].mine = 2
        playboard[x,y].num = matrix[x,y]
        list = getValidNeighbors((x,y))
        for coords in list:
            x = coords[0]
            y = coords[1]
            playboard[x,y].numSafe+=1
            playboard[x,y].numHidden-=1
            if(playboard[x,y].num == 0):
                playboard[x,y].mine = 2
                playboard[x,y].num = matrix[x,y]

#method that looks at a 0 coordinate and expands outwards until it hits a number in all directions
def bfs_from_0(playboard, start): #start has to be in format (i,j) as a tuple
    explored = set()
    queue = [start]

    while queue:
        node = queue.pop(0)
        x = node[0]
        y = node[1]
        if node not in explored:
            # print((x,y),playboard[x,y])
            if (x,y) not in knowledge_expanded:
                updateKB(playboard,(x,y))
                knowledge_expanded.add((x,y))

            explored.add(node)
            if (x,y) in set_of_coords:
                set_of_coords.remove((x,y))

            list = getValidNeighbors((x,y))
            for coords in list:
                x = coords[0]
                y = coords[1]
                if (matrix[x,y] == 0):
                    queue.append((x,y))
                else:
                    if (x,y) not in knowledge_expanded:
                        updateKB(playboard,(x,y))
                        knowledge_expanded.add((x,y))
                playboard[x,y].num = matrix[x,y]

    return playboard

#method to randomly initialize board with num_mines many mines
def createMine():
    random_matrix = np.zeros((dim, dim), dtype=np.int)
    mine_location = set()
    while len(mine_location)!= num_mines:
        value = np.random.randint(dim*dim)
        if(value not in mine_location):
            mine_location.add(value)
            x = int(value%dim)
            y = int(value/dim)
            random_matrix[x,y] = 9 #numerical representation of mine

    return random_matrix

#method to mark coordinates that satisfy condition numMines - numIdentMines = numHidden as flags
def mark_as_flags(x,y):
    list = getValidNeighbors((x,y))
    print("list",(x,y),list)
    for coords in list:
        x = coords[0]
        y = coords[1]
        if (playboard[x,y].mine == 0):
            print("turning into flag: ",(x,y))
            playboard[x,y].mine = 3

            if (x,y) in set_of_coords:
                set_of_coords.remove((x,y))
            if (x,y) not in knowledge_expanded:
                updateKB(playboard, (x,y))
                knowledge_expanded.add((x,y))
            print(playboard[x,y].mine)

#marking all neighbors that are safe as safe
def set_hidden_to_safe(x,y):
    list = getValidNeighbors((x,y))
    for coords in list:
        x = coords[0]
        y = coords[1]
        if (playboard[x,y].mine == 0):
            playboard[x,y].mine = 2
            if (x,y) not in knowledge_expanded:
                updateKB(playboard, (x,y))
                knowledge_expanded.add((x,y))

matrix = createMine()
print(matrix)

#check if coordinate is valid within the board
def isValid(dim,i, j):
    if(i>=0 and i<dim and j>=0 and j<dim):
        return True
    return False

#count mines around a specific index
def countMines(x, y, matrix):
    #get all 8 coordinates around a specific x,y coordinate and increment if it is a mine
    num_mines_around=0
    list = getValidNeighbors((x,y))
    for coords in list:
        x = coords[0]
        y = coords[1]
        if(matrix[x][y]==9):
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
knowledge_expanded = set()
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
if (matrix[v,w] != 0):
    if (matrix[v,w] == 9):
        playboard[v,w].mine = 1
    else:
        playboard[v,w].mine = 2
    if (v,w) not in knowledge_expanded:
        updateKB(playboard,(v,w))
        knowledge_expanded.add((v,w))
print("random",(v,w))
# ans_board[v,w] = matrix[v,w]
while(matrix[v,w] != 0):
    v = random.randint(0,dim-1)
    w = random.randint(0,dim-1)
    playboard[v,w].num = matrix[v,w]
    if (v,w) not in knowledge_expanded:
        updateKB(playboard,(v,w))
        knowledge_expanded.add((v,w))
    print((v,w))
print(agent2.populateEQMap(dim,playboard,set_of_coords))
playboard = bfs_from_0(playboard,(v,w))
for i in range(0,dim):
    for j in range(0,dim):
        print((i,j), playboard[i,j])

#while set size changes
deep_copy = set()
for coords in set_of_coords:
    deep_copy.add(coords)
while(len(set_of_coords)>0):
    graphics.display_graphics(playboard, dim)

    prev_len = len(set_of_coords)
    for coords in deep_copy:
        x = coords[0]
        y = coords[1]
        # print((x,y), playboard[x,y])
        if(playboard[x,y].mine == 2):
            if (playboard[x,y].num - playboard[x,y].numIdentMines == playboard[x,y].numHidden):
                print((x,y), "checkpoint 1")
                #make all numHidden as flag and remove flags from set_coords
                mark_as_flags(x,y)
                if (x,y) in set_of_coords:
                    set_of_coords.remove((x,y))
            if(playboard[x,y].num == playboard[x,y].numIdentMines):
                print("checkpoint 2")
                #mark hidden neighbors as safe
                set_hidden_to_safe(x,y)
                if (x,y) in set_of_coords:
                    set_of_coords.remove((x,y))

                #check if any of the neighbors are 0
                list = getValidNeighbors((x,y))
                for coords in list:
                    x = coords[0]
                    y = coords[1]
                    if(playboard[x,y].num == 0):
                        bfs_from_0(playboard, (x,y))


    deep_copy = set()
    for coords in set_of_coords:
        deep_copy.add(coords)
        #check for size of set if same
    if(prev_len == len(set_of_coords)):
        #generate a new random number
        if (len(set_of_coords) > 0):
            randCoord = set_of_coords.pop()
            set_of_coords.add(randCoord)
        v = randCoord[0]
        w = randCoord[1]
        print("Rand2", (v,w))
        playboard[v,w].num = matrix[v,w]
        if (v,w) not in knowledge_expanded:
            updateKB(playboard,(v,w))
            knowledge_expanded.add((v,w))
        if (v,w) in set_of_coords:
            set_of_coords.remove((v,w))

for i in range(0,dim):
    for j in range(0,dim):
        if (i,j) in set_of_coords:
            print((i,j), playboard[i,j])


#print(agent2.populateEQMap(dim,playboard,set_of_coords))
#graphics.display_graphics(playboard, dim)

print(playboard)
