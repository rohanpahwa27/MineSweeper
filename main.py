#!/usr/bin/python
import time
import numpy as np
from dataclasses import dataclass
import random
import pygame
from pprint import pprint
import graphics
import agent2
from func import *

@dataclass
class KB():
    mine: int #0 if hidden, 1 if mine, 2 if safe, 3 if flag
    num: int #num of surrounding mines
    numSafe: int #num of surrounding safe squares
    numIdentMines: int #num of identified mines (should be <= num)
    numHidden: int #num of hidden squares

def get_answer_key(dim, num_mines):


    matrix = createMine(dim, num_mines)
    #get the answer key board
    for i in range(0, dim):
        for j in range(0, dim):
            if(matrix[i,j]!=9):
                mine_num = countMines(i,j,matrix, dim)
                matrix[i, j] = mine_num

    print("---------ANSWER---------KEY---------")
    print(matrix)
    return matrix


def play_minesweeper(dim,matrix,num_mines,agent2_2,agent3):

    #keep track of flagged cells
    flag_counter = 0

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

    #keep clicking spots in the initial part of the game until you get a 0 so that you can expand safely from there
    while(matrix[v,w] != 0):
        v = random.randint(0,dim-1)
        w = random.randint(0,dim-1)
        if (matrix[v,w] == 9):
            set_of_coords.remove((v,w))
        if (w,v) not in clicked:
            clicked.append((w,v))
        if (v,w) not in knowledge_expanded:
            updateKB(playboard,(v,w), dim, matrix, clicked)
            knowledge_expanded.add((v,w))
        if len(clicked)>1:
            break

    #use this method to expand all the safe neighbors from the coordinate that has a 0 value
    #all values around a 0 are safe
    if playboard[v,w].num == 0:
        playboard = bfs_from_0(playboard,(v,w), dim, matrix, knowledge_expanded, set_of_coords, clicked)


    deep_copy = set()
    for coords in set_of_coords:
        deep_copy.add(coords)
    counter = 0

    #after some random clicks and one expansion from 0 start the game

    size = len(set_of_coords)


    #while size>0:

    while(len(set_of_coords)>0):
        prev_len = len(set_of_coords)


        #deep_copy is same as set_of_coords
        for coords in deep_copy:
            x = coords[0]
            y = coords[1]

            #if space is safe continue
            if(playboard[x,y].mine == 2):
                #this means the only spots that are left are mines
                if (playboard[x,y].num - playboard[x,y].numIdentMines == playboard[x,y].numHidden):
                    #make all numHidden as flag and remove flags from set_coords
                    flag_counter = mark_as_flags(x,y, dim, set_of_coords, knowledge_expanded, playboard, matrix, clicked, flag_counter)
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

        #run agent 3 if specified in parameters
            if agent3:
                if findBombs(playboard) == num_mines:
                    finishBoard(set_of_coords,playboard,matrix,clicked,True)
                    break
                if num_mines - findBombs(playboard) == len(set_of_coords):
                    finishBoard(set_of_coords,playboard,matrix,clicked,False)
                    break


        #run agent 2 if specified in parameters
        if(prev_len == len(set_of_coords)):

            #run agent 2 if specified in parameters
            if agent2_2 == True:
                prev_len = len(set_of_coords)
                counter+=1
                if agent3:
                    flag_counter = agent2.populateEQMap(dim, playboard, set_of_coords, matrix, clicked, knowledge_expanded, flag_counter,num_mines,True)
                else:
                    flag_counter = agent2.populateEQMap(dim, playboard, set_of_coords, matrix, clicked, knowledge_expanded, flag_counter,num_mines,False)


            #run agent 3 if specified in parameters
            if agent3:
                if findBombs(playboard) == num_mines:
                    finishBoard(set_of_coords,playboard,matrix,clicked,True)
                    break
                if num_mines - findBombs(playboard) == len(set_of_coords):
                    finishBoard(set_of_coords,playboard,matrix,clicked,False)
                    break
                    

            #generate a new random number
            #if size > 0:
            if prev_len == len(set_of_coords):
                if (len(set_of_coords) > 0):
                    randCoord = set_of_coords.pop()
                    set_of_coords.add(randCoord)
                v = randCoord[0]
                w = randCoord[1]
                if (w,v) not in clicked:
                    clicked.append((w,v))
                if (v,w) not in knowledge_expanded:
                    updateKB(playboard,(v,w), dim, matrix, clicked)
                    knowledge_expanded.add((v,w))
                if (v,w) in set_of_coords:
                    if(playboard[v,w].num == playboard[v,w].numIdentMines or playboard[v,w].mine == 1):
                        set_of_coords.remove((v,w))

    
    #this displays the board using pygame
    graphics.display_graphics(playboard, dim, clicked)

    return playboard, flag_counter
