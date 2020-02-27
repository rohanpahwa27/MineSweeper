#!/usr/bin/python

import numpy as np
from dataclasses import dataclass
import pygame

@dataclass
class KB():
    mine: int #0 if hidden, 1 if mine, 2 if safe, 3 if flag
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

kb1 = KB(0,0,0,0,0)
print(kb1)
print(kb1.mine)

#START game
# MAKE AN ARRAY OF EMPTY KBS THAT THE AI USES
playboard = np.full((dim, dim), KB(0,0,0,0,0))
#pprint (playboard)

# go through the board and update KB:
minesfound=0

matrix_cpy = matrix
print (matrix)
for v in range(0, dim):
    for w in range(0, dim):
        print (matrix[v,w])
        if matrix[v,w]==9:
            minesfound= minesfound+1
            playboard[v,w].mine = 1
        else:
            playboard[v,w].numMines = matrix[v,w]
            playboard[v,w].mine = 2
        print(playboard[v,w])
print (playboard)


#DISPLAY GRAPHICS
pygame.init()

#set up drawing window
screen = pygame.display.set_mode([520,520])
running = True

font = pygame.font.SysFont("arial", 36)

#run the game
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False

    screen.fill((255,255,255)) #fill background with white

    #define variables
    width = int(500/dim)
    black = (0,0,0)
    orange = (255,69,0)
    green = (0,100,0)
    blue = (0,0,128)

    #draw grid
    pygame.draw.rect(screen, black, (10,10,500,500),2)
    for i in range(int(500/dim), 500, int(500/dim)):
        pygame.draw.line(screen, black,(i+10,10),(i+10,510))
        pygame.draw.line(screen, black,(10,i+10),(510,i+10))


    #draw mines
    radius = int(width/3) #radius of mine
    for i in range(0, dim):
        for j in range(0, dim):
            if(matrix[i,j] == 9):
                si = 10+(i*width)
                sj = 10+(j*width)
                pygame.draw.circle(screen, orange, (int((10+(i*width)+(width/2))),int((10+(j*width)+(width/2)))),radius)
                pygame.draw.polygon(screen, orange, ((si+width/2,sj+(width/10)),(si+(width/3),sj+(width/4)),(si+(2*width/3),sj+(width/4)))) #top triangle
                pygame.draw.polygon(screen, orange, ((si+width/2,sj+(9*width/10)),(si+(width/3),sj+(3*width/4)),(si+(2*width/3),sj+(3*width/4)))) #bottom triangle
                pygame.draw.polygon(screen, orange, ((si+(2*width/3),sj+(width/4)),(si+(5*width/6),sj+(width/4)),(si+(3*width/4),sj+(width/2)))) #top right
                pygame.draw.polygon(screen, orange, ((si+(3*width/4),sj+(width/2)),(si+(5*width/6),sj+(3*width/4)),(si+(2*width/3),sj+(3*width/4)))) #bottom right
                pygame.draw.polygon(screen, orange, ((si+(width/3),sj+(width/4)),(si+(width/6),sj+(width/4)),(si+(width/4),sj+(width/2)))) #top left
                pygame.draw.polygon(screen, orange, ((si+(width/4),sj+(width/2)),(si+(width/6),sj+(3*width/4)),(si+(width/3),sj+(3*width/4)))) #bottom left

            if(matrix[i,j] >= 0 and matrix[i,j] <= 8):
                color = green
            if(matrix[i,j] == 0):
                color = black
            if(matrix[i,j] == 1):
                color = green
            if(matrix[i,j] == 2):
                color = blue
            #add colors for rest of numbers
            if(matrix[i,j] >= 0 and matrix[i,j] <= 8):
                #draw numbers in box
                text = font.render(str(matrix[i][j]), True, color)
                screen.blit(text,(i*width+10+(width/3),j*width+10+(width/8)))



    pygame.display.flip()


pygame.quit()
