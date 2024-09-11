def draw_board(sq_size):
    colors = [p.Color("white"), p.Color("gray")]

    for row in range(8):
        for col in range(8):
            color = colors[((row + col)%2)]
            p.draw.rect(self.screen, color, p.Rect(col*sq_size, row*sq_size, sq_size, sq_size))

    #p.display.update()
    


def draw_pieces(sq_size):
    for row in range(8):
        for col in range(8):
            piece = self.board[row][col]

            if piece.code != "--":
                self.screen.blit(piece_images[piece.code], p.Rect(col*sq_size, row*sq_size, sq_size, sq_size))

    #p.display.update()



def highlight_square():
    row, col = self.sq_selected
    p.draw.rect(self.screen, p.Color("yellow"), p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))



def is_valid(move):
    start_index, end_index = move
    start_row, start_col = start_index
    end_row, end_col = end_index

    piece = self.board[start_row][start_col]

    if piece.name != None:              #piece isnt an empty space
        available_moves = piece.get_available_moves(self.board, False)

        if [end_row, end_col] in available_moves:
            return True

    return False


import pygame as p
