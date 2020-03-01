import numpy as np
import sympy as sp
from func import isValid


def populateEQMap(dim, playboard, explored):
    equation_map = sp.zeros(1,dim*dim+1) #zeros in format of (# rows, # columns)
    rows = 0
    print("---------------------------------------------")

    for val in explored:
        x = val[0]
        y = val[1]
        #if item in explored set is safe, add its numMines to end of row in eq_map, then examine its neighbors
        if playboard[x,y].mine==2:
            if rows != 0:
                equation_map = equation_map.row_insert(rows, sp.zeros(1,dim*dim+1))
            print("(",x,",",y,")")
            equation_map[rows,dim*dim] = playboard[x,y].num - playboard[x,y].numIdentMines

            #check all neighbors and if it is hidden, change its index in eq_map to 1=
            if (isValid(dim,x+1,y) and playboard[x,y].mine ==0):
                equation_map[rows,dim*(x+1)+y] = 1
                print("hola muchacho",rows)
            if (isValid(dim,x+1,y+1) and playboard[x,y].mine ==0):
                print("hola muchacho",rows)
                equation_map[rows,dim*(x+1)+(y+1)] = 1
            if (isValid(dim,x,y+1) and playboard[x,y].mine ==0):
                print("hola muchacho",rows)
                equation_map[rows,dim*(x)+y+1] = 1
            if (isValid(dim,x-1,y+1) and playboard[x,y].mine ==0):
                print("hola muchacho",rows)
                equation_map[rows,dim*(x-1)+y+1] = 1
            if(isValid(dim,x-1,y) and playboard[x,y].mine ==0):
                print("hola muchacho",rows)
                equation_map[rows,dim*(x-1)+y] = 1
            if (isValid(dim,x-1,y-1) and playboard[x,y].mine ==0):
                print("hola muchacho",rows)
                equation_map[rows,dim*(x-1)+y-1] = 1
            if (isValid(dim,x,y-1) and playboard[x,y].mine ==0):
                print("hola muchacho",rows)
                equation_map[rows,dim*(x)+y-1] = 1
            if (isValid(dim,x+1,y-1) and playboard[x,y].mine ==0):
                print("hola muchacho",rows)
                equation_map[rows,dim*(x+1)+y-1] = 1
        rows+=1
    return equation_map

#def solveEqs(equation_map):
#    #fill this
#    #find variables
#    return
#


#need to call populateEQMap in main after strategy 2.1
#then need to solve equation_map and update kb for variables found

