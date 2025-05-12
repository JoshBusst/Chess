
from numpy import array, where, ones
from ui import PSL_mouse, getUserInput
from lib import *
from graphics import *
from copy import copy
from time import time_ns




# fix PSL so pieces can still be grabbed even when a sequence is active (currently selected piece must be deselected then a new piece can be picked up)

# maybe refactor a lil
# add forward and back buttons ie cycling through move history



# hover class for managing hovering pieces
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

    def clear(self) -> None:
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

def validSquare(row: int, col: int) -> bool:
    return row >= 0 and row < 8 and col >= 0 and col < 8

def validSquares(squares: list[list[int]]) -> bool:
    for square in squares:
        if not validSquare(*square):
            return False
        
    return True

def isTurn(piece: int, turn: bool) -> bool:
    if piece == EMPTY: return None
    return (pieceColour(piece) == 'w') == turn

def nextTurn() -> None:
    global turn
    turn = not turn

def findKing(colour: str, board: array) -> list[int]:
    result = where(board == pieceInt(colour + 'K'))

    if len(result[0]) == 0: return None

    row: int = result[0][0]
    col: int = result[1][0]

    return [row, col]

def opponentColour(colour: str) -> str:
    return 'w' if colour == 'b' else 'b'



### Piece management

def pieceStr(integer: int) -> str:
    return PIECE_CODES[integer]

def pieceStrs(integers: list[int]) -> array:
    return array([PIECE_CODES[i] for i in integers])

def pieceInt(string: str) -> int:
    return PIECE_CODES.index(string)

def pieceInts(strings: list[str]) -> array:
    return array([pieceInt(i) for i in strings])

def possibleMoves(square: list[int], board: array) -> list[list]:
    piece: int = getPiece(*square, board)
    if piece == EMPTY: return []

    moveFunc: callable = MOVE_FUNCTIONS[pieceStr(piece)[1]]
    moves: list[list] = moveFunc(*square, board)
    moves_special: list[list] = getSpecialMoves(square, board)

    return moves, moves_special

def getPiece(row: int, col: int, board: array) -> int:
    if validSquare(row, col): return board[row, col]

def remPiece(row: int, col: int, board: array) -> None:
    if validSquare(row, col): board[row, col] = EMPTY

def setPiece(row: int, col: int, board: array, piece: int) -> None:
    if validSquare(row, col): board[row, col] = piece

def pieceColour(piece: int) -> str:
    return pieceStr(piece)[0]

def pieceType(piece: int) -> str:
    return pieceStr(piece)[1]

def promotionLogic(move: list[list[int]], board: array) -> None:
    piece: str = pieceStr(getPiece(*move[1], board))

    if piece[0] == 'e': return

    if piece[1] == 'P':
        if (move[1][0] == 0 and piece[0] == 'w') or (move[1][0] == 7 and piece[0] == 'b'):
            promotion: str = getUserInput(['q','r','b','n'], "Which piece would you like to promote to? q/r/b/n")
            setPiece(*move[1], board, pieceInt(piece[0] + promotion.upper()))
            # return pieceInt(piece[0] + promotion.upper())

def checkmate(colour: str, board: array):
    # start = time_ns()
    kingSquare: list[int] = findKing(colour, board)
    kingColour: str = pieceColour(getPiece(*kingSquare, board))

    moves, specialMoves = possibleMoves(kingSquare, board)
    legalMoves: list = []

    for row in range(8):
        for col in range(8):
            piece: int = getPiece(row, col, board)
            square: list[int] = [row, col]

            if pieceColour(piece) == kingColour:
                moves, specialMoves = possibleMoves(square, board)

                for move in moves:
                    if legalMove(square, move, board):
                        legalMoves.append(move)

                for move in specialMoves:
                    if legalMove(*move[:2], board):
                        legalMoves.append(move)

    # print(f"Ran in: {round(((time_ns() - start)/(10**6)), 3)}ms")

    return len(legalMoves) == 0 and isInCheck(colour, board)

def getSpecialMoves(square: list[int], board: array):
    piece: int = getPiece(*square, board)

    if PIECE_CODES[piece][1] == "K":
        return kingSpecial(*square, board)
    elif PIECE_CODES[piece][1] == "P":
        return pawnSpecial(*square, board)

    return []



### Piece movement functions

def rook(row: int, col: int, board: array) -> list[list]:
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

    return moves

def knight(row: int, col: int, board: array) -> list[list]:
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

    return moves

def bishop(row: int, col: int, board: array) -> list[list]:
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

    return moves

def queen(row: int, col: int, board: array) -> list[list]:
    return bishop(row, col, board) + rook(row, col, board)

def king(row: int, col: int, board: array) -> list[list]:
    colour: str = pieceColour(getPiece(row, col, board))
    moves: list[list[int]] = []
    specialMoves: list[list[int]] = []

    # surrounding 8 squares
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

    return moves

def kingSpecial(row: int, col: int, board: array) -> tuple:
    colour: str = pieceColour(getPiece(row, col, board))
    moves: list = []

    # castling logic
    rank = 7 if colour == 'w' else 0
    queenside: bool = not any(castleTracker[colour][0:2]) and all(board[rank, 1:4] == pieceInts(('e','e','e')))
    kingside:  bool = not any(castleTracker[colour][1:3]) and all(board[rank, 5:7] == pieceInts(('e','e')))

    if queenside: moves.append([[row, col], [row, 2], [row, 0], [row, 3]])
    if kingside:  moves.append([[row, col], [row, 6], [row, 7], [row, 5]])

    return moves

def pawn(row: int, col: int, board: array) -> list[list]:
    colour: str = pieceColour(getPiece(row, col, board))
    moves: list[list] = []

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
        
    return moves

def pawnSpecial(row: int, col: int, board: array) -> tuple[list]:
    colour: str = pieceColour(getPiece(row, col, board))
    direction: int = int(colour == 'b')*2 - 1
    moves: list = []
    
    # en passant
    if len(moveLog) > 0:
        lastMove = moveLog[-1]

        if pieceStr(getPiece(*lastMove[1], board))[1] == 'P':
            coldiff = lastMove[1][1] - col
            rowdiff = lastMove[0][0] - lastMove[1][0]
            rightPosition = (colour == 'w' and row == 3) or (colour == 'b' and row == 4)

            if abs(coldiff) == 1 and abs(rowdiff) == 2 and rightPosition:
                moves.append([[row, col], [row + direction, col + coldiff], [row, col + coldiff]])
            
    return moves



### PSL Handles

def movePiecePSLHandle(squares: list[list[int]]) -> bool:
    assert(isinstance(squares[0], list))

    quitPSL: bool = True
    selectedPiece: int = getPiece(*squares[0], board)

    # break conditions
    invalidInput: bool = not validSquares(squares) or len(squares) not in [2, 4]
    wrongPieceSelected: bool = not isTurn(selectedPiece, turn)

    if invalidInput or wrongPieceSelected:
        psl.clearSequence()
        return True
    

    move: list = []
    animate: bool = False

    # exactly one trigger in two different squares ie drag and drop
    if len(squares) == 2 and squares[0] != squares[1]:
        move = squares

    # exactly two triggers in two DIFFERENT squares ie click to select and click to move
    elif len(squares) == 4 and (squares[0] == squares[1] and squares[2] == squares[3] and squares[0] != squares[3]):
        move = [squares[0], squares[2]]
        animate = True
    else:
        drawPieces(board)
        updateScreen()

        return False

        

    if legalMove(*move, board):
        _, specialMoves = possibleMoves(move[0], board)
        sMovesSmall: list = [m[:2] for m in specialMoves]

        if move in sMovesSmall:
            i: int = sMovesSmall.index(squares)
            movePieceSpecial(specialMoves[i], board)
            moveLog.append(specialMoves[i])

        else:
            if animate:
                point1 = square2pos(*move[0])
                point2 = square2pos(*move[1])

                move_animate(pieceImages[selectedPiece], point1, point2, dt=0.15)
                
            movePiece(*move, board)
            moveLog.append(move)

        promotionLogic(move[:2], board)

        nextTurn()
    
        
    # test for checkmate
    if checkmate('w' if turn else 'b', board):
        print(f"Checkmate! {"White" if not turn else "Black"} wins!")
        global lock
        lock = True

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

    return False



### Main Function(s)

def isInCheck(colour: str, board: array) -> bool:
    kingSquare: list[int] = findKing(colour, board)
    if kingSquare == None: return None

    oppColour: str = opponentColour(colour)
    
    # bishop/queen
    moves: list[list] = bishop(*kingSquare, board)
    pieces: list[int] = [getPiece(*move, board) for move in moves]
    if pieceInt(oppColour + 'B') in pieces: print('Bishop checks the king!'); return True
    if pieceInt(oppColour + 'Q') in pieces: print('Queen checks the king!');  return True
    
    # roook/queen
    moves: list[list] = rook(*kingSquare, board)
    pieces: list[int] = [getPiece(*move, board) for move in moves]
    if pieceInt(oppColour + 'R') in pieces: print('Rook checks the king!');   return True
    if pieceInt(oppColour + 'Q') in pieces: print('Queen checks the king!');  return True
    
    # knight
    moves: list[list] = knight(*kingSquare, board)
    pieces: list[int] = [getPiece(*move, board) for move in moves]
    if pieceInt(oppColour + 'N') in pieces: print('Knight checks the king!'); return True
    
    # king
    moves: list[list] = king(*kingSquare, board)
    pieces: list[int] = [getPiece(*move, board) for move in moves]
    if pieceInt(oppColour + 'K') in pieces: print('King checks the king!');   return True

    # pawn
    moves: list[list] = pawn(*kingSquare, board)
    pieces: list[int] = [getPiece(*move, board) for move in moves]
    if pieceInt(oppColour + 'P') in pieces: print('Pawn checks the king!');   return True
    
    return False

def legalMove(square1: list[int], square2: list[int], board: array) -> bool:
    piece1 = getPiece(*square1, board)
    piece2 = getPiece(*square2, board)

    # basic legality checks
    isEmpty:    bool = bool(piece1 == EMPTY)
    sameColour: bool = pieceColour(piece1) == pieceColour(piece2)


    # ensure move is in possible moveset
    inMoveSet: bool = False
    moves, specialMoves = possibleMoves(square1, board)

    if square2 in moves:
        inMoveSet = True
    elif len(specialMoves) > 0:
        if square2 in [move[1] for move in specialMoves]:
            inMoveSet = True
    

    # ensure check does not occur post-move
    p_board = copy(board)
    movePiece(square1, square2, p_board)

    inCheck: bool = isInCheck(pieceColour(piece1), p_board)
    if inCheck == None: return False

    return not any([isEmpty, sameColour, not inMoveSet, inCheck])

def movePiece(square1: list[int], square2: list[int], board: array) -> bool:
    board[*square2] = getPiece(*square1, board)
    board[*square1] = EMPTY

def movePieceSpecial(move: list[list[int]], board: array):
    if len(move) == 3: # en passant
        movePiece(move[0], move[1], board)
        remPiece(*move[2], board)
        
    elif len(move) == 4: # castling
        movePiece(move[0], move[1], board)
        movePiece(move[2], move[3], board)
    else:
        raise ValueError

def initBoard() -> array:
    drawBoard()

    board = ones([8,8], int)*EMPTY
    board[0,:] = array(pieceInts(['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']))
    board[1,:] = array(pieceInts(['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']))
    board[6,:] = array(pieceInts(['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP']))
    board[7,:] = array(pieceInts(['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']))

    return board





PIECE_CODES = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP", "e"]
MOVE_FUNCTIONS: dict[str, callable] = {"R": rook, "N": knight, "B": bishop, "Q": queen, "K": king, "P": pawn}
EMPTY = len(PIECE_CODES) - 1

TARGET_FPS = 50

clock = p.time.Clock()
psl = PSL_mouse()

# tracks the left rooks, king, and right rooks and if they have moved
castleTracker: dict[str, list] = {'w': [False, False, False], 'b': [False, False, False]}

board: array = initBoard()
turn: bool = True # white is true, black is false
moveLog: list[list] = []
hover: Hover = Hover()
lock: bool = False

ldown_seq: list[str] = ['ldown', 'lup']
rdown_seq: list[str] = ['rdown', 'rup']
select_seq: list[str] = ['ldown', 'lup', 'ldown', 'lup']
hover_seq: list[str] = ['ldown']


if __name__ == "__main__":
    drawPieces(board)
    updateScreen()

    # order does matter
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
                    if not lock:
                        hover.clear()
                        clearLayer(animationLayer)
                        psl.addClick(p.mouse.get_pressed())
                case _:
                    pass
        
        if hover.hovering:
            pieceHover(hover.piece, square2pos(hover.row, hover.col))
        else:
            drawPieces(board)

        updateScreen()

        clock.tick(TARGET_FPS)