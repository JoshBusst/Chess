class AI:
    def promote_pawn(self, board):
        rand = random.randint(1, 4)

        if rand == 1:
            return 'q'
        
        elif rand == 2:
            return 'r'
        
        elif rand == 3:
            return 'b'
        
        else:
            return 'k'



    def weight_move(move, colour, board):
        return 0




    def recurse_move_tree(branch):
        threshold_value = 0             #if a move is more valuable than this, investigate future moves. Elsewise continue
        #current_depth = 0               #move depth the machine is currently at
        #explored_depth = 0          #current depth machine has fully explored

        for i in range(len(self.move_tree[self.layer_track])):     #recurse first layer
            pass

            '''move = available_moves[i]
            
            self.main.move_piece(move, board, pieces, False)
            
            weight = self.weight_move(move, colour, board)
            moves = self.main.compile_moves(opp_colour, board)

            self.move_tree.append([move, weight, moves])'''



    def calc_move_tree(available_moves, colour, board):     #syntax for move_tree branch: [[[move1, weight], [move2, weight]], [[moves following move 1], [moves following move 2]]]
        white_pieces = copy.deepcopy(main.white_pieces)
        black_pieces = copy.deepcopy(main.black_pieces)

        self.layer_track = 0
        
        if len(move_tree) == 0:
            self.move_tree = [[]]
            
            for i in range(len(available_moves)):
                move = available_moves[i]

                weight = self.weight_move(move, colour, board)

                self.move_tree[0].append([move, weight])

        else:
            branch = self.move_tree[-1]
            
            if len(branch) > 1:             #the second last branch of the tree. For when a branch has started calculating the next branch but has yet to finish
                branch = self.move_tree[-2]
                next_branch = self.move_tree[-1]        #branch being calculated

                for i in range(len(branch)):
                    calculated_moves = [move[0] for move in next_branch[i]]
                    avail_moves = self.main.compile_moves()

                    
                    '''if len(next_branch[i]) == 0:        #moves for next branch havent been calculated
                        pass
                    
                    else:                               #moves have been calculated, move along
                        continue'''
            
            
            '''for i in range(len(branch)):
                for j in range(len()):
                    move = branch[i]
                    weight = self.weight_move(move, colour, board)
                    self.move_tree.append([move, weight])

                    if weight >= threshold_value:       #if move is worth enough, explore further
                        pass'''

                



    '''def assess_special_move(self, f_board, move, colour, opp_colour):
        return None



    def assess_move(self, f_board, move, colour, opp_colour):
        #en pasan or castling
        if len(move) > 2:
            return self.assess_special_move(f_board, move, coour, opp_colour)


        start_index, end_index = move



        
        #self.chess.move_piece(move, f_board)



    def weight_moves(self, board, moves, colour, opp_colour):
        #weight the available moves for a given colour based on the immediate
        #board state without considering future moves
        
        weights = []


        for move in moves:     #make each move theoretically and then assess the outcome board state
            f_board = copy.deepcopy(board)
            self.chess.move_piece(move, f_board)

            #board_state = self.assess_move(f_board, move, colour, opp_colour)
            
            weights.append(board_state)


        return weights'''
                
    
    
    def make_move(self, input_board, proficiency, colour):
        board = copy.deepcopy(input_board)          #this object is now an independant copy of input_board
        opp_colour = ''
        pieces = []

        if colour == 'white':
            opp_colour = 'white'
            pieces = [self.main.white_pieces, self.main.black_pieces]       #pieces relating to colour go first
        else:
            opp_colour = 'black'
            pieces = [self.main.black_pieces, self.main.white_pieces]

        '''
        After assessing the current board state and depth 1 moves, take each top rated
        move and assess it x moves in advance. After determining how the move plays
        out, assess the next move and so on. Do this within a given time frame of
        however many seconds corresponding to difficulty level. The faster moves are
        analysed the more moves can be assessed etc. After time limit is reached, take
        best move from what has been assessed.

        Assess immediate board state and move value based on factors such as centre
        space claim, opponent piece offence, piece defence, centre space attack,
        attacking higher level pieces, reducing opponent potential, increasing
        own potential, developing pieces, castling potential, reducing threat to
        own king and increasing threat to opponent king
        '''

        '''
        Another form of AI may assess each piece on the board at random and make a decisive
        move based on which moves available to it surpass a certain threshold. This
        threshold may be defined by any arbitrary difficulty definition system, but may
        also be subject to the events of the game such as how well the opponent is playing.
        If an opponent plays well, the threshold may increase, and better moves may need to
        be found as the AI becomes 'nervous'. Similarly if an opponent plays poorly the
        threshold may lower and the AI may 'relax' and become 'more confident' in response,
        considering less moves before making a decision and deciding faster.
        '''


        available_moves = self.main.compile_moves(colour, board)
        

        if int(proficiency) == 1:            #return an arbitrary selection of the available moves
            rand = random.randint(0, len(available_moves) - 1)

            move = available_moves[rand]

            return move

        elif proficiency == 2:          #return a semi proficient move
            pass

        elif proficiency == 3:
            #using the 'move tree' method instead of the standard weighted moves method

            self.calc_move_tree(available_moves, colour, board)
        
            '''weighted_moves = self.weight_moves(board, available_moves, colour, opp_colour)
            highest = [0, None]        #highest value then index. more indicies may also follow if multiple moves are weighted the same

            #find highest weighted move
            for i in range(len(weighted_moves)):
                weight = weighted_moves[i]
                
                if weight > highest[0]:
                    highest = [weight, i]

                elif weight == highest[0]:
                    highest.append(i)


            return highest'''

                        
    
    def __init__(self, main):
        self.board = []
        self.move_tree = []
        self.main = main


import copy, random, numpy
