'''Each of the following classes defines a specfic piece
type. Each comes with built in values that are defined
upon creation and correspond to relvant piece info. The
classes define the board pieces as objects, making them
easier to access and draw information from. They also
come with an in-built 'get_available_moves' function that
returns all legal moves available to the piece (not
considering check restrictions), and a get_offended_squares
function that returns the squares the piece can attack
should the opportunity to do so arise.
'''

class Lib:
    def get_valid_moves(self, board, colour):
        all_moves = self.get_all_moves(board, colour, True, self.moves_made[-1])
        valid_moves = []

        for move_set in all_moves:
            for end_pos in move_set[1]:
                start_pos = move_set[0]
                move = [start_pos, end_pos]

                if self.move_is_valid(move, colour):
                    valid_moves.append(move)

        return valid_moves
         
    def get_all_moves(self, board, colour, only_available_moves, last_move):
        all_moves = []
        pieces = self.get_pieces(board, colour)
        
        for i in range(len(pieces)):
            code = str(pieces[i][0])
            piece_type = code[1]
            moves = self.get_moves(board, pieces[i][1], piece_type, colour, only_available_moves, self.moves_made[-1])
            
            if moves != None and moves != []:
                all_moves.append([pieces[i][1], moves])

        return all_moves
    
    def get_moves(self, board, start_pos, piece_type, colour, only_avaiable_moves, last_move):
        moves = []

        if piece_type == 'K' or piece_type == '1':
            moves = self.king_moves(board, start_pos, colour, only_avaiable_moves)
        elif piece_type == 'Q' or piece_type == '2':
            moves = self.queen_moves(board, start_pos, colour, only_avaiable_moves)
        elif piece_type == 'R' or piece_type == '3':
            moves = self.rook_moves(board, start_pos, colour, only_avaiable_moves)
        elif piece_type == 'B' or piece_type == '4':
            moves = self.bishop_moves(board, start_pos, colour, only_avaiable_moves)
        elif piece_type == 'N' or piece_type == '5':
            moves = self.knight_moves(board, start_pos, colour, only_avaiable_moves)
        elif piece_type == 'P' or piece_type == '6':
            moves = self.pawn_moves(board, start_pos, colour, only_avaiable_moves, last_move)
        else:
            return None

        return moves
    
    def get_pieces(self, board, colour):
        pieces = []
        colour_decimal = ''

        if colour == 'w':
            colour_decimal = '1'
        elif colour == 'b':
            colour_decimal = '2'

        for row in range(8):
            for col in range(8):
                code = str(board[row, col])

                if colour_decimal == code[0]:
                    pieces.append([code, [row, col]])

        return pieces

    def king_moves(self, board, start_pos, colour, only_avaiable_moves):
        row, col = start_pos
        
        #the eight squares surrounding the king
        moves = [[row - 1, col - 1], [row - 1, col], [row - 1, col + 1], [row, col - 1],
                 [row, col + 1], [row + 1, col - 1], [row + 1, col], [row + 1, col + 1]]

        available_moves = []

        if only_avaiable_moves:
            match_colour = ''

            if colour == 'w':
                match_colour = '1'
            elif colour == 'b':
                match_colour = '2'

            for move in moves:
                rw, cl = move
            
                if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                    piece_code = str(board[rw, cl])
                    piece_colour = piece_code[0]
               
                    if piece_colour != match_colour:
                        available_moves.append(move)
     
        else:
            for move in moves:
                rw, cl = move
            
                if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                    available_moves.append(move)

        return available_moves

    def queen_moves(self, board, start_pos, colour, only_avaiable_moves):
        row, col = start_pos
        moves = []
        available_moves = []

        # straights
        for i in range(1, col + 1):             #row to the left of piece
            moves.append([row, col - i])
        
            if board[row, col - i] != 0:
                break

        for i in range(col + 1, 8):             #right row
            moves.append([row, i])
        
            if board[row, i] != 0:
                break

        for i in range(1, row + 1):             #upper column
            moves.append([row - i, col])
        
            if board[row - i, col] != 0:
                break

        for i in range(row + 1, 8):             #lower column
            moves.append([i, col])
        
            if board[i, col] != 0:
                break

        #diagonals
        for i in range(1, 8):          #upper left diagonal
            rw, cl = [row - i, col - i]

            if rw < 0 or cl < 0:
                break
        
            moves.append([rw, cl])
        
            if board[rw, cl] != 0:
                break
        
        for i in range(1, 8):           #lower right diagonal
            rw, cl = [row + i, col + i]

            if rw >= 8 or cl >= 8:
                break
        
            moves.append([rw, cl])
        
            if board[rw, cl] != 0:
                break
        
        for i in range(1, 8):               #lower left diagonal
            rw, cl = [row + i, col - i]

            if rw >= 8 or cl < 0:
                break

            moves.append([rw, cl])
        
            if board[rw, cl] != 0:
                break

        for i in range(1, 8):               #upper right diagonal
            rw, cl = [row - i, col + i]

            if rw < 0 or cl >= 8:
                break
        
            moves.append([rw, cl])
        
            if board[rw, cl] != 0:
                break

        if only_avaiable_moves:
            match_colour = ''

            if colour == 'w':
                match_colour = '1'
            elif colour == 'b':
                match_colour = '2'

            for move in moves:
                rw, cl = move

                piece_code = str(board[rw, cl])
                piece_colour = piece_code[0]

                if piece_colour != match_colour:
                    available_moves.append(move)
        else:
            available_moves = moves

        return available_moves

    def rook_moves(self, board, start_pos, colour, only_avaiable_moves):
        row, col = start_pos
        available_moves = []
        moves = []

        for i in range(1, col + 1):             #row to the left of piece
            rw, cl = [row, col - i]
            moves.append([rw, cl])
            
            if board[rw, cl] != 0:
                break

        for i in range(col + 1, 8):
            rw, cl = [row, i]
            moves.append([rw, cl])
            
            if board[rw, cl] != 0:
                break

        for i in range(1, row + 1):
            rw, cl = [row - i, col]
            moves.append([rw, cl])
            
            if board[rw, cl] != 0:
                break

        for i in range(row + 1, 8):
            rw, cl = [i, col]
            moves.append([rw, cl])
            
            if board[rw, cl] != 0:
                break

        if only_avaiable_moves:
            match_colour = ''

            if colour == 'w':
                match_colour = '1'
            elif colour == 'b':
                match_colour = '2'          

            for move in moves:
                rw, cl = move

                piece_code = str(board[rw, cl])
                piece_colour = piece_code[0]
                
                if piece_colour != match_colour:
                    available_moves.append(move)
        else:
            for move in moves:
                if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                    available_moves.append(move)
            
        return available_moves

    def bishop_moves(self, board, start_pos, colour, only_avaiable_moves):
        row, col = start_pos
        available_moves = []
        moves = []

        for i in range(1, 8):          #upper left diagonal
            rw, cl = [row - i, col - i]

            if rw < 0 or cl < 0:
                break
            
            moves.append([rw, cl])
            
            if board[rw, cl] != 0:
                break
            
        for i in range(1, 8):           #lower right diagonal
            rw, cl = [row + i, col + i]

            if rw >= 8 or cl >= 8:
                break

            moves.append([rw, cl])
            
            if board[rw, cl] != 0:
                break
            
        for i in range(1, 8):               #lower left diagonal
            rw, cl = [row + i, col - i]

            if rw >= 8 or cl < 0:
                break

            moves.append([rw, cl])
            
            if board[rw, cl] != 0:
                break

        for i in range(1, 8):               #upper right diagonal
            rw, cl = [row - i, col + i]

            if rw < 0 or cl >= 8:
                break
            
            moves.append([rw, cl])
            
            if board[rw, cl] != 0:
                break

        if only_avaiable_moves:
            match_colour = ''

            if colour == 'w':
                match_colour = '1'
            elif colour == 'b':
                match_colour = '2'

            for move in moves:
                rw, cl = move

                piece_code = str(board[rw, cl])
                piece_colour = piece_code[0]
                
                if piece_colour != match_colour:
                    available_moves.append(move)
        else:
            available_moves = moves

        return available_moves

    def knight_moves(self, board, start_pos, colour, only_avaiable_moves):
        row, col = start_pos
        available_moves = []
        
        moves = [[row - 2, col - 1], [row - 2, col + 1],
                    [row + 2, col - 1], [row + 2, col + 1],
                    [row - 1, col - 2], [row + 1, col - 2],
                    [row - 1, col + 2], [row + 1, col + 2]]

        if only_avaiable_moves:
            match_colour = ''

            if colour == 'w':
                match_colour = '1'
            elif colour == 'b':
                match_colour = '2'

            for move in moves:
                rw, cl = move
                
                if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                    piece_code = str(board[rw, cl])
                    piece_colour = piece_code[0]

                    if piece_colour != match_colour:
                        available_moves.append(move)
        else:
            for move in moves:
                rw, cl = move
                        
                if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                    available_moves.append(move)

        return available_moves

    def pawn_moves(self, board, start_pos, colour, only_avaiable_moves, last_move):
        row, col = start_pos
        available_moves = []
        moves = []

        # different colours move in different directions
        if colour == 'w':
            has_moved = True

            if row == 6:
                has_moved = False

            if row - 1 >= 0:
                if col - 1 >= 0:
                    if board[row - 1, col - 1] != 0:
                        moves.append([row - 1, col - 1])

                if col + 1 < 8:
                    if board[row - 1, col + 1] != 0:
                        moves.append([row - 1, col + 1])

                if row - 1 >= 0:
                    if board[row - 1, col] == 0:
                        moves.append([row - 1, col])

                        if row - 2 >= 0 and not has_moved:
                            if board[row - 2, col] == 0:
                                moves.append([row - 2, col])

            # en pasan
            if row == 3 and last_move != [] and last_move != None: # white can only use en pasan in this row
                start_index, end_index = last_move
                row_start, col_start = start_index
                row_end, col_end = end_index
                
                last_piece = str(board[row_end, col_end])

                if row_end - row_start == 2: # check the piece moved two squares forward
                    if last_piece[1] == '6':
                        if end_index == [row, col + 1]:
                            print('en pasan')
                            print([[row - 1, col + 1], [row, col + 1]])
                            #moves.append([[row - 1, col + 1], [row, col + 1], [0, 0]])

                        elif end_index == [row, col - 1]:
                            print('en pasan')
                            print([[row - 1, col - 1], [row, col - 1], [0, 0]])
                            #moves.append([[row - 1, col - 1], [row, col - 1]])
        else:
            has_moved = True

            if row == 1:
                has_moved = False

            if row + 1 < 8:
                if col - 1 >= 0 and board[row + 1, col - 1] != 0:
                    moves.append([row + 1, col - 1])


                if col + 1 < 8 and board[row + 1, col + 1] != 0:
                    moves.append([row + 1, col + 1])


                if row + 1 < 8:
                    if board[row + 1, col] == 0:
                        moves.append([row + 1, col])

                        if row + 2 < 8:
                            if board[row + 2, col] == 0 and not has_moved:
                                moves.append([row + 2, col])

             #en pasan
            if row == 4 and last_move != None: # black can only use en pasan in this row
                start_index, end_index = last_move
                row_start, col_start = start_index
                row_end, col_end = end_index
                
                last_piece = str(board[row_end, col_end])

                if row_start - row_end == 2: # check the piece moved two squares forward
                    if last_piece[1] == '6':
                        if end_index == [row, col + 1]:
                            moves.append([[row + 1, col + 1], [row, col + 1], [0, 0]])

                        elif end_index == [row, col - 1]:
                            moves.append([[row + 1, col - 1], [row, col - 1], [0, 0]])

        if only_avaiable_moves:
            match_colour = ''

            if colour == 'w':
                match_colour = '1'
            elif colour == 'b':
                match_colour = '2'

            for move in moves:
                match_colour = ''

                if colour == 'w':
                    match_colour = '1'
                elif colour == 'b':
                    match_colour = '2'

                if len(move) != 2:
                    available_moves.append(move)
                    continue

                rw, cl = move
                piece = str(board[rw, cl])
                piece_colour = piece[0]

                if piece_colour != match_colour:
                    available_moves.append(move)
        else:
            available_moves = moves

        return available_moves

    def is_in_check(self, board, pos, colour):
        row, col = pos

        match_colour = '2'

        if colour == 'w':
            match_colour = '1'

        # straights
        for i in range(1, col + 1): # row to the left of piece
            piece = str(board[row, col - i])
            piece_colour, piece_type = piece[:2]

            if piece_colour == match_colour:
                break

            if piece_type == '2' or piece_type == '3': # rook or queen in a straight
                return True
            elif piece_colour != '0':
                break

        for i in range(col + 1, 8): # right row
            piece = str(board[row, i])
            piece_colour, piece_type = piece[:2]

            if piece_colour == match_colour:
                break

            if piece_type == '2' or piece_type == '3': # rook or queen in a straight
                return True
            elif piece_colour != '0':
                break

        for i in range(1, row + 1): # upper column
            piece = str(board[row - i, col])
            piece_colour, piece_type = piece[:2]

            if piece_colour == match_colour:
                break

            if piece_type == '2' or piece_type == '3': # rook or queen in a straight
                return True
            elif piece_colour != '0':
                break

        for i in range(row + 1, 8): # lower column
            piece = str(board[i, col])
            piece_colour, piece_type = piece[:2]

            if piece_colour == match_colour:
                break

            if piece_type == '2' or piece_type == '3': # rook or queen in a straight
                return True
            elif piece_colour != '0':
                break


        # diagonals
        for i in range(1, 8):          #upper left diagonal
            rw, cl = [row - i, col - i]

            if rw < 0 or cl < 0:
                break
        
            piece = str(board[rw, cl])
            piece_colour, piece_type = piece[:2]

            if piece_colour == match_colour:
                break
        
            if piece_type == '4' or piece_type == '2': # bishop or queen in a diagonal
                return True
            elif piece_colour != '0':
                break
        
        for i in range(1, 8):           #lower right diagonal
            rw, cl = [row + i, col + i]

            if rw >= 8 or cl >= 8:
                break
        
            piece = str(board[rw, cl])
            piece_colour, piece_type = piece[:2]

            if piece_colour == match_colour:
                break
        
            if piece_type == '4' or piece_type == '2': # bishop or queen in a diagonal
                return True
            elif piece_colour != '0':
                break
        
        for i in range(1, 8):               #lower left diagonal
            rw, cl = [row + i, col - i]

            if rw >= 8 or cl < 0:
                break

            piece = str(board[rw, cl])
            piece_colour, piece_type = piece[:2]

            if piece_colour == match_colour:
                break

            if piece_type == '4' or piece_type == '2': # bishop or queen in a diagonal
                return True
            elif piece_colour != '0':
                break

        for i in range(1, 8):               #upper right diagonal
            rw, cl = [row - i, col + i]

            if rw < 0 or cl >= 8:
                break
        
            piece = str(board[rw, cl])
            piece_colour, piece_type = piece[:2]

            if piece_colour == match_colour:
                break

            if piece_type == '4' or piece_type == '2': # bishop or queen in a diagonal
                return True
            elif piece_colour != '0':
                break

        # knight moves
        moves = [[row - 2, col - 1], [row - 2, col + 1],
                 [row + 2, col - 1], [row + 2, col + 1],
                 [row - 1, col - 2], [row + 1, col - 2],
                 [row - 1, col + 2], [row + 1, col + 2]]

        for move in moves:
            rw, cl = move
                
            if rw >= 0 and rw < 8 and cl >= 0 and cl < 8:
                piece = str(board[rw, cl])
                piece_colour, piece_type = piece[:2]

                if piece_colour != match_colour and piece_type == '5':
                    return True
        
        upper_pawns = [[row + 1, col - 1], [row + 1, col + 1]]
        lower_pawns = [[row - 1, col - 1], [row - 1, col + 1]]

        if colour == 'b':
            if row + 1 < 8 and col - 1 >= 0:
                if board[row + 1, col - 1] == 16: # 16 = white pawn
                    return True

            if row + 1 < 8 and col + 1 < 8:
                if board[row + 1, col + 1] == 16:
                    return True
        else:
            if row - 1 >= 0 and col - 1 >= 0:
                if board[row - 1, col - 1] == 26: # 26 = black pawn
                    return True

            if row - 1 >= 0 and col + 1 < 8:
                if board[row - 1, col + 1] == 26:
                    return True

        return False

    def next_player(self):
        if self.current_player == 'w':
            self.current_player = 'b'
        else:
            self.current_player = 'w'

    def move_is_valid(self, move, colour):
        piece = None
        end_piece = None
        start_pos = move[0]
        end_pos = move[1]

        try:
            start_row, start_col = start_pos
            end_row, end_col = end_pos
            piece = self.board[start_row, start_col]
            end_piece = self.board[end_row, end_col]
        except IndexError:
            return False

        if piece not in self.PIECES:
            return False

        piece_code, _, _ = self.PIECES[piece]
        piece_colour, piece_type = piece_code
        end_colour = None
        end_type = None
        
        if end_piece in self.PIECES:
            end_code, _, _ = self.PIECES[end_piece]
            end_colour, end_type = end_code

        if piece_colour != colour or end_colour == colour:
            return False

        moves = self.get_moves(self.board, start_pos, piece_type, colour, True, self.moves_made[-1])


        king_pos = []
        king_code = 0

        if colour == 'w':
            king_code = 11
        else:
            king_code = 21

        p_board = copy.copy(self.board)

        self.move_pseudo_piece(p_board, move)

        for row in range(8):
            for col in range(8):
                if p_board[row, col] == king_code:
                    king_pos = [row, col]
                    break
        
        if self.is_in_check(p_board, king_pos, colour):
            return False

        if end_pos in moves:
            return True

        return False

    def assess_board(self, board, colour):
        key_values = [0, 0, 0, 0, 0] # material value (50%), centre space (20%), 
                        # available moves (10%), 
        

        ### Calculate material value
        white_pieces = self.get_pieces(board, 'w')
        black_pieces = self.get_pieces(board, 'b')

        white_value = 0
        black_value = 0
        
        for piece in white_pieces:
            code, _ = piece
            _, val, _ = self.PIECES[round(float(code))]

            white_value += val

        for piece in black_pieces:
            code, _ = piece
            _, val, _ = self.PIECES[round(float(code))]

            black_value += val


        ### Calculate centre space control
        white_moves = self.get_valid_moves(board, 'w')
        black_moves = self.get_valid_moves(board, 'b')

        centre_squares = [[3, 3], [3, 4], [4, 3], [4, 4]]
        centre_adjacents = [[2, 2], [2, 3], [2, 4], [2, 5],
                            [3, 2], [3, 5], [4, 2], [4, 5],
                            [5, 2], [5, 3], [5, 4], [5, 5]]

        centre_value_white = 0
        centre_value_black = 0

        for move in white_moves:
            if move in centre_adjacents:
                centre_value_white += 1
            elif move in centre_squares:
                centre_value_white += 2
        
        for move in black_moves:
            if move in centre_adjacents:
                centre_value_black += 1
            elif move in centre_squares:
                centre_value_black += 2


        ### Calculate piece development
        num_white_moves = len(white_moves)
        num_black_moves = len(black_moves)

        ### Load values
        if colour == 'w':
            key_values[0] = white_value - black_value
            key_values[1] = (centre_value_white - centre_value_black)/20
            key_values[2] = num_white_moves - num_black_moves
        else:
            key_values[0] =  black_value - white_value
            key_values[1] = (centre_value_black - centre_value_white)/20
            key_values[2] = num_black_moves - num_white_moves


        ### Calculate final board value
        state_value = key_values[0]*0.5 + key_values[1]*0.2 + key_values[2]*0.1

        return state_value

    def init_board(self, board):
        # white is 1 in tens column, black is 2
        # king = 1, queen = 2, rook = 3, bishop = 4, knight = 5, pawn = 6
        # white knight would be 15, black king is 21
        board[0] = (23, 25, 24, 22, 21, 24, 25, 23)
        board[1] = (26, 26, 26, 26, 26, 26, 26, 26)
        board[6] = (16, 16, 16, 16, 16, 16, 16, 16)
        board[7] = (13, 15, 14, 12, 11, 14, 15, 13)

        return board

    def move_piece(self, move):
        self.moves_made.append(move)

        start_row, start_col = move[0]
        end_row, end_col = move[1]
        piece_code, _, _ = self.PIECES[self.board[start_row, start_col]]
        self.board[end_row, end_col] = self.board[start_row, start_col]
        self.board[start_row, start_col] = 0

        if piece_code[1] == 'K':
            if piece_code[0] == 'w':
                self.kings_moved[0] = True
            else:
                self.kings_moved[1] = True

        elif piece_code[1] == 'R':
            dir = 0

            if start_col - end_col < 0:
                dir = 1

            if piece_code[0] == 'w':
                self.white_rooks_moved[dir] = True
            else:
                self.black_rooks_moved[dir] = True

        size = len(move)
        
        if size == 3:
            captured_pawn_row, captured_pawn_col = move[2]
            self.board[captured_pawn_row, captured_pawn_col] = 0

        elif size == 4:
            if piece_code[0] == 'w':
                self.king
            rook_start_row, rook_start_col = move[2]
            rook_end_row, rook_end_col = move[3]
            self.board[rook_start_row, rook_start_col] = self.board[rook_end_row, rook_end_col]
            self.board[rook_end_row, rook_end_col] = 0

    def move_pseudo_piece(self, board, move):
        start_row, start_col = move[0]
        end_row, end_col = move[1]

        board[end_row, end_col] = board[start_row, start_col]
        board[start_row, start_col] = 0

        size = len(move)
        
        if size == 3:
            captured_pawn_row, captured_pawn_col = move[2]
            board[captured_pawn_row, captured_pawn_col] = 0

        elif size == 4:
            rook_start_row, rook_start_col = move[2]
            rook_end_row, rook_end_col = move[3]
            board[rook_start_row, rook_start_col] = board[rook_end_row, rook_end_col]
            board[rook_end_row, rook_end_col] = 0

    def __init__(self):
        # initialise base game variables
        self.current_player = 'w'
        self.moves_made = [None] # store game moves. 0 is important
        self.game_over = False
        self.player1_colour = 'w'
        self.player2_colour = 'b'
        self.board = np.zeros((8, 8))
        self.board = self.init_board(self.board)

        # extra lib data
        self.PIECE_STRINGS = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']
        self.PIECE_DECIMALS = [11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0]

        # data structure layout: {key: [piece_code, value, board_position]}
        self.PIECES = {11.0: ['wK', 0, []], 12.0: ['wQ', 9, []], 13.0: ['wR', 5, []],
              14.0: ['wB', 3, []], 15.0: ['wN', 3, []], 16.0: ['wP', 1, []],
              21.0: ['bK', 0, []], 22.0: ['bQ', 9, []], 23.0: ['bR', 5, []],
              24.0: ['bB', 3, []], 25.0: ['bN', 3, []], 26.0: ['bP', 1, []]}

        # special move data
        self.white_rooks_moved = [False, False]
        self.black_rooks_moved = [False, False]
        self.kings_moved = [False, False]
        
        
import numpy as np
import copy