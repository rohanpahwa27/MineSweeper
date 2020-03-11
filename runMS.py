import matplotlib.pyplot as plt
from main import *
import numpy as np


#
# #test with user input make sure to uncomment graphics
# print("Please enter the dimension of the size board you want to play on: ")
# dim = int(input())
# print("Enter how many mines you want in the board: ")
# num_mines = int(input())
#
# matrix = get_answer_key(dim, num_mines)
# #playboard1, flags1 = play_minesweeper(dim,matrix,num_mines,False,0)
# playboard2, flags2 = play_minesweeper(dim,matrix,num_mines,True,0)
# playboard2, flags2 = play_minesweeper(dim,matrix,num_mines,True,3)
#

#***START ANALYSIS***


agent1_scores = []
agent2_scores = []
agent3_scores = []


#testing for data
dim = 15
num_mines = 15
while num_mines <= 225:
    flags_a1 = 0
    flags_a2 = 0
    flags_a3 = 0
    for i in range(0,5):
	    matrix = get_answer_key(dim, num_mines)
	    #run without agent 2
	    playboard1, flags1 = play_minesweeper(dim,matrix,num_mines,False,0)
	    for i in range(0,dim):
	        for j in range(0, dim):
	            if(playboard1[i,j].mine == 3):
	                flags_a1+=1

	    #run with agent2
	    playboard2, flags2 = play_minesweeper(dim,matrix,num_mines,True,0)
	    for i in range(0,dim):
	        for j in range(0, dim):
	            if(playboard2[i,j].mine == 3):
	                flags_a2+=1
        #run with agent3
	    playboard3, flags3 = play_minesweeper(dim,matrix,num_mines,True,3)
	    for i in range(0,dim):
	        for j in range(0, dim):
	            if(playboard3[i,j].mine == 3):
	                flags_a3+=1
    #add as a tuple as density vs flag success rate
    agent1_scores.append((num_mines/225, float(flags_a1/(num_mines*5))))
    agent2_scores.append((num_mines/225, float(flags_a2/(num_mines*5))))
    agent3_scores.append((num_mines/225, float(flags_a3/(num_mines*5))))

    print("MINES ", num_mines)
    num_mines+=15

#make numpy arrays out of data to put in scatterplot
x = np.empty(len(agent1_scores))
y1 = np.empty(len(agent1_scores))
y2 = np.empty(len(agent2_scores))
y3 = np.empty(len(agent3_scores))

ctr = 0

for item in agent1_scores:
    print("num_mines1: ", item[0], "score1: ", item[1])
    x[ctr] = item[0]
    y1[ctr] = item[1]
    ctr += 1

ctr = 0
for item2 in agent2_scores:
    print("num_mines2: ", item2[0], "score2: ", item2[1])
    y2[ctr] = item2[1]
    ctr += 1

ctr = 0
for item3 in agent3_scores:
    print("num_mines3: ", item3[0], "score3: ", item3[1])
    y3[ctr] = item3[1]
    ctr += 1


# print(x)
# print(y1)
# print(y2)

#plot data in scatterplot
plt.scatter(x,y1,color='r', label = 'Agent 1')
plt.scatter(x,y2,color='b', label = 'Agent 2')
plt.scatter(x,y3,color='g', label = 'Agent 3')
plt.title('Avg score vs Mine density')
plt.xlabel('Mine Density')
plt.ylabel('Average Final Score')
plt.legend()
plt.savefig('avgscore_minedensity.png')
plt.show()

#***END ANALYSIS***
