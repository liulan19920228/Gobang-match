import string
import math
import numpy as np
class GameBoard:
    markers = {0: " ", -1: "L", 1: "D"}
    values=[1,-1]
    winner = None
    moves = []
    movesnum = 0
    board = []
   
    def __init__(self, board_size):
        self.size = board_size
        self.board = [0 for i in xrange(self.size * self.size)] 

    def is_cell_legal(self, pos):
        if (pos < 0 or pos >= self.size *self.size):
            return False
        return (self.board[pos] == 0)

    def othercolor(self,val):
        if val == 1:
            result = -1
        elif val == -1:
            result = 1
        return result
        
    
    def index(self, row, col):
        return (self.size*row+col)
    
    def board_size(self):
        return self.size

#    def terminate(self):
#        return (0 not in self.board)

    def marker_color(self,order):
        return self.values[order]

#    def set_cell(self, row, col, val):
#        self.board[row][col] = val

    def get_cell(self, pos):
        return (self.board[pos])

    def do_move(self,pos,val):
        if not self.is_cell_legal(pos):
            return False
        elif self.win_status(pos,val):
            self.winner=self.values.index(val)
        elif self.movesnum == self.size*self.size:
            self.winner = -1  #TIE
        self.moves.append(pos)
        self.board[pos] = val
        self.movesnum +=1
        return True

    def undo_move(self,pos):
        self.movesnum -=1
        self.winner = None
        self.board[pos] = 0
        self.moves.remove(pos)
                
    def move_set(self):
        result = []
        for x in self.moves:
            if (x+1)%self.size != 0:
                if self.is_cell_legal(x+1):
                    result.append(x+1)
                if self.is_cell_legal(x+self.size+1):
                    result.append(x+self.size+1)
                if self.is_cell_legal(x-self.size+1):
                    result.append(x-self.size+1)
            if x%self.size != 0:
                if self.is_cell_legal(x-1):
                    result.append(x-1)
                if self.is_cell_legal(x+self.size-1):
                    result.append(x+self.size-1)
                if self.is_cell_legal(x-self.size-1):
                    result.append(x-self.size-1)
            if self.is_cell_legal(x+self.size):
                result.append(x+self.size)
            if self.is_cell_legal(x-self.size):
                result.append(x-self.size)
        return np.unique(result)            

    def win_status(self, pos, val):
        row = pos/self.size
        col = pos - row*self.size
        for d in [(0,1),(1,0),(1,1),(1,-1)]:
            count = 1
            for s in [-1, 1]:
                for i in range(1, 5):
                    new_row = row + d[1]*i*s
                    new_col = col +d[0]*i*s
                    if (new_row < 0 or new_row >= self.size or new_col < 0 or new_col >= self.size or self.get_cell(self.index(new_row, new_col)) != val):
                        break
                    else:
                        count += 1
                    self.c1=count
            if count >= 5:
                return True
            
        return False

    def win_step(self, val):
        for pos in self.move_set():
            if (self.win_status(pos, val)):
                return pos
        return


    def __str__(self):
        display = "\n "+" "
        for x in range(self.size):
            display += "   " + str(string.lowercase[x])
        display += "\n"
        for row in range(self.size):
            display += "   "+('+'+ '-'*3)*self.size+'+'+'\n'
            if row < 9:
                display +=" "               
            display += str(row + 1) +" | "
            for col in range(self.size):
                display += self.markers[self.get_cell(self.index(row, col))] + " | "
            display += "\n"
        display += "   "+('+'+ '-'*3)*self.size+'+'+'\n'
        return display 
