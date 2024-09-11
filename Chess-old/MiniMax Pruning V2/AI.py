class AI:
    def basic_move(self, board, colour, opp_colour, depth, retMax, current_value):
        all_moves = self.lib.get_all_moves(board, colour, True, self.lib.moves_made[-1])
        values = []
        current_max = -100
        current_min = 100
        mod = 10

        if all_moves == []:
            return None, None

        if depth > 0:
            branch_value = 0

            for move in all_moves:
                p_board = copy.deepcopy(board)
                self.lib.move_pseudo_piece(p_board, move)
                self.positions_assessed += 1

                if self.positions_assessed % mod == 0:
                    print("%d positions assessed" %self.positions_assessed)
                
                branch_value, _ = self.basic_move(p_board, opp_colour, colour, depth - 1, not retMax, (current_max if retMax else current_min))
                    
                if branch_value == None:
                    continue

                if retMax:
                    if branch_value < current_value:
                        return [branch_value, move]
                else:
                    branch_value = -branch_value

                    if branch_value > current_value:
                        return [branch_value, move]
                    
                if branch_value > current_max:
                    current_max = branch_value

                if branch_value < current_min:
                    current_min = branch_value

                values.append([branch_value, move])

            return self.pick_move(values, retMax)

        else:
            for move in all_moves:
                p_board = copy.deepcopy(board)
                self.lib.move_pseudo_piece(p_board, move)
                self.positions_assessed += 1
                
                if self.positions_assessed % mod == 0:
                    print("%d positions assessed" %self.positions_assessed)

                branch_value = self.lib.assess_board(p_board)

                if retMax:
                    values.append([branch_value, move])
                else:
                    values.append([-branch_value, move])
            
            selection = self.pick_move(values, retMax)

            return selection

    def promote_pawn(self, board):
        rand = random.randint(1, 4) # random integer
        pieces = ['q', 'r', 'b', 'k'] # list of available promotions
        
        return pieces[rand] # return a random promotion piece

    def pick_move(self, moves, retMax):
        valid_moves = []
        count = 0
        val = 0

        if retMax:
            val = max(moves)[0]
        else:
            val = min(moves)[0]

        for i in range(len(moves)):
            move = moves[i]

            if move[0] == val:
                count += 1
                valid_moves.append(move)

        rand = random.randint(0, count - 1)
        move = valid_moves[rand]

        return move

    def random_move(self, board, piece_dict, colour):
        # get all legal moves and then validate all of them at once
        moves = [move for move in self.lib.get_moves(board, piece_dict, colour, False) if self.lib.move_is_valid(board, move)]
        
        # pick a random move
        rand_int = random.randint(0, len(moves) - 1)
        move = moves[rand_int]

        return move

    def make_move(self, board, piece_dict, proficiency, colour):
        opp_colour = ('w' if colour == 'b' else 'b')

        if proficiency == 1:
            move = self.random_move(board, piece_dict, colour)
            return move

        '''elif proficiency == 2:
            self.positions_assessed = 0
            move_values = self.move(board, colour, opp_colour, 1, True)
            move = self.pick_move(move_values, True)

            if basic_move == (None, None):
                print("Game over! Player wins!")
                exit()

            move = basic_move[1]
            state = self.lib.assess_board(board)

            if self.lib.move_is_valid(board, move, colour):
                self.lib.move_piece(move)
                self.lib.next_player()'''

    def __init__(self, lib_object):
        self.lib = lib_object



import copy, random, time
import numpy as np

if __name__ == '__main__':
    import Lib
    lib = Lib.Lib()
    
    board = lib.init_board()

    start = time.time()
    lib.assess_board(lib.board)
    print("Run time: %f s" %(time.time() - start))

    #AI = AI(lib)
    #AI.make_move(board, 2, 'w')

    #print(lib.print_board(lib.board))