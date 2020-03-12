import numpy as np
from dataclasses import dataclass
import random
import pprint



#make sure no elements repeat in a list
def norepeats(k,solList):
    for i in solList:
        if i[0] == k:
            return False
    return True

#solve the given matrix
def matsolve(mat,solList):
    for i in range (len(mat)):
        ones=[]
        negs=[]
        sol=0

        #add all 1's and -1's to appropriate list
        for j in range (len(mat[0])-1):
            if mat[i][j]==1:
                ones.append(j)
            if mat[i][j]== -1:
                negs.append(j)

        #find the clue in the last column of the matrix
        sol = mat[i][j+1]

        #if there is only one variable with a coefficient of 1, and the clue = 1, then that variable = 1 and all other variables = 0
        if len(ones) == 1 and sol == 1:
            if norepeats(ones[0],solList):
                solList.append([ones[0], 1])
            #set everthing else in the list equal to zeros
            for k in range (len(negs)):
                if norepeats(negs[k],solList):
                    solList.append([negs[k], 0])
        #if there are no coefficients of -1 and the clue = 0, then all variables with coefficient 1 are also 0
        if len(negs) == 0 and sol == 0:
            for k in ones:
                if norepeats(k,solList):
                    solList.append([k,0])
        #if there are no coefficients of 1 and the clue = 0, then all variables with coefficient -1 are also 0
        if len(ones) == 0 and sol == 0:
            for k in negs:
                if norepeats(k,solList):
                    solList.append([k,0])
        #if there is only one variable with coefficient 1, one variable with coeff. -1, and the solution is -1, then the variable with coeff. 1 is 0 and the other variable is 1
        if len(ones) == 1 and sol == -1 and len(negs)== 1: # can this change to: if sol == -1 and len(negs)== 1:
            if norepeats(ones[0],solList):
                solList.append([ones[0], 0])
            if norepeats(negs[0],solList):
                solList.append([negs[0], 1])
    return solList

def matsubs(mat, solList):
    for i in range (len(solList)):
        for j in range (len(mat)):
            l = (-1)*solList[i][1]*mat[j][solList[i][0]]
            if mat[j][solList[i][0]]!=0:
                mat[j][len(mat[0])-1] = mat[j][len(mat[0])-1] + l
                mat[j][solList[i][0]]= 0
    return mat

#check if the matrix is solved
def matsolved(mat):
    for i in range (len(mat)):
        for j in range (len(mat[0])):
            if mat[i][j] != 0:
                return False
    return True


def solvematrix(mat):
    solList = []
    prevmat= np.empty([len(mat),len(mat[0])], dtype=int)
    for i in range (len(mat)):
        for j in range (len(mat[0])):
            prevmat[i][j] = mat[i][j]

    solList = matsolve(mat,solList)
    # ctr = 0
    # while matsolved(mat) == False:
    #     ctr+=1
    #     print(ctr)
    #     if(ctr>4):
    #         break
        
    #     solList = matsolve(mat,solList)
    #     mat = matsubs(mat, solList)
    #     if  np.array_equal (prevmat, mat) ==True:
    #         break
    #     for i in range (len(mat)):
    #         for j in range (len(mat[0])):
    #             prevmat[i][j] = mat[i][j]
    return(solList)


