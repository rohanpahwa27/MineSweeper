import matplotlib.pyplot as plt
from main import *


agent1_scores = []
agent2_scores = []

#test with user input make sure to uncomment graphics
# print("Please enter the dimension of the size board you want to play on: ")
# dim = int(input())
# print("Enter how many mines you want in the board: ")
# num_mines = int(input())
#
# matrix = get_answer_key(dim, num_mines)
# playboard1, flags1 = play_minesweeper(dim,matrix,False)
# playboard2, flags2 = play_minesweeper(dim,matrix,True)

#testing for data
dim = 15
num_mines = 15
while num_mines <= 225:
    flags_a1 = 0
    flags_a2 = 0
    for i in range(0,5):
        matrix = get_answer_key(dim, num_mines)
        #run without agent 2
        playboard1, flags1 = play_minesweeper(dim,matrix,False)
        for i in range(0,dim):
            for j in range(0, dim):
                if(playboard1[i,j].mine == 3):
                    flags_a1+=1

        #run with agent2
        playboard2, flags2 = play_minesweeper(dim,matrix,True)
        for i in range(0,dim):
            for j in range(0, dim):
                if(playboard2[i,j].mine == 3):
                    flags_a2+=1
    #add as a tuple as density vs flag success rate
    agent1_scores.append((num_mines/225, float(flags_a1/(num_mines*5))))
    agent2_scores.append((num_mines/225, float(flags_a2/(num_mines*5))))
    print("MINES ", num_mines)
    num_mines+=15

for item in agent1_scores:
    print("num_mines1: ", item[0], "score1: ", item[1])

for item2 in agent2_scores:
    print("num_mines2: ", item2[0], "score2: ", item2[1])
