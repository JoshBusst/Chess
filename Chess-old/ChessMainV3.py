class Chess:
    def board_config(self, input_board):
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
                    return piece




    def promote_pawns(self):
        for i in range(8):
            top_sqr = self.board[0][i]
            bottom_sqr = self.board[7][i]

            if top_sqr.name == 'pawn':
                selection = input("Please select piece promotion (n, b, r, q): ")
                while selection not in ['n', 'b', 'r', 'q']:
                    selection = input("Please select n, b, r or q: ")

                new_piece = pieces.initialise_piece(top_sqr.colour[0] + selection.upper())
                new_piece.pos = [0, i]

                for j in range(len(self.white_pieces)):
                    piece = self.white_pieces[i]

                    if top_sqr.pos == [0, i]:
                        self.white_pieces[i] = new_piece
                        

                self.board[0][i] = new_piece
                

            if bottom_sqr.name == 'pawn':
                selection = input("Please select piece promotion (n, b, r, q): ")
                while selection not in ['n', 'b', 'r', 'q']:
                    selection = input("Please select n, b, r or q: ")

                new_piece = pieces.initialise_piece(top_sqr.colour[0] + selection.upper())
                new_piece.pos = [7, i]

                for j in range(len(self.black_pieces)):
                    piece = self.black_pieces[i]

                    if bottom_sqr.pos == [7, i]:
                        self.black_pieces[i] = new_piece

                        
                self.board[7][i] = new_piece


        print(self.board_config(self.board))

                



    def is_in_check(self, colour, board, pieces, highlight):        #king.pos is not being updated!!!!!!!
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

            
        return False



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



    def compile_pieces(self, colour):               #compile pieces of a certain colour and their available moves
        pieces = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                
                if piece.colour == colour:
                    pieces.append(piece)


        return pieces
    


    def load_images(self):
        pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
        images = {}

        for piece in pieces:
            images[piece] = p.transform.scale(p.image.load("images/%s.png" %piece), (self.sq_size, self.sq_size))

        return images


    
    def move_single_piece(self, move, board, pieces, real_move):
        #break move up into useable indicies
        start_index, end_index = move
        start_row, start_col = start_index
        end_row, end_col = end_index


        #edit board state. move should already have been validated
        piece = board[start_row][start_col]
        piece.has_moved = True
        
        end_square = board[end_row][end_col]


        #edit the piece variables
        if end_square.name != None:
            for i in range(len(pieces)):
                if pieces[i].pos == [end_row, end_col]:
                    del pieces[i]
                    break

        
        piece.pos = [end_row, end_col]
            

        #destroy the instance of the piece being captured
        del board[end_row][end_col]
        
        board[end_row].insert(end_col, piece)
        board[start_row][start_col] = self.blank_space



    def multi_move_piece(self, moves, board, pieces):       #special moves include castling and en pasan
        #moves are given in the format [[start], [end, start, end]] for king then rook (or pawn and pawn) respectively
        start_index_1 = moves[0]
        end_index_1, start_index_2, end_index_2 = moves[1]

        move_1 = [start_index_1, end_index_1]
        move_2 = [start_index_2, end_index_2]

        self.move_single_piece(move_1, board, pieces, False)       #dont store this move as it has already been stored


        if end_index_2 != ['--', '--']:     #en pasan deletes a piece instead of overwriting it with another, hence ['--', '--']
            self.move_single_piece(move_2, board, pieces, False)

        else:
            board[start_index_2[0]][start_index_2[1]] = self.blank_space





    #everything above this line can probably be exported to a resource file to improve readability and decrease clutter




            
    def move_piece(self, move, board, pieces, store):
        if store:
            self.moves_made.append(move)

            
        if len(move[1]) == 2:       #single move
            self.move_single_piece(move, board, pieces, store)

        elif len(move[1]) > 2:      #special move
            self.multi_move_piece(move, board, pieces)
            


    def next_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1



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



    def highlight_squares(self):
        for sqr in self.squares_to_highlight:
            row, col = sqr
            p.draw.rect(self.screen, p.Color("red"), p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))


        if len(self.sq_selected) == 2:
            row, col = self.sq_selected
            p.draw.rect(self.screen, p.Color("yellow"), p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))


    
    def initialise_board(self):
        for row in range(8):                #initialise board objects
            for col in range(8):
                piece_code = self.board[row][col]

                self.board[row][col] = pieces.initialise_piece(piece_code)
                self.board[row][col].pos = [row, col]

                if piece_code[1] == 'K':
                    if piece_code[0] == 'w':
                        self.white_king = self.board[row][col]
                    else:
                        self.black_king = self.board[row][col]



    def AI_move(self, colour):
        move = self.AI.make_move(self.board, self.AI_proficiency, colour)
        pieces = []

        if colour == 'white':
            pieces = self.black_pieces
        else:
            pieces = self.white_pieces
            

        self.move_piece(move, self.board, pieces, True)

        self.current_player = 1



    def player_move(self, colour):
        #colour = self.player_colour
        
        for event in p.event.get():
            if event.type == p.QUIT:
                exit()

                
            if event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()        #x and y location of the mouse
                col = location[0] // self.sq_size   #round to nearest row and col
                row = location[1] // self.sq_size

                if self.sq_selected == [row, col]:      #deselect if the same square is clicked again
                    self.sq_selected = []
                    player_clicks = []
                    continue


                if len(self.player_clicks) == 0:
                    piece = self.board[row][col]

                    if piece.colour == colour:
                        self.sq_selected = [row, col]
                        self.player_clicks = [[row, col]]

                else:           #player has clicked two squares
                    if self.board[row][col].colour == colour:
                        self.sq_selected = [row, col]
                        self.player_clicks = [[row, col]]
                    
                    else:
                        sqr = self.board[row][col]
                        start_row, start_col = self.player_clicks[0]
                        player_move = [[start_row, start_col], [row, col]]
                        moves = self.compile_moves(colour, self.board)


                        for move in moves:
                            pieces = []

                            if colour == 'white':
                                pieces = self.black_pieces      #only black pieces will be updated as white is moving
                            else:
                                pieces = self.white_pieces


                            if not self.is_in_check(self.player_colour, self.board, pieces, True):
                                if len(move[1]) == 2:
                                    if player_move == move:
                                        self.move_piece(move, self.board, pieces, True)
                                        self.next_player()
                                    
                                else:
                                    #format for special moves is [[start], [end, start, end]]
                                    index = [move[0], move[1][0]]

                                    if index == player_move:
                                        self.move_piece(move, self.board, pieces, True)
                                        self.next_player()
                        

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


        #set up pygame
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


            #time.sleep(0.05)            #delay every run so as to reduce computational strain




    def standard_game(self):
        #set up standard game variables
        player_colour = input("Please select player colour (w or b): ")
        while player_colour not in ['w', 'b']:
            player_colour = input("Please reselect (w or b): ")


        ai_prof = input("Please select difficulty level 1-3: ")
        while ai_prof not in ['1', '2', '3']:
            ai_prof = input("Please reselect. Choose a difficulty from 1 to 3: ")

        self.AI_proficiency = ai_prof
        

        if player_colour == 'w':
            self.player_colour = 'white'
            self.AI_colour = 'black'
        else:
            self.player_colour = 'black'
            self.AI_colour = 'white'
                
            
        self.sq_selected = []
        self.player_clicks = []
        self.AI = AI_v2.AI(self)


        #set up pygame
        p.init()
        
        self.screen = p.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(p.Color('white'))

        self.draw_board()
        self.draw_pieces()
        
        
        while True:
            temp_board = copy.deepcopy(self.board)      #used to check if board has updated
            
                    
            if self.current_player == 1:
                self.player_move(self.player_colour)

            elif self.current_player == 2:
                self.AI_move(self.AI_colour)


            #if board has updated, update some features
            if self.board_config(temp_board) != self.board_config(self.board):
                self.promote_pawns()
                self.is_in_check(self.player_colour, self.board, self.black_pieces, True)
                self.is_in_check(self.AI_colour, self.board, self.white_pieces, True)
                self.squares_to_highlight = []


            #these need to be updated even when the board may not have updated
            self.draw_board()
            self.highlight_squares()
            self.draw_pieces()
            p.display.update()
            
            
            #time.sleep(0.05)            #delay every run so as to reduce computational strain


                    
    def start_game(self):
        self.initialise_board()

        self.white_pieces = self.compile_pieces('white')
        self.black_pieces = self.compile_pieces('black')
        

        game_type = input("Select game mode (s = standard, v = versus, b = battle): ")

        while game_type not in ['s', 'v', 'b']:
            game_type = input("Please select s, v or b: ")


        if game_type == 's':
            self.standard_game()

        elif game_type == 'v':
            self.versus_game()

        elif game_type == 'b':
            pass


    
    def __init__(self):
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        
        self.screen_width = self.screen_height = 512
        self.sq_size = int(self.screen_height // 8)
        self.piece_images = self.load_images()
        self.blank_space = pieces.Empty_Square()

        self.game_over = False
        self.current_player = 1                   #1 signifies white, 2 signifies black
        self.moves_made = [0]       #the 0 is important for later use
        
        self.squares_to_highlight = []

        self.white_king = []
        self.black_king = []
        self.white_pieces = []
        self.black_pieces = []





import numpy, copy, random, time
import pygame as p
import Pieces as pieces
import AI_V2

chess = Chess()
chess.start_game()



