#!/usr/bin/python
import time
import numpy as np
from dataclasses import dataclass
import random
import pygame
from pprint import pprint
import graphics
import graphicsAk
import agent2
from func import *

@dataclass
class KB():
    mine: int #0 if hidden, 1 if mine, 2 if safe, 3 if flag
    num: int #num of surrounding mines
    numSafe: int #num of surrounding safe squares
    numIdentMines: int #num of identified mines (should be <= num)
    numHidden: int #num of hidden squares
         
def get_answer_key():
  
    #fills a matrix of size dim*dim with num_mines many mines
    print("Please enter the dimension of the size board you want to play on: ")
    dim = int(input())
    #dim = 10
    print("Enter how many mines you want in the board: ")
    num_mines = int(input())
    #num_mines = 20
    matrix = createMine(dim, num_mines)
    #get the answer key board
    for i in range(0, dim):
        for j in range(0, dim):
            if(matrix[i,j]!=9):
                mine_num = countMines(i,j,matrix, dim)
                matrix[i, j] = mine_num

    print("---------ANSWER---------KEY---------")
    print(matrix)
    return dim,matrix


def play_minesweeper(dim,matrix,agent2_2):
    #initialize a set of all the coordinates (concept of visited array, remove from this one you no longer need)
    clicked = []
    set_of_coords = set()
    knowledge_expanded = set()
    for i in range(0, dim):
        for j in range(0, dim):
            set_of_coords.add((i,j))

    #initialize an empty knowledge base
    playboard = np.empty(shape=(dim,dim), dtype=object)
    for o in range(0, dim):
        for p in range(0, dim):
            KBTemp= KB(0,-1,0,0,0)
            playboard[o][p]= KBTemp

    #method to mark the how many hidden neighbors each coordinate has
    setHidden(playboard, dim)

    #beginning of game, pick a random number to start at
    v = random.randint(0,dim-1)
    w = random.randint(0,dim-1)

    #expose this number
    playboard[v,w].num = matrix[v,w]
    if (w,v) not in clicked:
        clicked.append((w,v))
        # print("appended", (v,w))
    #update the knowledge base (playboard) based on if it is a 9(mine) or not
    if (matrix[v,w] != 0):
        if (matrix[v,w] == 9):
            playboard[v,w].mine = 1
            set_of_coords.remove((v,w))
        else:
            playboard[v,w].mine = 2
            playboard[v,w].num = matrix[v,w] #BEATRICE ADDED
        if (v,w) not in knowledge_expanded:
            updateKB(playboard,(v,w), dim, matrix, clicked)
            knowledge_expanded.add((v,w))
    # print("random",(v,w))

    #keep clicking spots in the initial part of the game until you get a 0 so that you can expand safely from there
    while(matrix[v,w] != 0):
        v = random.randint(0,dim-1)
        w = random.randint(0,dim-1)
        playboard[v,w].num = matrix[v,w]
        if (w,v) not in clicked:
            clicked.append((w,v))
            # print("appended", (v,w))
        if (v,w) not in knowledge_expanded:
            updateKB(playboard,(v,w), dim, matrix, clicked)
            knowledge_expanded.add((v,w))
        if len(clicked)>dim/3:
            break
        # print("Random: ", (v,w))
    #pprint(agent2.populateEQMap(dim,playboard,set_of_coords))

    #use this method to expand all the safe neighbors from the coordinate that has a 0 value
    #all values around a 0 are safe
    if playboard[v,w].num == 0:
        playboard = bfs_from_0(playboard,(v,w), dim, matrix, knowledge_expanded, set_of_coords, clicked)

    # for i in range(0,dim):
    #     for j in range(0,dim):
    #         print((i,j), playboard[i,j])

    deep_copy = set()
    for coords in set_of_coords:
        deep_copy.add(coords)
    counter = 0

    #after some random clicks and one expansion from 0 start the game

    size = len(set_of_coords)


    #while size>0:

    while(len(set_of_coords)>0):
        #graphics.display_graphics(playboard, dim)

        prev_len = len(set_of_coords)
        # prev_len = size
        # print("SIZE", size)
        # print("prev", prev_len)

        #deep_copy is same as set_of_coords
        for coords in deep_copy:
            x = coords[0]
            y = coords[1]

            #if space is safe continue
            if(playboard[x,y].mine == 2):
                #this means the only spots that are left are mines
                if (playboard[x,y].num - playboard[x,y].numIdentMines == playboard[x,y].numHidden):
                    #make all numHidden as flag and remove flags from set_coords
                    mark_as_flags(x,y, dim, set_of_coords, knowledge_expanded, playboard, matrix, clicked)
                    if (x,y) in set_of_coords:
                        set_of_coords.remove((x,y))

                #this means that all the mines around this location are either flagged or been clicked on, so you can mark as safe
                if(playboard[x,y].num == playboard[x,y].numIdentMines):
                    #mark hidden neighbors as safe
                    set_hidden_to_safe(x,y, dim, playboard, knowledge_expanded, matrix, clicked)
                    if (x,y) in set_of_coords:
                        set_of_coords.remove((x,y))

                    #check if any of the neighbors are 0
                    list = getValidNeighbors((x,y), dim)
                    for coords in list:
                        x = coords[0]
                        y = coords[1]
                        if(playboard[x,y].num == 0):
                            if (x,y) in set_of_coords:
                                bfs_from_0(playboard, (x,y), dim, matrix, knowledge_expanded, set_of_coords, clicked)


        deep_copy = set()
        for coords in set_of_coords:
            deep_copy.add(coords)
            #check for size of set if same




        if(prev_len == len(set_of_coords)):
            if agent2_2 == True:
            #if prev_len == size:
                prev_len = len(set_of_coords)
                # print("here")
                counter+=1

                # print("The length of clicked before is ", len(clicked))
                # print("-------------------- start -----------------------")
                agent2.populateEQMap(dim, playboard, set_of_coords, matrix, clicked, knowledge_expanded)
                # print("--------------------- end ------------------------")
                # print("The length of clicked after is ", len(clicked))
                # print("in main")
                # pprint(set_of_coords)

            #generate a new random number
            #if size > 0: 
            if prev_len == len(set_of_coords):
                if (len(set_of_coords) > 0):
                    randCoord = set_of_coords.pop()
                    set_of_coords.add(randCoord)
                v = randCoord[0]
                w = randCoord[1]
                #playboard[v,w].num = matrix[v,w]
                if (w,v) not in clicked:
                    clicked.append((w,v))
                    # print("randomly appended", (v,w))
                if (v,w) not in knowledge_expanded:
                    updateKB(playboard,(v,w), dim, matrix, clicked)
                    knowledge_expanded.add((v,w))
                if (v,w) in set_of_coords:
                    if(playboard[v,w].num == playboard[v,w].numIdentMines or playboard[v,w].mine == 1):
                        set_of_coords.remove((v,w))


    # for i in range(0,dim):
    #     for j in range(0,dim):
    #         if (i,j) in set_of_coords:
    #             print((i,j), playboard[i,j])


    #print(agent2.populateEQMap(dim,playboard,set_of_coords))
    print("this is the FINAL LENGTH", len(clicked))
    # for obj in clicked:
    #     print(obj)
    graphics.display_graphics(playboard, dim, clicked)
