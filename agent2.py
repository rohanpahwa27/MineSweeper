import numpy as np
#import sympy as sp
from func import *
from mat import rref
from pprint import pprint
from matrix import *


def populateEQMap(dim, playboard, explored, matrix, clicked):
    #equation_map = sp.zeros(1,dim*dim+1) #zeros in format of (# rows, # columns)
    equation_map = np.zeros((1,dim*dim+1)) #zeros in format of (# rows, # columns)
    rows = 0
    #print("---------------------------------------------")

    for val in explored:
        x = val[0]
        y = val[1]
        #if item in explored set is safe, add its numMines to end of row in eq_map, then examine its neighbors
        if playboard[x,y].mine==2:
            if rows != 0:
                #equation_map = equation_map.row_insert(rows, np.zeros((1,dim*dim+1)))
                equation_map = np.append(equation_map, np.zeros((1,dim*dim+1)),axis = 0)
#            print("(",x,",",y,")")
#            print(rows)
#            print(dim*dim)
#            print(equation_map.shape)
            equation_map[rows,dim*dim] = playboard[x,y].num - playboard[x,y].numIdentMines
#            print(playboard[x,y].num)
#            print(playboard[x,y].numIdentMines)

            #check all neighbors and if it is hidden, change its index in eq_map to 1=
            list = getValidNeighbors((x,y), dim)
            for coords in list:
                x = coords[0]
                y = coords[1]
                if(playboard[x,y].mine == 0):
                    equation_map[rows,dim*x+y] = 1
            rows+=1
    # pprint(equation_map)

    #reduce row echelon equation_map, and then solve for values of variables (can only be 0 or 1)
    rref_equation_map = rref(equation_map)
    #feed rref_equation_map into matrix.py --> return list of solutions
    sols = []
    sols = solvematrix(equation_map)
    for item in sols:
      a,b = divmod(item[0], dim)
      if item[1] == 0:
        playboard[a][b].mine = 2
        updateKB(playboard,(a,b),dim,matrix,clicked)
        print("used agent 2 to update safe: ",(a,b))
      if item[1] == 1:
        playboard[a][b].mine = 1
        updateKB(playboard,(a,b),dim,matrix,clicked)
        print("used agent 2 to update mine: ",(a,b))

    # for i in range (len(sols)):
    #   a, b = divmod(sols[i][0], dim)
    #   if sols[i][1]==0:
    #       playboard[a][b].mine=2
    
    
        
    




#need to call populateEQMap in main after strategy 2.1
#then need to solve equation_map and update kb for variables found
