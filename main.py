#!/usr/bin/python

import numpy as np
from dataclasses import dataclass
import pygame

@dataclass
class KB():
    mine: bool #1 if it is a mine, 0 if it is safe, 2 if it is hidden
    numMines: int #num of surrounding mines
    numSafe: int #num of surrounding safe squares (should =
    numIdentMines: int #num of identified mines (should be <= numMines)
    numHidden: int #num of hidden squares

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

print("---------ANSWER-----------KEY--------------------")
print(matrix)

kb1 = KB(True,0,0,0,0)
print(kb1)
print(kb1.mine)



#DISPLAY GRAPHICS
pygame.init()

#set up drawing window
screen = pygame.display.set_mode([520,520])
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False

    screen.fill((255,255,255)) #fill background with white

    white = (0,0,0)
    pygame.draw.rect(screen, white, (10,10,500,500),2)

    width = int(500/dim)
    for i in range(int(500/dim), 500, int(500/dim)):
        pygame.draw.line(screen, white,(i+10,10),(i+10,510))
        pygame.draw.line(screen, white,(10,i+10),(510,i+10))

    radius = int(width/3)
    for i in range(0, dim):
        for j in range(0, dim):
            if(matrix[i,j] == 9):
                pygame.draw.circle(screen, white, (int((10+(i*width)+(width/2))),int((10+(j*width)+(width/2)))),radius)


    pygame.display.flip()

pygame.quit()
