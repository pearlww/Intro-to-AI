import JohanAI
import random
import sys
import numpy as np


def ray(img, mid, dir):
    obstruction_dist = 0
    obstruction_dir = 0
    obstruction_amount = 0
    irrelevant = False
    score = img[mid,mid]
    for i in range(2):
        dir = np.array(dir)*-1
        for j in range(2):
            current_value = img[mid+(j+1)*dir[0],mid+(j+1)*dir[1]]
            if current_value == -1:
                obstruction_dist = j
                obstruction_amount = obstruction_amount+1
                obstruction_dir = dir
                break
            score = score+current_value
    
    if obstruction_amount == 1:
        dir = obstruction_dir*-1
        for j in range(2-obstruction_dist):
            if img[mid+(j+3)*dir[0],mid+(j+3)*dir[1]] == -1:
                irrelevant = True
                break
    elif obstruction_amount == 2:
        irrelevant = True
    
    if irrelevant:
        return 0
    else:
        return score

def ray_dir(img, dir):
    score = 0
    mid = 4
    if img[mid,mid]>-1:
        if dir == 0:
            score = ray(img, mid, [1,0]) # ⇳
        elif dir == 1:
            score = ray(img, mid, [0,1]) # ⇔
        elif dir == 2:
            score = ray(img, mid, [1,1]) # ⤡
        elif dir == 3:
            score = ray(img, mid, [1,-1]) # ⤢
        else:
            pass
    return score

def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value

def convolution2d(img, dir):
    img = np.pad(img, 4, pad_with, padder=-1)
    y, x = img.shape
    y = y - 9 + 1
    x = x - 9 + 1
    score_matrix = np.zeros((y,x))
    for i in range(y):
        for j in range(x):
            score_matrix[i][j] = ray_dir(img[i:i+9, j:j+9], dir)
    return score_matrix

def total_score_matrix(img):
    score_matrix = []
    for i in range(4):
        score_matrix.append(convolution2d(img,i))
    return score_matrix

def score_increasing_spots(score_matrix, board):
    highest_score = np.amax(score_matrix)
    high_value_spots = []
    if highest_score:
        where_in_list = np.where(score_matrix == highest_score)
        for i in range(len(where_in_list[0])):
            direction = [[1,0], [0,1], [1,1], [1,-1]] # ⇳, ⇔, ⤡, ⤢
            direction_index = where_in_list[0][i]
            direction = direction[direction_index]
            position = [where_in_list[1][i],where_in_list[2][i]]
            if board[position[0], position[1]]:
                for j in [-1, 1]:
                    for k in range(2):
                        try:
                            current_position = [position[0]+(k+1)*direction[0]*j,position[1]+(k+1)*direction[1]*j]
                            if board[current_position[0], current_position[1]] == -1:
                                break
                            if not board[current_position[0], current_position[1]] and not any(p == current_position for p in high_value_spots):
                                high_value_spots.append(current_position)
                        except:
                            pass
            elif not any(p == position for p in high_value_spots):
                high_value_spots.append(position)

        return highest_score, high_value_spots
    else:
        return highest_score, high_value_spots

def highest_value_spots(high_value_spots, score_matrix):
    score_matrix_sum = sum(score_matrix)
    new_high_value_spots = []
    for i in range(len(high_value_spots)):
        new_high_value_spots.append(score_matrix_sum[high_value_spots[i][0],high_value_spots[i][1]])
    highest_value = np.amax(new_high_value_spots)
    where_in_list = np.where(new_high_value_spots == highest_value)
    new_high_value_spots = []
    for i in range(len(where_in_list[0])):
        new_high_value_spots.append(high_value_spots[where_in_list[0][i]])
    return new_high_value_spots

def common_spots(position0, position1):
    joint_spots = []
    for i in range(len(position0)):
        if any(p == position0[i] for p in position1):
            joint_spots.append(position0[i])
    return joint_spots

def AI_Jakob(board, player):
    board = board*player
    my_score_matrix = total_score_matrix(board)
    my_highest_score, my_high_value_spots = score_increasing_spots(my_score_matrix, board)
    board = board*-1
    your_score_matrix = total_score_matrix(board)
    your_highest_score, your_high_value_spots = score_increasing_spots(your_score_matrix, board)
    if my_highest_score < your_highest_score:
        highest_threats = highest_value_spots(your_high_value_spots, your_score_matrix)
        if len(highest_threats)-1:
            joint_spots = common_spots(highest_threats, my_high_value_spots)
            if len(joint_spots) > 1:
                my_move = highest_value_spots(joint_spots, my_score_matrix)
            elif len(joint_spots) == 1:
                my_move = joint_spots[0]
            else:
                my_move = highest_value_spots(highest_threats, my_score_matrix)
        else:
            my_move = highest_threats[0]
    elif my_highest_score+your_highest_score == 0:
        m,n = board.shape
        my_move = [[round(m/2)-1,round(n/2)-1]]
    else:
        highest_opportunity = highest_value_spots(my_high_value_spots, my_score_matrix)
        if len(highest_opportunity)-1:
            joint_spots = common_spots(highest_opportunity, your_high_value_spots)
            if len(joint_spots) > 1:
                my_move = highest_value_spots(joint_spots, your_score_matrix)
            elif len(joint_spots) == 1:
                my_move = joint_spots[0]
            else:
                my_move = highest_value_spots(highest_opportunity, your_score_matrix)
        else:
            my_move = highest_opportunity[0]
    print(my_high_value_spots,my_highest_score)
    if len(np.shape(my_move))-1:
        return my_move[random.randint(0,len(my_move)-1)]
    else:
        return my_move

def AI_Johan(board, Player):
    score_matrix = JohanAI.SumMatrixWhite(board*Player)
    highest_score = np.amax(score_matrix)
    my_move = []
    if highest_score:
        where_in_list = np.where(score_matrix == highest_score)
        for i in range(len(where_in_list[0])):
            my_move.append([where_in_list[0][i],where_in_list[1][i]])
    else:
        m,n = board.shape
        my_move = [[round(m/2)-1,round(n/2)-1]]

    if len(np.shape(my_move))-1:
        return my_move[random.randint(0,len(my_move)-1)]
    else:
        return my_move

def AI_Random(board):
    random_move = []
    where_in_list = np.where(board == 0)
    for i in range(len(where_in_list[0])):
        random_move.append([where_in_list[0][i],where_in_list[1][i]])
    
    return random_move[random.randint(0,len(random_move)-1)]

def remove_common_spots(position0, position1):
    joint_spots = position0
    for i in range(len(position1)):
        if position1[i] not in position0:
            joint_spots.append(position1[i])
    return joint_spots

def estimate_value(board, player):
    white_score_matrix = total_score_matrix(board)
    white_highest_score, white_high_value_spots = score_increasing_spots(white_score_matrix, board)
    white_score = white_highest_score+1-(1/len(white_high_value_spots))
    board = board*-1
    black_score_matrix = total_score_matrix(board)
    black_highest_score, black_high_value_spots = score_increasing_spots(black_score_matrix, board)
    black_score = black_highest_score+1-(1/len(black_high_value_spots))

    est_value = 0
    if black_score < white_score:
        est_value = white_score
    elif black_score > white_score:
        est_value = -black_score
    else:
        if player == 1:
            est_value = -black_score
        else:
            est_value = white_score
    
    return est_value

def AI_MinMax(board, depth, player):
    tree = []
    for i in range(depth):
        if len(tree) != 0:
            pass
        white_score_matrix = total_score_matrix(board)
        white_highest_score, white_high_value_spots = score_increasing_spots(white_score_matrix, board)
        board = board*-1
        black_score_matrix = total_score_matrix(board)
        black_highest_score, black_high_value_spots = score_increasing_spots(black_score_matrix, board)
        board = board*-1
        positions = remove_common_spots(white_high_value_spots, black_high_value_spots)
        tmp_list = []
        for j in range(len(positions)):
            tmp_list.append(positions[j])
        tree.append(tmp_list)
    print('tree:',tree[0][1])

def game_over(board):
    if any(5 in i for i in total_score_matrix(board)):
        return True
    if any(5 in i for i in total_score_matrix(board*-1)):
        return True
    else:
        return False

def minimax(board, depth, player):
    #if any(-1 in i for i in board):
    #    return [-1, -1, -6]
    if player == 1:
        best = [-1, -1, [-6, -6]]
    else:
        best = [-1, -1, [+6, +6]]

    white_score_matrix = total_score_matrix(board)
    white_highest_score, white_high_value_spots = score_increasing_spots(white_score_matrix, board)
    decimal = len(white_high_value_spots)
    if decimal != 0:
        white_score = white_highest_score+1-(1/decimal)
    else:
        white_score = white_highest_score
    board = board*-1
    black_score_matrix = total_score_matrix(board)
    black_highest_score, black_high_value_spots = score_increasing_spots(black_score_matrix, board)
    decimal = len(black_high_value_spots)
    board = board*-1
    if decimal != 0:
        black_score = black_highest_score+1-(1/decimal)
    else:
        black_score = black_highest_score


    if depth == 0 or game_over(board):
        score = [-1, -1, 0]
        if black_highest_score < white_highest_score:
            score[2] = [white_score, -black_score]
        elif black_highest_score > white_highest_score:
            score[2] = [-black_score, white_score]
        else:
            if player != 1:
                score[2] = [-black_score, white_score]
            else:
                score[2] = [white_score, -black_score]
        return score
    
    positions = remove_common_spots(white_high_value_spots, black_high_value_spots)

    for likely_pos in positions:
        x, y = likely_pos[0], likely_pos[1]
        board[x,y] = player
        score = minimax(board, depth -1, -player)
        score[0] = x
        score[1] = y
        board[x,y] = 0

        if player == 1:
            if score[2][0] > best[2][0]:
                best = score
            elif score[2][0] == best[2][0] and score[2][1] > best[2][1]:
                best = score
        else:
            if score[2][0] < best[2][0]:
                best = score
            elif score[2][0] == best[2][0] and score[2][1] < best[2][1]:
                best = score
    print(best)
    return best