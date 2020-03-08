import matplotlib.pyplot as plt
from main import *

dim,matrix = get_answer_key()

#run without agent 2
play_minesweeper(dim,matrix,False)
#run with agent 2
play_minesweeper(dim,matrix,True)