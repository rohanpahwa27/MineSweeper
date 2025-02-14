import numpy as np

#method that finds how many bombs have been flagged or exploded
def findBombs(playboard):
    mines = 0
    for i in range(len(playboard)):
        for j in range(len(playboard)):
            if playboard[i,j].mine == 1 or playboard[i,j].mine == 3:
                mines+=1
    return mines

#returns a list of all valid neighbors around a specific coordinate
def getValidNeighbors(coord, dim):
    x = coord[0]
    y = coord[1]
    list = []
    if (isValid(dim,x+1,y)):
        list.append((x+1,y))
    if (isValid(dim,x+1,y+1)):
        list.append((x+1,y+1))
    if (isValid(dim,x,y+1)):
        list.append((x,y+1))
    if (isValid(dim,x-1,y+1)):
        list.append((x-1,y+1))
    if(isValid(dim,x-1,y)):
        list.append((x-1,y))
    if (isValid(dim,x-1,y-1)):
        list.append((x-1,y-1))
    if (isValid(dim,x,y-1)):
        list.append((x,y-1))
    if (isValid(dim,x+1,y-1)):
        list.append((x+1,y-1))
    return list

#initialize knowledge base with number of hidden squares in each coordinate of board
def setHidden(playboard, dim):
    #coordinates that are not corner and edge have 8 hidden spots around them
    for i in range(1,dim-1):
        for j in range(1,dim-1):
            playboard[i,j].numHidden = 8

    #corner coordinates have 3 hidden spots around them
    playboard[0,0].numHidden = 3
    playboard[0,dim-1].numHidden = 3
    playboard[dim-1,0].numHidden = 3
    playboard[dim-1,dim-1].numHidden = 3

    #edge coordinates have 5 hidden spots around them
    for i in range(1,dim-1):
        playboard[0,i].numHidden = 5
        playboard[i,0].numHidden = 5
        playboard[dim-1,i].numHidden = 5
        playboard[i,dim-1].numHidden = 5

#updates knowledge base
def updateKB(playboard, coord, dim, matrix, clicked):
    x = coord[0]
    y = coord[1]
    #if coordinate is a 9 means a mine, so increase all identified mines by 1, and decrease hidden by 1 of neighbors
    if (matrix[x,y] == 9):
        if (playboard[x,y].mine != 3):
            playboard[x,y].mine = 1
        list = getValidNeighbors((x,y), dim)
        for coords in list:
            x = coords[0]
            y = coords[1]
            playboard[x,y].numIdentMines+=1
            playboard[x,y].numHidden-=1
    else:
    #if coordinate is not a mine increase neighbors safe and decrease neighbors hidden
        playboard[x,y].mine = 2
        playboard[x,y].num = matrix[x,y]
        if (y,x) not in clicked:
            clicked.append((y,x))
        list = getValidNeighbors((x,y), dim)
        for coords in list:
            r = coords[0]
            s = coords[1]
            playboard[r,s].numSafe+=1
            playboard[r,s].numHidden-=1
            if(playboard[x,y].num == 0):
                playboard[r,s].mine = 2
                playboard[r,s].num = matrix[r,s]
                if (s,r) not in clicked:
                    clicked.append((s,r))

#method that looks at a 0 coordinate and expands outwards until it hits a number in all directions
def bfs_from_0(playboard, start, dim, matrix, knowledge_expanded, set_of_coords, clicked): #start has to be in format (i,j) as a tuple
    explored = set()
    queue = [start]

    while queue:
        node = queue.pop(0)
        x = node[0]
        y = node[1]
        if node not in explored:
            if (x,y) not in knowledge_expanded:
                updateKB(playboard,(x,y), dim, matrix, clicked)
                knowledge_expanded.add((x,y))

            explored.add(node)
            if (x,y) in set_of_coords:
                set_of_coords.remove((x,y))

            list = getValidNeighbors((x,y), dim)
            for coords in list:
                x = coords[0]
                y = coords[1]
                if (matrix[x,y] == 0):
                    queue.append((x,y))
                else:
                    if (x,y) not in knowledge_expanded:
                        updateKB(playboard,(x,y), dim, matrix, clicked)
                        knowledge_expanded.add((x,y))
                playboard[x,y].num = matrix[x,y]
                if(y,x) not in clicked:
                    clicked.append((y,x))

    return playboard

#method to randomly initialize board with num_mines many mines
def createMine(dim, num_mines):
    random_matrix = np.zeros((dim, dim), dtype=np.int)
    mine_location = set()
    while len(mine_location)!= num_mines:
        value = np.random.randint(dim*dim)
        if(value not in mine_location):
            mine_location.add(value)
            x = int(value%dim)
            y = int(value/dim)
            random_matrix[x,y] = 9 #numerical representation of mine

    return random_matrix

#method to mark coordinates that satisfy condition numMines - numIdentMines = numHidden as flags
def mark_as_flags(x,y, dim, set_of_coords, knowledge_expanded, playboard, matrix, clicked, flag_counter):

    list = getValidNeighbors((x,y), dim)
    flags = len(list)
    for coords in list:
        x = coords[0]
        y = coords[1]
        if (playboard[x,y].mine == 0):
            playboard[x,y].mine = 3
            flag_counter+=1
            if (y,x) not in clicked:
                clicked.append((y,x))

            if (x,y) in set_of_coords:
                set_of_coords.remove((x,y))
            if (x,y) not in knowledge_expanded:
                updateKB(playboard, (x,y), dim, matrix, clicked)
                knowledge_expanded.add((x,y))
    return flag_counter

#marking all neighbors that are safe as safe
def set_hidden_to_safe(x,y, dim, playboard, knowledge_expanded, matrix, clicked):
    list = getValidNeighbors((x,y), dim)
    for coords in list:
        x = coords[0]
        y = coords[1]
        if (playboard[x,y].mine == 0):
            playboard[x,y].mine = 2
            if (x,y) not in knowledge_expanded:
                updateKB(playboard, (x,y), dim, matrix, clicked)
                knowledge_expanded.add((x,y))

#check if coordinate is valid within the board
def isValid(dim,i, j):
    if(i>=0 and i<dim and j>=0 and j<dim):
        return True
    return False

#count mines around a specific index
def countMines(x, y, matrix, dim):
    #get all 8 coordinates around a specific x,y coordinate and increment if it is a mine
    num_mines_around=0
    list = getValidNeighbors((x,y), dim)
    for coords in list:
        x = coords[0]
        y = coords[1]
        if(matrix[x][y]==9):
            num_mines_around+=1

    return num_mines_around

#if agent 3 is called, immediately complete the board
def finishBoard(set_of_coords,playboard,matrix,clicked,safe):
    for item in set_of_coords:
        x = item[0]
        y = item[1]
        if safe:
            playboard[x,y].mine = 2
            playboard[x,y].num = matrix[x,y]
        else:
            playboard[x,y].mine = 3
        if (y,x) not in clicked:
            clicked.append((y,x))
    set_of_coords.clear()

