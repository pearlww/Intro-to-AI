from consts import *
from chessboard import ChessBoard
from AIs import AI_Jakob, AI_Johan


class Pearls_AI(object):
    
    def __init__(self,ratio,board,state,depth):

        self.ratio = ratio
        self.gameBoard= board
        self.pos=[-1,-1]
        self.depth=depth
        self.state=state


    def change_state(self,state):
        if state == BoardState.BLACK:
            return BoardState.WHITE
        else:
            return BoardState.BLACK

            
    def cal_shape(self, i, j, xdirection, ydirection,state,shape_count):

        shape=[]

        for step in range(-5, 5):  
            #beyond the border
            if j + xdirection * step < 0 or j + xdirection * step >= N:
                break
            if i + ydirection * step < 0 or i + ydirection * step >= N:
                break
          
            # calculate the shape    
            if self.gameBoard.get_current_position_state(i + ydirection * step,j + xdirection * step) == state:
                shape.append(1)
            elif self.gameBoard.get_current_position_state(i + ydirection * step,j + xdirection * step) == BoardState.EMPTY:
                shape.append(0)
            else:
                shape.append(2)

        # move window to find if there is a threat shape
        max_threat_shape_index=-1
        for index,threat_shape in enumerate(threat_list):
            for i in range(5):
                window5=shape[i:i+5]
                window6=shape[i:i+6]
                if window5==threat_shape or window6==threat_shape:
                    # successful match, then to find the max threat shape
                    # the higher index, the higher threat
                    if index > max_threat_shape_index:
                        max_threat_shape_index = index
                        max_threat_shape = threat_shape

        if max_threat_shape_index == -1:
            #print("no threat in this direction")
            pass
        else:
            if max_threat_shape_index < 2:
                shape_count[5] += 1
            elif max_threat_shape_index < 5:
                shape_count[4] += 1
            elif max_threat_shape_index < 8:
                shape_count[3] += 1
            elif max_threat_shape_index < 13:
                shape_count[2] += 1
            elif max_threat_shape_index < 14:
                shape_count[1] += 1
            else:
                shape_count[0] += 1


    # give score of each place
    def evaluate(self,state):

        # the input state is enemy's
        enemy_state=state
        # four directions: horizontal, vertical, two diagonals
        directions = [[1, 0], 
                      [0, 1], 
                      [1, -1], 
                      [1, 1]]

        for i in range(N):
            for j in range(N):
                if self.gameBoard.get_current_position_state(i,j)== BoardState.EMPTY:
                    continue
                else:
                    for axis in directions:                                       
                        self.cal_shape(i, j, axis[0],axis[1],enemy_state,enemy_shapes)        
        
        #print("enemy shapes:", enemy_shapes)
        enemy_score = np.sum(WEIGHTS*enemy_shapes)

        my_state = self.change_state(state)        
        for i in range(N):
            for j in range(N):
                if self.gameBoard.get_current_position_state(i,j)== BoardState.EMPTY:
                    continue
                else:
                    for axis in directions:                                       
                        self.cal_shape(i, j, axis[0],axis[1],my_state,my_shapes)

        #print("my shapes:", my_shapes)
        my_score = np.sum(WEIGHTS*my_shapes)

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

        #max
        if state == BoardState.BLACK:
            value = -9999
            for i in range(N):
                for j in range(N):
                    if self.gameBoard.get_current_position_state(i,j) == BoardState.EMPTY:
                        # try a move
                        self.set_board(i,j,state)
                        score = self.minimax_tree(depth-1,BoardState.WHITE)
                        if score>value:
                            value=score
                            self.pos=[i,j]
                        # undo the move    
                        self.reset_board(i,j)

        #min
        elif state == BoardState.WHITE:
            value = 9999
            for i in range(N):
                for j in range(N):
                    if self.gameBoard.get_current_position_state(i,j) == BoardState.EMPTY:
                        # try a move
                        self.set_board(i,j,state)
                        score = self.minimax_tree(depth-1,BoardState.BLACK)
                        if score<value:
                            value=score
                            self.pos=[i,j]
                        self.reset_board(i,j)

        return value

    def search(self):

        value=self.minimax_tree(self.depth,self.state)
        if self.pos!=[-1,-1]:
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
    def generate(self):
        pass
    
class Johans_AI(object):
    def __init__(self,board,state,depth):
        self.gameBoard= board
        self.pos=[-1,-1]
        self.depth=depth
        if state == BoardState.WHITE:
            self.Player = 1
        else:
            self.Player = -1
        self.backend_board = np.zeros((N,N))
    
    def search(self):
        for i in range(N):
            for j in range(N):
                if self.gameBoard.get_current_position_state(i,j) == BoardState.WHITE:
                    self.backend_board[i,j] = 1
                elif self.gameBoard.get_current_position_state(i,j) == BoardState.BLACK:
                    self.backend_board[i,j] = -1
                else:
                    self.backend_board[i,j] = 0

        self.pos = AI_Johan(self.backend_board, self.Player)

        if self.pos!=[-1,-1]:
            print("position of AI:", self.pos)
            return self.pos
        else:
            print("AI error")

class Jakobs_AI(object):
    def __init__(self,board,state,depth):
        self.gameBoard= board
        self.pos=[-1,-1]
        self.depth=depth
        if state == BoardState.WHITE:
            self.Player = 1
        else:
            self.Player = -1
        self.backend_board = np.zeros((N,N))
    
    def search(self):
        for i in range(N):
            for j in range(N):
                if self.gameBoard.get_current_position_state(i,j) == BoardState.WHITE:
                    self.backend_board[i,j] = 1
                elif self.gameBoard.get_current_position_state(i,j) == BoardState.BLACK:
                    self.backend_board[i,j] = -1
                else:
                    self.backend_board[i,j] = 0

        self.pos = AI_Jakob(self.backend_board, self.Player)

        print(self.backend_board)
        if self.pos!=[-1,-1]:
            print("position of AI:", self.pos)
            return self.pos
        else:
            print("AI error")