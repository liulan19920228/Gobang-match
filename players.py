import re
from random import randint

class Human_Player:
    def __init__(self, player_name, board, player_id, depth):
        self.name = player_name
        self.game = board
        self.color = board.marker_color(player_id)
        self.cut_level = depth
        if self.color == 1:
            self.adv_color =-1
        else:
            self.adv_color = 1        
        self.size = self.game.board_size()

    def get_name(self):
        return self.name

    def make_move(self):
        result = True
        while result:
            move = raw_input("%s's <Move> (row,col): " % self.name)            
            location = re.split('(\d+)', move)
            if location[1].isdigit() and location[0].isalpha():
#            if True:
                col = ord(location[0])-96-1
                row = int(location[1])-1
#                col=randint(0,self.size-1)
#                row=randint(0,self.size-1)
                if (row >= 0 and col >=0 and row < self.size and col < self.size):
                    pos = self.game.index(row, col)
                    if (self.game.is_cell_legal(pos)):
                        self.game.do_move(pos, self.color)
                        print pos/self.size, pos-pos/self.size*self.size
                        result = False
                    else:
                        print "That spot has been taken, try a new one"
                else:
                    print "Wrong range of row and colume"
            else:
                print "Please enter a row in letter, and a column in number"

class AI_Player(Human_Player):
    move = []

    def evaluation(self):
        return self.eval_fn(self.color) - 1.1*self.eval_fn(self.adv_color)
    

    def eval_fn(self, val):

#        W5=2000.0
        W4=2000.0
        W3=1000.0
        W2=10.0
        W1=50.0
        if self.game.win_step(val) != None:
            return 10000.0
#        Five_connect = self.pattern_counter([[0,val,val,val,val,0]])
        Four_connect = self.pattern_counter([[0,val,val,val,val,0]])
        Three_connect = self.pattern_counter([[0,val,val,val,0],[val,0,val,val,val],[val,val,0,val,val],[val,val,val,0,val]])
        Two_connect = self.pattern_counter([[0,val,val,0,0],[0,0,val,val,0]])
        score = Four_connect * W4 + Three_connect* W3 + Two_connect *W2

#        if Two_connect>1:
#            score += W1
#        if Three_connect>1:
#            score +=W5
#        if Four_connect>1:
#            score +=W5
        return score

    def pattern_counter(self, p):
        count = 0
        for pos in self.game.moves:
            row = pos/self.size
            col = pos - row*self.size
            for i in range(0,len(p)):
                count3=0
                for d in [[1,1],[1,-1],[0,1],[1,0],[0,-1],[-1,0],[-1,-1],[-1,1]]:
                    new_row = row +(len(p[i])-2)*d[1]
                    new_col = col +(len(p[i])-2)*d[0]
                    count2 = 0
                    if 0<=new_row<self.size and 0<=new_col<self.size and 0<=row +(-1)*d[1]<self.size and 0<=col +(-1)*d[0]<self.size:
                        for j in range(-1,len(p[i])-1):
                            if self.game.get_cell(self.game.index(row +j*d[1], col+j*d[0])) != p[i][j+1]:
                                break
                            else:
                                count2 +=1
                        if count2 >= len(p[i]):
                            count3 += 1
                count +=count3
        return count
        
    def alpha_beta_prunning(self):
        def minimax(alpha,beta,depth,color):
            if depth == 0 or not self.game.winner is None:
                return self.evaluation()
            if color == self.color:
                v = float('-inf')
                for action in self.game.move_set():
                    self.game.do_move(action,color)
                    v = max(v,minimax(alpha,beta,depth-1,self.game.othercolor(color)))
                    self.game.undo_move(action)
                    alpha = max(alpha,v)
                    if alpha >= beta:
                        return alpha
                return v
            v=float('inf')
            for action in self.game.move_set():
                self.game.do_move(action,color)
                v = min(v,minimax(alpha,beta,depth-1,self.game.othercolor(color)))
                self.game.undo_move(action)
                beta = min(beta,v)
                if beta <= alpha:
                    return beta
            return v
               
##        def max_value(alpha,beta,depth):
##            if depth == 0 or not self.game.winner is None:
##                return self.evaluation()
##            v = float('-inf')
##            for action in self.game.move_set():
##                self.game.do_move(action, self.color)
##                v = max(v, min_value(alpha, beta, depth-1))
##                self.game.undo_move(action)
##                alpha = max(alpha, v)
##                if alpha>= beta:
##                    return alpha
##            return v
##
##        def min_value(alpha,beta,depth):
##            if depth == 0 or not self.game.winner is None:
##                return self.evaluation()
##            v=float('inf')
##            for action in self.game.move_set():
##                self.game.do_move(action, self.adv_color)
##                v = min(v, max_value(alpha, beta, depth-1))
##                self.game.undo_move(action)
##                beta = min(beta, v)
##                if beta <= alpha:
##                    return beta
##            return v
        
        best_score = float('-inf')
        beta = float('inf')
        best_action = None
        for a in self.game.move_set():
            self.game.do_move(a, self.color)
#            v = min_value(best_score, beta, self.cut_level-1)
            v=minimax(best_score,beta,self.cut_level-1,self.game.othercolor(self.color))
            self.game.undo_move(a)
            if v > best_score:
                best_score = v
                best_action = a
        return best_action
        
    def make_move(self):
        if len(self.game.moves) == 0:
            self.game.do_move(self.game.index(self.size/2, self.size/2), self.color)
            print self.size/2, self.size/2
            return
        pos= self.game.win_step(self.color)
        if pos != None:
            self.game.do_move(pos, self.color)
            print pos/self.size, pos-pos/self.size*self.size
            return
        pos= self.game.win_step(self.adv_color)
        if pos != None:
            self.game.do_move(pos, self.color)
            print pos/self.size, pos-pos/self.size*self.size
            return
        else:
            for p in self.game.move_set():
                self.game.do_move(p,self.color)
                if self.pattern_counter([[0,self.color,self.color,self.color,self.color,0]])>0:
                    return
                else:
                    self.game.undo_move(p)

        pos=self.alpha_beta_prunning()
        self.game.do_move(pos, self.color)
        print pos/self.size, pos-pos/self.size*self.size
        return
            




