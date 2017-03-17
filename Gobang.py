import re
#from random import randint
from board import GameBoard
from players import Human_Player, AI_Player
import time

#def set_play_order(players):
#    whos_first = randint(1,2)
#    # If number was 2, we want to reverse the player's order
#    if (whos_first == 2):
#        players.reverse()

players = []
size=11
depth=2
board = GameBoard(size)
players.append(AI_Player("AI", board, 0, depth))
players.append(Human_Player("Human", board, 1, depth))

playing = True
while playing:
#    set_play_order(players)
    print "\nMATCH: %s vs %s." % (players[0].get_name(), players[1].get_name())
    print board
    moves = 0
    current_player_id = 0
    active_turn = True
    while active_turn:
        moves += 1
        player = players[current_player_id]       
        print "%s's turn: Move #%d..." % (player.get_name(), moves)
        start_time=time.time()
        player.make_move()
        print board
        print time.time()-start_time
        if board.winner != None:
            active_turn = False
        else:
            if (current_player_id == 1):
                current_player_id = 0
            else:
                current_player_id = 1

    if (board.winner == 0 or 1):
        print "The WINNER is %s!\n" % players[board.winner].get_name()
    else:
        print "It was a TIE game!\n"

    playing = False


