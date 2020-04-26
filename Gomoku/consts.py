from enum import Enum
import numpy as np

# the size of the chessboard. you can choose 7, 11, 15, 19...
N=15

# the search depth. only odd numbers
DEPTH=1

# the type of AI. >1 more attack, <1 more defense
RATIO=1

# If 0, player vs player
# If 1, player vs AI
# If 2, AI vs AI
MODE= 1

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


WEIGHTS=np.array([6,5,4,3,2,1])

# Five, liveFour, sleepFour, liveThree, sleepThree, liveTwo
my_shapes=np.array([0,0,0,0,0,0])

enemy_shapes=np.array([0,0,0,0,0,0])

class BoardState(Enum):
    EMPTY=0
    BLACK=1
    WHITE=2