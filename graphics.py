
import pygame as p
import numpy, copy, random, time
from numbers import Number
from lib import *
from ui import PSL_mouse
from time import sleep
from math import sqrt, atan2 as ang



### Miscellaneous Helper Functions

# makes colour1 appear more like colour2 by a percentage defined by opacity
def blendColours(colour1: tuple, colour2: tuple, opacity: float=0.5) -> tuple:
    return (int((1 - opacity) * colour1[0] + opacity * colour2[0]),  # R component
            int((1 - opacity) * colour1[1] + opacity * colour2[1]),  # G component
            int((1 - opacity) * colour1[2] + opacity * colour2[2]),   # B component
    )

def squareIsDark(row: int, col: int) -> bool:
    return not(even(row) == even(col))

def getSquareColour(row: int, col: int) -> tuple:
    return BOARD_COLOURS[squareIsDark(row, col)]

def validSquare(row: int, col: int) -> bool:
    return row >= 0 and row < 8 and col >= 0 and col < 8

def validSquares(squares: list[list[int]]) -> bool:
    for square in squares:
        if not validSquare(*square):
            return False
        
    return True

def pieceStr(integer: int) -> str:
    if integer == EMPTY: return 'empty'
    return PIECE_CODES[integer]

def pieceStrs(integers: list[int]) -> list[str]:
    strings: list[str] = []

    for integer in integers:
        strings.append(pieceStr(integer))

    return strings

def pieceInt(string: str) -> int:
    return PIECE_CODES.index(string)

def pieceInts(strings: list[str]) -> list[int]:
    integers: list[int] = []

    for string in strings:
        integers.append(pieceInt(string))

    return integers

def loadImage(imagePath: str) -> p.Surface:
    return p.transform.scale(p.image.load(imagePath), (SQUARE_SIZE, SQUARE_SIZE))

def loadImages() -> list[p.Surface]:
    images: list[p.Surface] = []

    for code in PIECE_CODES:
        images.append(loadImage(f"images/{code}.png"))

    return images

def getMouseSquare() -> list[int]:
    [i, j] = p.mouse.get_pos()

    row = i // SQUARE_SIZE
    col = j // SQUARE_SIZE

    return [col, row]

def movePossible(piece: int, square1: list[int], square2: list[int]) -> bool:
    return square2 in possibleMoves(piece, square1)

def possibleMoves(piece: int, square: list[int]) -> list[list[int]]:
    if piece == EMPTY: return []

    moveFunc: callable = MOVE_FUNCTIONS[pieceStr(piece)[1]]
    return moveFunc(*square)

def getPiece(row: int, col: int) -> int:
    if validSquare(row, col):
        return board[row, col]

def pieceColour(piece: int) -> str:
    return pieceStr(piece)[0]



### Piece Functions

def rook(row: int, col: int) -> list[list[int]]:
    tracker: list[bool] = [True, True, True, True]
    colour: str = pieceColour(getPiece(row, col))
    moves = []

    for i in range(1,8):
        squares = [[row + i, col],
                   [row - i, col],
                   [row, col - i],
                   [row, col + i]]
        
        for i, square in enumerate(squares):
            if validSquare(*square):
                opColour = pieceColour(getPiece(*square))

                if opColour not in [colour, 'e'] and tracker[i]:
                    moves.append(square)
                    tracker[i] = False
                elif opColour == colour:
                    tracker[i] = False
                
                if tracker[i]:
                    moves.append(square)
            
            if not any(tracker): break

    return moves

def knight(row: int, col: int) -> list[list[int]]:
    colour: str = pieceColour(getPiece(row, col))
    moves: list[list[int]] = []

    squares = [[row + 2, col + 1],
               [row + 2, col - 1],
               [row + 1, col + 2],
               [row + 1, col - 2],
               [row - 1, col + 2],
               [row - 1, col - 2],
               [row - 2, col + 1],
               [row - 2, col - 1]]
    
    for square in squares:
        if validSquare(*square):
            if pieceColour(getPiece(*square)) != colour:
                moves.append(square)

    return moves

def bishop(row: int, col: int) -> list[list[int]]:
    tracker: list[bool] = [True, True, True, True]
    colour: str = pieceColour(getPiece(row, col))
    moves: list[list[int]] = []

    for i in range(1,8):
        squares = [[row + i, col + i],
                   [row + i, col - i],
                   [row - i, col + i],
                   [row - i, col - i]]
        
        for i, square in enumerate(squares):
            if validSquare(*square):
                opColour = pieceColour(getPiece(*square))

                if opColour not in [colour, 'e'] and tracker[i]:
                    moves.append(square)
                    tracker[i] = False
                elif opColour == colour:
                    tracker[i] = False
                
                if tracker[i]:
                    moves.append(square)

            if not any(tracker): break

    return moves

def queen(row: int, col: int) -> list[list[int]]:
    return bishop(row, col) + rook(row, col)

def king(row: int, col: int) -> list[list[int]]:
    colour: str = pieceColour(getPiece(row, col))
    moves: list[list[int]] = []

    squares = [[row + 1, col + 1],
               [row + 1, col],
               [row + 1, col - 1],
               [row, col + 1],
               [row, col - 1],
               [row - 1, col + 1],
               [row - 1, col],
               [row - 1, col - 1]]
    
    for i, square in enumerate(squares):
            if validSquare(*square):
                if pieceColour(getPiece(*square)) != colour:
                    moves.append(square)

    return moves

def pawn(row: int, col: int) -> list[list[int]]:
    colour: str = pieceColour(getPiece(row, col))
    moves: list[list[int]] = []

    direction: int = int(colour == 'b')*2 - 1
    forwardSquares = [[row + direction, col]]
    
    attackSquares = [[row + direction, col + 1],
                     [row + direction, col - 1]]
    
    if (colour == 'w' and row == 6) or (colour == "b" and row == 1):
        forwardSquares.append([row + 2*direction, col])
    
    for square in attackSquares:
        piece = getPiece(*square)

        if piece not in [None, EMPTY] and pieceColour(piece) != colour:
            moves.append(square)

    for square in forwardSquares:
        if getPiece(*square) == EMPTY:
            moves.append(square)
        else:
            break

    return moves




### Graphics Functions

def drawBoard() -> None:
    for row in range(8):
        for col in range(8):
            drawSquare(row, col, BOARD_COLOURS[(row + col)%2])

def drawHighlights() -> None:
    for row, col in squares_highlighted:
        squareColour: tuple = getSquareColour(row, col)
        highlightColour: tuple = blendColours(squareColour, HIGHLIGHT_PRIMARY, opacity=HIGHLIGHT_INTENSITY)

        drawSquare(row, col, highlightColour)

def drawPiece(pieceInt: int, row: int, col: int) -> None:
    i = row*SQUARE_SIZE
    j = col*SQUARE_SIZE
    screen.blit(pieceImages[pieceInt], p.Rect(j, i, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces() -> None:
    for row in range(8):
        for col in range(8):
            piece = board[row,col]

            if piece != EMPTY:
                drawPiece(piece, row, col)

def drawSquare(row: int, col: int, colour: p.Color) -> None:
    i = col*SQUARE_SIZE
    j = row*SQUARE_SIZE

    p.draw.rect(screen, colour, p.Rect(i, j, SQUARE_SIZE, SQUARE_SIZE))

def highlightSquare(square: list[int]) -> None:
    if square in squares_highlighted:
        squares_highlighted.remove(square)
    else:
        squares_highlighted.append(square)

def clearHighlights() -> None:
    squares_highlighted.clear()

def drawArrow(square1: list[int], square2: list[int]) -> None:
    print(f"Drawing arrow from {square1} to {square2}!")
    diff_vector: numpy.array = numpy.subtract(square1, square2)
    length: float = sqrt(diff_vector.dot(diff_vector))
    angle: float = ang(diff_vector[1], diff_vector[0])
    
    scaled_rotated_body = p.transform.rotate(p.transform.scale_by(arrowBody, (length,1)), angle)
    rotated_head = p.transform.rotate(arrowHead, angle)

    screen.blit(rotated_head, (10,100))
    screen.blit(scaled_rotated_body, (10,10))

def updateScreen() -> None:
    drawBoard()
    drawHighlights()
    drawPieces()

    p.display.update()

def pieceHover(row: int, col: int) -> None:
    global update

    print(f"Piece {[row, col]} is hovering")
    update = True

def getArrowGraphic() -> list[p.Surface]:
    arrowBody: p.Surface = p.Surface((SQUARE_SIZE, SQUARE_SIZE/3))
    arrowBody.fill(HIGHLIGHT_SECONDARY)

    head_x: int = SQUARE_SIZE*2/3
    head_y: int = SQUARE_SIZE/2
    arrowHead: p.Surface = p.Surface((head_x, head_y), p.SRCALPHA)
    p.draw.polygon(arrowHead, HIGHLIGHT_SECONDARY, ((0,0),(0,head_y),(head_x,head_y/2),(0,0)))

    return arrowHead, arrowBody



### PSL Handles

def movePiecePSLHandle(clickData: list[list[int]]) -> bool:
    assert(isinstance(clickData[0], list))
    
    if not validSquares(clickData): error("Invalid input type. Squares are not valid type")

    if len(clickData) == 2:
        if clickData[0] != clickData[1]:
            movePiece(*clickData)
            return False

    elif len(clickData) == 4:
        if clickData[0] == clickData[1] and clickData[2] == clickData[3]:
            movePiece(clickData[0], clickData[2])
        
        return False

    print(f"Click data: {clickData}")
    print(f"Active sequence: {psl.activeSequence}")

    return True

def rClickPSLHandle(clickData: list[list[int]]) -> bool:
    assert(len(clickData) == 2 and isinstance(clickData[0], list))

    if not validSquares(clickData): error("Parameter fault in rClickPSLHandle}")

    if len(clickData) == 2:
        if clickData[0] == clickData[1]:
            highlightSquare(clickData[0])
        else:
            drawArrow(*clickData)

    return False

def ldownPSLHandle(clickData: list[list[int]]) -> bool:
    if not validSquares(clickData): error("Square data invalid for ldownPSLHandle")

    clearHighlights()
    pieceHover(*clickData[0])

    return True



### Main Function(s)

def movePiece(square1: list[int], square2: list[int]) -> bool:
    cprint(f"Moving {square1} to {square2}")
    
    # check there is a piece on square1
    # check square 2 is not occupied by piece of same colour
    # check that square is a possible piece move
    # psuedo move the piece and check if board state is valid. If not, do not finalise piece move

    piece1 = getPiece(*square1)
    piece2 = getPiece(*square2)

    if pieceStr(piece1) == EMPTY: return
    if pieceColour(piece1) == pieceColour(piece2): return
    if not movePossible(piece1, square1, square2): return

    cprint(f"{pieceStr(piece1)} takes {pieceStr(piece2)}")
    board[*square1] = EMPTY
    board[*square2] = piece1

def initBoard() -> numpy.array:
    board = numpy.ones([8,8], int)*EMPTY
    board[0,:] = numpy.array(pieceInts(['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']))
    board[1,:] = numpy.array(pieceInts(['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']))
    board[6,:] = numpy.array(pieceInts(['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP']))
    board[7,:] = numpy.array(pieceInts(['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']))

    return board

def main() -> None:
    drawBoard()
    drawPieces()
    updateScreen()

    psl.addSequence(['ldown'], ldownPSLHandle, onclick=getMouseSquare)
    psl.addSequence(['rdown', 'rup'], rClickPSLHandle, onclick=getMouseSquare)
    psl.addSequence(['ldown', 'lup'], movePiecePSLHandle, onclick=getMouseSquare)
    psl.addSequence(['ldown', 'lup', 'ldown', 'lup'], movePiecePSLHandle, onclick=getMouseSquare)

    while True:
        for e in p.event.get():
            match e.type:
                case p.QUIT:
                    exit()
                case p.MOUSEBUTTONDOWN | p.MOUSEBUTTONUP:
                    psl.addClick(p.mouse.get_pressed())
                case _:
                    pass

        updateScreen()
        sleep(0.01)



SCREEN_WIDTH = SCREEN_HEIGHT = 800
SQUARE_SIZE = int(SCREEN_HEIGHT // 8)

PIECE_CODES = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
MOVE_FUNCTIONS: dict[str, callable] = {"R": rook, "N": knight, "B": bishop, "Q": queen, "K": king, "P": pawn}
EMPTY = len(PIECE_CODES)

pieceImages = loadImages()
board: numpy.array = initBoard()

LDOWN = 0
LUP = 1
MDOWN = 2
MUP = 3
RDOWN = 4
RUP = 5

BOARD_COLOURS: list[tuple] = [(255,215,183), (163,108,77)]
HIGHLIGHT_PRIMARY: tuple = (255,100,100)
HIGHLIGHT_SECONDARY: tuple = (252,247,189)
HIGHLIGHT_INTENSITY = 0.8

squares_highlighted: list[list] = []
drawn_arrows: list[list] = []
redraw_squares: list[list] = []


p.init()
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
psl = PSL_mouse()

[arrowHead, arrowBody] = getArrowGraphic()


if __name__ == "__main__":
    main()

    