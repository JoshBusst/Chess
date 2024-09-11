import ChessEngine
import pygame as p


width = height = 512
dimension = 8   #dimensions of a chess board is 8x8
sqSize = height // dimension
maxFPS = 15
images = {}




'''
initialise a global dictionary of images. This will only call once for efficiency
'''

def LoadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]

    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/%s.png" %piece), (sqSize, sqSize))




'''
This will be the main driver and handle user input and updating graphics
'''

def Main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    LoadImages()
    running = True
    sqSelected = ()         #tracks last sqaure selected by the player
    playerClicks = []        #tracks the players clicks

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()        #x and y location of the mouse
                col = location[0] // sqSize
                row = location[1] // sqSize

                if sqSelected == (row, col):    #if same square is clicked twice
                    sqSelected = ()             #deselect piece
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)     #append for both first and second clicks

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    #print(move.GetChessNotation())
                    gs.MakeMove(move)
                    sqSelected = ()
                    playerClicks = []


        DrawGameState(screen, gs)
        clock.tick(maxFPS)
        p.display.flip()




'''
Draws graphics within a current gamestate
'''

def DrawGameState(screen, gs):
    DrawBoard(screen)
    #can add in piece highlights here later
    DrawPieces(screen, gs.board)




'''
Draw board squares
'''

def DrawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]

    for row in range(dimension):
        for col in range(dimension):
            color = colors[((row + col)%2)]
            p.draw.rect(screen, color, p.Rect(col*sqSize, row*sqSize, sqSize, sqSize))




'''
Draws pieces on the board given the current game state
'''

def DrawPieces(screen, board):
    for row in range(dimension):
        for col in range(dimension):
            piece = board[row][col]

            if piece != "  ":
                screen.blit(images[piece], p.Rect(col*sqSize, row*sqSize, sqSize, sqSize))
                

    

if __name__ == '__main__':
    Main()



    
    
