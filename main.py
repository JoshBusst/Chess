
from numpy import array, where, ones
from ui import getUserInput
from lib import *
import graphics as g
from ui import getMouseButtonStr
from copy import copy
from time import time_ns





# promotion logic needs to be NON BLOCKING!
# update graphics to accomodate static and then dyanmic screen size changes
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



class Sequence:
    active: list[str]
    squares: list[list]

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

    def add(self, buttonStr: str, square: list[int]):
        self.active.append(buttonStr)
        self.squares.append(square)



### Miscellaneous helper functions

def square2coord(square: list[int]) -> str:
    ranks: str = '87654321'
    files: str = 'abcdefgh'

    return files[square[1]] + ranks[square[0]]

def coord2square(coord: str) -> list[int]:
    ranks: str = '87654321'
    files: str = 'abcdefgh'

    return [int(ranks[int(coord[1])]), files.index(coord[0])]

def getMouseSquare(mouse_IJ: tuple[int]) -> list[int]:
    return g.pos2square(mouse_IJ)

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
    return pieceStr(piece)[1] if piece != EMPTY else 'e'

def promotionLogic(move: list[list[int]], board: array) -> None:
    piece: str = pieceStr(getPiece(*move[1], board))

    if piece[0] == 'e': return

    if piece[1] == 'P':
        if (move[1][0] == 0 and piece[0] == 'w') or (move[1][0] == 7 and piece[0] == 'b'):
            promotion: str = getUserInput(['q','r','b','n'], "Which piece would you like to promote to? q/r/b/n")
            setPiece(*move[1], board, pieceInt(piece[0] + promotion.upper()))
            # return pieceInt(piece[0] + promotion.upper())

def checkmate(turn: bool, board: array):
    colour: str = 'w' if turn else 'b'

    if not isInCheck(colour, board): return False

    kingSquare: list[int] = findKing(colour, board)
    kingColour: str = pieceColour(getPiece(*kingSquare, board))

    moves, specialMoves = possibleMoves(kingSquare, board)

    for row in range(8):
        for col in range(8):
            piece: int = getPiece(row, col, board)
            square: list[int] = [row, col]

            if pieceColour(piece) == kingColour:
                moves, specialMoves = possibleMoves(square, board)

                for move in moves:
                    if legalMove([square, move], possibleMoves(square, board), board):
                        return False

                for move in specialMoves:
                    if legalMove(move, possibleMoves(square, board), board):
                        return False

    # print(f"Ran in: {round(((time_ns() - start)/(10**6)), 3)}ms")

    return True

def getSpecialMoves(square: list[int], board: array):
    piece: int = getPiece(*square, board)

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
        if pieceType(getPiece(*lastMove[1], board)) == 'P':
            coldiff = lastMove[1][1] - col
            rowdiff = lastMove[0][0] - lastMove[1][0]
            rightPosition = (colour == 'w' and row == 3) or (colour == 'b' and row == 4)

            if abs(coldiff) == 1 and abs(rowdiff) == 2 and rightPosition:
                moves.append([[row, col], [row + direction, col + coldiff], [row, col + coldiff]])
            
    return moves




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

# ensures user input is converted to its full representation
def getMove(move: list[list], specialMoves: tuple[list], board: array) -> list[list]:
    specialMovesSimple: list[list] = [m[:2] for m in specialMoves]

    if move in specialMovesSimple:
        i: int = specialMovesSimple.index(move)
        return specialMoves[i]

    return copy(move)

def legalMove(move: list[list], possibleMoves: list[list], board: array) -> bool:
    square1 = square2 = []
    
    if len(move) in [2,3]:
        square1, square2 = move[:2]
    else:
        square1, square2 = move[2:4]

    piece1 = getPiece(*square1, board)
    piece2 = getPiece(*square2, board)

    # basic legality checks
    isEmpty:    bool = bool(piece1 == EMPTY)
    sameColour: bool = pieceColour(piece1) == pieceColour(piece2)

    if isEmpty or sameColour: return False


    # ensure move is in possible moveset
    inMoveSet: bool = False
    moves, specialMoves = possibleMoves

    if square2 in moves:
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

def movePiece(square1: list[int], square2: list[int], board: array) -> bool:
    board[*square2] = getPiece(*square1, board)
    board[*square1] = EMPTY

def movePieceSpecial(move: list[list[int]], board: array):
    if len(move) == 3: # en passant
        movePiece(*move[:2], board)
        remPiece(*move[2], board)
        
    elif len(move) == 4: # castling
        movePiece(*move[:2], board)
        movePiece(*move[2:4], board)
    else:
        raise ValueError

def initBoard() -> array:
    board = ones([8,8], int)*EMPTY
    board[0,:] = array(pieceInts(['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']))
    board[1,:] = array(pieceInts(['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']))
    board[6,:] = array(pieceInts(['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP']))
    board[7,:] = array(pieceInts(['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']))

    return board

def animatedMove(squares: list[list]):
    assert(len(squares) == 4)

    moves, specialMoves = possibleMoves(sequence.squares[0], board)
    move: list[list] = getMove(squares[1:3], specialMoves, board)
    
    if legalMove(move, [moves, specialMoves], board):
        if len(move) in [2, 3]:
            point1 = g.square2pos(*move[0])
            point2 = g.square2pos(*move[1])

            # move_animate(pieceImages[selectedPiece], point1, point2, dt=0.15)

            movePiece(*move[:2], board)

            # delete piece if en passant
            if len(move) == 3: remPiece(*move[2], board)

        elif len(move) == 4:
            movePiece(*move[:2], board)
            movePiece(*move[2:4], board)
        
        moveLog.append(move)
        nextTurn()
    else:
        print("ILLEGAL MOVE!")

    g.drawPieces(board)
    g.updateScreen()

def updateGraphics(mouse_IJ: tuple[int]) -> p.Surface:
    win: p.Surface = g.updateScreen()

    if hover.hovering:
        g.pieceHover(hover.piece, g.square2pos(hover.row, hover.col), mouse_IJ)
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
    mouseSquare: list[int] = getMouseSquare(mouse_IJ_rel)

    if buttonClicked == None: return

    sequence.add(buttonClicked, mouseSquare)
    

    # manage hovering pieces
    hover.clear()
    g.clearLayer(g.animationLayer)

    if buttonClicked == 'ldown':
        g.clearUserStyling()
        piece: int = getPiece(*mouseSquare, board)

        if isTurn(piece, turn):
            hover.set(piece, *mouseSquare)
            sequence.clear()
            sequence.add(buttonClicked, mouseSquare)
        
    if sequence.active[0] in ['lup','rup']: sequence.clear()
    

    if any([sequence.match(seq) for seq in sequences]):
        if sequence.active == sequences[0]:
            piece: int = getPiece(*sequence.squares[0], board)

            if piece == EMPTY or not isTurn(piece, turn):
                sequence.clear()
            elif sequence.squares[0] != sequence.squares[1]:
                moves, specialMoves = possibleMoves(sequence.squares[0], board)
                move: list[list] = getMove(sequence.squares, specialMoves, board)

                if legalMove(move, [moves, specialMoves], board):
                    if len(move) == 2:
                        movePiece(*move, board)
                    else:
                        movePieceSpecial(move, board)

                    moveLog.append(move)
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
            if isTurn(getPiece(*sequence.squares[0], board), turn):
                animatedMove(sequence.squares)
                promotionLogic(sequence.squares[1:3], board)

            sequence.clear()
    else:
        sequence.clear()

        
    print(moveLog)

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