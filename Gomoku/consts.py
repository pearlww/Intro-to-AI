from enum import Enum
import numpy as np

# the size of the chessboard. you can choose 7, 11, 15, 19...
N=7

# the search depth. only odd numbers
DEPTH=1

# the type of AI. >1 more attack, <1 more defense
RATIO=1

# If false, player vs player; If true, player vs AI
enable_ai= True

threat_list=[[0, 1, 1, 0, 0], #live two
             [0, 0, 1, 1, 0],
             [1, 1, 0, 1, 0], #sleep three
             [0, 0, 1, 1, 1],
             [1, 1, 1, 0, 0],
             [0, 1, 1, 1, 0], # live three
             [0, 1, 0, 1, 1, 0],
             [0, 1, 1, 0, 1, 0],
             [1, 1, 1, 0, 1], #sleep four
             [1, 1, 0, 1, 1],
             [1, 0, 1, 1, 1],
             [1, 1, 1, 1, 0],
             [0, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 0], # live four
             [1, 1, 1, 1, 1]]    #five


WEIGHTS=np.array([10000,1000,100,10,4,1])




class BoardState(Enum):
    EMPTY=0
    BLACK=1
    WHITE=2