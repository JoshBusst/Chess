'''
The library (Lib) and Piece objects of the main chess program. The Lib
object contains all universal game data such as the board, several
constants, and useful methods accessible to all external processes.
The Piece object is a container for quick access to imperative piece
data. It also links the piece to its move function: a piece-specific
function that returns available moves for that piece.
'''

class Piece:
    def dummy_function(self, *args):
        return [[]]

    def sterilise(self):
        self.has_moved = None
        self.colour = '-'
        self.type = '-'
        self.code = '--'
        self.value = 0
        self.pos = (None, None)

        setattr(self, 'get_moves', self.dummy_function)

    def __init__(self, piece_code, value, pos, move_function_pointer):
        self.has_moved = False
        self.colour = piece_code[0]
        self.type = piece_code[1]
        self.code = piece_code
        self.value = value
        self.pos = pos
        
        if move_function_pointer != None:
            setattr(self, 'get_moves', move_function_pointer)
        else:
            setattr(self, 'get_moves', self.dummy_function)




class Lib:
    def get_all_moves(self, board, colour, only_valid_moves, last_move):
        pieces = self.get_pieces(board, colour, False)

        return self.get_all_moves2(board, colour, only_valid_moves, last_move, pieces)

    def get_all_moves(self, board, colour, only_valid_moves, last_move, pieces):
        all_moves = []
        
        for piece in pieces:
            moves = self.get_moves(board, piece.pos)

            if only_valid_moves:
                for move in moves:
                    if self.move_is_valid(board, move):
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

    def assess_position(self, board, colour):
        pieces = self.get_pieces(board, colour)

        for piece in pieces:
            piece.get_moves()
        P = 200*(wK - bK) + 9*(wR - bR) + 3*() + (wP - bP) - 0.5*(wD - bD + wS - bS + wI - bI) + 0.1*(wM - bM)
    

        
    def print_board(self, board):
        print([[piece.code for piece in row] for row in board])

    def next_player(self):
        self.current_player = 'w' if self.current_player == 'b' else 'b'

    def get_moves(self, board, piece_dict, colour, threatened_only): # return available moves in a singular list of tuple pairs not segregated by separate pieces [(start_pos), (end_pos), ...]
        moves = []

        for code in (self.PIECE_CODES[:6] if colour == 'w' else self.PIECE_CODES[6:]):
            for piece in piece_dict[code]:
                piece_moves = piece.get_moves(board, piece, threatened_only, self.moves_made[-1])
                moves += piece_moves

        moves = [move for move in moves if move != []]

        return moves

    def is_in_check(self, board, piece_dict, colour):
        king = piece_dict[colour + 'K'][0]
        opp_colour = ('b' if colour == 'w' else 'w')

        # get offended squares and format them such that only end positions are retained, remove start and special move indicies
        #offended_squares = [move[1] for move in self.get_moves(board, piece_dict, opp_colour, True)]
        offended_squares = self.get_moves(board, piece_dict, opp_colour, True)

        # check if king is present in the list of offended squares
        lst = [sqr[1] for sqr in offended_squares]
        if king.pos in lst:
            sqr = offended_squares[lst.index(king.pos)][0]
            print(f'{king.pos} is under attack by {sqr}')
            #print(offended_squares)
            return True
        else:
            pass
            #print(f'{king.pos} does not exist within the following list')
            #print(offended_squares)

        return False
    
    def move_is_valid(self, board, move):
        # unpack move data and validate indicies
        start_pos, end_pos = move[:2]
        
        # set up quick access, easily readable variable aliases. Validate piece variable
        piece = board[start_pos]
        end_sqr = board[end_pos]

        if piece.code == '--':
            return False

        # ensure move indicies are valid
        for _, index in enumerate(start_pos + end_pos):
            if index < 0 or 7 < index:
                return False

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
        piece_dict = self.init_piece_dict(p_board)
        self.move_piece(p_board, move)
        check = self.is_in_check(p_board, piece_dict, piece.colour)

        if check:
            #print(f'{piece.colour} is in check')
            #self.print_board(p_board)
            return False
        else:
            pass
            #print(f'{piece.colour} is not in check')

        # check move is a valid piece move
        piece_moves = piece.get_moves(board, piece, False, self.moves_made[-1])

        for piece_move in piece_moves:
            if piece_move[0:2] == move: # only test first two indicies. A player move will only contain clicked squares, not full special moves
                return True

        # if the move check above has failed, return false
        return False

    def move_piece(self, board, move):
        start_pos, end_pos = move[:2] # ensure only first two positions are loaded

        # update piece data and piece dict
        board[start_pos].has_moved = True
        board[start_pos].pos = end_pos
        board[end_pos].sterilise() # empty the piece instance so it cannot be later used by piece_dict

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
            if board[row, col + 1].colour == board[row, col + 2].colour == '-' and not board[row, col + 3].has_moved:
                available_moves.append([(row, col), (row, col + 2), (row, col + 3), (row, col + 1)])

            # castling left
            if board[row, col - 1].colour == board[row, col - 2].colour == board[row, col - 3].colour == '-' and not board[row, col - 4].has_moved:
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
        moves = [(row + delta, col), (row + 2*delta, col)] if piece.has_moved else [(row + delta, col), (row + 2*delta, col)] # legal forward moves for a pawn
        threats = [(row + delta, col - 1), (row + delta, col + 1)] # squares threatened by the pawn

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
            return available_moves + available_threats

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

        ''' be careful when working with board and piece_dict variables. These
            should contain exactly the same object references and hence update
            one another, however they can be sneaky in that if a variable
            is only deleted from one list and not the other, the reference
            still exists and can be used, causing all sorts of problems'''


        
        
import numpy as np
import copy

if __name__ == '__main__':
    lib = Lib()

    lib.print_board(lib.board)