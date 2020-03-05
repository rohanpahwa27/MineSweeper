import numpy as np


#add a multiple of one row of a matrix to another row
def add_mult(dim,mat,constant, row_orig, row_to_modify):
    for i in range(0, dim): #dim
        val = mat[row_orig, i]*constant
        mat[row_to_modify, i] += val

#interchange two rows of a matrix
def interchange(dim,mat,swap1, swap2):
    for i in range(0, dim):
        val = mat[swap1, i]
        mat[swap1, i] = mat[swap2,i]
        mat[swap2, i] = val

#multiply one row of a matrix by -1
def multiply_neg(dim,mat,row):
    for i in range(0, dim):
        mat[row, i] *= -1

def multiply_const(dim,mat,constant,row):
	for i in range(0,dim):
		mat[row,i] *= constant

