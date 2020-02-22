import numpy as np

def createMine():
    dim = 10
    num_mines = 5
    random_matrix = np.random.randint(1,size=(dim,dim))

    mine_location = set()
    #for i in range(0, num_mines):
    while len(mine_location)!= num_mines:
        value = np.random.randint(dim*dim)
        if(value not in mine_location):
            mine_location.add(value)
            x = int(value%dim)
            y = int(value/dim)
            random_matrix[x][y] = 1

    print(random_matrix)

createMine()