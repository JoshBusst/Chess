
from numpy import array, where, ones, int8
from ui import getUserInput
from lib import *
import graphics as g
from ui import getMouseButtonStr
from copy import copy
from time import time_ns




# refactor to use n64 format instead of [row, col]

# promotion logic needs to be NON BLOCKING!
# update graphics to accomodate static and then dyanmic screen size changes
# maybe refactor a lil
# add forward and back buttons ie cycling through move history



# hover class for managing hovering pieces
class Hover:
    def __init__(self):
        self.hovering: bool = False
        self.piece: int = EMPTY
        self.sqnum: int8 = None

    def set(self, piece: int, sqnum: int8) -> None:
        self.hovering = True
        self.piece = piece
        self.sqnum = sqnum

    def clear(self) -> None:
        self.hovering = False
        self.piece = EMPTY
        self.sqnum = None



class Sequence:
    active: list[str]
    squares: list[int8]

    def __init__(self):
        self.active = []
        self.squares = []

    def clear(self) -> None:
        self.active.clear()
        self.squares.clear()

    # return true if full or partial sequence match is found
    def match(self, matchSeq: list) -> bool:
        if len(self.active) > len(matchSeq): return False

        return not any([self.active[i] != matchSeq[i] for i in range(len(self.active))])

    def add(self, buttonStr: str, sqnum: int8):
        self.active.append(buttonStr)
        self.squares.append(sqnum)



### Miscellaneous helper functions

# convert to n64 number  format
def square2num(square: tuple) -> int8:
    return int8(8*square[0] + square[1])

# convert from n64 nubmer format to [row, col]
def num2square(num: int8) -> tuple:
    return (num // 8, num % 8)

def num2pgn(num: int8) -> str:
    return square2pgn(num2square(num))

def pgn2num(pgn: str) -> int8:
    return square2num(pgn2square(pgn))

def square2pgn(square: list[int]) -> str:
    ranks: str = '87654321'
    files: str = 'abcdefgh'

    return files[square[1]] + ranks[square[0]]

def pgn2square(coord: str) -> list[int]:
    ranks: str = '87654321'
    files: str = 'abcdefgh'

    return [int(ranks[int(coord[1])]), files.index(coord[0])]

# uses n64 to return n64 row manipulation
def addrow(sqnum: int8, add: int) -> int8:
    return int8(int(sqnum) + add*8)

def addrows(sqnum: int8, adds: list[int]) -> list[int8]:
    return [addrow(sqnum, add) for add in adds]

# uses n64 to return n64 row manipulation
def addcol(sqnum: int8, add: int) -> int8:
    return sqnum + add

def addcols(sqnum: int8, adds: list[int]) -> list[int8]:
    return [addcols(sqnum, add) for add in adds]

def getMouseSqnum(mouse_IJ: tuple[int]) -> int8:
    return g.pos2num_dyna(mouse_IJ)

def validSquare(sqnum: int8) -> bool:
    return sqnum >= 0 and sqnum < 64

def validSquares(sqnums: list[int8]) -> bool:
    return any([validSquare(sqnum) for sqnum in sqnums])

def isTurn(piece: int, turn: bool) -> bool:
    if piece == EMPTY or None: return False
    return (pieceColour(piece) == 'w') == turn

def nextTurn() -> None:
    global turn
    turn = not turn

def findKing(colour: str, board: array) -> int8:
    result = where(board == pieceInt(colour + 'K'))

    if len(result[0]) == 0: return None

    return int8(result[0][0])

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

def possibleMoves(sqnum: int8, board: array) -> list[list]:
    piece: int = getPiece(sqnum, board)
    if piece == EMPTY: return []

    moveFunc: callable = MOVE_FUNCTIONS[pieceStr(piece)[1]]
    moves: list[list] = moveFunc(sqnum, board)
    moves_special: list[list] = getSpecialMoves(sqnum, board)

    return moves, moves_special

def getPiece(sqnum: int8, board: array) -> int:
    if validSquare(sqnum): return board[sqnum]

def remPiece(sqnum: int8, board: array) -> None:
    if validSquare(sqnum): board[sqnum] = EMPTY

def setPiece(sqnum: int8, board: array, piece: int) -> None:
    if validSquare(sqnum): board[sqnum] = piece

def pieceColour(piece: int) -> str:
    return pieceStr(piece)[0]

def pieceType(piece: int) -> str:
    return pieceStr(piece)[1] if piece != EMPTY else 'e'

def promotionLogic(move: list[int8], board: array) -> None:
    piece: str = pieceStr(getPiece(move[1], board))
    row, _ = num2square(move[1])

    if piece[0] == 'e': return

    if piece[1] == 'P':
        if (row == 0 and piece[0] == 'w') or (row == 7 and piece[0] == 'b'):
            promotion: str = getUserInput(['q','r','b','n'], "Which piece would you like to promote to? q/r/b/n")
            setPiece(move[1], board, pieceInt(piece[0] + promotion.upper()))
            # return pieceInt(piece[0] + promotion.upper())

def checkmate(turn: bool, board: array):
    colour: str = 'w' if turn else 'b'

    if not isInCheck(colour, board): return False

    kingSqnum: int8 = findKing(colour, board)
    kingColour: str = pieceColour(getPiece(kingSqnum, board))

    moves, specialMoves = possibleMoves(kingSqnum, board)

    for sqnum in range(64):
        piece: int = getPiece(sqnum, board)
        square: list[int] = [row, col]

        if pieceColour(piece) == kingColour:
            moves, specialMoves = possibleMoves(square, board)

            for move in moves:
                if legalMove([square, move], possibleMoves(square, board), board):
                    return False

            for move in specialMoves:
                if legalMove(move, possibleMoves(square, board), board):
                    return False

    return True

def getSpecialMoves(sqnum: list[int], board: array):
    piece: int = getPiece(sqnum, board)

    if pieceType(piece) == "K":
        return kingSpecial(*square, board)
    elif pieceType(piece) == "P":
        return pawnSpecial(*square, board)
    
    return []

def clickInRange(mouse_IJ_rel: list[int]) -> bool:
    if mouse_IJ_rel[0] < 0 or mouse_IJ_rel[0] > g.SCREEN_DIMS[0]:
        return False
    
    if mouse_IJ_rel[1] < 0 or mouse_IJ_rel[1] > g.SCREEN_DIMS[1]:
        return False
    
    return True



### Piece movement functions

def rook(sqnum: int8, board: array) -> list[list]:
    tracker: list[bool] = [True, True, True, True]
    colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[int8] = []

    for i in range(1,8):
        sqnums = [
            addcol(sqnum, i),
            addcol(sqnum,-i),
            addrow(sqnum, i),
            addrow(sqnum,-i),
        ]
        
        for i, sqnum in enumerate(sqnums):
            if validSquare(sqnum):
                opColour = pieceColour(getPiece(sqnum, board))

                if opColour not in [colour, 'e'] and tracker[i]:
                    moves.append(sqnum)
                    tracker[i] = False
                elif opColour == colour:
                    tracker[i] = False
                
                if tracker[i]:
                    moves.append(sqnum)
            
            if not any(tracker): break

    return moves

def knight(sqnum: int8, board: array) -> list[int8]:
    colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[int8] = []


    sqnums: list[int8] = [
        addrow(addcol(sqnum,  1),  2),
        addrow(addcol(sqnum, -1),  2),
        addrow(addcol(sqnum,  2),  1),
        addrow(addcol(sqnum, -2),  1),
        addrow(addcol(sqnum,  1), -2),
        addrow(addcol(sqnum, -1), -2),
        addrow(addcol(sqnum,  2), -1),
        addrow(addcol(sqnum, -2), -1),
    ]
    
    for sqnum in sqnums:
        if validSquare(sqnum):
            if pieceColour(getPiece(sqnum, board)) != colour:
                moves.append(sqnum)

    return moves

def bishop(sqnum: int8, board: array) -> list[int8]:
    tracker: list[bool] = [True, True, True, True]
    colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[int8] = []

    for i in range(1,8):
        sqnums = [
            addrow(addcol(sqnum,  1),  1),
            addrow(addcol(sqnum, -1),  1),
            addrow(addcol(sqnum,  1), -1),
            addrow(addcol(sqnum, -1), -1),
        ]
        
        for i, sqnum in enumerate(sqnums):
            if validSquare(sqnum):
                opColour = pieceColour(getPiece(sqnum, board))

                if opColour not in [colour, 'e'] and tracker[i]:
                    moves.append(sqnum)
                    tracker[i] = False
                elif opColour == colour:
                    tracker[i] = False
                
                if tracker[i]:
                    moves.append(sqnum)

            if not any(tracker): break

    return moves

def queen(sqnum: int8, board: array) -> list[int8]:
    return bishop(sqnum, board) + rook(sqnum, board)

def king(sqnum: int8, board: array) -> list[int8]:
    colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[list[int]] = []
    specialMoves: list[list[int]] = []

    # surrounding 8 squares
    sqnums: list[int8] = [
        [addrow(addcol(sqnum, i), j) for j in range(-1,1) if not(i==j==0)] for i in range(-1,1)
    ]
    
    for sqnums in sqnums:
        if validSquare(sqnum):
            if pieceColour(getPiece(sqnum, board)) != colour:
                moves.append(sqnum)

    return moves

def kingSpecial(sqnum: int8, board: array) -> tuple[list]:
    colour: str = pieceColour(getPiece(sqnum, board))
    moves: tuple[list] = []

    # castling logic
    rank = 7 if colour == 'w' else 0
    queenside: bool = not any(castleTracker[colour][0:2]) and all(board[rank, 1:4] == pieceInts(('e','e','e')))
    kingside:  bool = not any(castleTracker[colour][1:3]) and all(board[rank, 5:7] == pieceInts(('e','e')))

    if queenside: moves.append([sqnum, *addcols(sqnum, [-2,-4,-1])])
    if kingside:  moves.append([sqnum, *addcols(sqnum, [ 2, 3, 1])])

    return moves

def pawn(sqnum: int8, board: array) -> list[int8]:
    colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[int8] = []

    direction: int = int(colour == 'b')*2 - 1

    # forward squares
    forwardSquares = [addrow(sqnum, direction)]
    row, _ = num2square(sqnum)

    if (colour == 'w' and row == 6) or (colour == "b" and row == 1):
        forwardSquares.append(addrow(sqnum, 2*direction))
    
    for sqnum in forwardSquares:
        if getPiece(sqnum, board) == EMPTY:
            moves.append(sqnum)
        else:
            break
    

    # attack squares
    attackSquares = [
        addrow(addcol(sqnum,  1), direction),
        addrow(addcol(sqnum, -1), direction),
    ]

    for sqnum in attackSquares:
        piece = getPiece(sqnum, board)

        if piece not in [None, EMPTY] and pieceColour(piece) != colour:
            moves.append(sqnum)
        
    return moves

def pawnSpecial(sqnum, board: array) -> tuple[list]:
    colour: str = pieceColour(getPiece(sqnum, board))
    direction: int = int(colour == 'b')*2 - 1
    moves: list = []
    
    # en passant
    row, col = num2square(sqnum)

    if len(moveLog) > 0:
        lastMove = moveLog[-1] #num2square(moveLog[-1])
        if pieceType(getPiece(lastMove[1], board)) == 'P':
            lmrow1, _ = num2square(lastMove[0])
            lmrow2, lmcol2 = num2square(lastMove[1])

            coldiff = lmcol2 - col
            rowdiff = lmrow1 - lmrow2
            rightPosition = (colour == 'w' and row == 3) or (colour == 'b' and row == 4)

            if abs(coldiff) == 1 and abs(rowdiff) == 2 and rightPosition:
                moves.append([sqnum, addrow(addcol(sqnum, coldiff), direction), addcol(sqnum, coldiff)])
            
    return moves




### Main Function(s)

def isInCheck(colour: str, board: array) -> bool:
    kingSquare: int8 = findKing(colour, board)
    if kingSquare == None: return None

    oppColour: str = opponentColour(colour)
    
    # bishop/queen
    sqnums: list[int8] = bishop(kingSquare, board)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'B') in pieces: print('Bishop checks the king!'); return True
    if pieceInt(oppColour + 'Q') in pieces: print('Queen checks the king!');  return True
    
    # roook/queen
    sqnums: list[int8] = rook(kingSquare, board)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'R') in pieces: print('Rook checks the king!');   return True
    if pieceInt(oppColour + 'Q') in pieces: print('Queen checks the king!');  return True
    
    # knight
    sqnums: list[int8] = knight(kingSquare, board)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'N') in pieces: print('Knight checks the king!'); return True
    
    # king
    sqnums: list[int8] = king(kingSquare, board)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'K') in pieces: print('King checks the king!');   return True

    # pawn
    sqnums: list[int8] = pawn(kingSquare, board)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'P') in pieces: print('Pawn checks the king!');   return True
    
    return False

# ensures user input is converted to its full representation
def getMove(move: list[list], specialMoves: tuple[list], board: array) -> tuple[int8]:
    specialMovesSimple: list[list] = [m[:2] for m in specialMoves]

    if move in specialMovesSimple:
        i: int = specialMovesSimple.index(move)
        return specialMoves[i]

    return tuple([square2num(square) for square in copy(move)])

def legalMove(move: tuple[int8], possibleMoves: list[list], board: array) -> bool:
    sqnum1 = sqnum2 = 0
    
    if len(move) in [2,3]:
        sqnum1, sqnum2 = move[:2]
    else:
        sqnum1, sqnum2 = move[2:4]

    piece1 = getPiece(sqnum1, board)
    piece2 = getPiece(sqnum2, board)

    # basic legality checks
    isEmpty:    bool = bool(piece1 == EMPTY)
    sameColour: bool = pieceColour(piece1) == pieceColour(piece2)

    if isEmpty or sameColour: return False


    # ensure move is in possible moveset
    inMoveSet: bool = False
    moves, specialMoves = possibleMoves

    if sqnum2 in moves:
        inMoveSet = True
    elif move in specialMoves:
        inMoveSet = True
    

    # ensure check does not occur post-move
    p_board = copy(board)
    if len(move) == 2:
        movePiece(*move, p_board)
    else:
        movePieceSpecial(move, p_board)

    inCheck: bool = isInCheck(pieceColour(piece1), p_board)
    if inCheck == None: return False

    return not any([not inMoveSet, inCheck])

def movePiece(sqnum1: int8, sqnum2: int8, board: array) -> bool:
    s1: tuple = num2square(sqnum1)
    s2: tuple = num2square(sqnum2)

    board[*s2] = getPiece(sqnum1, board)
    board[*s1] = EMPTY

def movePieceSpecial(move: list[int8], board: array):
    if len(move) == 3: # en passant
        movePiece(*move[:2], board)
        remPiece(move[2], board)
        
    elif len(move) == 4: # castling
        movePiece(*move[:2], board)
        movePiece(*move[2:4], board)
    else:
        raise ValueError

def initBoard() -> array:
    board = ones(64, int)*EMPTY
    board[ 0 :  8] = array(pieceInts(['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']))
    board[ 8 : 16] = array(pieceInts(['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']))
    board[48 : 56] = array(pieceInts(['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP']))
    board[56 : 64] = array(pieceInts(['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']))

    return board

def animatedMove(squares: list[list]):
    assert(len(squares) == 4)

    moves, specialMoves = possibleMoves(sequence.squares[0], board)
    move: tuple[int8] = getMove(squares[1:3], specialMoves, board)
    
    if legalMove(move, [moves, specialMoves], board):
        if len(move) in [2, 3]:
            point1 = g.num2pos(move[0])
            point2 = g.num2pos(move[1])

            # move_animate(pieceImages[selectedPiece], point1, point2, dt=0.15)

            movePiece(*move[:2], board)

            # delete piece if en passant
            if len(move) == 3: remPiece(move[2], board)

        elif len(move) == 4:
            movePiece(*move[:2], board)
            movePiece(*move[2:4], board)
        
        moveLog.append(move)
        nextTurn()
    else:
        print("ILLEGAL MOVE!")

    g.drawPieces(board)
    # g.updateScreen()

def updateGraphics(mouse_IJ: tuple[int]) -> p.Surface:
    win: p.Surface = g.updateScreen(800)

    if hover.hovering:
        g.pieceHover(hover.piece, g.num2pos(hover.sqnum), mouse_IJ)
    else:
        g.drawPieces(board)
    
    return win

def updateGame(mouse_buttons: tuple[int], mouse_IJ_rel: tuple[int]) -> None:
    global gameover
    if gameover: return

    if not clickInRange(mouse_IJ_rel):
        sequence.clear()
        hover.clear()
        g.clearLayer(g.animationLayer)
        return

    buttonClicked: str = getMouseButtonStr(mouse_buttons)
    mouseSqnum: int8 = getMouseSqnum(mouse_IJ_rel)

    if buttonClicked == None: return

    sequence.add(buttonClicked, mouseSqnum)
    

    # manage hovering pieces
    hover.clear()
    g.clearLayer(g.animationLayer)

    if buttonClicked == 'ldown':
        g.clearUserStyling()
        piece: int = getPiece(mouseSqnum, board)

        if isTurn(piece, turn):
            hover.set(piece, mouseSqnum)
            sequence.clear()
            sequence.add(buttonClicked, mouseSqnum)
        
    if sequence.active[0] in ['lup','rup']: sequence.clear()
    

    if any([sequence.match(seq) for seq in sequences]):
        if sequence.active == sequences[0]:
            piece: int = getPiece(sequence.squares[0], board)

            if piece == EMPTY or not isTurn(piece, turn):
                sequence.clear()
            elif sequence.squares[0] != sequence.squares[1]:
                moves, specialMoves = possibleMoves(sequence.squares[0], board)
                move: tuple[int8] = getMove(sequence.squares, specialMoves, board)

                if legalMove(move, [moves, specialMoves], board):
                    if len(move) == 2:
                        movePiece(*move, board)
                    else:
                        movePieceSpecial(move, board)

                    moveLog.append((move))
                    promotionLogic(sequence.squares, board)
                    nextTurn()
                else:
                    print("ILLEGAL MOVE!")

                sequence.clear()

        # handle arrows and highlights
        elif sequence.active == sequences[1]:
            if sequence.squares[0] == sequence.squares[1]:
                g.addSquareHighlight(*sequence.squares[0])
            else:
                g.addArrow(*sequence.squares)
            
            sequence.clear()

        # animated piece moves
        elif sequence.active == sequences[2]:
            if isTurn(getPiece(sequence.squares[0], board), turn):
                animatedMove(sequence.squares)
                promotionLogic(sequence.squares[1:3], board)

            sequence.clear()
    else:
        sequence.clear()

    if checkmate(turn, board):
        print(f"Game over! {'White' if turn else 'Black'} wins!")
        gameover = True
            



PIECE_CODES = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP", "e"]
MOVE_FUNCTIONS: dict[str, callable] = {"R": rook, "N": knight, "B": bishop, "Q": queen, "K": king, "P": pawn}
EMPTY = len(PIECE_CODES) - 1

TARGET_FPS = 100

clock = p.time.Clock()
fps_tracker: list[float] = [0]*100
fps_count: int = 0
last_time: float = 0
nano: int = 10**9
gameover: bool = False

# tracks the left rooks, king, and right rooks and if they have moved
castleTracker: dict[str, list] = {'w': [False, False, False], 'b': [False, False, False]}

board: array = initBoard()
turn: bool = True # white is true, black is false
moveLog: list[list] = []
hover: Hover = Hover()
sequence: Sequence = Sequence()
sequences: list[tuple] = [['ldown', 'lup'], ['rdown', 'rup'], ['ldown', 'lup', 'ldown', 'lup']]



if __name__ == "__main__":
    import pygame as p
    import graphics as g


    def mouseRel(win_dims: tuple[int]) -> tuple[int]:
        return tuple([int(v) for v in array(p.mouse.get_pos()) - array(win_dims)])

    win = p.display.set_mode((800,800))
    p.init()
    g.init()

    win_x, win_y = (0,0)
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                exit()
            elif e.type in (p.MOUSEBUTTONDOWN, p.MOUSEBUTTONUP):
                updateGame(p.mouse.get_pressed(), mouseRel((win_x, win_y)))
    
    
        screen = updateGraphics(mouseRel((win_x, win_y)))
        win.blit(screen, (win_x, win_y))
        p.display.update()

        # track FPS
        time = time_ns()
        fps_tracker.pop(0)
        fps_tracker.append(nano/(time - last_time))
        
        last_time = time

        # draw avg fps at a custom rate (in Hz)
        if fps_count > TARGET_FPS//5:
            fps_count = 0

            g.clearLayer(g.extrasLayer)
            fps_avg: float = str(round(sum(fps_tracker)/len(fps_tracker)))
            g.drawSprite(g.extrasLayer, g.textSprite(str(fps_avg)), (2,2))
        else:
            fps_count += 1

        clock.tick(TARGET_FPS)