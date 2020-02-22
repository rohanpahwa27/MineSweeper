import numpy as np

dim = 10
num_mines = 5
#fills a matrix of size dim*dim with num_mines many mines
def createMine():

    #random_matrix = np.random.randint(1,size=(dim,dim))
    random_matrix = np.zeros((dim, dim), dtype=np.int)
    mine_location = set()
    #for i in range(0, num_mines):
    while len(mine_location)!= num_mines:
        value = np.random.randint(dim*dim)
        if(value not in mine_location):
            mine_location.add(value)
            x = int(value%dim)
            y = int(value/dim)
            random_matrix[x,y] = 9 #numerical representation of mine

    return random_matrix

matrix = createMine()
print(matrix)

def isValid(i, j):
    if(i>=0 and i<dim and j>=0 and j<dim):
        return True
    return False

#count mines around a specific index
def countMines(x, y, matrix):
    #get all 8 coordinates around a specific x,y coordinate and increment if it is a mine
    num_mines_around=0
    if(isValid(x+1, y)):
        if(matrix[x+1][y]==9):
            num_mines_around+=1
    if(isValid(x+1, y+1)):
        if(matrix[x+1][y+1]==9):
            num_mines_around+=1
    if(isValid(x, y+1)):
        if(matrix[x][y+1]==9):
            num_mines_around+=1
    if(isValid(x-1, y+1)):
        if(matrix[x-1][y+1]==9):
            num_mines_around+=1
    if(isValid(x-1, y)):
        if(matrix[x-1][y]==9):
            num_mines_around+=1
    if(isValid(x-1, y-1)):
        if(matrix[x-1][y-1]==9):
            num_mines_around+=1
    if(isValid(x, y-1)):
        if(matrix[x][y-1]==9):
            num_mines_around+=1
    if(isValid(x+1, y-1)):
        if(matrix[x+1][y-1]==9):
            num_mines_around+=1
    return num_mines_around

for i in range(0, dim):
    for j in range(0, dim):
        if(matrix[i,j]!=9):
            mine_num = countMines(i,j,matrix)
            matrix[i, j] = mine_num

print("---------ANSWER-------KEY-----------------------")
print(matrix)
