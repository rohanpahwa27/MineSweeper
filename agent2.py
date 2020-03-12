import numpy as np
#import sympy as sp
from func import *
from mat import rref
from pprint import pprint
from matrix import *


def populateEQMap(dim, playboard, explored, matrix, clicked, knowledge_expanded, flag_counter, num_mines, agent3):
    #make a row of dim*dim+1 zeros
    equation_map = np.zeros((1,dim*dim+1)) #zeros in format of (# rows, # columns)
    rows = 0
    toberem = []

    #if agent 3 is called, add a boundary condition using number of mines remaining
    if agent3:
        equation_map[0][dim*dim] = num_mines - findBombs(playboard)

    #go through each element of set_of_coords
    for val in explored:
        x = val[0]
        y = val[1]

        #if agent 3 is called, add a boundary condition using number of mines remaining
        if agent3:
            if playboard[x,y].mine == 0:
                equation_map[0][dim*x+y] = 1
            if rows == 0:
                rows += 1

        #if item in explored set is safe, add its numMines to end of row in eq_map, then examine its neighbors
        if playboard[x,y].mine==2:
            #if there are 0 surrounding mines, do not add to matrix
            if playboard[x,y].num == playboard[x,y].numIdentMines:
                toberem.append((x,y))
                continue
            #add a row of zeros to matrix in order to store new data
            if rows != 0:
                equation_map = np.append(equation_map, np.zeros((1,dim*dim+1)),axis = 0)

            #add number of remaining surrounding mines to final column of matrix
            equation_map[rows,dim*dim] = playboard[x,y].num - playboard[x,y].numIdentMines

            #check all neighbors and if it is hidden, change its index in eq_map to 1
            list = getValidNeighbors((x,y), dim)
            for coords in list:
                x = coords[0]
                y = coords[1]
                if(playboard[x,y].mine == 0):
                    equation_map[rows,dim*x+y] = 1
            rows+=1
   

    #reduce row echelon equation_map, and then solve for values of variables (can only be 0 or 1)
    rref_equation_map = rref(equation_map)

    #solve the matrix, which returns in a list of solutions
    sols = []
    sols = solvematrix(equation_map)

    #go through list of solutions and update playboard accordingly
    for item in sols:
        a = int(item[0]/dim) #row number
        b = item[0]%dim #col number

        #if coordinate returns a 0, it is safe, so reveal the clue, update neighbors, and remove from explored
        if item[1] == 0:
            playboard[a,b].mine = 2
            playboard[a,b].num = matrix[a,b]
            if (b,a) not in clicked:
                clicked.append((b,a))
            updateKB(playboard,(a,b),dim,matrix,clicked)
            if playboard[a,b].num == playboard[a,b].numIdentMines:
                explored.remove((a,b))
        #if coordinate returns a 1, it is a mine, so flag it, update neighbors, and remove from explored
        if item[1] == 1:
            playboard[a,b].mine = 3 #mark as a flag
            flag_counter+=1
            if (b,a) not in clicked:
                clicked.append((b,a))
            updateKB(playboard,(a,b),dim,matrix,clicked)
            explored.remove((a,b))

    #remove any items from explored where all surrounding mines have been found
    for item in toberem:
        explored.remove(item)

    return flag_counter


