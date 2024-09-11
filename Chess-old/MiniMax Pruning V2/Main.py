class Chess(object):
    def draw_board(self):
        colours = [p.Color("white"), p.Color("gray")]

        for row in range(8): # loop over each square on the board
            for col in range(8):
                # alternate square colours in a check pattern
                colour = colours[((row + col)%2)]

                # draw each square on the board
                x_dim = col*self.SQ_SIZE
                y_dim = row*self.SQ_SIZE
                p.draw.rect(self.screen, colour, p.Rect(x_dim, y_dim, self.SQ_SIZE, self.SQ_SIZE))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = lib.board[row, col]

                # draw piece at index, if it exists
                if piece.code in lib.PIECE_CODES:
                    # set image parameters
                    img = self.PIECE_IMAGES[piece.code]
                    x_dim = col*self.SQ_SIZE
                    y_dim = row*self.SQ_SIZE

                    # draw image
                    self.screen.blit(img, p.Rect(x_dim, y_dim, self.SQ_SIZE, self.SQ_SIZE))

    def highlight_squares(self): # highlight squares to highlight recent moves and selected squares
        for sqr in self.squares_to_highlight: # loop over recent move squares to be highlighted
            # square parameters
            row, col = sqr
            x_dim = col*self.SQ_SIZE
            y_dim = row*self.SQ_SIZE

            # draw highlight
            p.draw.rect(self.screen, p.Color("red"), p.Rect(x_dim, y_dim, self.SQ_SIZE, self.SQ_SIZE))

        if self.sq_selected != None:
            if len(self.sq_selected) == 2: # highlight selected squares, if they exist
                row, col = self.sq_selected
                x_dim = col*self.SQ_SIZE
                y_dim = row*self.SQ_SIZE

                # draw highlight
                p.draw.rect(self.screen, p.Color("yellow"), p.Rect(x_dim, y_dim, self.SQ_SIZE, self.SQ_SIZE))

    def load_images(self):
        images = {}

        # load each piece image into the images dictionary
        for i in range(len(lib.PIECE_CODES)):
            img = p.image.load("images/%s.png" %lib.PIECE_CODES[i])
            images[lib.PIECE_CODES[i]] = p.transform.scale(img, (self.SQ_SIZE, self.SQ_SIZE))

        return images

    def player_move(self, colour):
        # check screen clicks. If no clicks, this function quits and the main loop continues. This ensures the window can be closed at any time
        for event in p.event.get():
            if event.type == p.QUIT: # window has been closed
                exit()

            # left button has been clicked
            if event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # x and y location of the mouse upon click
                col = location[0] // self.SQ_SIZE # find the column corresponding to x
                row = location[1] // self.SQ_SIZE # find the row corresponding to y

                # deselect if the same square is clicked twice in a row
                if self.sq_selected == (row, col):
                    self.sq_selected = ()
                    self.player_clicks = []
                    continue

                sqr = lib.board[row, col]

                if len(self.player_clicks) == 0: # check if this is the first mouse click
                    if sqr.colour == colour: # if piece is of player colour, select it and update click history
                        self.sq_selected = (row, col)
                        self.player_clicks = [(row, col)]
                        
                else: # player has clicked a second square
                    if sqr.colour == colour: # if piece colour matches player colour, update history and select new piece
                        self.sq_selected = (row, col)
                        self.player_clicks = [(row, col)]

                    else: # else, this square is empty or an opponent piece
                        start_pos = self.player_clicks[0]
                        end_pos = (row, col)
                        move = [start_pos, end_pos]


                        ### Band-aid
                        ### Fix: fix special move issue where full move is not present due to player_clicks only possess start and end positions. ###
                        ### Drawback: get_moves() is called twice, here and in move_is_valid(). This is wasteful computationally ###

                        all_moves = lib.get_moves(lib.board, lib.piece_dict, colour, False)
                        full_move = [m for m in all_moves if m[:2] == move] # redefine move in its full form
                        full_move = full_move[0] if len(full_move) > 0 else full_move # format move such that it has no undeeded outer brackets
                        full_move = move if full_move == [] else full_move
                        ### End band-aid ###

                        valid = lib.move_is_valid(lib.board, full_move) # check move validity

                        if valid:
                            lib.move_piece(lib.board, full_move)
                            lib.next_player()
                        else:
                            print(f"Move {move} for {colour} is invalid") # print invalid move data

                        # reset click and GUI variables
                        self.sq_selected = ()
                        self.player_clicks = []
                        self.squares_to_highlight = []

    def AI_move(self, colour):
        start = time.time()
        move = AI.make_move(lib.board, lib.piece_dict, 1, colour)
        run_time = time.time() - start
        print(f"Thinking time: {run_time} s")

        lib.move_piece(lib.board, move)
        lib.next_player()

    def main_loop(self):
        p.init()
        
        self.screen = p.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.fill(p.Color('white'))
        
        self.draw_board()
        self.draw_pieces()

        p.display.update()

        while not lib.game_over:
            # manage current move
            if lib.current_player == lib.player1_colour:
                self.player_move(lib.player1_colour)
            else:
                self.AI_move(lib.player2_colour)
        
            # update visuals
            self.draw_board()
            self.highlight_squares()
            self.draw_pieces()
            p.display.update()
            
            #print(f"Assessment: {lib.assess_board(lib.board)}")
            time.sleep(0.02)
            
    def __init__(self):
        # initialise game window essentials
        self.SCREEN_WIDTH = self.SCREEN_HEIGHT = 512
        self.SQ_SIZE = int(self.SCREEN_HEIGHT // 8)
        self.PIECE_IMAGES = self.load_images()

        # GUI related variables
        self.sq_selected = None
        self.player_clicks = []
        self.squares_to_highlight = [] # stores squares to be highlighted



import random, time
import pygame as p
import numpy as np
import Lib
import AI

if __name__ == '__main__':
    lib = Lib.Lib()
    AI = AI.AI(lib)
    chess = Chess()

    #selection = input("Colour (w or b): ")

    #while selection.lower() not in ['w', 'b']:
    #    selection = input("Please select only w or b: ")
    
    lib.player1_colour = 'w'
    lib.player2_colour = 'b'
    chess.main_loop()
