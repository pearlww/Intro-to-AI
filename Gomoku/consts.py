from enum import Enum

# the size of the chessboard
# you can choose 7, 11, 15, 19...
N=15

class BoardState(Enum):
    EMPTY=0
    BLACK=1
    WHITE=2