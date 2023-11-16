class Chess:
    def mark_checked_squares(self, colour, board):
        self.checked_squares = [[False, False, False, False, False, False, False, False],
                           [False, False, False, False, False, False, False, False],
                           [False, False, False, False, False, False, False, False],
                           [False, False, False, False, False, False, False, False],
                           [False, False, False, False, False, False, False, False],
                           [False, False, False, False, False, False, False, False],
                           [False, False, False, False, False, False, False, False],
                           [False, False, False, False, False, False, False, False]]
                           
        pieces = self.compile_pieces(colour)


        for piece in pieces:
            moves = piece[1]

            for move in moves:
                row, col = move

                self.checked_squares[row][col] = True

        return self.checked_squares



    def offended_squares(self, colour):
        #compile available moves and determine end positions for each piece or 'offended squares'
        #pieces, moves = self.compile_pieces(colour)
        offended_squares = []
        offended_by = []
        pieces = self.compile_pieces(colour)

        for piece in pieces:
            moves = piece.get_available_moves(self.board, False)
            offensive_moves = []

            if piece.name == 'pawn':        #ensure forward movements arent counted as offensive moves
                row, col = piece.pos
                
                for move in moves:
                    if col != move[1]:          #cols are not the same. move is offensive
                        offensive_moves.append(move)
                        
            else:
                offensive_moves = moves
                        
            
            for move in offensive_moves:
                offended_squares.append(move)
                offended_by.append(piece)


        return offended_squares, offended_by



    def compile_moves(self, colour):
        available_moves = []
        opp_colour = 'white'

        if colour == 'white':
            opp_colour = 'black'


        pieces = self.compile_pieces(colour)
        
        for piece in pieces:
            moves = piece.get_available_moves(self.board, True)

            for move in moves:
                available_moves.append([piece.pos, move])


        return available_moves



    def compile_pieces(self, colour):               #compile pieces of a certain colour and their available moves
        opp_colour = 'white'
        pieces = []
        available_moves = []

        if colour == 'white':
            opp_colour = 'black'

            
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                
                if piece.colour == colour:
                    pieces.append(piece)


        '''for piece in pieces:
            moves = piece.get_available_moves(self.board, False)
            offensive_moves = []

            if piece.name == 'pawn':            #ensure forward movements arent counted as offended squares
                for move in moves:
                    row, col = move

                    if col != piece.pos[1]:         #if cols are the same, move is not offensive
                        offensive_moves.append(move)

            
            available_moves.append(offensive_moves)'''


        return pieces


            
    def print_board(self):          #print the 'code' variable possessed by each object on the board
        board = []


        #assemble the code variables
        for line in self.board:
            new_line = []
            
            for piece in line:
                new_line.append(piece.code)

            board.append(new_line)


        #print the variables
        [print(line) for line in board]
        print()



    '''def is_in_check(self, colour):
        king_piece = None
        colour_code = colour[0]
        pieces = []                     #opponents pieces. Used to find available opponent moves
        opp_colour = 'white'            #opponent colour

        if colour == 'white':
            opp_colour = 'black'
        

        #compile list of available opponent pieces as well as the king piece for the colour in question
        pieces = self.compile_pieces(opp_colour)

        available_moves = []

        for index in pieces:
            piece, moves = index

            if len(moves) > 0:
                available_moves.append(moves)
        


        return False'''

        

    def load_images(self):
        pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
        images = {}

        for piece in pieces:
            images[piece] = p.transform.scale(p.image.load("images/%s.png" %piece), (self.sq_size, self.sq_size))

        return images



    def highlight_squares(self):        #highlight check positions and selected pieces
        row, col = self.sq_selected
        p.draw.rect(self.screen, p.Color("yellow"), p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))
        
        for sqr in self.squares_to_highlight:
            row, col = sqr
            p.draw.rect(self.screen, p.Color("red"), p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))



    def is_valid(self, move):
        start_index, end_index = move
        start_row, start_col = start_index
        end_row, end_col = end_index

        piece = self.board[start_row][start_col]

        if piece.name != None:              #piece isnt an empty space
            available_moves = piece.get_available_moves(self.board, False)

            if [end_row, end_col] in available_moves:
                return True

        return False



    
    def draw_board(self):
        colors = [p.Color("white"), p.Color("gray")]

        for row in range(8):
            for col in range(8):
                color = colors[((row + col)%2)]
                p.draw.rect(self.screen, color, p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))
        


    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece.code != "--":
                    self.screen.blit(self.piece_images[piece.code], p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))

        #p.display.update()



    def multi_move_piece(self, moves):                 #used for castling, moves two pieces in one turn
        move_1 = [moves[0], moves[1]]
        move_2 = [moves[2], moves[3]]

        self.move_piece(move_1)
        self.move_piece(move_2)



    def move_piece(self, move):
        #break move up into useable indicies
        start_index, end_index = move
        start_row, start_col = start_index
        end_row, end_col = end_index


        #move should already have been validated
        
        #edit board state
        piece = self.board[start_row][start_col]
        piece.has_moved = True
        piece.pos = [end_row, end_col]
        
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = self.blank_space



    def valid_moves(self, colour):
        opp_colour = 'white'

        if colour == 'white':
            opp_colour = 'black'


        #compile available pieces and moves for given colour, determine squares offended by opposition
        own_pieces = self.compile_pieces(colour)         #relevant to the colour passed
        own_moves = self.compile_moves(colour)

        offended_squares, offended_by = self.offended_squares(opp_colour)

        king_piece = []

        #store king piece as useable variable
        for piece in own_pieces:
            if piece.name == 'king':
                king_piece = piece
                break


        #determine if king is in check and by which pieces
        king_in_check = False
        checked_by = []

        for i in range(len(offended_squares)):
            sqr = offended_squares[i]
            
            if king_piece.pos == sqr:
                king_in_check = True
                checked_by.append(offended_by[i])
                

        if king_in_check:
            self.pieces_to_highlight = [piece.pos for piece in checked_by]

            #find available moves

        else:
            return own_moves



    def initialise_board(self):
        #initialise the board objects
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]

                if piece == '--':
                    self.board[i][j] = self.blank_space

                elif piece[0] == 'w':
                    if piece[1] == 'P':
                        self.board[i][j] = pieces.Pawn('white')

                    elif piece[1] == 'N':
                        self.board[i][j] = pieces.Knight('white')

                    elif piece[1] == 'B':
                        self.board[i][j] = pieces.Bishop('white')

                    elif piece[1] == 'R':
                        self.board[i][j] = pieces.Rook('white')

                    elif piece[1] == 'Q':
                        self.board[i][j] = pieces.Queen('white')

                    elif piece[1] == 'K':
                        self.board[i][j] = pieces.King('white')

                    self.board[i][j].pos = [i, j]
                    
                else:
                    if piece[1] == 'P':
                        self.board[i][j] = pieces.Pawn('black')

                    elif piece[1] == 'N':
                        self.board[i][j] = pieces.Knight('black')

                    elif piece[1] == 'B':
                        self.board[i][j] = pieces.Bishop('black')

                    elif piece[1] == 'R':
                        self.board[i][j] = pieces.Rook('black')

                    elif piece[1] == 'Q':
                        self.board[i][j] = pieces.Queen('black')

                    elif piece[1] == 'K':
                        self.board[i][j] = pieces.King('black')
                        
                    self.board[i][j].pos = [i, j]
        
        self.draw_board()
        self.draw_pieces()
        
        p.display.update()



    def main_loop(self):
        self.initialise_board()
        
        player_clicks = []        #tracks the players clicks

        
        while True:
            if self.game_over:
                break

            #keep a copy of the current board, if it changes then reprint board and pieces
            temp_board = copy.deepcopy(self.board)

            if self.current_player == 2:        #manage black moves
                self.current_player = 1
                move = self.AI.make_move(self.board, 1, 'black')
                self.move_piece(move)


            for event in p.event.get():
                if event.type == p.QUIT:
                    exit()
                
                elif event.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()        #x and y location of the mouse
                    col = location[0] // self.sq_size
                    row = location[1] // self.sq_size

                    if self.sq_selected == [row, col]:
                        self.sq_selected = []
                        player_clicks = []
                        continue
                    

                    if self.current_player == 1:            #manage white moves
                        if len(player_clicks) == 0:
                            piece = self.board[row][col]

                            if piece.colour == 'white':
                                self.sq_selected = [row, col]
                                player_clicks = [[row, col]]

                        elif len(player_clicks) == 1:
                            if self.board[row][col].colour == 'white':
                                self.sq_selected = [row, col]
                                player_clicks = [[row, col]]
                            
                            else:
                                sqr = self.board[row][col]
                                start_row, start_col = player_clicks[0]
                                move = [[start_row, start_col], [row, col]]
                                      
                                if move in self.valid_moves('white'):
                                    self.move_piece(move)
                                    self.current_player = 2

                                self.sq_selected = []
                                player_clicks = []
                                self.squares_to_highlight = []      #moev is valid and therefore palyer is no longer in check

                    '''else:
                        if len(player_clicks) == 0:
                            piece = self.board[row][col]

                            if piece.colour == 'white':
                                self.sq_selected = [row, col]
                                player_clicks = [[row, col]]
                                self.piece_to_highlight = self.sq_selected

                        elif len(player_clicks) == 1:
                            if self.board[row][col].colour == 'white':
                                self.sq_selected = [row, col]
                                player_clicks = [[row, col]]

                            else:
                                sqr = self.board[row][col]
                                print(player_clicks)
                                start_row, start_col = player_clicks[0]
                                move = [[start_row, start_col], [row, col]]

                                if self.is_valid(move):
                                    self.move_piece(move)
                                    self.current_player = 2

                                self.sq_selected = []
                                player_clicks = []
                                self.piece_to_highlight = []'''


                    #print(self.mark_checked_squares('black', self.board))
                    

            #update visuals
            self.draw_board()
            
            if len(self.sq_selected) == 2 or len(self.squares_to_highlight) > 0:
                self.highlight_squares()

                
            self.draw_pieces()
            p.display.update()


        
    def __init__(self):
        self.game_over = False
        self.current_player = 2                   #1 signifies white, 2 signifies black
        self.AI = AI.AI(self)
        self.blank_space = pieces.Empty_Square()
        self.sq_selected = []
        self.checked_squares = []
        self.moves = []
        self.squares_to_highlight = []
        
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]


        screen_width = screen_height = 512
        self.sq_size = int(screen_height // 8)

        p.init()
        self.screen = p.display.set_mode((screen_width, screen_height))
        #clock = p.time.Clock()
        self.screen.fill(p.Color("white"))
        self.piece_images = self.load_images()

        self.main_loop()
                      
    

import numpy, copy, random, time
import pygame as p
import Pieces as pieces
import AI

chess = Chess()
