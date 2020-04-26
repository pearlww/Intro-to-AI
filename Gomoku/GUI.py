# Part of the GUI code is referenced from https://github.com/TongTongX/Gomoku/blob/master/board_gui.py 

import tkinter as tk
import math

from consts import *



class BoardCanvas(tk.Canvas):
    """Apply the tkinter Canvas Widget to plot the game board and stones."""
    
    def __init__(self, board, master=None, height=0, width=0):
        
        tk.Canvas.__init__(self, master, height=height, width=width)
        # show the board
        self.draw_gameBoard()

        self.gameBoard = board
        self.turn = BoardState.BLACK
        self.depth = DEPTH
        self.gameover=False

        self.prev_exist = False
        self.prev_row = -1
        self.prev_col = -1


    def draw_gameBoard(self):
        """Plot the game board."""

        # N horizontal lines
        for i in range(N):
            start_pixel_x = (i + 1) * 30
            start_pixel_y =  30
            end_pixel_x = (i + 1) * 30
            end_pixel_y = N * 30
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

        # N vertical lines
        for j in range(N):
            start_pixel_x =  30
            start_pixel_y = (j + 1) * 30
            end_pixel_x = N * 30
            end_pixel_y = (j + 1) * 30
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

        # place a "star" to particular intersections 
        self.draw_star((N-3)/4,(N-3)/4)    #(3,3)
        self.draw_star((3*N-1)/4,(N-3)/4)  #(11,3)
        self.draw_star((N-1)/2,(N-1)/2)    #(7,7)
        self.draw_star((N-3)/4,(3*N-1)/4)  #(3,11)
        self.draw_star((3*N-1)/4,(3*N-1)/4)#(11,11)


    def draw_star(self, row, col):
        """Draw a "star" on a given intersection
        
        Args:
            row, col (i.e. coord of an intersection)
        """
        start_pixel_x = (row + 1) * 30 - 2
        start_pixel_y = (col + 1) * 30 - 2
        end_pixel_x = (row + 1) * 30 + 2
        end_pixel_y = (col + 1) * 30 + 2
        
        self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill = 'black')


    def draw_stone(self, row, col):
        """Draw a stone (with a circle on it to denote latest move) on a given intersection.
        
        Specify the color of the stone depending on the turn.
        
        Args:
            row, col (i.e. coord of an intersection)
        """

        inner_start_x = (row + 1) * 30 - 4
        inner_start_y = (col + 1) * 30 - 4
        inner_end_x = (row + 1) * 30 + 4
        inner_end_y = (col + 1) * 30 + 4

        outer_start_x = (row + 1) * 30 - 6
        outer_start_y = (col + 1) * 30 - 6
        outer_end_x = (row + 1) * 30 + 6
        outer_end_y = (col + 1) * 30 + 6

        start_pixel_x = (row + 1) * 30 - 10
        start_pixel_y = (col + 1) * 30 - 10
        end_pixel_x = (row + 1) * 30 + 10
        end_pixel_y = (col + 1) * 30 + 10
        
        if self.turn == BoardState.BLACK:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')
            self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='white')
            self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='black')
        elif self.turn == BoardState.WHITE:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')
            self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='black')
            self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='white')


    def draw_prev_stone(self, row, col):
        """Draw the previous stone with single color.
        
        Specify the color of the stone depending on the turn.
        
        Args:
            row, col (i.e. coord of an intersection)
        """
        
        start_pixel_x = (row + 1) * 30 - 10
        start_pixel_y = (col + 1) * 30 - 10
        end_pixel_x = (row + 1) * 30 + 10
        end_pixel_y = (col + 1) * 30 + 10
        
        if self.turn == BoardState.BLACK:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')
        elif self.turn == BoardState.WHITE:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')


    def change_state(self):
        if self.turn == BoardState.BLACK:
            self.turn = BoardState.WHITE
        else:
            self.turn = BoardState.BLACK


    def one_step(self,row,col):
        

        self.draw_stone(row,col)

        if self.prev_exist == False:
            self.prev_exist = True
        else:
            self.draw_prev_stone(self.prev_row, self.prev_col)

        self.prev_row, self.prev_col = row, col

        self.gameBoard.set_current_position_state(row,col,self.turn)

        # check result
        result = self.gameBoard.get_chess_result()

        # If the user wins the game, end the game and unbind.
        if  result != BoardState.EMPTY:
            self.create_text( (N*30+30)/2, N*30+50, text = '{} WINS !!'.format(result.name))
            print("{} WINS !!".format(result.name))
            self.unbind('<Button-1>')
            self.gameover=True

        # change turn and go on    
        else:
            self.change_state()
            print('{} turn now...\n'.format(self.turn._name_))

        # show the updated chess board
        map=self.gameBoard.get_chessBoard()
        print(m.value for m in map)


    def player_click(self,event):

        valid_pos = False

        # since a user might not click exactly on an intersection, place the stone onto
        # the intersection closest to where the user clicks
        for i in range(N):
            for j in range(N):
                pixel_x = (i + 1) * 30
                pixel_y = (j + 1) * 30
                square_x = math.pow((event.x - pixel_x), 2)
                square_y = math.pow((event.y - pixel_y), 2)
                distance =  math.sqrt(square_x + square_y)

                # since there is noly one intersection such that the distance between it 
                # and where the user clicks is less than 15, it is not necessary to find 
                # the actual least distance
                if (distance < 15) and (self.gameBoard.get_current_position_state(i,j) == BoardState.EMPTY):
                    valid_pos = True
                    self.one_step(i,j)
                    break	# break the inner for loop
            else:
                continue 

            break		# break the outer for loop
        
        return valid_pos

    def AI_vs_AI(self,event,ai):
        
        ret =self.player_click(event)
        if ret and (not self.gameover):       
            # # unbind to ensure the user cannot click anywhere until the program has placed a white stone already
            # self.unbind('<Button-1>')

            pos = ai.search()
            self.one_step(pos[0],pos[1])

            # # bind after the program makes its move so that the user can continue to play	    
            # self.bind('<Button-1>', lambda event, arg=ai: self.player_vs_AI(event,arg))
        else:
            print("Invalid position")

    def player_vs_AI(self,event,ai):

        ret =self.player_click(event)
        if ret and (not self.gameover):       
            # # unbind to ensure the user cannot click anywhere until the program has placed a white stone already
            # self.unbind('<Button-1>')

            pos = ai.search()
            self.one_step(pos[0],pos[1])

            # # bind after the program makes its move so that the user can continue to play	    
            # self.bind('<Button-1>', lambda event, arg=ai: self.player_vs_AI(event,arg))
        else:
            print("Invalid position")
    
    def AI_vs_AI(self,event,ai1,ai2):
        while not self.gameover:
            pos = ai1.search()
            self.one_step(pos[0],pos[1])
            if self.gameover:
                break
            pos = ai2.search()
            self.one_step(pos[0],pos[1])   
       

       



