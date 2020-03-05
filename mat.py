from pprint import pprint
from test import *

#mat = np.array([[1,2,0,1,0,0], [0,0,0,3,0,0],[0,0,1,3,1,0],[0,0,0,0,0,1]], dtype = float)
# mat = np.array([[0,1,2], [1,2,1],[2,7,8]], dtype = float)
mat = np.array([[0,1], [1,2],[0,5]], dtype = float)

def rref(mat):
	print("-------------------ORIGINAL MATRIX-------------------")
	pprint(mat)

	rows = mat.shape[0]
	cols = mat.shape[1]


	#organize rows in order of # of starting zeros (least to greatest)
	r = 0
	for a in range(0, cols):
		for b in range(r,rows):
			if mat[b][a] != 0:
				interchange(cols,mat,b,r)
				r+=1
			if r == rows:
				break


	#reduce the rows
	for i in range(0,rows):
		f=0
		while (f<cols and mat[i][f] == 0):
			f+=1

		#if it is a row of zeros, move to the next line
		if f == cols:
			continue

		#make all the other numbers in the col = 0
		if mat[i][f] == 1: #if pivot is already a 1, just change everything else in its column
			for j in range(0,rows):
				if j==i:
					continue
				add_mult(cols,mat,-mat[j][f],i,j)
			continue
		if mat[i][f] != 1: #make pivot 1 before changing everything else in the column
			multiply_const(cols,mat,1/mat[i][f],i)
			for j in range(0,rows):
				if j==i:
					continue
				add_mult(cols,mat,-mat[j][f],i,j)


	#organize rows in order of # of starting zeros (least to greatest) - aka put rows of zeros at end
	r = 0
	for a in range(0, cols):
		for b in range(r,rows):
			if mat[b][a] != 0:
				interchange(cols,mat,b,r)
				r+=1
			if r == rows:
				break
	print("-------------------FINAL RREF-------------------")
	pprint(mat)

#run rref
rref(mat)
