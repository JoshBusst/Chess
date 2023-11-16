class Chess:
    '''def board_config(self, input_board):
        board = []


        #assemble the code variables
        for line in input_board:
            new_line = []
            
            for piece in line:
                new_line.append(piece.code)

            board.append(new_line)


        return board



    def list_offended_squares(self, board, pieces):
        offended_squares = []
        offended_by = []
            

        for piece in pieces:
            squares = piece.get_offended_squares(board)
            
            for move in squares:
                offended_squares.append(move)
                offended_by.append(piece)


        return offended_squares, offended_by



    def find_king(self, colour, board):
        code = colour[0] + 'K'

        for line in board:
            for piece in line:
                if piece.code == code:
                    return piece'''


    def is_move_valid(piece, move, colour):
        moves = piece.get_available_moves(self.board, False, self.moves_made[-1])
        start_row, start_col = copy.copy(piece.pos)
        row, col = move

        if move in moves:
            self.board[row][col] = piece
            piece.pos = [row, col]

            if is_in_check(colour, self.board, )

            
        


    def next_player(self): # update current player
        self.current_player = (1 if self.current_player == 2 else 2)



    def promote_pawns(self):

        # check first rank for pawns to promote (last rank is machines rank)
        for i in range(8):
            first_rank_piece = self.board[0][i]
            #eighth_rank_piece = self.board[7][i]


            if first_rank_piece.name == 'pawn':

                # users choice of promotion
                selection = input("Please select piece promotion (n, b, r, q): ")

                # ensure valid selection
                while selection not in ['n', 'b', 'r', 'q']:
                    selection = input("Please select n, b, r or q: ")


                # initialise new piece
                new_piece = pieces.initialise_piece(first_rank_piece.colour[0] + selection.upper())
                new_piece.pos = [0, i]

                # save new piece to board
                self.board[0][i] = new_piece



    '''def is_in_check(self, colour, board, pieces, highlight):        #king.pos is not being updated!!!!!!!
        king = self.find_king(colour, board)
        opp_colour = ''


        if colour == 'white':
            opp_colour = 'black'
        else:
            opp_colour = 'white'

            
        offended_squares, offended_by = self.list_offended_squares(board, pieces)


        for i in range(len(offended_squares)):
            sqr = offended_squares[i]
            
            if king.pos == sqr:
                if highlight:       #if true the function is not predicting moves, it is determining if any pieces are currently in check
                    piece = offended_by[i]      #piece offending the king
                    print('%s king is in check! Offended by %s %s' %(king.colour, piece.colour, piece.name))
                    self.squares_to_highlight.append(king.pos)
                    self.squares_to_highlight.append(piece.pos)
                
                return True

            
        return False'''



    def compile_moves(self, colour, board):
        available_moves = []
        pieces = []
        opp_pieces = []
        opp_colour = ''
        

        if colour == 'white':
            pieces = self.white_pieces
            opp_pieces = self.black_pieces
            opp_colour = 'black'
        else:
            pieces = self.black_pieces
            opp_pieces = self.white_pieces
            opp_colour = 'white'

        
        for piece in pieces:
            moves = []
            
            if len(self.moves_made) > 0:
                moves = piece.get_available_moves(board, False, self.moves_made[-1])
            else:
                moves = piece.get_available_moves(board, False, None)
                

            for move in moves:
                if len(move) > 0:
                    available_moves.append([piece.pos, move])


        valid_moves = []


        for move in available_moves:
            f_board = copy.deepcopy(board)             #fake board
            f_pieces = copy.copy(opp_pieces)        #editable pieces variables for use in self.is_in_check
            #print([piece.code for piece in f_pieces])
            self.move_piece(move, f_board, f_pieces, False)
            #print([piece.code for piece in f_pieces])


            if not self.is_in_check(colour, f_board, f_pieces, False):
                #print(self.board_config(f_board))
                valid_moves.append(move)


        if len(valid_moves) == 0:
            print("Game over! %s has checkmated %s!" %(opp_colour, colour))
            exit()


        return valid_moves



    def compile_pieces(self, colour): # compile pieces of a certain colour and their available moves
        pieces = []

        # loop over each row and then each column
        for row in range(8):
            for col in range(8):

                # the piece at index [row, col]
                piece = self.board[row][col]

                # append all pieces of desired colour to pieces list
                if piece.colour == colour:
                    pieces.append(piece)

        return pieces
    


    def load_images(self): # load piece specific images
        
        # piece codes
        pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
        images = {}

        # load each piece image into the images dictionary
        for piece in pieces:
            images[piece] = p.transform.scale(p.image.load("images/%s.png" %piece), (self.sq_size, self.sq_size))


        return images


            
    def move_piece(self, move, board, pieces, store):
        '''if store:
            self.moves_made.append(move)

            
        if len(move[1]) == 2:       #single move
            self.move_single_piece(move, board, pieces, store)

        elif len(move[1]) > 2:      #special move
            self.multi_move_piece(move, board, pieces)'''



    def draw_board(self): # draw lines and background features of the board
        colors = [p.Color("white"), p.Color("gray")]

        # loop over each square on the board
        for row in range(8):
            for col in range(8):

                # alternate square colours in a check pattern
                color = colors[((row + col)%2)]

                # draw each square on the board
                x_dim = col*self.sq_size
                y_dim = row*self.sq_size
                p.draw.rect(self.screen, color, p.Rect(x_dim, y_dim, self.sq_size, self.sq_size))
        


    def draw_pieces(self): # draw the piece images onto the board

        # loop over each square
        for row in range(8):
            for col in range(8):

                # get piece
                piece = self.board[row][col]

                # draw piece at index, if it exists
                if piece.code != "--":
                    
                    # set image parameters
                    img = self.piece_images[piece.code]
                    x_dim = col*self.sq_size
                    y_dim = row*self.sq_size

                    # draw image
                    self.screen.blit(img, p.Rect(x_dim, y_dim, self.sq_size, self.sq_size))



    def highlight_squares(self): # highlight squares to highlight recent moves and selected squares

        # loop over recent move squares to be highlighted
        for sqr in self.squares_to_highlight:

            # square parameters
            row, col = sqr
            x_dim = col*self.sq_size
            y_dim = row*self.sq_size

            # draw highlight
            p.draw.rect(self.screen, p.Color("red"), p.Rect(x_dim, y_dim, self.sq_size, self.sq_size))


        # highlight selected squares, if they exist
        if len(self.sq_selected) == 2:
            row, col = self.sq_selected
            x_dim = col*self.sq_size
            y_dim = row*self.sq_size

            # draw highlight
            p.draw.rect(self.screen, p.Color("yellow"), p.Rect(x_dim, y_dim, self.sq_size, self.sq_size))

    
    
    def initialise_board(self): # load board variables and data
        
        # initialise board objects
        for row in range(8):
            for col in range(8):
                
                # current piece index
                piece_code = self.board[row][col]

                # initialise piece
                self.board[row][col] = pieces.initialise_piece(piece_code)
                self.board[row][col].pos = [row, col]

                # initialise king pieces
                if piece_code == 'wK':
                    self.white_king = self.board[row][col]
                elif piece_code == 'bK':
                    self.black_king = self.board[row][col]



    def AI_move(self, colour): # facilitate AI move

        # call to AI class
        move = self.AI.make_move(self.board, self.AI_proficiency, colour)
        pieces = []

        # set pieces variable
        if colour == 'white':
            pieces = self.black_pieces
        else:
            pieces = self.white_pieces
            

        # call to move_piece function
        self.move_piece(move, self.board, pieces, True)



    def player_move(self, colour): # accepts colour input for reusability across game modes

        # check screen clicks
        for event in p.event.get():

            # window has been closed
            if event.type == p.QUIT:
                exit()


            # left button has been clicked
            if event.type == p.MOUSEBUTTONDOWN:
                
                location = p.mouse.get_pos() # x and y location of the mouse upon click
                col = location[0] // self.sq_size # find the column corresponding to x
                row = location[1] // self.sq_size # find the row corresponding to y

                # deselect if the same square is clicked twice in a row
                if self.sq_selected == [row, col]:
                    self.sq_selected = []
                    player_clicks = []
                    continue

                piece = self.board[row][col] # select the piece at index [row, col]

                # this is the first mouse click
                if len(self.player_clicks) == 0:

                    # if piece is of player colour, select it and update click history
                    if piece.colour == colour:
                        self.sq_selected = [row, col]
                        self.player_clicks = [[row, col]]
                        

                else: # player has clicked a second square

                    # if piece colour matches passed colour, update history and select new piece
                    if piece.colour == colour:
                        self.sq_selected = [row, col]
                        self.player_clicks = [[row, col]]

                    else: # if not, this square is empty or an opponent piece
                        
                        start_row, start_col = self.player_clicks[0]
                        piece = self.board[start_row][start_col]
                        move = [row, col]

                        if self.is_move_valid(piece, move, colour):
                            pass                


                        self.sq_selected = []
                        self.player_clicks = []
                        self.squares_to_highlight = []      #move is valid and therefore palyer is no longer in check



    def versus_game(self):
        p1_colour = input("Player 1, please select colour (w or b): ")
        while p1_colour not in ['w', 'b']:
            p1_colour = input("Please reselect (w or b): ")
        

        if p1_colour == 'w':
            self.p1_colour = 'white'
            self.p2_colour = 'black'
        else:
            self.p1_colour = 'black'
            self.p2_colour = 'white'

                
        self.sq_selected = []
        self.player_clicks = []


        # set up pygame
        p.init()
        
        self.screen = p.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(p.Color('white'))
        
        self.draw_board()
        self.draw_pieces()
        

        while True:
            temp_board = copy.deepcopy(self.board)      #used to check if board has updated
            
                    
            if self.current_player == 1:
                self.player_move(self.p1_colour)

            elif self.current_player == 2:
                self.player_move(self.p2_colour)


            #if board has updated, update some features
            if self.board_config(temp_board) != self.board_config(self.board):
                #self.promote_pawns()
                self.squares_to_highlight = []


            #these need to be updated even when the board may not have updated
            self.draw_board()
            self.highlight_squares()
            self.draw_pieces()
            p.display.update()


            #time.sleep(0.05)            #delay every run so as to reduce computational strain'''




    def standard_game(self):
        
        # set up standard game variables
        player_colour = input("Please select player colour (w or b): ")
        
        while player_colour not in ['w', 'b']: # ensure selection is valid
            player_colour = input("Please reselect (w or b): ")


        # difficulty selection 
        ai_proficiency = input("Please select difficulty level 1-3: ")
        
        while ai_proficiency not in ['1', '2', '3']: # ensure valid selection
            ai_proficiency = input("Please reselect. Choose a difficulty from 1 to 3: ")


        # set poficiency
        self.AI_proficiency = ai_proficiency


        # set up colour variables
        if player_colour == 'w':
            self.player_colour = 'white'
            self.AI_colour = 'black'
        else:
            self.player_colour = 'black'
            self.AI_colour = 'white'
                

        # set up GUI variables and AI object
        self.sq_selected = []
        self.player_clicks = []
        self.AI = AI.AI(self) # pass reference to parent class to AI object for communication purposes


        # set up pygame and GUI
        p.init()
        
        self.screen = p.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(p.Color('white'))


        # draw board and pieces
        self.draw_board()
        self.draw_pieces()
        

        # enter main loop
        while True:
            if self.current_player == 1: # players move
                self.player_move(self.player_colour)

            elif self.current_player == 2: # AIs move
                self.AI_move(self.AI_colour)

            else:
                print("Error in self.current_player. Exiting...")
                exit()


            self.next_player()
            self.promote_pawns()
            #self.is_in_check(self.player_colour, self.board, self.black_pieces, True)
            #self.is_in_check(self.AI_colour, self.board, self.white_pieces, True)
            self.squares_to_highlight = []


            self.draw_board()
            self.highlight_squares()
            self.draw_pieces()
            p.display.update()

            time.sleep(0.05)


                    
    def start_game(self): # facilitate game start operations such as game mode and object initialisation

        self.initialise_board() # initialise the game board
        self.white_pieces = self.compile_pieces('white') # load the white pieces for easy piece tracking
        self.black_pieces = self.compile_pieces('black') # load the black pieces

        
        # prompt user for game mode
        game_mode = input("Select game mode (s = standard, v = versus, b = battle): ")

        # ensure valid selection
        while game_mode not in ['s', 'v', 'b']:
            game_mode = input("Please select s, v or b: ")


        # enter correct game mode
        if game_mode == 's':
            self.standard_game()

        elif game_mode == 'v':
            self.versus_game()

        elif game_mode == 'b':
            pass


    
    def __init__(self):

        # the game board
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        # pygame screen dimensions
        self.screen_width = self.screen_height = 512
        self.sq_size = int(self.screen_height // 8)
        self.piece_images = self.load_images()
        self.blank_space = pieces.Empty_Square()

        self.game_over = False
        self.current_player = 1 # 1 signifies white, 2 signifies black
        self.moves_made = [0] # the 0 is important for later use

        self.squares_to_highlight = [] # stores squares to be highlighted

        self.white_king = [] # track the location of the white king, prevents constant king searching
        self.black_king = [] # track black king
        
        self.white_pieces = [] # track all white pieces and locations
        self.black_pieces = [] # track all black pieces and locations





import numpy, copy, random, time
import pygame as p
import Pieces as pieces
import AI

chess = Chess()
chess.start_game()



