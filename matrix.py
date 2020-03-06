import numpy as np
from dataclasses import dataclass
import random
import pprint
from scipy import linalg
from sympy import *


A = Matrix([[1,1,1,0,0,0,0,0,0,0,0,0,1],
            [0,1,1,1,0,0,0,0,0,0,0,0,2],
            [0,0,1,1,1,0,0,0,0,0,0,0,1],
            [0,0,0,1,1,1,0,0,0,0,0,0,2],
            [0,0,0,0,1,1,1,0,0,0,0,0,1],
            [0,0,0,0,0,1,1,1,1,1,0,0,2],
            [0,0,0,0,0,0,0,0,1,1,1,0,1],
            [0,0,0,0,0,0,0,0,0,1,1,1,2],
            [0,0,0,0,0,0,0,0,0,0,1,1,1]])
#z= np.linalg.solve(A, b)
z = Matrix(A).rref()
dim = 10
matrixlen= 13
rows = 9
solList =[]
p = Matrix(z[0])
#print(p)
#print( p.row(0).col(0))
#convert to numpy array

def convertmatrix(rows, matrixlen, p):
    mat= np.empty([rows, matrixlen],dtype=int)
    for i in range(0, rows):
        for j in range(0, matrixlen):
            mat[i][j]=p.row(i).col(j).dot([1])
    #pprint (mat)
    return mat


def matsolve(mat):
    for i in range (len(mat)):
        ones=[]
        negs=[]
        sol=0
        for j in range (len(mat[0])-1):
            #print(mat[i][j])
            if mat[i][j]==1:
                #print("hi")
                ones.append(j)
            if mat[i][j]== -1:
                negs.append(j)
        sol= mat[i][j+1]
        if len(ones) == 1 and sol == 1:
            solList.append([ones[0], 1])
            #set everthing else in the list equal to zeros
            for k in range (len(negs)):
                solList.append([negs[k], 0])
        if len(ones) == 1 and len(negs) == 0 and sol == 0:
            solList.append([ones[0], 0])
        if len(ones) == 0 and sol == 0 and len(negs)!= 0:
            solList.append([ones[0], 1])
            #set everthing else in the list equal to zeros
            for k in range (len(negs)):
                solList.append([negs[k], 0])
        if len(ones) == 1 and sol == -1 and len(negs)== 1:
            solList.append([ones[0], 0])
            solList.append([negs[0], 1])
    print (solList)
    return solList

def matsubs(mat, solList):
    for i in range (len(solList)):
        for j in range (len(mat)):
            '''
            print("index ", j,solList[i][0])
            print("------------------------------------------------")
            '''
            l = (-1)*solList[i][1]*mat[j][solList[i][0]]
            #print(mat[j][len(mat[0])-1])
            if mat[j][solList[i][0]]!=0:
                mat[j][len(mat[0])-1] = mat[j][len(mat[0])-1] + l
                mat[j][solList[i][0]]= 0
    #pprint( mat)
    return mat
#check if the matrix is solved
def matsolved(mat):
    for i in range (len(mat)):
        for j in range (len(mat[0])):
            if mat[i][j] != 0:
                return False
    return True


mat = convertmatrix(rows, matrixlen, p)
prevmat= np.empty([len(mat),len(mat[0])], dtype=int)
for i in range (len(mat)):
    for j in range (len(mat[0])):
        prevmat[i][j] = mat[i][j]
while matsolved(mat) == False:
    print ("matb4", mat)
    solList = matsolve(mat)
    mat = matsubs(mat, solList)
    print("prevmat", prevmat)
    print("mat", mat)
    if  np.array_equal (prevmat, mat) ==True:
        print("hi")
        break
    for i in range (len(mat)):
        for j in range (len(mat[0])):
            prevmat[i][j] = mat[i][j]
print (solList)
'''

mat = matsubs(mat, solList)
solList = matsolve(mat)
#prevmat = 1
mat = matsubs(mat, solList)
    #pprint("currmat ", mat)
'''
