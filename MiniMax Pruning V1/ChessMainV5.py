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
                if piece in lib.PIECES:
                    # set image parameters
                    img = self.PIECE_IMAGES[piece]
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
        for i in range(len(lib.PIECE_STRINGS)):
            img = p.image.load("images/%s.png" %lib.PIECE_STRINGS[i])
            images[lib.PIECE_DECIMALS[i]] = p.transform.scale(img, (self.SQ_SIZE, self.SQ_SIZE))

        return images

    def player_move(self, colour):
        # check screen clicks
        for event in p.event.get():
            if event.type == p.QUIT: # window has been closed
                exit()

            # left button has been clicked
            if event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # x and y location of the mouse upon click
                col = location[0] // self.SQ_SIZE # find the column corresponding to x
                row = location[1] // self.SQ_SIZE # find the row corresponding to y

                # deselect if the same square is clicked twice in a row
                if self.sq_selected == [row, col]:
                    self.sq_selected = []
                    self.player_clicks = []
                    continue

                sqr = lib.board[row, col]
                sqr_colour = None

                if sqr in lib.PIECES:
                    sqr_code, _, _ = lib.PIECES[sqr]
                    sqr_colour, _ = sqr_code

                if len(self.player_clicks) == 0: # check if this is the first mouse click
                    # if piece is of player colour, select it and update click history
                    if sqr_colour == lib.player1_colour:
                        self.sq_selected = [row, col]
                        self.player_clicks = [[row, col]]
                        
                else: # player has clicked a second square
                    # if piece colour matches player colour, update history and select new piece
                    if sqr_colour == colour:
                        self.sq_selected = [row, col]
                        self.player_clicks = [[row, col]]

                    else: # else, this square is empty or an opponent piece
                        start_pos = self.player_clicks[0]
                        end_pos = [row, col]
                        move = [start_pos, end_pos]

                        if lib.move_is_valid(move, colour):
                            lib.move_piece(move)
                            lib.next_player()

                        self.sq_selected = []
                        self.player_clicks = []
                        self.squares_to_highlight = []      # move is valid and therefore palyer is no longer in check

    def AI_move(self, colour):
        start = time.time()
        move = AI.make_move(lib.board, 2, colour)
        run_time = time.time() - start
        print('Thinking time: %f s' %run_time)

    def main_loop(self):
        p.init()
        
        self.screen = p.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.fill(p.Color('white'))
        
        self.draw_board()
        self.draw_pieces()

        p.display.update()

        while not lib.game_over:
            if lib.current_player == lib.player1_colour:
                self.player_move(lib.player1_colour)
            else:
                self.AI_move(lib.player2_colour)
        
            self.draw_board()
            self.highlight_squares()
            self.draw_pieces()

            p.display.update()

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
import Chesslib
import AI_Crawlers as AI

if __name__ == '__main__':
    lib = Chesslib.Lib()
    AI = AI.AI(lib)
    chess = Chess()

    #selection = input("Colour (w or b): ")

    #while selection.lower() not in ['w', 'b']:
    #    selection = input("Please select only w or b: ")
    
    lib.player1_colour = 'w'
    lib.player2_colour = 'b'
    chess.main_loop()
