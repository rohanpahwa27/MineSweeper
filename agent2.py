import numpy as np
#import sympy as sp
from func import *
from mat import rref
from pprint import pprint
from matrix import *


def populateEQMap(dim, playboard, explored, matrix, clicked, knowledge_expanded):
    # print("THE SIZE OF EXPLORED IS FIRST", len(explored))
    # print("set_of_coords:")
    # pprint(explored)
    equation_map = np.zeros((1,dim*dim+1)) #zeros in format of (# rows, # columns)
    # print("size ", equation_map.shape)
    rows = 0
    #print("---------=[]
    toberem = []
    # for val in explored:
    #     x = val[0]
    #     y = val[1]
    #     if playboard[x,y].mine == 2 and playboard[x,y].num != playboard[x,y].numIdentMines:
    #         boolshit.add((x,y))
    #     elif playboard[x,y].mine == 0:
    #         boolshit.add((x,y))
    
    # for i in range(len(explored)):
    #     explored.pop()

    for val in explored:
        x = val[0]
        y = val[1]
        # print("HELP ME",playboard[x,y].mine,playboard[x,y].num)
        # print(matrix[x,y])
        # print("X IS", x)
        # print("Y IS", y)
        # #print("Y,X is",playboard[y,x].mine, playboard[y,x].num)
        # print("X,Y is",playboard[x,y].mine, playboard[x,y].num)
        #if item in explored set is safe, add its numMines to end of row in eq_map, then examine its neighbors
        if playboard[x,y].mine==2:
            #if there are 0 surrounding mines, do not add to matrix
            if playboard[x,y].num == playboard[x,y].numIdentMines:
                toberem.append((x,y))
                continue
            #print("HELP", playboard[x,y].num, playboard[x,y].num-playboard[x,y].numIdentMines)

            if rows != 0:
                equation_map = np.append(equation_map, np.zeros((1,dim*dim+1)),axis = 0)

            equation_map[rows,dim*dim] = playboard[x,y].num - playboard[x,y].numIdentMines

            #check all neighbors and if it is hidden, change its index in eq_map to 1
            list = getValidNeighbors((x,y), dim)
            for coords in list:
                x = coords[0]
                y = coords[1]
                if(playboard[x,y].mine == 0):
                    #print(x, "*", y, "=", dim*x+y)
                    equation_map[rows,dim*x+y] = 1
            rows+=1
    # pprint(equation_map)

    #reduce row echelon equation_map, and then solve for values of variables (can only be 0 or 1)
    rref_equation_map = rref(equation_map)
    #pprint ("ref eq map ", rref_equation_map)
    #feed rref_equation_map into matrix.py --> return list of solutions

    #print("THE SIZE OF BS IS CURRENTLY", len(boolshit))
    # explored = set()
    sols = []
    sols = solvematrix(equation_map)
    for item in sols:
        a = int(item[0]/dim) #row number
        b = item[0]%dim #col number
        # print("num ", item[0])
        # print("a",a)
        # print("b",b)
        # print("this is supposed to be", matrix[a,b])
        if item[1] == 0:
            playboard[a,b].mine = 2
            playboard[a,b].num = matrix[a,b]
            if (b,a) not in clicked:
                clicked.append((b,a))
                # print("marked as appended", (a,b))
            updateKB(playboard,(a,b),dim,matrix,clicked)
            print("used agent 2 to update safe: ",(a,b))
            if playboard[a,b].num == playboard[a,b].numIdentMines:
                explored.remove((a,b))
        if item[1] == 1:
            playboard[a,b].mine = 3 #mark as a flag
            #updateKB(playboard,(a,b),dim,matrix,clicked)
            if (b,a) not in clicked:
                clicked.append((b,a))
                # print("marked as appended", (a,b))
            updateKB(playboard,(a,b),dim,matrix,clicked)
            print("used agent 2 to update mine: ",(a,b))
            explored.remove((a,b))

    for item in toberem:
        explored.remove(item)
    # print("THE SIZE OF EXPLORED IS CURRENTLY", len(explored))

    #return explored
    # print("in agent 2")
    # pprint(explored)
    #return explored
    # for i in range (len(sols)):
    #   a, b = divmod(sols[i][0], dim)
    #   if sols[i][1]==0:
    #       playboard[a][b].mine=2
    
    
        
    




#need to call populateEQMap in main after strategy 2.1
#then need to solve equation_map and update kb for variables found
