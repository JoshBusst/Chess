
from numpy import array, where, ones
from lib import *
from graphics import *
from copy import copy

# finalise refactor to deprecate PSL
# add special move functionality
# add king check logic (ie block illegal check moves)


BUTTONS = {'mouse': ('lup','ldown','mup','mdown','rup','rdown')}



class Hover:
    def __init__(self):
        self.hovering: bool = False
        self.piece: int = EMPTY
        self.row: int = None
        self.col: int = None

    def set(self, piece: int, row: int, col: int) -> None:
        self.hovering = True
        self.piece = piece
        self.row = row
        self.col = col

    def wipe(self) -> None:
        self.hovering = False
        self.piece = EMPTY
        self.row = None
        self.col = None


### Miscellaneous helper functions

def square2coord(square: list[int]) -> str:
    ranks: str = '87654321'
    files: str = 'abcdefgh'

    return files[square[1]] + ranks[square[0]]

def coord2square(coord: str) -> list[int]:
    ranks: str = '87654321'
    files: str = 'abcdefgh'

    return [int(ranks[int(coord[1])]), files.index(coord[0])]

def getMouseSquare() -> list[int]:
    return pos2square(p.mouse.get_pos())

def getButtonStr(buttonsPressed: tuple[bool], prevClicks: tuple[bool]) -> str:
    triggerButton: tuple[bool] = tuple([buttonsPressed[i] != prevClicks[i] for i in range(3)])

    ind: int = triggerButton.index(True)
    tButtonState: bool = buttonsPressed[ind]

    return BUTTONS['mouse'][2*ind + int(tButtonState)]



def pieceStr(integer: int) -> str:
    return PIECE_CODES[integer]

def pieceStrs(integers: list[int]) -> array:
    return array([PIECE_CODES[i] for i in integers])

def pieceInt(string: str) -> int:
    return PIECE_CODES.index(string)

def pieceInts(strings: list[str]) -> array:
    return array([pieceInt(i) for i in strings])

def validSquare(row: int, col: int) -> bool:
    return row >= 0 and row < 8 and col >= 0 and col < 8

def validSquares(squares: list[list[int]]) -> bool:
    for square in squares:
        if not validSquare(*square):
            return False
        
    return True

def movePossible(piece: int, square1: list[int], square2: list[int], board: array) -> bool:
    moves, specialMoves = possibleMoves(piece, square1, board)

    # print(moves)
    # print(specialMoves)
    # print(square2)
    
    if square2 in moves:
        return True
    
    if len(specialMoves) > 0:
        if square2 in [move[0] for move in specialMoves]:
            return True
        
    return False

def possibleMoves(piece: int, square: list[int], board: array) -> list[list]:
    if piece == EMPTY: return []

    moveFunc: callable = MOVE_FUNCTIONS[pieceStr(piece)[1]]
    return moveFunc(*square, board)

def empty(squares: list[int] | list[list[int]], board) -> bool:
    if isinstance(squares[0], list):
        return [getPiece(*square, board) == EMPTY for square in squares]
    else:
        return getPiece(*squares, board) == EMPTY

def getPiece(row: int, col: int, board: array) -> int:
    if validSquare(row, col): return board[row, col]

def pieceColour(piece: int) -> str:
    return pieceStr(piece)[0]

def isTurn(piece: int, turn: bool) -> bool:
    if piece == EMPTY: return None
    return  (pieceColour(piece) == 'w') == turn

def nextTurn() -> None:
    global turn
    turn = not turn

def findKing(colour: str, board: array) -> list[int]:
    result = where(board == pieceInt(colour + 'K'))

    if result == []:
        log(result)
        return None

    row: int = result[0][0]
    col: int = result[1][0]

    return [row, col]

def opponentColour(colour: str) -> str:
    return 'w' if colour == 'b' else 'b'

# 0 = cant castle, 1 = queenside only, 2 = kingside only, 3 = either
def canCastle(colour: str, board: array) -> int:
    rank = 7 if colour == 'w' else 0
    castle: int = 0

    if not any(castleTracker[colour][0:2]) and all(board[rank, 1:4] == pieceInts(('e','e', 'e'))):
        # queenside
        castle += 1
    
    if not any(castleTracker[colour][1:3]) and all(board[rank, 5:7] == pieceInts(('e','e'))):
        # kingside
        castle += 2
    
    return castle



### Piece movement functions

def rook(row: int, col: int, board: array) -> list[list[int]] | list:
    tracker: list[bool] = [True, True, True, True]
    colour: str = pieceColour(getPiece(row, col, board))
    moves = []

    for i in range(1,8):
        squares = [[row + i, col],
                   [row - i, col],
                   [row, col - i],
                   [row, col + i]]
        
        for i, square in enumerate(squares):
            if validSquare(*square):
                opColour = pieceColour(getPiece(*square, board))

                if opColour not in [colour, 'e'] and tracker[i]:
                    moves.append(square)
                    tracker[i] = False
                elif opColour == colour:
                    tracker[i] = False
                
                if tracker[i]:
                    moves.append(square)
            
            if not any(tracker): break

    return moves, []

def knight(row: int, col: int, board: array) -> list[list[int]] | list:
    colour: str = pieceColour(getPiece(row, col, board))
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
            if pieceColour(getPiece(*square, board)) != colour:
                moves.append(square)

    return moves, []

def bishop(row: int, col: int, board: array) -> list[list[int]] | list:
    tracker: list[bool] = [True, True, True, True]
    colour: str = pieceColour(getPiece(row, col, board))
    moves: list[list[int]] = []

    for i in range(1,8):
        squares = [[row + i, col + i],
                   [row + i, col - i],
                   [row - i, col + i],
                   [row - i, col - i]]
        
        for i, square in enumerate(squares):
            if validSquare(*square):
                opColour = pieceColour(getPiece(*square, board))

                if opColour not in [colour, 'e'] and tracker[i]:
                    moves.append(square)
                    tracker[i] = False
                elif opColour == colour:
                    tracker[i] = False
                
                if tracker[i]:
                    moves.append(square)

            if not any(tracker): break

    return moves, []

def queen(row: int, col: int, board: array) -> list[list[int]] | list:
    return bishop(row, col, board)[0] + rook(row, col, board)[0], []

def king(row: int, col: int, board: array) -> list[list[int]] | list[list[int]]:
    colour: str = pieceColour(getPiece(row, col, board))
    moves: list[list[int]] = []
    specialMoves: list[list[int]] = []

    squares = ([row + 1, col + 1],
               [row + 1, col    ],
               [row + 1, col - 1],
               [row,     col + 1],
               [row,     col - 1],
               [row - 1, col + 1],
               [row - 1, col    ],
               [row - 1, col - 1])
    
    for square in squares:
        if validSquare(*square):
            if pieceColour(getPiece(*square, board)) != colour:
                moves.append(square)

    castle: int = canCastle(colour, board)

    if castle in (1, 3):
        specialMoves.append([[row, 2], [row, 0], [row, 3]])
    
    if castle in (2, 3):
        specialMoves.append([[row, 6], [row, 7], [row, 5]])

    return moves, specialMoves

def pawn(row: int, col: int, board: array) -> list[list[int]] | list[list[int]]:
    colour: str = pieceColour(getPiece(row, col, board))
    moves: list[list[int]] = []

    direction: int = int(colour == 'b')*2 - 1
    forwardSquares = [[row + direction, col]]
    
    attackSquares = [[row + direction, col + 1],
                     [row + direction, col - 1]]
    
    if (colour == 'w' and row == 6) or (colour == "b" and row == 1):
        forwardSquares.append([row + 2*direction, col])
    
    for square in attackSquares:
        piece = getPiece(*square, board)

        if piece not in [None, EMPTY] and pieceColour(piece) != colour:
            moves.append(square)

    for square in forwardSquares:
        if getPiece(*square, board) == EMPTY:
            moves.append(square)
        else:
            break

    return moves, []



### PSL Handles

def movePiecePSLHandle(squares: list[list[int]]) -> bool:
    assert(isinstance(squares[0], list))

    quitPSL: bool = True
    selectedPiece: int = getPiece(*squares[0], board)

    # break conditions
    invalidInput: bool = not validSquares(squares) or len(squares) not in [2, 4]
    selectedWrongPiece: bool = not isTurn(selectedPiece, turn)

    if invalidInput or selectedWrongPiece:
        psl.clearSequence()
        return True

    # exactly one click in two different squares
    if len(squares) == 2 and squares[0] != squares[1]:
        if legalMove(*squares[0:2]):
            movePiece(*squares[0:2], board)
            nextTurn()
    
    # exactly two clicks in two DIFFERENT squares        
    elif len(squares) == 4 and (squares[0] == squares[1] and squares[2] == squares[3] and not squares[0] == squares[3]):
        if legalMove(squares[0], squares[2]):
            point1 = square2pos(*squares[0])
            point2 = square2pos(*squares[3])

            print("Animating move...")

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

    piece: int = getPiece(*clickData[0], board)

    if isTurn(piece, turn):
        hover.set(piece, *clickData[0])

        # pieceHover(piece, *clickData[0])

    return False

def handleClicks(clicks: list[str]) -> None:
    sequences: list[list[str]] = [['ldown', 'lup'],
                                  ['rdown', 'rup'],
                                  ['ldown', 'lup', 'ldown', 'lup'],
                                  ['ldown']]
    
    if clicks[-2:] == sequences[0]:
    
    psl.addSequence(['ldown', 'lup'], movePiecePSLHandle, onclick=getMouseSquare)
    psl.addSequence(['rdown', 'rup'], rClickPSLHandle, onclick=getMouseSquare)
    psl.addSequence(['ldown', 'lup', 'ldown', 'lup'], movePiecePSLHandle, onclick=getMouseSquare)
    psl.addSequence(['ldown'], ldownPSLHandle, onclick=getMouseSquare)



### Main Function(s)

def isInCheck(colour: str, board: array) -> bool:
    kingSquare = findKing(colour, board)
    if kingSquare == None: return None

    oppColour = opponentColour(colour)
    
    moves, _ = bishop(*kingSquare, board)
    pieces = [getPiece(*move, board) for move in moves]
    if pieceInt(oppColour + 'B') in pieces: print('Bishop checks the king!'); return True
    if pieceInt(oppColour + 'Q') in pieces: print('Queen checks the king!'); return True
    
    moves, _ = rook(*kingSquare, board)
    pieces = [getPiece(*move, board) for move in moves]
    if pieceInt(oppColour + 'R') in pieces: print('Rook checks the king!'); return True
    if pieceInt(oppColour + 'Q') in pieces: print('Queen checks the king!'); return True
    
    moves, _ = knight(*kingSquare, board)
    pieces = [getPiece(*move, board) for move in moves]
    if pieceInt(oppColour + 'N') in pieces: print('Knight checks the king!'); return True

    return False

def legalMove(square1: list[int], square2: list[int]) -> bool:
    piece1 = getPiece(*square1, board)
    piece2 = getPiece(*square2, board)

    isEmpty: bool = bool(piece1 == EMPTY)
    sameColour: bool = pieceColour(piece1) == pieceColour(piece2)
    notPossible = not movePossible(piece1, square1, square2, board)
    
    p_board = copy(board)
    movePiece(square1, square2, p_board)
    inCheck: bool = isInCheck(pieceColour(piece1), p_board)
    if inCheck == None: return False

    return not any([isEmpty, sameColour, notPossible, inCheck])

def movePiece(square1: list[int], square2: list[int], board: array) -> bool:
    board[*square2] = getPiece(*square1, board)
    board[*square1] = EMPTY

def initBoard() -> array:
    drawBoard()

    board = ones([8,8], int)*EMPTY
    board[0,:] = array(pieceInts(['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']))
    board[1,:] = array(pieceInts(['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']))
    board[6,:] = array(pieceInts(['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP']))
    board[7,:] = array(pieceInts(['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']))

    return board

def main() -> None:
    drawPieces(board)
    updateScreen()
    
    prevClicks: tuple[bool] = (0,0,0)
    clicks: list[str] = []

    while True:
        for e in p.event.get():
            match e.type:
                case p.QUIT:
                    exit()
                case p.MOUSEBUTTONDOWN | p.MOUSEBUTTONUP:
                    hover.wipe()
                    clearLayer(animationLayer)
                    
                    buttonsPressed = p.mouse.get_pressed()

                    if buttonsPressed == prevClicks: # if held or released twice consecutively. Negates mouse scroll wheel triggers
                        clicks = []
                    else:
                        triggerButtonStr: str = getButtonStr(buttonsPressed, prevClicks)
                        clicks.append(triggerButtonStr)
                        prevClicks = buttonsPressed
                case _:
                    pass
        
        if hover.hovering:
            pieceHover(hover.piece, hover.row, hover.col)
        else:
            drawPieces(board)

        updateScreen()

        clock.tick(TARGET_FPS)





if __name__ == "__main__":
    PIECE_CODES = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP", "e"]
    MOVE_FUNCTIONS: dict[str, callable] = {"R": rook, "N": knight, "B": bishop, "Q": queen, "K": king, "P": pawn}
    EMPTY = len(PIECE_CODES) - 1

    TARGET_FPS = 50

    clock = p.time.Clock()

    # tracks the left rooks, king, and right rooks and if they have moved
    castleTracker: dict[str, list] = {'w': [False, False, False], 'b': [False, False, False]}

    board: array = initBoard()
    p_board: array = initBoard() # planning board. Used for theoretical moves

    turn: bool = True # white is true, black is false

    hover: Hover = Hover()
    
    main()