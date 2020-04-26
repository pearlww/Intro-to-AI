import tkinter as tk
from consts import *
from GUI import BoardCanvas
from chessboard import ChessBoard
from AI import Pearls_AI, Johans_AI, Jakobs_AI


class BoardFrame(tk.Frame):
    """The Frame Widget is mainly used as a geometry master for other widgets, or to
    provide padding between other widgets.
    """
    
    def __init__(self, board, master = None):
        tk.Frame.__init__(self, master)
        self.create_widgets()


    def create_widgets(self):
        
        self.boardCanvas = BoardCanvas(board,height = N*30+100, width = N*30+30)
        #self.boardCanvas.bind('<Button-1>', self.boardCanvas.gameStart)
        self.boardCanvas.pack()


if __name__ == "__main__":
    window = tk.Tk()
    window.wm_title("GOMOKU GAME")

    board = ChessBoard()
    gui_board = BoardFrame(board,window)
    gui_board.pack()

    
    if MODE == 0: 
        gui_board.boardCanvas.bind('<Button-1>', gui_board.boardCanvas.player_click)
    elif MODE == 1:
        #ai=Pearls_AI(RATIO, board, BoardState.WHITE,DEPTH)    
        ai=Jakobs_AI(board, BoardState.WHITE, DEPTH)
        #ai=Johans_AI(board, BoardState.WHITE, DEPTH)
        gui_board.boardCanvas.bind('<Button-1>',lambda event, arg=ai: gui_board.boardCanvas.player_vs_AI(event,arg))
    else:  
        #ai2=Pearls_AI(RATIO, board, BoardState.BLACK,DEPTH) 
        ai1=Jakobs_AI(board, BoardState.BLACK, DEPTH)
        ai2=Jakobs_AI(board, BoardState.WHITE, DEPTH)
        gui_board.boardCanvas.bind('<Button-1>',lambda event, ai1=ai1, ai2=ai2: gui_board.boardCanvas.AI_vs_AI(event,ai1,ai2))        

    window.mainloop()