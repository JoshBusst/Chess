class Chess:
    def is_in_check(self, colour, board, highlight):
        king = self.find_king(colour, board)
        opp_colour = ''
        
        
        if colour == 'white':
            opp_colour = 'black'
        else:
            opp_colour = 'white'

            
        offended_squares, offended_by = self.list_offended_squares(opp_colour, board)


        for i in range(len(offended_squares)):
            sqr = offended_squares[i]
            
            if king.pos == sqr:
                piece = offended_by[i]

                if highlight:       #the function is not predicting moves, it is determining if any pieces are currently in check
                    print('%s king is in check! Offended by %s %s' %(king.colour, piece.colour, piece.name))
                    self.squares_to_highlight.append(king.pos)
                    self.squares_to_highlight.append(piece.pos)
                
                return True
            

        return False



    def find_king(self, colour, board):
        code = colour[0] + 'K'
        
        for row in range(8):
            for col in range(8):
                if board[row][col].code == code:
                    king = copy.deepcopy(board[row][col])
                    king.pos = [row, col]
                    return king



    def list_offended_squares(self, colour, board):
        offended_squares = []
        offended_by = []
        pieces = self.compile_pieces(colour, board)
            

        for piece in pieces:
            squares = piece.get_offended_squares(board)
            
            for move in squares:
                offended_squares.append(move)
                offended_by.append(piece)


        return offended_squares, offended_by



    def compile_all_moves(self, board):                #compile all available moves at the end of each turn
        white_moves = self.compile_moves('white', board)
        black_moves = self.compile_moves('black', board)

        return white_moves, black_moves



    def compile_moves(self, colour, board):
        available_moves = []
        opp_colour = 'white'

        if colour == 'white':
            opp_colour = 'black'


        pieces = self.compile_pieces(colour, board)
        
        for piece in pieces:
            moves = piece.get_available_moves(board, False, self.moves_made[-1])

            for move in moves:
                if len(move) > 0:
                    available_moves.append([piece.pos, move])


        valid_moves = []


        for move in available_moves:
            f_board = copy.deepcopy(board)             #fake board
            self.move_piece(move, f_board, False)
            
            if not self.is_in_check(colour, f_board, False):
                valid_moves.append(move)


        if len(valid_moves) == 0:
            print("Game over! %s has checkmated %s!" %(opp_colour, colour))
            exit()


        return valid_moves



    def compile_all_pieces(self):           #recalculate all available pieces at the end of each turn
        self.white_pieces = self.compile_pieces('white', self.board)
        self.black_pieces = self.compile_pieces('black', self.board)



    def compile_pieces(self, colour, board):               #compile pieces of a certain colour and their available moves
        opp_colour = 'white'
        pieces = []

        if colour == 'white':
            opp_colour = 'black'

            
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                
                if piece.colour == colour:
                    pieces.append(piece)


        return pieces



    def promote_pawns(self):
        for i in range(8):
            sqr_top = self.board[0][i]
            sqr_bottom = self.board[7][i]

            if sqr_top.code == 'wP':
                selection = input('Pawn promotion? ').lower()

                #validate selection
                while selection != 'q' and selection != 'r' and selection != 'b' and selection != 'k':
                    selection = input('Please select q, r, b or k: ')
                    

                if selection == 'q':
                    self.board[0][i] = pieces.Queen('white')
                
                elif selection == 'r':
                    self.board[0][i] = pieces.Rook('white')
                
                elif selection == 'b':
                    self.board[0][i] = pieces.Bishop('white')
                
                else:
                    self.board[0][i] = pieces.Knight('white')


                self.board[0][i].pos = [0, i]
                

            elif sqr_bottom.code == 'bP':
                selection = self.AI.promote_pawn(self.board)


                if selection == 'q':
                    self.board[7][i] = pieces.Queen('black')
                
                elif selection == 'r':
                    self.board[7][i] = pieces.Rook('black')
                
                elif selection == 'b':
                    self.board[7][i] = pieces.Bishop('black')
                
                else:
                    self.board[7][i] = pieces.Knight('black')


                self.board[7][i].pos = [7, i]



    def board_codes(self, input_board):
        board = []


        #assemble the code variables
        for line in input_board:
            new_line = []
            
            for piece in line:
                new_line.append(piece.code)

            board.append(new_line)


        return board


            
    def print_board(self):          #print the 'code' variable possessed by each object on the board
        print(self.board_codes(self.board))
        print()

        

    def load_images(self):
        pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
        images = {}

        for piece in pieces:
            images[piece] = p.transform.scale(p.image.load("images/%s.png" %piece), (self.sq_size, self.sq_size))

        return images



    def pawn_promotion_menu(self):
        p.draw.rect(self.screen, p.Color("yellow"), p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))



    def highlight_squares(self):        #highlight check positions and selected pieces
        for sqr in self.squares_to_highlight:
            row, col = sqr
            p.draw.rect(self.screen, p.Color("red"), p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))


        if len(self.sq_selected) == 2:
            row, col = self.sq_selected
            p.draw.rect(self.screen, p.Color("yellow"), p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))



    def is_valid(self, move):
        start_index, end_index = move
        start_row, start_col = start_index
        end_row, end_col = end_index

        piece = self.board[start_row][start_col]

        if piece.name != None:              #piece isnt an empty space
            available_moves = piece.get_available_moves(self.board, False, self.moves_made[-1])

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



    def multi_move_piece(self, moves, board):                 #used for castling, moves two pieces in one turn
        #moves are given in the format [[start], [end, start, end]] for king then rook (or pawn and pawn) respectively
        start_index_1 = moves[0]
        end_index_1, start_index_2, end_index_2 = moves[1]
        
        move_1 = [start_index_1, end_index_1]
        move_2 = [start_index_2, end_index_2]

        self.move_piece(move_1, board, False)       #dont store this move as it has already been stored


        if end_index_2 != ['--', '--']:     #en pasan deletes a piece instead of overwriting it with another, hence ['--', '--']
            self.move_piece(move_2, board, False)

        else:
            board[start_index_2[0]][start_index_2[1]] = self.blank_space



    def move_piece(self, move, board, store):
        #break move up into useable indicies
        start_index, end_index = move

        if store:
            self.moves_made.append(move)

        if len(end_index) > 2:          #castling or en pasan
            self.multi_move_piece(move, board)
            return
            
        start_row, start_col = start_index
        end_row, end_col = end_index


        #move should already have been validated
        
        #edit board state
        piece = board[start_row][start_col]
        piece.has_moved = True
        piece.pos = [end_row, end_col]

        #first, destroy the instance of the piece being captured
        board[end_row][end_col].pos = None
        
        board[end_row][end_col] = piece
        board[start_row][start_col] = self.blank_space



    def valid_moves(self, colour):
        opp_colour = 'white'

        if colour == 'white':
            opp_colour = 'black'


        #compile available pieces and moves for given colour, determine squares offended by opposition
        own_pieces = self.compile_pieces(colour)         #relevant to the colour passed
        own_moves = self.compile_moves(colour, self.board)

        offended_squares, offended_by = self.list_offended_squares(opp_colour, self.board)

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
                        self.white_king = self.board[i][j]

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
                        self.black_king = self.board[i][j]
                        
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

            #keep a copy of the current board to register board state updates
            temp_board = copy.deepcopy(self.board)
            

            if self.current_player == 2:        #manage black moves
                self.current_player = 1
                move = self.AI.make_move(self.board, self.AI_proficiency, 'black')
                self.move_piece(move, self.board, True)
                #time.sleep(1)

            else:           #ensure two board state updates CANNOT happen in one loop
                for event in p.event.get():
                    if event.type == p.QUIT:
                        exit()
                    
                    elif event.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()        #x and y location of the mouse
                        col = location[0] // self.sq_size
                        row = location[1] // self.sq_size

                        if self.sq_selected == [row, col]:      #deselect if the same square is clicked again
                            self.sq_selected = []
                            player_clicks = []
                            continue
                        

                        if self.current_player == 1:            #manage white moves
                            if len(player_clicks) == 0:
                                piece = self.board[row][col]

                                if piece.colour == 'white':
                                    self.sq_selected = [row, col]
                                    player_clicks = [[row, col]]

                            elif len(player_clicks) == 1:           #player has clicked two squares
                                if self.board[row][col].colour == 'white':
                                    self.sq_selected = [row, col]
                                    player_clicks = [[row, col]]
                                
                                else:
                                    sqr = self.board[row][col]
                                    start_row, start_col = player_clicks[0]
                                    player_move = [[start_row, start_col], [row, col]]
                                    moves = self.compile_moves('white', self.board)

                                    for move in moves:
                                        if len(move[1]) == 2:
                                            if player_move == move:
                                                self.move_piece(move, self.board, True)
                                                self.current_player = 2
                                            
                                        else:
                                            #format for castling moves is [[start], [end, start, end]]
                                            index = [move[0], move[1][0]]

                                            if index == player_move:
                                                self.multi_move_piece(move, self.board)
                                                self.current_player = 2
                                    

                                    self.sq_selected = []
                                    player_clicks = []
                                    self.squares_to_highlight = []      #move is valid and therefore palyer is no longer in check

                    '''elif self.current_player == 2:            #manage white moves
                        if len(player_clicks) == 0:
                            piece = self.board[row][col]

                            if piece.colour == 'black':
                                self.sq_selected = [row, col]
                                player_clicks = [[row, col]]

                        elif len(player_clicks) == 1:           #player has clicked two squares
                            if self.board[row][col].colour == 'black':
                                self.sq_selected = [row, col]
                                player_clicks = [[row, col]]
                            
                            else:
                                sqr = self.board[row][col]
                                start_row, start_col = player_clicks[0]
                                player_move = [[start_row, start_col], [row, col]]
                                moves = self.compile_moves('black', self.board)

                                
                                for move in moves:      #handle special moves
                                    if len(move[1]) == 2:
                                        if player_move == move:
                                            self.move_piece(move, self.board, True)
                                            self.current_player = 1
                                        
                                    else:
                                        #format for castling moves is [[start], [end, start, end]]
                                        index = [move[0], move[1][0]]

                                        if index == player_move:
                                            self.multi_move_piece(move, self.board)
                                            self.current_player = 1

                                self.sq_selected = []
                                player_clicks = []
                                self.squares_to_highlight = []'''


            #if board has updated, update all graphics related features and some other processes
            if self.board_codes(temp_board) != self.board_codes(self.board):
                self.promote_pawns()
                self.squares_to_highlight = []
                self.is_in_check('white', self.board, True)
                self.is_in_check('black', self.board, True)


            #these need to be updated even when the board may not have updated
            self.draw_board()
            self.highlight_squares()
            self.draw_pieces()
            p.display.update()


        
    def __init__(self):
        self.game_over = False
        self.current_player = 1                   #1 signifies white, 2 signifies black
        self.AI = AI.AI(self)
        self.blank_space = pieces.Empty_Square()
        self.sq_selected = []
        self.moves_made = [0]
        self.squares_to_highlight = []
        self.AI_proficiency = 1

        self.white_pieces = []
        self.black_pieces = []
        self.white_moves = []           #available white moves. Recalculated at the end of each turn
        self.black_moves = []           #available black moves
        self.white_king = []
        self.black_king = []
        self.offended_squares = []      #squares offended by the opposition. Used for 'check' related tasks
        
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
        self.piece_images = self.load_images()

        p.init()
        self.screen = p.display.set_mode((screen_width, screen_height))
        self.screen.fill(p.Color("white"))

        self.main_loop()
                      
    

import numpy, copy, random, time
import pygame as p
import Pieces as pieces
import AI

chess = Chess()
