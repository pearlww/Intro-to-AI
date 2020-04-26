# 3rd party modules
import sys
import numpy as np
from PyQt5 import QtGui
import random

# Application files
import JohanAI
from AIs import AI_Johan, AI_Jakob, AI_Random, total_score_matrix, AI_MinMax, minimax

# Test functions
def testInput(c,r):             # Input test
    print(board)
    return

# Game functions
def isGameOver(board):
    if any(5 in i for i in total_score_matrix(board)):
        print('GAME OVER, white (1) wins')
        return True
    if any(5 in i for i in total_score_matrix(board*-1)):
        print('GAME OVER, black (-1) wins')
        return True
    else:
        return False

def invaild_move(placement, board):
    c = placement[0]
    r = placement[1]
    if board[c,r]:
        print('ERROR CANT PLACE THERE: \nColumn:', c, '\nRow:',r)
        return True
    else:
        return False

def updateBoard(placement,board,playerTurn):
    c = placement[0]
    r = placement[1]
    if playerTurn:
        board[c,r] = 1
    else:
        board[c,r] = -1
    return board
#----

# Constants
boardSize = 15
#----
#'''
# Start variables
gameOver = False
board = np.zeros((boardSize,boardSize))
playerTurn = 0
while gameOver != True:
    if playerTurn:
        # Player white (1)
        # placement = AI_Jakob(board,1)
        placement = minimax(board, 2, 1)
        print('placement',placement)
        placement = [placement[0], placement[1]]
        print('player white:',placement)
        game_over = invaild_move(placement, board)
        board = updateBoard(placement,board,playerTurn)
        playerTurn = 0
    else:
        # Player black (-1)
        placement = AI_Jakob(board, -1)
        print('player black:',placement)
        game_over = invaild_move(placement,board)
        board = updateBoard(placement,board,playerTurn)
        playerTurn = 1

    print(board)
    if game_over == True or isGameOver(board):
        break
print('/////////////////////////')
    
#----
'''
# Play game x amount of times
stats = []
for i in range(100):
    gameOver = False
    board = np.zeros((boardSize,boardSize))
    playerTurn = 0
    turns = 0
    player_won = 0
    while gameOver != True:
        turns = turns+1
        if playerTurn:
            # Player white (1)
            placement = AI_Random(board)
            game_over = invaild_move(placement, board)
            board = updateBoard(placement,board,playerTurn)
            playerTurn = 0
        else:
            # Player black (-1)
            placement = AI_Random(board)
            game_over = invaild_move(placement,board)
            board = updateBoard(placement,board,playerTurn)
            playerTurn = 1
        
        if game_over == True or isGameOver(board):
            if playerTurn:
                player_won = -1
            else:
                player_won = 1
            break
    stats.append([turns,player_won])
print(stats)
'''