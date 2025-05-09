
import numpy
from ui import PSL_mouse
from lib import *
from graphics import *


# add special move functionality
# add king check logic (ie block illegal check moves)
# occasional glitch in piece animations. Unsure of source



### Miscellaneous helper functions

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

def getMouseSquare() -> list[int]:
    return pos2square(p.mouse.get_pos())

def validSquare(row: int, col: int) -> bool:
    return row >= 0 and row < 8 and col >= 0 and col < 8

def validSquares(squares: list[list[int]]) -> bool:
    for square in squares:
        if not validSquare(*square):
            return False
        
    return True

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

def isTurn(piece: int, turn: bool) -> bool:
    if piece == EMPTY: return None
    return  (pieceColour(piece) == 'w') == turn

def nextTurn() -> None:
    global turn
    turn = not turn



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



### PSL Handles

def movePiecePSLHandle(squares: list[list[int]]) -> bool:
    assert(isinstance(squares[0], list))

    quitPSL: bool = True
    selectedPiece: int = getPiece(*squares[0])

    # break conditions
    invalidInput: bool = not validSquares(squares) or len(squares) not in [2, 4]
    selectedWrongPiece: bool = not isTurn(selectedPiece, turn)

    if invalidInput or selectedWrongPiece:
        psl.clearSequence()
        return True

    # input handlers
    if len(squares) == 2 and squares[0] != squares[1]:
        if legalMove(*squares[0:2]):
            movePiece(*squares[0:2], board)
            nextTurn()
        
    elif len(squares) == 4 and (squares[0] == squares[1] and squares[2] == squares[3] and not squares[0] == squares[3]):
        if legalMove(squares[0], squares[2]):
            point1 = square2pos(*squares[0])
            point2 = square2pos(*squares[3])

            move_animate(pieceImages[selectedPiece], point1, point2, dt=0.15)
            movePiece(squares[0], squares[2], board)
            nextTurn()
    else:
        quitPSL = False

    drawPieces(board)
    updateScreen()

    return quitPSL

def rClickPSLHandle(clickData: list[list[int]]) -> bool:
    assert(len(clickData) == 2 and isinstance(clickData[0], list))

    if not validSquares(clickData): error("Parameter fault in rClickPSLHandle}")

    if len(clickData) == 2:
        if clickData[0] == clickData[1]:
            addSquareHighlight(*clickData[0])
        else:
            addArrow(*clickData)

    return True

def ldownPSLHandle(clickData: list[list[int]]) -> bool:
    if not validSquares(clickData): error("Square data invalid for ldownPSLHandle")

    clearUserStyling()

    piece: int = getPiece(*clickData[0])

    if isTurn(piece, turn):
        pieceHover(piece, square2pos(clickData[0]))

    return False



### Main Function(s)

def legalMove(square1: list[int], square2: list[int]) -> bool:
    piece1 = getPiece(*square1)
    piece2 = getPiece(*square2)

    isEmpty: bool = piece1 == EMPTY
    sameColour: bool = pieceColour(piece1) == pieceColour(piece2)
    notPossible = not movePossible(piece1, square1, square2)

    return not any([isEmpty, sameColour, notPossible])

# moves a piece. Does NOT check for legality
def movePiece(square1: list[int], square2: list[int], board: numpy.array) -> bool:
    board[*square2] = getPiece(*square1)
    board[*square1] = EMPTY

def newBoard() -> numpy.array:
    board = numpy.ones([8,8], int)*EMPTY
    board[0,:] = numpy.array(pieceInts(['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']))
    board[1,:] = numpy.array(pieceInts(['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']))
    board[6,:] = numpy.array(pieceInts(['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP']))
    board[7,:] = numpy.array(pieceInts(['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']))

    return board

def main() -> None:
    drawPieces(board)
    updateScreen()

    psl.addSequence(['ldown', 'lup'], movePiecePSLHandle, onclick=getMouseSquare)
    psl.addSequence(['rdown', 'rup'], rClickPSLHandle, onclick=getMouseSquare)
    psl.addSequence(['ldown', 'lup', 'ldown', 'lup'], movePiecePSLHandle, onclick=getMouseSquare)
    psl.addSequence(['ldown'], ldownPSLHandle, onclick=getMouseSquare)

    while True:
        for e in p.event.get():
            match e.type:
                case p.QUIT:
                    exit()
                case p.MOUSEBUTTONDOWN | p.MOUSEBUTTONUP:
                    psl.addClick(p.mouse.get_pressed())
                case _:
                    pass

        drawPieces(board)
        updateScreen()

        clock.tick(TARGET_FPS)




PIECE_CODES = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
MOVE_FUNCTIONS: dict[str, callable] = {"R": rook, "N": knight, "B": bishop, "Q": queen, "K": king, "P": pawn}
EMPTY = len(PIECE_CODES)

TARGET_FPS = 50

clock = p.time.Clock()
psl = PSL_mouse()

board: numpy.array = newBoard()
turn: bool = True # white is true, black is false


if __name__ == "__main__":
    main()


    