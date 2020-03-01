import numpy as np

def populateEQMap(dim, playboard, equation_map):
    rows = 0
    zeeros = np.zeros(dim*dim+1, dtype=int)
    for val in set_of_cords:
        x = val[0]
        y = val[1]
        if playboard[x,y].mine==2:
            equation_map.append(zeeros)
            eq_ind = dim*x+y
            equation_map[rows][dim*dim] = playboard[x][y].num - playboard[x][y].numIdentMines
            if (isValid(x+1,y) and playboard[x][y].mine ==0):
                equation_map[rows][dim*(x+1)+y] = 1
            if (isValid(x+1,y+1) and playboard[x][y].mine ==0):
                equation_map[rows][dim*(x+1)+(y+1)] = 1
            if (isValid(x,y+1) and playboard[x][y].mine ==0):
                equation_map[rows][dim*(x)+y+1] = 1
            if (isValid(x-1,y+1) and playboard[x][y].mine ==0):
                equation_map[rows][dim*(x-1)+y+1] = 1
            if(isValid(x-1,y) and playboard[x][y].mine ==0):
                equation_map[rows][dim*(x-1)+y] = 1
            if (isValid(x-1,y-1) and playboard[x][y].mine ==0):
                equation_map[rows][dim*(x-1)+y-1] = 1
            if (isValid(x,y-1) and playboard[x][y].mine ==0):
                equation_map[rows][dim*(x)+y-1] = 1
            if (isValid(x+1,y-1) and playboard[x][y].mine ==0):
                equation_map[rows][dim*(x+1)+y-1] = 1
        rows+=1
    return equation_map

def solveLinear(dim, matrix):
    equation_map =  numpy.zeros((0,dim*dim+1))
    equation_map = populateEQMap(dim, matrix, equation_map)
