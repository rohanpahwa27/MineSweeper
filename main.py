#!/usr/bin/python

import numpy as np
from dataclasses import dataclass
import random
import pygame
from pprint import pprint
import graphics
import graphicsAk

@dataclass
class KB():
    mine: int #0 if hidden, 1 if mine, 2 if safe, 3 if flag
    numMines: int #num of surrounding mines
    numSafe: int #num of surrounding safe squares
    numIdentMines: int #num of identified mines (should be <= numMines)
    numHidden: int #num of hidden squares

dim = 10
num_mines = 10
#fills a matrix of size dim*dim with num_mines many mines

def setHidden(playboard):
    for i in range(1,dim-1):
        for j in range(1,dim-1):
            playboard[i,j].numHidden = 8

    playboard[0,0].numHidden = 3
    playboard[0,dim-1].numHidden = 3
    playboard[dim-1,0].numHidden = 3
    playboard[dim-1,dim-1].numHidden = 3

    for i in range(1,dim-1):
        playboard[0,i].numHidden = 5
        playboard[i,0].numHidden = 5
        playboard[dim-1,i].numHidden = 5
        playboard[i,dim-1].numHidden = 5

def updateKB(coord):
    x = coord[0]
    y = coord[1]
    if (matrix[x,y] == 9):
        playboard[x,y].mine = 1
        if (isValid(x+1,y)):
            playboard[x+1,y].numIdentMines+=1
            playboard[x+1,y].numHidden-=1
        if (isValid(x+1,y+1)):
            playboard[x+1,y+1].numIdentMines+=1
            playboard[x+1,y+1].numHidden-=1
        if (isValid(x,y+1)):
            playboard[x,y+1].numIdentMines+=1
            playboard[x,y+1].numHidden-=1
        if (isValid(x-1,y+1)):
            playboard[x-1,y+1].numIdentMines+=1
            playboard[x-1,y+1].numHidden-=1
        if(isValid(x-1,y)):
            playboard[x-1,y].numIdentMines+=1
            playboard[x-1,y].numHidden-=1
        if (isValid(x-1,y-1)):
            playboard[x-1,y-1].numIdentMines+=1
            playboard[x-1,y-1].numHidden-=1
        if (isValid(x,y-1)):
            playboard[x,y-1].numIdentMines+=1
            playboard[x,y-1].numHidden-=1
        if (isValid(x+1,y-1)):
            playboard[x+1,y-1].numIdentMines+=1
            playboard[x+1,y-1].numHidden-=1
    else:
        playboard[x,y].mine = 2
        if (isValid(x+1,y)):
            playboard[x+1,y].numSafe+=1
            playboard[x+1,y].numHidden-=1
        if (isValid(x+1,y+1)):
            playboard[x+1,y+1].numSafe+=1
            playboard[x+1,y+1].numHidden-=1
        if (isValid(x,y+1)):
            playboard[x,y+1].numSafe+=1
            playboard[x,y+1].numHidden-=1
        if (isValid(x-1,y+1)):
            playboard[x-1,y+1].numSafe+=1
            playboard[x-1,y+1].numHidden-=1
        if(isValid(x-1,y)):
            playboard[x-1,y].numSafe+=1
            playboard[x-1,y].numHidden-=1
        if (isValid(x-1,y-1)):
            playboard[x-1,y-1].numSafe+=1
            playboard[x-1,y-1].numHidden-=1
        if (isValid(x,y-1)):
            playboard[x,y-1].numSafe+=1
            playboard[x,y-1].numHidden-=1
        if (isValid(x+1,y-1)):
            playboard[x+1,y-1].numSafe+=1
            playboard[x+1,y-1].numHidden-=1

    


def bfs_from_0(bfs_test, start): #start has to be in format (i,j) as a tuple
    explored = set()
    queue = [start]

    while queue:
        node = queue.pop(0)
        x = node[0]
        y = node[1]
        updateKB((x,y))
        if node not in explored:
            explored.add(node)
            if (isValid(x+1,y)):
                if (matrix[x+1,y] == 0):
                    queue.append((x+1,y))
                bfs_test[x+1,y] = matrix[x+1,y]

            if (isValid(x+1,y+1)):
                if (matrix[x+1,y+1] == 0):
                    queue.append((x+1,y+1))
                bfs_test[x+1,y+1] = matrix[x+1,y+1]

            if (isValid(x,y+1)):
                if (matrix[x,y+1] == 0):
                    queue.append((x,y+1))
                bfs_test[x,y+1] = matrix[x,y+1]

            if (isValid(x-1,y+1)):
                if (matrix[x-1,y+1] == 0):
                    queue.append((x-1,y+1))
                bfs_test[x-1,y+1] = matrix[x-1,y+1]

            if(isValid(x-1,y)):
                if (matrix[x-1,y] == 0):
                    queue.append((x-1,y))
                bfs_test[x-1,y] = matrix[x-1,y]

            if (isValid(x-1,y-1)):
                if (matrix[x-1,y-1] == 0):
                    queue.append((x-1,y-1))
                bfs_test[x-1,y-1] = matrix[x-1,y-1]

            if (isValid(x,y-1)):
                if (matrix[x,y-1] == 0):
                    queue.append((x,y-1))
                bfs_test[x,y-1] = matrix[x,y-1]

            if (isValid(x+1,y-1)):
                if (matrix[x+1,y-1] == 0):
                    queue.append((x+1,y-1))
                bfs_test[x+1,y-1] = matrix[x+1,y-1]

    return bfs_test


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

# START game
# MAKE AN ARRAY OF EMPTY KBS THAT THE AI USES

playboard = np.empty(shape=(dim,dim), dtype=object)
for o in range(0, dim):
    for p in range(0, dim):
        KBTemp= KB(0,0,0,0,0)
        playboard[o][p]= KBTemp
setHidden(playboard)
# #print (playboard)
#
#
#
# # method to count how many identified mines
# '''
# def updateBlock(x, y, playboard):
#     #check all 8 spots around
#     #edge cases
#     if
# '''
#
# # go through the board and update KB:
# minesfound=0
#
# pygame.init()
#
# # initilize set of random numbers
# randomspots= set()
# v = random.randint(0,dim-1)
# w = random.randint(0,dim-1)
#
# #set up drawing window
# screen = pygame.display.set_mode([520,520])
#
# pygame.display.set_caption("Play Board")
# running = True
#
# font = pygame.font.SysFont("arial", 36)
#
# #run the game
# while running:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             running = False
#
#     screen.fill((255,255,255)) #fill background with white
#
#     #define variables
#     width = int(500/dim)
#     black = (0,0,0)
#     orange = (255,69,0)
#     green = (0,100,0)
#     blue = (0,0,128)
#
#     #draw grid
#     pygame.draw.rect(screen, black, (10,10,500,500),2)
#     for i in range(int(500/dim), 500, int(500/dim)):
#         pygame.draw.line(screen, black,(i+10,10),(i+10,510))
#         pygame.draw.line(screen, black,(10,i+10),(510,i+10))
#
#     #pygame.display.flip()
#
#     #draw mines
#     radius = int(width/3) #radius of mine
#     for i in range(0, dim):
#         for j in range(0, dim):
#             #for l in range(0, dim*dim):
#             # while (dim*v + w) in randomspots:
#             #     v = random.randint(0,dim-1)
#             #     w = random.randint(0,dim-1)
#             # randomspots.add(dim*v+w)
#             # #print (v,w)
#             # if matrix[v,w]==9:
#             #
#             #     minesfound= minesfound+1
#             #     playboard[v,w].mine = 1
#             #     playboard[v,w].numMines = 9
#             # else:
#             #     playboard[v,w].numMines = matrix[v,w]
#             #     playboard[v,w].mine = 2
#
#             #pygame.time.wait(500)
#             if(playboard[i,j].mine == 1):
#                 si = 10+(i*width)
#                 sj = 10+(j*width)
#                 pygame.draw.circle(screen, orange, (int((10+(i*width)+(width/2))),int((10+(j*width)+(width/2)))),radius)
#                 pygame.draw.polygon(screen, orange, ((si+width/2,sj+(width/10)),(si+(width/3),sj+(width/4)),(si+(2*width/3),sj+(width/4)))) #top triangle
#                 pygame.draw.polygon(screen, orange, ((si+width/2,sj+(9*width/10)),(si+(width/3),sj+(3*width/4)),(si+(2*width/3),sj+(3*width/4)))) #bottom triangle
#                 pygame.draw.polygon(screen, orange, ((si+(2*width/3),sj+(width/4)),(si+(5*width/6),sj+(width/4)),(si+(3*width/4),sj+(width/2)))) #top right
#                 pygame.draw.polygon(screen, orange, ((si+(3*width/4),sj+(width/2)),(si+(5*width/6),sj+(3*width/4)),(si+(2*width/3),sj+(3*width/4)))) #bottom right
#                 pygame.draw.polygon(screen, orange, ((si+(width/3),sj+(width/4)),(si+(width/6),sj+(width/4)),(si+(width/4),sj+(width/2)))) #top left
#                 pygame.draw.polygon(screen, orange, ((si+(width/4),sj+(width/2)),(si+(width/6),sj+(3*width/4)),(si+(width/3),sj+(3*width/4)))) #bottom left
#
#
#             if(playboard[i,j].numMines >= 0 and playboard[i,j].numMines <= 8):
#                 color = green
#             if(playboard[i,j].numMines == 0):
#                 color = black
#             if(playboard[i,j].numMines == 1):
#                 color = green
#             if(playboard[i,j].numMines == 2):
#                 color = blue
#             #add colors for rest of numbers
#             if(playboard[i,j].mine == 2):
#                 #draw numbers in box
#                 text = font.render(str(playboard[i][j].numMines), True, color)
#                 screen.blit(text,(i*width+10+(width/3),j*width+10+(width/8)))
#
#             #pygame.display.update(pygame.Rect(i*width+10, j*width+10, width, width))
#     pygame.display.flip()
#
#
#
# pygame.quit()

# ans_board = matrix
# ans_board.fill(-1)
#graphicsAk.display_graphics(ans_board, dim)

v = random.randint(0,dim-1)
w = random.randint(0,dim-1)
bfsTest = np.zeros((dim, dim), dtype=np.int)
bfsTest.fill(-1)
bfsTest[v,w] = matrix[v,w]
if (matrix[v,w] == 9):
    playboard[v,w].mine = 1
else:
    playboard[v,w].mine = 2
print((v,w))
# ans_board[v,w] = matrix[v,w]
while(matrix[v,w] != 0):
    v = random.randint(0,dim-1)
    w = random.randint(0,dim-1)
    bfsTest[v,w] = matrix[v,w]
    print((v,w))
# ans_board = bfs_from_0((v,w))

bfsTest = bfs_from_0(bfsTest, (v,w))

print(playboard)

graphicsAk.display_graphics(bfsTest, dim)
#graphics.display_graphics(testBFS, dim)
