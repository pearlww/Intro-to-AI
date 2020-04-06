from consts import *
from chessboard import ChessBoard
import numpy as np


class AI(object):
    
    def __init__(self,ratio,board,color,depth):

        self.ratio = ratio
        self.gameBoard= board
        self.pos=[-1,-1]
        self.depth=depth
        self.color=color
        
        # Five, liveFour, sleepFour, liveThree, sleepThree, liveTwo
       # self.my_shapes=np.array([0,0,0,0,0,0])
        #self.enemy_shapes=np.array([0,0,0,0,0,0])


    def change_state(self,state):
        if state == BoardState.BLACK:
            return BoardState.WHITE
        else:
            return BoardState.BLACK

            
    def cal_shape(self, i, j, state,shape_count):

        # four directions: horizontal, vertical, two diagonals
        directions = [(1, 0), 
                      (0, 1), 
                      (1, -1), 
                      (1, 1)]

        for (xdirection, ydirection) in directions:
            shape=[]
            for step in range(-5, 5):  
                #beyond the border
                if j + xdirection*step < 0 or j + xdirection*step >= N:
                    continue
                if i + ydirection*step < 0 or i + ydirection*step >= N:
                    continue
            
                # calculate the shape    
                if self.gameBoard.get_current_position_state( i+ydirection*step, j+xdirection*step) == state:
                    shape.append(1)
                elif self.gameBoard.get_current_position_state( i+ydirection*step, j+xdirection*step) == BoardState.EMPTY:
                    shape.append(0)
                else:
                    shape.append(-1)


            threat_shape_index = -1
            if len(shape)<5:
                continue
            elif len(shape)==5:                
                for index,threat_shape in enumerate(threat_list):
                    if shape==threat_shape:
                        if index > threat_shape_index:
                            threat_shape_index = index                
            else:
                # move window to find if there is a threat shape
                for index,threat_shape in enumerate(threat_list):
                    for offset in range(len(shape)-5):
                        window6=shape[offset:offset+6]
                        if window6==threat_shape:
                            # successful match, then to find the max threat shape
                            # the higher index, the higher threat
                            if index > threat_shape_index:
                                threat_shape_index = index


            if threat_shape_index == -1:
                continue
            if threat_shape_index < 2:
                shape_count[5] += 1
            elif threat_shape_index < 5:
                shape_count[4] += 1
            elif threat_shape_index < 8:
                shape_count[3] += 1
            elif threat_shape_index < 13:
                shape_count[2] += 1
            elif threat_shape_index < 14:
                shape_count[1] += 1
            else:
                shape_count[0] += 1

        return shape_count

    # give score of the current chessboard
    def evaluate(self,state):

        self.my_shapes=np.array([0,0,0,0,0,0])
        self.enemy_shapes=np.array([0,0,0,0,0,0])

        for i in range(N):
            for j in range(N):
                if self.gameBoard.get_current_position_state(i,j)== BoardState.EMPTY:
                    continue
                else:              
                    self.enemy_shapes += self.cal_shape(i, j, state, self.enemy_shapes)        
       
        for i in range(N):
            for j in range(N):
                if self.gameBoard.get_current_position_state(i,j)== BoardState.EMPTY:
                    continue
                else:                                 
                    self.my_shapes += self.cal_shape(i, j, self.change_state(state), self.my_shapes)


        enemy_score = np.sum(WEIGHTS*self.enemy_shapes)
        my_score = np.sum(WEIGHTS*self.my_shapes)

        total_score = RATIO * my_score - enemy_score 
                    
        return total_score


    def reset_board(self,i,j):
        self.gameBoard.set_current_position_state(i,j,BoardState.EMPTY)


    def set_board(self,i,j,state):
        self.gameBoard.set_current_position_state(i,j,state)


    # DFS(recursive search the whole board and find the best place)
    def minimax_tree(self,depth,state):

        if depth == 0:    
            return self.evaluate(state)

        #min
        if state == BoardState.BLACK:
            value = 9999
            for i in range(N):
                for j in range(N):

                    if not self.has_neighbor([i,j]):
                        continue

                    if self.gameBoard.get_current_position_state(i,j) == BoardState.EMPTY:
                        # try a move
                        self.set_board(i,j,state)
                        score = self.minimax_tree(depth-1,BoardState.WHITE)
                        if score<value:        
                            value=score
                            self.pos=[i,j]
                        # undo the move    
                        self.reset_board(i,j)
            return value

        # max (AI)
        elif state == BoardState.WHITE:
            value = -9999
            score_map = [[value for j in range(N)] for i in range(N)]

            for i in range(N):
                for j in range(N):

                    if not self.has_neighbor([i,j]):
                        continue

                    if self.gameBoard.get_current_position_state(i,j) == BoardState.EMPTY:
                        # try a move
                        self.set_board(i,j,state)
                        score = self.minimax_tree(depth-1,BoardState.BLACK)
                        score_map[i][j]=score

                        if score>value:
                            my_shapes = self.my_shapes
                            enemy_shapes = self.enemy_shapes
                            value=score
                            self.pos=[i,j]
                        self.reset_board(i,j)
            print("score map:\n", np.matrix(score_map))
            print("enemy shapes:", enemy_shapes)
            print("my shapes:", my_shapes)
            return value


    def search(self):

        value=self.minimax_tree(self.depth,self.color)
        if self.pos != [-1,-1]:
            print("position of AI:", self.pos)
            print("score of the position:", value)
            return self.pos
        else:
            print("AI error")    


    # optimization 1 
    def alpha_beta_pruning(self):
        pass

    
    # optimization 2 
    # instead of searching all places, searching most possible place
    def has_neighbor(self,pt):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if pt[0]+i<0 or pt[0]+i>=N or pt[1]+j<0 or pt[1]+j>=N:
                    continue
                if self.gameBoard.get_current_position_state(pt[0]+i, pt[1]+j) != BoardState.EMPTY:
                    return True
        return False
    
    