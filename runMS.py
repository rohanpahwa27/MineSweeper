import matplotlib.pyplot as plt
from main import *
import numpy as np



#test with user input, make sure to uncomment graphics
print("Please enter the dimension of the size board you want to play on: ")
dim = int(input())
print("Enter how many mines you want in the board: ")
num_mines = int(input())

matrix = get_answer_key(dim, num_mines)
#agent1
playboard1, flags1 = play_minesweeper(dim,matrix,num_mines,False,False)
#agent2
playboard2, flags2 = play_minesweeper(dim,matrix,num_mines,True,False)
#agent3
playboard3, flags3 = play_minesweeper(dim,matrix,num_mines,True,True)


#***START ANALYSIS***


# agent1_scores = []
# agent2_scores = []
# agent3_scores = []
# times_arr = []


# #testing for data
# dim = 15
# num_mines = 15
# while num_mines <= 225:
#     flags_a1 = 0
#     flags_a2 = 0
#     flags_a3 = 0
#     timer1=0
#     timer2=0
#     timer3=0
#     for i in range(0,5):
#         matrix = get_answer_key(dim, num_mines)
       
#         #run with agent1
#         t1s = time.time()
#         playboard1, flags1 = play_minesweeper(dim,matrix,num_mines,False, False)
#         t1e = time.time()
#         timer1+=(t1e-t1s)
        
#         for i in range(0,dim):
#             for j in range(0, dim):
#                 if(playboard1[i,j].mine == 3):
#                     flags_a1+=1

#         #run with agent2
#         t2s = time.time()
#         playboard2, flags2 = play_minesweeper(dim,matrix,num_mines, True, False)
#         t2e = time.time()
#         timer2+=(t2e-t2s)

#         for i in range(0,dim):
#             for j in range(0, dim):
#                 if(playboard2[i,j].mine == 3):
#                     flags_a2+=1

#         #run with agent3
#         t3s = time.time()
#         playboard3, flags3 = play_minesweeper(dim,matrix, num_mines, True, True)
#         t3e = time.time()
#         timer3+=(t3e-t3s)
#         for i in range(0,dim):
#             for j in range(0, dim):
#                 if(playboard3[i,j].mine == 3):
#                     flags_a3+=1
#     #add as a tuple as density vs flag success rate
#     agent1_scores.append((num_mines/225, float(flags_a1/(num_mines*5))))
#     agent2_scores.append((num_mines/225, float(flags_a2/(num_mines*5))))
#     agent3_scores.append((num_mines/225, float(flags_a3/(num_mines*5))))
#     times_arr.append(("agent1", num_mines/225, float(timer1/5)))
#     times_arr.append(("agent2", num_mines/225, float(timer2/5)))
#     times_arr.append(("agent3", num_mines/225, float(timer3/5)))

#     print("MINES ", num_mines)
#     num_mines+=15

# #make numpy arrays out of data to put in scatterplot 
# x = np.empty(len(agent1_scores))
# y1 = np.empty(len(agent1_scores))
# y2 = np.empty(len(agent2_scores))
# y3 = np.empty(len(agent2_scores))
# ctr = 0

# for time in times_arr:
#     print(time[0], "mine density: ", time[1], "avg time: ", time[2])

# for item in agent1_scores:
#     print("num_mines1: ", item[0], "score1: ", item[1])
#     x[ctr] = item[0]
#     y1[ctr] = item[1]
#     ctr += 1

# ctr = 0
# for item2 in agent2_scores:
#     print("num_mines2: ", item2[0], "score2: ", item2[1])
#     y2[ctr] = item2[1]
#     ctr += 1

# ctr = 0
# for item3 in agent3_scores:
#     print("num_mines3: ", item3[0], "score3: ", item3[1])
#     y3[ctr] = item3[1]
#     ctr += 1

# #plot data in scatterplot
# plt.scatter(x,y1,color='r', label = 'Agent 1')
# plt.scatter(x,y2,color='b', label = 'Agent 2')
# plt.scatter(x,y3,color='g', label = 'Agent 3')
# plt.title('Avg score vs Mine density')
# plt.xlabel('Mine Density')
# plt.ylabel('Average Final Score')
# plt.legend()
# plt.savefig('avgscore_minedensity.png')
# plt.show()

#***END ANALYSIS***
