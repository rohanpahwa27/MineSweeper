from pprint import pprint
from test import *

#find the reduced row echelon form of any matrix
def rref(matrix):

	#determine the number of rows and columns
	rows = matrix.shape[0]
	cols = matrix.shape[1]


	#organize rows in order of # of starting zeros (least to greatest)
	r = 0
	for a in range(0, cols):
		for b in range(r,rows):
			if matrix[b][a] != 0:
				interchange(cols,matrix,b,r)
				r+=1
			if r == rows:
				break


	#reduce the rows
	for i in range(0,rows):
		f=0
		while (f<cols and matrix[i][f] == 0):
			f+=1

		#if it is a row of zeros, move to the next line
		if f == cols:
			continue

		#make all the other numbers in the col = 0
		if matrix[i][f] == 1: #if pivot is already a 1, just change everything else in its column
			for j in range(0,rows):
				if j==i:
					continue
				add_mult(cols,matrix,-matrix[j][f],i,j)
			continue
		if matrix[i][f] != 1: #make pivot 1 before changing everything else in the column
			multiply_const(cols,matrix,1/matrix[i][f],i)
			for j in range(0,rows):
				if j==i:
					continue
				add_mult(cols,matrix,-matrix[j][f],i,j)


	#organize rows in order of # of starting zeros (least to greatest) - aka put rows of zeros at end
	r = 0
	for a in range(0, cols):
		for b in range(r,rows):
			if matrix[b][a] != 0:
				interchange(cols,matrix,b,r)
				r+=1
			if r == rows:
				break
