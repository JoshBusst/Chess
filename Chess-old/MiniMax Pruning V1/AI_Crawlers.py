class AI:
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

    def basic_move(self, board, colour, opp_colour, depth, retMax, current_value):
        all_moves = self.lib.get_valid_moves(board, colour)
        values = []
        current_max = -100
        current_min = 100
        mod = 1000

        if all_moves == []:
            return None, None

        if depth > 0:
            branch_value = 0

            for move in all_moves:
                p_board = copy.copy(board)
                self.lib.move_pseudo_piece(p_board, move)
                self.positions_assessed += 1

                if self.positions_assessed % mod == 0:
                    pass #print("%d positions assessed" %self.positions_assessed)
                
                branch_value, _ = self.basic_move(p_board, opp_colour, colour, depth - 1, not retMax, current_max)
                    
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
                p_board = copy.copy(board)
                self.lib.move_pseudo_piece(p_board, move)
                self.positions_assessed += 1
                
                if self.positions_assessed % mod == 0:
                    pass #print("%d positions assessed" %self.positions_assessed)

                branch_value = self.lib.assess_board(p_board, colour)

                '''print(p_board)
                print(branch_value)
                print()'''

                if retMax:
                    values.append([branch_value, move])
                else:
                    values.append([-branch_value, move])
            
            selection = self.pick_move(values, retMax)

            return selection

    def random_move(self, board, colour):
        moves = self.lib.get_valid_moves(board, colour)
        
        rand_int = random.randint(0, len(moves) - 1)
        move = moves[rand_int]

        return move

    def make_move(self, board, proficiency, colour):
        opp_colour = 'w'

        if colour == 'w':
            opp_colour = 'b'

        if proficiency == 1:
            move = self.random_move(board, colour)
            
            print("Current board state prior: %d" %self.lib.assess_board(board, colour))

            if self.lib.move_is_valid(move, colour):
                self.lib.move_piece(move)
                self.lib.next_player()

            print("Current board state after: %d" %self.lib.assess_board(board, colour))

        elif proficiency == 2:
            self.positions_assessed = 0
            move_tree = self.basic_move(board, colour, opp_colour, 1, True, -100)

            if move_tree == (None, None):
                print("Game over! Player wins!")
                exit()

            start_pos = move_tree[1][0]
            end_pos = move_tree[1][1]

            move = [start_pos, end_pos]
            state = self.lib.assess_board(board, colour)
            
            if False:
                move_tree2 = self.basic_move(board, colour, opp_colour, 1, True, -100)
                move_tree3 = self.basic_move(board, colour, opp_colour, 2, True, -100)
                start_pos2 = move_tree[1][0]
                start_pos3 = move_tree[1][0]
                end_pos2 = move_tree[1][1]
                end_pos3 = move_tree[1][1]
                move2 = [start_pos2, end_pos2]
                move3 = [start_pos3, end_pos3]
                print(move2)
                print(move3)
                print(move_tree2[0] - state)
                print(move_tree3[0] - state)

            if self.lib.move_is_valid(move, colour):
                self.lib.move_piece(move)
                self.lib.next_player()

    def __init__(self, lib_object):
        self.lib = lib_object



import copy, random, numpy, time

if __name__ == '__main__':
    a = [[-3, [[0, 1], [2, 0]]], [-3, [[0, 1], [2, 2]]], [-3, [[0, 2], [1, 1]]], [-3, [[0, 2], [2, 0]]], [-3, [[0, 7], [0, 6]]], [-3, [[1, 0], [2, 0]]], [-3, [[1, 0], [3, 0]]], [-3, [[1, 2], [2, 2]]], [-3, [[1, 2], [3, 2]]], [-3, [[1, 3], [2, 3]]], [-3, [[1, 4], [2, 4]]], [-3, [[1, 5], [2, 5]]], [-3, [[1, 5], [3, 5]]], [-3, [[1, 6], [2, 6]]], [-3, [[1, 6], [3, 6]]], [-3, [[1, 7], [2, 7]]], [-3, [[1, 7], [3, 7]]], [-3, [[2, 1], [3, 1]]], [-3, [[3, 3], [5, 2]]], [-3, [[3, 3], [5, 4]]], [0, [[3, 3], [4, 1]]], [0, [[3, 3], [2, 5]]], [-3, [[3, 3], [4, 5]]]]

    import Chesslib
    lib = Chesslib.Lib()
    
    board = numpy.zeros((8, 8))
    board = lib.init_board(board)

    AI = AI(lib)
    print(AI.pick_move(a, True))
    #print('basic move')
    #print(AI.basic_move(board, 'w', 'b', 1, True))