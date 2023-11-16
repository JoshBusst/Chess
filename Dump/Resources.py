def mark_checked_squares(colour, board):
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



def compile_pieces(colour):               #compile pieces of a certain colour and their available moves
    opp_colour = 'white'
    pieces = []

    if colour == 'white':
        opp_colour = 'black'

        
    for row in range(8):
        for col in range(8):
            piece = self.board[row][col]
            
            if piece.colour == colour:
                pieces.append(piece)
                

    available_moves = []

    for piece in pieces:
        moves = piece.get_available_moves(self.board, False)
        available_moves.append(moves)


    output = []

    for i in range(len(pieces)):
        output.append([pieces[i], available_moves[i]])


    return output


        
def print_board():          #print the 'code' variable possessed by each object on the board
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

    

def load_images(sq_size):
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    images = {}

    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/%s.png" %piece), (sq_size, sq_size))

    return images


import pygame as p

    
