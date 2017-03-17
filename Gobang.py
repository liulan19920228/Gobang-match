import re
import sys
#from random import randint
from board import GameBoard
from players import Human_Player, AI_Player
import time

players = []
size = 11
depth = 2
Reverse = False
for i in range(len(sys.argv)):
    if sys.argv[i] == ‘-l’
       Reverse = True
    if sys.argv[i] == ‘-n’
       size = int(sys.argv[i+1])
end

board = GameBoard(size)
if not Reverse:
    players.append(Human_Player("human", board, 0, depth))
    players.append(AI_Player("COM", board, 1, depth))
else:
    players.append(Human_Player("COM", board, 0, depth))
    players.append(AI_Player("human", board, 1, depth))
        

playing = True
while playing:
#    print "\nMATCH: %s vs %s." % (players[0].get_name(), players[1].get_name())
    print board
    moves = 0
    current_player_id = 0
    active_turn = True
    while active_turn:
        moves += 1
        player = players[current_player_id]       
#        print "%s's turn: Move #%d..." % (player.get_name(), moves)
        start_time=time.time()
        player.make_move()
        print board
#        print time.time()-start_time
        if board.winner != None:
            active_turn = False
        else:
            if (current_player_id == 1):
                current_player_id = 0
            else:
                current_player_id = 1

    if (board.winner == 0 ):
        print "Dark plyer %s wins!\n" % players[board.winner].get_name()
    elif (board.winner == 1):
        print "Light player %s wins!\n" % players[board.winner].get_name()
    else:
        print "It was a TIE game!\n"

    playing = False





