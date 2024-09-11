'''
The library (Lib) and Piece objects of the main chess program. The Lib
object contains all universal game data such as the board, several
constants, and useful methods accessible to all external processes.
The Piece object is a container for quick access to imperative piece
data. It also links the piece to its move function: a piece-specific
function that returns available moves for that piece.
'''

class Piece:
    def __init__(self, piece_code, value, pos, move_function_pointer):
        self.has_moved = False
        self.colour = piece_code[0]
        self.type = piece_code[1]
        self.code = piece_code
        self.value = value
        self.pos = pos
        
        if move_function_pointer != None:
            setattr(self, 'get_moves', move_function_pointer)



class Lib:
    def print_board(self, board):
        print_board = [[None]*8, [None]*8, [None]*8, [None]*8, [None]*8, [None]*8, [None]*8, [None]*8]

        for row in range(8):
            for col in range(8):
                print_board[row][col] = board[row][col].colour + board[row][col].type

        print(print_board)

    def get_all_moves(self, board, colour, only_valid_moves, last_move):
        pieces = self.get_pieces(board, colour, False)

        return self.get_all_moves2(board, colour, only_valid_moves, last_move, pieces)


    def get_all_moves(self, board, colour, only_valid_moves, last_move, pieces):
        all_moves = []
        
        for piece in pieces:
            moves = self.get_moves(board, piece.pos)

            if only_valid_moves:
                for move in moves:
                    if self.move_is_valid(board, move, colour):
                        all_moves.append(move)

            else:
                for move in moves:
                    all_moves.append(move)

        return all_moves
    
    def get_pieces(self, board, colour, get_object):
        pieces = []

        if get_object:
            for row in range(8):
                for col in range(8):
                    sqr = board[row][col]

                    if sqr.colour == colour:
                        pieces.append(sqr)

        else:
            for row in range(8):
                for col in range(8):
                    sqr = board[row][col]

                    if sqr.colour == colour:
                        pieces.append([row, col])

        return pieces

    
    def find_piece(self, board, code):
        for row in range(8):
            for col in range(8):
                piece = board[row][col]

                if piece.colour + piece.type == code:
                    return [row, col]

        return [None, None]
    '''
    def is_in_check(self, board, colour):
        king_pos = self.find_piece(board, colour + 'K')
        row, col = king_pos

        ### Straights
        for i in range(1, col + 1): # row to the left of piece
            sqr = board[row][col - i]
            
            if sqr.colour == colour:
                break

            elif sqr.colour != '-':
                if sqr.type == 'Q' or sqr.type == 'R':
                    return True

                break

        for i in range(col + 1, 8): # row to the right
            sqr = board[row][i]
            
            if sqr.colour == colour:
                break

            elif sqr.colour != '-':
                if sqr.type == 'Q' or sqr.type == 'R':
                    return True

                break

        for i in range(1, row + 1): # upper column
            sqr = board[row - i][col]

            if sqr.colour == colour:
                break

            elif sqr.colour != '-':
                if sqr.type == 'Q' or sqr.type == 'R':
                    return True

                break

        for i in range(row + 1, 8): # lower column
            sqr = board[i][col]

            if sqr.colour == colour:
                break

            elif sqr.colour != '-':
                if sqr.type == 'Q' or sqr.type == 'R':
                    return True

                break


        ### Diagonals
        for i in range(1, 8): # upper left diagonal
            rw, cl = [row - i, col - i]

            if rw < 0 or cl < 0:
                break

            sqr = board[rw][cl]
        
            if sqr.colour == colour:
                break

            elif sqr.colour != '-':
                if sqr.type == 'Q' or sqr.type == 'D':
                    return True

                break
        
        for i in range(1, 8): # lower right diagonal
            rw, cl = [row + i, col + i]

            if rw >= 8 or cl >= 8:
                break
        
            sqr = board[rw][cl]
        
            if sqr.colour == colour:
                break

            elif sqr.colour != '-':
                if sqr.type == 'Q' or sqr.type == 'D':
                    return True

                break
        
        for i in range(1, 8): # lower left diagonal
            rw, cl = [row + i, col - i]

            if rw >= 8 or cl < 0:
                break

            sqr = board[rw][cl]
        
            if sqr.colour == colour:
                break

            elif sqr.colour != '-':
                if sqr.type == 'Q' or sqr.type == 'D':
                    return True

                break

        for i in range(1, 8):               #upper right diagonal
            rw, cl = [row - i, col + i]

            if rw < 0 or cl >= 8:
                break
        
            sqr = board[rw][cl]
        
            if sqr.colour == colour:
                break

            elif sqr.colour != '-':
                if sqr.type == 'Q' or sqr.type == 'D':
                    return True

                break

        ### Knight moves
        knight_moves = [[row - 2, col - 1], [row - 2, col + 1],
                        [row + 2, col - 1], [row + 2, col + 1],
                        [row - 1, col - 2], [row + 1, col - 2],
                        [row - 1, col + 2], [row + 1, col + 2]]

        for move in knight_moves:
            rw, cl = move
                
            if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                sqr = board[rw][cl]

                if sqr.colour != colour and sqr.type == 'N':
                    return True
        

        ### Pawn moves
        # upper_pawns = [[row + 1, col - 1], [row + 1, col + 1]]
        # lower_pawns = [[row - 1, col - 1], [row - 1, col + 1]]

        if colour == 'w':
            if row + 1 < 8 and col - 1 >= 0:
                sqr = board[row + 1][col - 1]

                if sqr.colour == 'b' and sqr.type == 'P':
                    return True

            elif row + 1 < 8 and col + 1 < 8:
                sqr = board[row + 1][col + 1]

                if sqr.colour == 'b' and sqr.type == 'P':
                    return True

        elif colour == 'b':
            if row - 1 >= 0 and col - 1 >= 0:
                sqr = board[row - 1][col - 1]

                if sqr.colour == 'w' and sqr.type == 'P':
                    return True

            elif row - 1 >= 0 and col + 1 < 8:
                sqr = board[row - 1][col + 1]

                if sqr.colour == 'w' and sqr.type == 'P':
                    return True

        return False
    '''

    def next_player(self):
        if self.current_player == 'w':
            self.current_player = 'b'
        else:
            self.current_player = 'w'

    def assess_board(self, board):
        key_values = [0, 0, 0, 0, 0] # material value (50%), centre space (20%), 
                                     # available moves (10%), 
        
        ### Calculate material value
        white_pieces = self.get_pieces(board, 'w', True)
        black_pieces = self.get_pieces(board, 'b', True)

        white_value = 0
        black_value = 0
        
        for piece in white_pieces:
            white_value += piece.value

        for piece in black_pieces:
            black_value += piece.value


        ### Calculate centre space control
        white_moves = self.get_all_moves(board, 'w', True, self.moves_made[-1], white_pieces)
        black_moves = self.get_all_moves(board, 'b', True, self.moves_made[-1], black_pieces)

        centre_squares = [[3, 3], [3, 4], [4, 3], [4, 4]]
        centre_adjacents = [[2, 2], [2, 3], [2, 4], [2, 5],
                            [3, 2], [3, 5], [4, 2], [4, 5],
                            [5, 2], [5, 3], [5, 4], [5, 5]]

        centre_value_white = 0
        centre_value_black = 0

        for move in white_moves:
            if move in centre_adjacents:
                centre_value_white += 0.5
            elif move in centre_squares:
                centre_value_white += 1
        
        for move in black_moves:
            if move in centre_adjacents:
                centre_value_black += 0.5
            elif move in centre_squares:
                centre_value_black += 1


        ### Calculate piece space to move
        num_white_moves = len(white_moves)
        num_black_moves = len(black_moves)


        ### Load values
        key_values[0] = (white_value - black_value)
        key_values[1] = (centre_value_white - centre_value_black)/20 # 20 is double the value of all centre squares and adjacents being occupied. This somewhat normalises the value
        key_values[2] = (num_white_moves - num_black_moves)/20 # suppose 20 is max number of available moves


        ### Calculate final board value
        state_value = key_values[0]*0.5 + key_values[1]*0.2 + key_values[2]*0.1

        return state_value



    def get_pieces_from_board(self, board, colour):
        pieces = []

        for row in range(8):
            for col in range(8):
                sqr = board[row][col]

                if sqr.colour == colour:
                    pieces.append(sqr)

        return pieces
  
    def assess_position(self, board, colour):
        pieces = self.get_pieces(board, colour)

        for piece in pieces:
            piece.get_moves()
        P = 200*(wK - bK) + 9*(wR - bR) + 3*() + (wP - bP) - 0.5*(wD - bD + wS - bS + wI - bI) + 0.1*(wM - bM)
    
    '''def get_moves(self, board, pos):
        moves = []
        row, col = pos
        piece = board[row][col]

        options = {'K': self.king_moves(board, pos, piece.colour),
                   'Q': self.queen_moves(board, pos, piece.colour),
                   'R': self.rook_moves(board, pos, piece.colour),
                   'B': self.bishop_moves(board, pos, piece.colour),
                   'K': self.knight_moves(board, pos, piece.colour),
                   'P': self.pawn_moves(board, pos, piece.colour, self.moves_made[-1])
                   }

        moves = options[piece.type]

        tally = 0

        for code in self.PIECE_CODES[:6]: # white pieces
            tally += len(self.piece_dict[code])

        print(f'{tally}: number of white pieces left')

        return moves

    '''
    
    def move_pseudo_piece(self, board, move):
        # move first piece indexed. This will always happen
        start_pow, end_pos = move[:2]

        board[end_pos] = board[start_pos]
        board[start_pos] = self.EMPTY

        # get move size
        size = len(move)

        if size == 3: # if move is size 3, en pasan is at play. Destroy piece referenced in third index
            dead_pos = move[2]
            board[dead_pos] = self.EMPTY

        elif size == 4: # if move is size 4, castling is at play. Move second piece (ie the rook) to desired location
            rook_start_pos, rook_end_pos = move[3:5]

            board[rook_end_pos] = board[rook_start_pos]
            board[rook_start_pos] = self.EMPTY






    def get_moves(self, board, piece_dict, colour): # return available moves in a singular list of tuple pairs not segregated by separate pieces [(start_pos), (end_pos), ...]
        moves = []

        if colour == 'w':
            moves = [[piece.get_moves(board, piece, True, self.moves_made[-1]) for piece in piece_dict[code]][0] for code in self.PIECE_CODES[:6]]
        else:
            moves = [[piece.get_moves(board, piece, True, self.moves_made[-1]) for piece in piece_dict[code]][0] for code in self.PIECE_CODES[7:]]

        return moves

    def is_in_check(self, board, colour):
        king = self.piece_dict[colour + 'K'][0]

        opp_colour = ('b' if colour == 'w' else 'w')

        all_moves = []

        for move_set in self.get_moves(board, self.piece_dict, opp_colour):
            all_moves += move_set

        all_moves = [move[1] for move in all_moves] # remove start indicies and special move indicies as we only care about offended squares

        if king.pos in all_moves:
            print(f'{king.pos} exists within the following list')
            print(all_moves)
            return True
        else:
            print(f'{king.pos} does not exist within the following list')
            print(all_moves)

        return False
    
    def move_is_valid(self, board, move, colour):
        # unpack move data and validate indicies
        start_pos, end_pos = move[:2]

        for _, index in enumerate(start_pos + end_pos):
            if index < 0 or 7 < index:
                return False

        piece = board[start_pos]
        end_sqr = board[end_pos]


        # perform basic special move validations
        if len(move) == 3: # en pasan
            dead_pos = move[2]

            if board[dead_pos].type != 'P':
                return False

        elif len(move) == 4: # castling
            rook = board[move[3]]

            if piece.has_moved or rook.has_moved:
                return False


        # validate types and colours
        if piece.code == '--' or piece.colour == end_sqr.colour:
            return False


        # ensure a self-check does not result after the move
        p_board = copy.deepcopy(board)
        self.move_piece(p_board, move)
        check = self.is_in_check(p_board, colour)

        if check:
            print(f'{colour} is in check')
            return False
        else:
            print(f'{colour} is not in check')

        # check move is a valid piece move
        piece_moves = piece.get_moves(board, piece, False, self.moves_made[-1])

        for piece_move in piece_moves:
            if piece_move[0:2] == move: # only test first two indicies. A player move will only contain clicked squares, not full special moves
                return True

        # if the move check above has failed, return false
        return False

    def move_piece(self, board, move):
        start_pos, end_pos = move[:2] # ensure only first two positions are loaded

        # update piece data
        board[start_pos].has_moved = True
        board[start_pos].pos = end_pos

        # move piece, overwrite end position and destroy piece reference at start position
        board[end_pos] = board[start_pos]
        board[start_pos] = self.EMPTY

        # get move size
        size = len(move)

        if size == 3: # if move is size 3, en pasan is at play. Destroy piece referenced in third index
            dead_pos = move[2]
            board[dead_pos] = self.EMPTY

        elif size == 4: # if move is size 4, castling is at play. Move second piece (ie the rook) to desired location
            rook_start_pos, rook_end_pos = move[3:5]
            
            board[rook_start_pos].has_moved = True
            board[rook_start_pos].pos = rook_end_pos

            board[rook_end_pos] = board[rook_start_pos]
            board[rook_start_pos] = self.EMPTY
    
    def king_moves(self, board, piece, threatened, _):
        row, col = piece.pos
        
        # the eight squares surrounding the king
        moves = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col - 1),
                 (row, col + 1), (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

        available_moves = []
        
        # standard moves
        for rw, cl in moves:
            if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                available_moves.append([(row, col), (rw, cl)])

        # castling
        if not piece.has_moved:
            # castling right
            if board[row, col + 1].colour == '-' and board[row, col + 2] == '-' and not board[row, col + 3].has_moved:
                available_moves.append([(row, col), (row, col + 2), (row, col + 3), (row, col + 1)])

            # castling left
            if board[row, col - 1].colour == board[row, col - 2] == board[row, col - 3].colour == '-' and not board[row, col - 4].has_moved:
                available_moves.append([(row, col), (row, col - 2), (row, col - 4), (row, col - 1)])

        return available_moves

    def queen_moves(self, board, piece, threatened_only, _):
        row, col = piece.pos
        moves = []

        ### Straights
        for i in range(1, col + 1): # row to the left of piece
            rw, cl = (row, col - i)
            moves.append((rw, cl))
            
            if board[rw, cl].colour != '-':
                break

        for i in range(col + 1, 8): # row to the right
            rw, cl = (row, i)
            moves.append((rw, cl))
            
            if board[rw, cl].colour != '-':
                break

        for i in range(1, row + 1): # upper column
            rw, cl = (row - i, col)
            moves.append((rw, cl))
            
            if board[rw, cl].colour != '-':
                break

        for i in range(row + 1, 8): # lower column
            rw, cl = (i, col)
            moves.append((rw, cl))
            
            if board[rw, cl].colour != '-':
                break


        ### Diagonals
        for i in range(1, 8): # upper left diagonal
            rw, cl = (row - i, col - i)

            if rw < 0 or cl < 0:
                break
            
            sqr = board[rw, cl]
            moves.append((rw, cl))

            if sqr.colour != '-':
                break
            
        for i in range(1, 8): # lower right diagonal
            rw, cl = (row + i, col + i)

            if rw >= 8 or cl >= 8:
                break

            sqr = board[rw, cl]
            moves.append((rw, cl))

            if sqr.colour != '-':
                break
            
        for i in range(1, 8): # lower left diagonal
            rw, cl = (row + i, col - i)

            if rw >= 8 or cl < 0:
                break

            sqr = board[rw, cl]
            moves.append((rw, cl))

            if sqr.colour != '-':
                break

        for i in range(1, 8): # upper right diagonal
            rw, cl = (row - i, col + i)

            if rw < 0 or cl >= 8:
                break
            
            sqr = board[rw, cl]
            moves.append((rw, cl))

            if sqr.colour != '-':
                break

        valid_moves = []

        if threatened_only:
            for move in moves:
                valid_moves.append([(row, col), move])
        else:
            for move in moves:
                if board[move].colour != piece.colour:
                    valid_moves.append([(row, col), move])

        return valid_moves

    def rook_moves(self, board, piece, threatened_only, _):
        row, col = piece.pos
        moves = []

        for i in range(1, col + 1): # row to the left of piece
            rw, cl = (row, col - i)
            moves.append((rw, cl))
            
            if board[rw, cl].colour != '-':
                break

        for i in range(col + 1, 8): # row to the right
            rw, cl = (row, i)
            moves.append((rw, cl))
            
            if board[rw, cl].colour != '-':
                break

        for i in range(1, row + 1): # upper column
            rw, cl = (row - i, col)
            moves.append((rw, cl))
            
            if board[rw, cl].colour != '-':
                break

        for i in range(row + 1, 8): # lower column
            rw, cl = (i, col)
            moves.append((rw, cl))
            
            if board[rw, cl].colour != '-':
                break

        valid_moves = []

        if threatened_only:
            for move in moves:
                valid_moves.append([(row, col), move])
        else:
            for move in moves:
                if board[move].colour != piece.colour:
                    valid_moves.append([(row, col), move])

        return valid_moves

    def bishop_moves(self, board, piece, threatened_only, _):
        row, col = piece.pos
        moves = []

        for i in range(1, 8): # upper left diagonal
            rw, cl = (row - i, col - i)

            if rw < 0 or cl < 0:
                break
            
            sqr = board[rw, cl]
            moves.append((rw, cl))

            if sqr.colour != '-':
                break
            
        for i in range(1, 8): # lower right diagonal
            rw, cl = (row + i, col + i)

            if rw >= 8 or cl >= 8:
                break

            sqr = board[rw, cl]
            moves.append((rw, cl))

            if sqr.colour != '-':
                break
            
        for i in range(1, 8): # lower left diagonal
            rw, cl = (row + i, col - i)

            if rw >= 8 or cl < 0:
                break

            sqr = board[rw, cl]
            moves.append((rw, cl))

            if sqr.colour != '-':
                break

        for i in range(1, 8): # upper right diagonal
            rw, cl = (row - i, col + i)

            if rw < 0 or cl >= 8:
                break
            
            sqr = board[rw, cl]
            moves.append((rw, cl))

            if sqr.colour != '-':
                break

        valid_moves = []

        if threatened_only:
            for move in moves:
                valid_moves.append([(row, col), move])
        else:
            for move in moves:
                if board[move].colour != piece.colour:
                    valid_moves.append([(row, col), move])
        
        return valid_moves

    def knight_moves(self, board, piece, threatened_only, _):
        row, col = piece.pos
        
        moves = [(row - 2, col - 1), (row - 2, col + 1),
                    (row + 2, col - 1), (row + 2, col + 1),
                    (row - 1, col - 2), (row + 1, col - 2),
                    (row - 1, col + 2), (row + 1, col + 2)]

        available_moves = []
        valid_moves = []

        for move in moves:
            rw, cl = move
                        
            if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                available_moves.append(move)

        if threatened_only:
            for move in available_moves:
                valid_moves.append([(row, col), move])
        else:
            for move in available_moves:
                if board[move].colour != piece.colour:
                    valid_moves.append([(row, col), move])

        return valid_moves

    def pawn_moves(self, board, piece, threatened_only, last_move):
        row, col = piece.pos

        delta = (-1 if piece.colour == 'w' else 1) # delta denotes direction of travel for white (up board hence -1) or black (down board hence +1)
        moves = [(row + delta, col), (row + 2*delta, col)]
        threats = [(row + delta, col - 1), (row + delta, col + 1)]

        available_moves = []
        available_threats = []

        # forward moves
        for rw, cl in moves:
            if 0 <= rw and rw <= 7 and 0 <= cl and cl <= 7:
                if board[rw, cl].code == '--':
                    available_moves.append([(row, col), (rw, cl)])
                else:
                    break

        # attack moves
        for rw, cl in threats:
            if 0 <= rw and rw <= 7 and 0 <= cl and cl <= 7:
                if board[rw, cl].code != '--':
                    available_threats.append([(row, col), (rw, cl)])

        # en pasan
        if last_move != None:
            pass

        if threatened_only:
            return available_threats
        else:
            print(f'pawn moves {available_moves + available_threats}')
            return available_moves + available_threats

        


        '''
        # different colours move in different directions
        if piece.colour == 'w':
            if row - 1 >= 0:
                if col - 1 >= 0:
                    if board[row - 1, col - 1].colour == 'b':
                        moves.append([(row, col), (row - 1, col - 1)])

                if col + 1 < 8:
                    if board[row - 1, col + 1].colour == 'b':
                        moves.append([(row, col), (row - 1, col + 1)])

                if board[row - 1, col].colour == '-':
                    moves.append([(row, col), (row - 1, col)])

                    if not piece.has_moved and board[row - 2, col].colour == '-':
                        moves.append([(row, col), (row - 2, col)])

            # en pasan
            if row == 3 and last_move != None and last_move != [None]: # white can only use en pasan in this row
                start_index, end_index = last_move
                row_start, col_start = start_index
                row_end, col_end = end_index
                
                last_piece = board[row_end, col_end]

                if abs(row_end - row_start) == 2 and last_piece.type == 'P': # check the piece moved two squares forward and is a pawn
                    if end_index == (row, col + 1):
                        moves.append([(row, col), (row - 1, col + 1), (row, col + 1)])

                    elif end_index == [row, col - 1]:
                        moves.append([(row, col), (row - 1, col - 1), (row, col - 1)])
        else:
            if row + 1 < 8:
                if col - 1 >= 0:
                    if board[row + 1, col - 1].colour == 'w':
                        moves.append([(row, col), (row + 1, col - 1)])

                if col + 1 < 8:
                    if board[row + 1, col + 1].colour == 'w':
                        moves.append([(row, col), (row + 1, col + 1)])

                if board[row + 1, col].colour == '-':
                    moves.append([(row, col), (row + 1, col)])

                    if not piece.has_moved and board[row + 2, col].colour == '-':
                        moves.append([(row, col), (row + 2, col)])

            # en pasan
            if row == 4 and last_move != [None]: # black can only use en pasan in this row
                start_index, end_index = last_move
                row_start, col_start = start_index
                row_end, col_end = end_index
                
                last_piece = board[row_end, col_end]

                if abs(row_end - row_start) == 2 and last_piece.type == 'P': # check the piece moved two squares forward and is a pawn
                    if end_index == (row, col + 1):
                        moves.append([(row, col), (row + 1, col + 1), (row, col + 1)])

                    elif end_index == (row, col - 1):
                        moves.append([(row, col), (row + 1, col - 1), (row, col - 1)])
                        
        return moves
        '''

    def init_board(self):
        tmp = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                 ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                 ['--', '--', '--', '--', '--', '--', '--', '--'],
                 ['--', '--', '--', '--', '--', '--', '--', '--'],
                 ['--', '--', '--', '--', '--', '--', '--', '--'],
                 ['--', '--', '--', '--', '--', '--', '--', '--'],
                 ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                 ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        board = np.empty((8, 8), dtype=Piece)

        # replace string data with object references
        for row in range(8):
            for col in range(8):
                code = tmp[row][col]

                if code == '--':
                    board[row, col] = self.EMPTY
                else:
                    if code[1] == 'K':
                        board[row, col] = Piece(code, 200, (row, col), self.king_moves)
                    elif code[1] == 'Q':
                        board[row, col] = Piece(code, 9, (row, col), self.queen_moves)
                    elif code[1] == 'R':
                        board[row, col] = Piece(code, 5, (row, col), self.rook_moves)
                    elif code[1] == 'B':
                        board[row, col] = Piece(code, 3, (row, col), self.bishop_moves)
                    elif code[1] == 'N':
                        board[row, col] = Piece(code, 3, (row, col), self.knight_moves)
                    elif code[1] == 'P':
                        board[row, col] = Piece(code, 1, (row, col), self.pawn_moves)
                    else:
                        print('Error. Piece code not found.')
                        exit()

        return board

    def init_piece_dict(self, board):
        dict = {'wK': [], 'wQ': [], 'wR': [], 'wB': [], 'wN': [], 'wP': [], 'bK': [], 'bQ': [], 'bR': [], 'bB': [], 'bN': [], 'bP': []}
        
        for row in range(8):
            for col in range(8):
                obj = board[row][col]

                if obj.code != '--':
                    dict[obj.code].append(obj)

        return dict

    def __init__(self):
        # initialise game constants
        self.EMPTY = Piece('--', 0, [None, None], None)
        self.PIECE_CODES = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']

        # initialise base game variables
        self.current_player = 'w'
        self.moves_made = [None] # store game moves. None is important for later use
        self.game_over = False
        self.player1_colour = 'w'
        self.player2_colour = 'b'
        self.board = self.init_board() # dynamic numpy array containing Piece variables

        # initialise piece-tracking dictionaries
        self.piece_move_dict = {'K': self.king_moves, 'Q': self.queen_moves, 'R': self.rook_moves, 'B': self.bishop_moves, 'N': self.knight_moves, 'P': self.pawn_moves}
        self.piece_dict = self.init_piece_dict(self.board)


        
        
import numpy as np
import copy

if __name__ == '__main__':
    move = [(1, 2), (3, 3)]
    start_pos, end_pos = move[:2]

    for i, m in enumerate(start_pos + end_pos):
        print(m)
