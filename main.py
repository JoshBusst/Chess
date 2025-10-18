
from numpy import array, where, ones
from ui import getUserInput
from lib import *
import graphics as g
from ui import getMouseButtonStr
from copy import copy
from time import time_ns
from random import randint




# refactor to use n64 format instead of [row, col]

# promotion logic needs to be NON BLOCKING!
# update graphics to accomodate static and then dyanmic screen size changes
# maybe refactor a lil
# add forward and back buttons ie cycling through move history



### castling logic broken. Can still castle even if king has moved ###


# hover class for managing hovering pieces
class Hover:
    def __init__(self):
        self.hovering: bool = False
        self.piece: int = EMPTY
        self.sqnum: int = None

    def set(self, piece: int, sqnum: int) -> None:
        self.hovering = True
        self.piece = piece
        self.sqnum = sqnum

    def clear(self) -> None:
        self.hovering = False
        self.piece = EMPTY
        self.sqnum = None



class Sequence:
    active: list[str]
    squares: list[int]

    def __init__(self):
        self.active = []
        self.squares = []

    def clear(self) -> None:
        self.active.clear()
        self.squares.clear()

    # return true if full or partial sequence match is found
    def match(self, matchSeq: list) -> bool:
        if len(self.active) > len(matchSeq): return False

        return all([self.active[i] == matchSeq[i] for i in range(len(self.active))])

    def add(self, buttonStr: str, sqnum: int):
        self.active.append(buttonStr)
        self.squares.append(sqnum)



class Player:
    colour: str
    name: str

    def __init__(self, name: str, colour: str):
        self.name = name
        self.colour = colour



def agentMove(agent: Player, board: array):
    moves = getAllLegalMoves(agent.colour, board)
    print('agent moves')
    print(moves)

    # for move in moves:
    #     g.addArrow(*move)

    return moves[randint(0,len(moves)-1)]


### Miscellaneous helper functions

def flatten(nested_list: list[list]) -> list:
    return [item for sublist in nested_list for item in sublist]

def printBoard(board: array) -> None:
    printStr: str = ""

    for i in range(8):
        for j in range(8):
            piece = board[i*8+j]

            if piece == EMPTY:
                printStr += " .."
            else:
                printStr += " " + pieceStr(piece)

        printStr += "\n"

    print(printStr + '\n')

# convert to n64 number  format
def square2num(square: tuple) -> int:
    return int(8*square[0] + square[1])

# convert from n64 nubmer format to [row, col]
def num2square(num: int) -> tuple:
    return (num // 8, num % 8)

def num2pgn(num: int) -> str:
    return square2pgn(num2square(num))

def pgn2num(pgn: str) -> int:
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
def addrow(sqnum: int, add: int) -> int:
    return int(int(sqnum) + add*8)

def addrows(sqnum: int, adds: list[int]) -> list[int]:
    return [addrow(sqnum, add) for add in adds]

# uses n64 to return n64 row manipulation
def addcol(sqnum: int, add: int) -> int:
    return int(sqnum + add)

def addcols(sqnum: int, adds: list[int]) -> list[int]:
    return [addcol(sqnum, add) for add in adds]

def getMouseSqnum(mouse_IJ: tuple[int]) -> int:
    return g.pos2num_dyna(mouse_IJ)

def validSqnum(sqnum: int) -> bool:
    return sqnum >= 0 and sqnum < 64

def validSquare(sq):
    return sq[0] < 8 and sq[0] >= 0 and sq[1] < 8 and sq[1] >= 0

def validSqnums(sqnums: list[int]) -> bool:
    return any([validSqnum(sqnum) for sqnum in sqnums])

def isTurn(piece: int, turn: bool) -> bool:
    if piece == EMPTY or None: return False
    return (pieceColour(piece) == 'w') == turn

def nextTurn() -> None:
    global turn
    turn = not turn

def playerTurn(player: Player):
    return turn == (player.colour == 'w')

def findKing(colour: str, board: array) -> int:
    result = where(board == pieceInt(colour + 'K'))

    if len(result[0]) == 0: return None

    return int(result[0][0])

def opponentColour(colour: str) -> str:
    return 'w' if colour == 'b' else 'b'



### Interface Classes
def getThemes():
    pass

def setTheme():
    pass

def getMoveHistory():
    pass

def historySet():
    pass

def getBoard():
    pass

def setBoard():
    pass

def playMove():
    pass

def importFEN():
    pass

def exportFEN():
    pass



### Piece management

def pieceStr(integer: int) -> str:
    return PIECE_CODES[integer]

def pieceStrs(integers: list[int]) -> array:
    return array([PIECE_CODES[i] for i in integers])

def pieceInt(string: str) -> int:
    return PIECE_CODES.index(string)

def pieceInts(strings: list[str]) -> array:
    return array([pieceInt(i) for i in strings])

def possibleMoves(sqnum: int, board: array) -> list | list:
    piece: int = getPiece(sqnum, board)
    if piece == EMPTY: return []
    
    moveFunc: callable = MOVE_FUNCTIONS[pieceStr(piece)[1]]
    moves: list[list] = moveFunc(sqnum, board)
    
    moves_special: list[list] = getSpecialMoves(sqnum, board)

    return moves, moves_special

def getPiece(sqnum: int, board: array) -> int:
    if validSqnum(sqnum): return board[sqnum]

def remPiece(sqnum: int, board: array) -> None:
    if validSqnum(sqnum): board[sqnum] = EMPTY

def setPiece(sqnum: int, board: array, piece: int) -> None:
    if validSqnum(sqnum): board[sqnum] = piece

def pieceColour(piece: int) -> str:
    return pieceStr(piece)[0]

def pieceType(piece: int) -> str:
    return pieceStr(piece)[1] if piece != EMPTY else 'e'

def promotionLogic(move: list[int], board: array) -> None:
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

    if not isInCheck(colour, board):
        return False

    kingSqnum: int = findKing(colour, board)
    moves, _ = possibleMoves(kingSqnum, board)

    legals: list[tuple] = legalMoves([(kingSqnum, move) for move in moves], moves, board)

    if len(legals) == 0:
        return True
    
    return False

    # for sqnum in range(64):
    #     piece: int = getPiece(sqnum, board)

    #     if pieceColour(piece) == kingColour:
    #         moves, specialMoves = possibleMoves(sqnum, board)
    #         for move in moves:
    #             if legalMove([sqnum, move], moves, specialMoves, board):
    #                 return False

    #         for move in specialMoves:
    #             if legalMove(move, moves, specialMoves, board):
    #                 return False

    # return True

def getSpecialMoves(sqnum: int, board: array):
    piece: int = getPiece(sqnum, board)

    if pieceType(piece) == "K":
        return kingSpecial(sqnum, board)
    elif pieceType(piece) == "P":
        return pawnSpecial(sqnum, board)
    
    return []

def getAllLegalMoves(colour: str, board: array):
    legals: list = []
    count = 0

    for sqnum in range(64):
        if pieceColour(getPiece(sqnum, board)) == colour:
            count += 1
            moves, specialMoves = possibleMoves(sqnum, board)
            legals += legalMoves([(sqnum, move) for move in moves], moves + specialMoves, board)

    # print(f"{count} pieces counted!")
    return legals

def getAllPossibleMoves(colour: str, board: array):
    allMoves: list = []
    count = 0

    for sqnum in range(64):
        if pieceColour(getPiece(sqnum, board)) == colour:
            count += 1
            moves, specialMoves = possibleMoves(sqnum, board)

            allMoves += specialMoves
            allMoves += [[int(sqnum), move] for move in moves]

    # print(f"{count} pieces counted!")
    return allMoves

def clickInRange(mouse_IJ_rel: list[int]) -> bool:
    if mouse_IJ_rel[0] < 0 or mouse_IJ_rel[0] > g.SCREEN_DIMS[0]:
        return False
    
    if mouse_IJ_rel[1] < 0 or mouse_IJ_rel[1] > g.SCREEN_DIMS[1]:
        return False
    
    return True

def getMouseRel(win_dims: tuple[int]) -> tuple[int]:
    return tuple([int(v) for v in array(p.mouse.get_pos()) - array(win_dims)])



### Piece movement functions

def rook(sqnum: int, board: array, colour: str=None) -> list[int]:
    tracker: list[bool] = [True, True, True, True]
    if colour == None: colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[int] = []

    row, col = num2square(sqnum)

    for i in range(1,8):
        squares = [
            [row, col + i],
            [row, col - i],
            [row + i, col],
            [row - i, col],
        ]
        
        # sqnums = [
        #     addcol(sqnum, i),
        #     addcol(sqnum,-i),
        #     addrow(sqnum, i),
        #     addrow(sqnum,-i),
        # ]
        
        for i, square in enumerate(squares):
            if validSquare(square):
                opColour = pieceColour(getPiece(square2num(square), board))

                if opColour not in [colour, 'e'] and tracker[i]:
                    moves.append(square2num(square))
                    tracker[i] = False
                elif opColour == colour:
                    tracker[i] = False
                
                if tracker[i]:
                    moves.append(square2num(square))
            
            if not any(tracker): break

    return moves

def knight(sqnum: int, board: array, colour: str=None) -> list[int]:
    if colour == None: colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[int] = []

    row, col = num2square(sqnum)
    squares = [
        [row - 2, col - 1],
        [row - 2, col + 1],
        [row - 1, col - 2],
        [row - 1, col + 2],
        [row + 1, col - 2],
        [row + 1, col + 2],
        [row + 2, col - 1],
        [row + 2, col + 1],
    ]

    for square in squares:
        if validSquare(square):
            if pieceColour(getPiece(square2num(square), board)) != colour:
                moves.append(square2num(square))

    # sqnums: list[int] = [
    #     addrow(addcol(sqnum,  1),  2),
    #     addrow(addcol(sqnum, -1),  2),
    #     addrow(addcol(sqnum,  2),  1),
    #     addrow(addcol(sqnum, -2),  1),
    #     addrow(addcol(sqnum,  1), -2),
    #     addrow(addcol(sqnum, -1), -2),
    #     addrow(addcol(sqnum,  2), -1),
    #     addrow(addcol(sqnum, -2), -1),
    # ]
    
    # for sq in sqnums:
    #     if validSqnum(sq):
    #         if pieceColour(getPiece(sq, board)) != colour:
    #             moves.append(sq)

    return moves

def bishop(sqnum: int, board: array, colour: str=None) -> list[int]:
    tracker: list[bool] = [True, True, True, True]
    if colour == None: colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[int] = []

    row, col = num2square(sqnum)

    for i in range(1,8):
        squares = [
            [row + i, col + i],
            [row - i, col + i],
            [row + i, col - i],
            [row - i, col - i],
        ]
        # sqnums = [square2num(sq) for sq in squares]
        # sqnums = [
        #     addrow(addcol(sqnum,  i),  i),
        #     addrow(addcol(sqnum, -i),  i),
        #     addrow(addcol(sqnum,  i), -i),
        #     addrow(addcol(sqnum, -i), -i),
        # ]
        
        for i, square in enumerate(squares):
            if validSquare(square):
                opColour = pieceColour(getPiece(square2num(square), board))

                if opColour not in [colour, 'e'] and tracker[i]:
                    moves.append(square2num(square))
                    tracker[i] = False
                elif opColour == colour:
                    tracker[i] = False
                
                if tracker[i]:
                    moves.append(square2num(square))

            if not any(tracker): break

    return moves

def queen(sqnum: int, board: array, colour: str=None) -> list[int]:
    return bishop(sqnum, board, colour=colour) + rook(sqnum, board, colour=colour)

def king(sqnum: int, board: array, colour: str=None) -> list[int]:
    if colour == None: colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[list[int]] = []

    row, col = num2square(sqnum)

    # surrounding 8 squares
    # sqnums: list[int] = flatten([
    #     [addrow(addcol(sqnum, i), j) for j in range(-1,2) if not(i==j==0)] for i in range(-1,2)
    # ])
    squares: list[int] = flatten([
        [[row + i, col + j] for j in range(-1,2) if not(i==j==0)] for i in range(-1,2)
    ])
    
    for square in squares:
        if validSquare(square):
            if pieceColour(getPiece(square2num(square), board)) != colour:
                moves.append(square2num(square))

    return moves

def kingSpecial(sqnum: int, board: array, colour: str=None) -> list[tuple]:
    if colour == None: colour: str = pieceColour(getPiece(sqnum, board))
    moves: list = []

    # castling logic
    rank = 7 if colour == 'w' else 0

    start: int = addrow(0,rank)
    slce: slice = slice(start, start + 8)
    rng: list = list(range(64))

    queenside: bool = not any(castleTracker[colour][0:2]) and all(board[slce][1:4] == pieceInts(('e','e','e')))
    notAttackedQS: bool = not any([isAttacked(sqnum, colour, board) for sqnum in rng[slce][1:4]])
    kingside:  bool = not any(castleTracker[colour][1:3]) and all(board[slce][5:7] == pieceInts(('e','e')))
    notAttackedKS: bool = not any([isAttacked(sqnum, colour, board) for sqnum in rng[slce][5:7]])

    if queenside and notAttackedQS: moves.append((sqnum, *addcols(sqnum, [-2,-4,-1])))
    if kingside  and notAttackedKS: moves.append((sqnum, *addcols(sqnum, [ 2, 3, 1])))

    return moves

def pawn(sqnum: int, board: array, colour: str=None) -> list[int]:
    if colour == None: colour: str = pieceColour(getPiece(sqnum, board))
    moves: list[int] = []
    row, col = num2square(sqnum)

    direction: int = 1 if colour == 'b' else -1

    # forward squares
    forwardSquares = [addrow(sqnum, direction)]
    row, _ = num2square(sqnum)

    if (colour == 'w' and row == 6) or (colour == "b" and row == 1):
        forwardSquares.append(addrow(sqnum, 2*direction))
    
    for forward in forwardSquares:
        if getPiece(forward, board) == EMPTY:
            moves.append(forward)
        else:
            break

    # attack squares
    # attackSquares = [
    #     addrow(addcol(sqnum,  1), direction),
    #     addrow(addcol(sqnum, -1), direction),
    # ]
    attackSquares = [
        [row + direction, col + 1],
        [row + direction, col - 1],
    ]
    
    for attack in attackSquares:
        if validSquare(attack):
            piece = getPiece(square2num(attack), board)

            if piece not in [None, EMPTY] and pieceColour(piece) != colour:
                moves.append(square2num(attack))
        
    return moves

def pawnSpecial(sqnum, board: array, colour: str=None) -> list[tuple]:
    if colour == None: colour: str = pieceColour(getPiece(sqnum, board))
    direction: int = int(colour == 'b')*2 - 1
    moves: list = []
    
    # en passant
    row, col = num2square(sqnum)

    if len(moveLog) > 0:
        lastMove = moveLog[-1]

        if pieceType(getPiece(lastMove[1], board)) == 'P':
            lmrow1, _ = num2square(lastMove[0])
            lmrow2, lmcol2 = num2square(lastMove[1])

            coldiff = lmcol2 - col
            rowdiff = lmrow1 - lmrow2
            rightPosition = (colour == 'w' and row == 3) or (colour == 'b' and row == 4)

            if abs(coldiff) == 1 and abs(rowdiff) == 2 and rightPosition:
                moves.append((sqnum, addrow(addcol(sqnum, coldiff), direction), addcol(sqnum, coldiff)))
            
    return moves



### Main Function(s)

def isInCheck(colour: str, board: array) -> bool:
    kingSqnum: int = findKing(colour, board)
    # print(f"Black king is on sq {kingSqnum}" if colour == 'b' else f"White king is on sq {kingSqnum}")
    if kingSqnum == None: return None

    inCheck: int = isAttacked(kingSqnum, colour, board)

    # match inCheck:
    #     case 1:
    #         print('Bishop checks the king!')
    #     case 2:
    #         print('Queen checks the king!')
    #     case 3:
    #         print('Rook checks the king!')
    #     case 4:
    #         print('Knight checks the king!')
    #     case 5:
    #         print('King checks the king!')
    #     case 6:
    #         print('Pawn checks the king!')
    #     case 0:
    #         pass
    #     case _:
    #         print("Undefined behaviour!")
    #         raise TypeError
        
    return bool(inCheck)

# check if colour is under attack on sqnum
def isAttacked(sqnum: int, colour: str, board: array) -> int:
    oppColour: str = opponentColour(colour)

    # bishop/queen
    sqnums: list[int] = bishop(sqnum, board, colour=colour)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'B') in pieces: return 1
    if pieceInt(oppColour + 'Q') in pieces: return 2
    
    # roook/queen
    sqnums: list[int] = rook(sqnum, board, colour=colour)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'R') in pieces: return 3
    if pieceInt(oppColour + 'Q') in pieces: return 2
    
    # knight
    sqnums: list[int] = knight(sqnum, board, colour=colour)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'N') in pieces: return 4
    
    # king
    sqnums: list[int] = king(sqnum, board, colour=colour)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'K') in pieces: return 5

    # pawn
    sqnums: list[int] = pawn(sqnum, board, colour=colour)
    pieces: list[int] = [getPiece(sqnum, board) for sqnum in sqnums]
    if pieceInt(oppColour + 'P') in pieces: return 6
    
    return 0

# ensures user input is converted to its full representation
def getMove(move: tuple[int], specialMoves: list[tuple], board: array) -> tuple[int]:
    specialMovesSimple: list[list] = [m[:2] for m in specialMoves]
    m: tuple[int] = tuple(move)
    
    if m in specialMovesSimple:
        i: int = specialMovesSimple.index(m)
        return tuple(copy(specialMoves[i]))

    return copy(m)

def legalMove(move: tuple[int], moves: list[tuple], specialMoves: list[tuple], board: array) -> bool:
    colour: str = pieceColour(getPiece(move[0], board))

    if move[1] in moves or move in specialMoves:
        p_board = copy(board)
        
        if len(move) == 2:
            movePiece(*move, p_board)
        else:
            movePieceSpecial(move, p_board)

        inCheck: bool = isInCheck(colour, p_board)
        if inCheck == None or inCheck == True:
            return False
        
        return True
    
    return False

    # sqnum1 = sqnum2 = 0
    # verbose = True
    
    # if len(move) in [2,3]:
    #     sqnum1, sqnum2 = move[:2]
    # else:
    #     sqnum1, sqnum2 = move[2:4]

    # piece1 = getPiece(sqnum1, board)
    # piece2 = getPiece(sqnum2, board)

    # # basic legality checks
    # isEmpty:    bool = bool(piece1 == EMPTY)
    # sameColour: bool = pieceColour(piece1) == pieceColour(piece2)

    # if isEmpty or sameColour:
    #     if verbose: print("First square is empty or pieces are same colour!")
    #     return False


    # # ensure move is in possible moveset
    # inMoveSet: bool = False

    # if sqnum2 in moves:
    #     inMoveSet = True
    # elif move in specialMoves:
    #     inMoveSet = True
    

    # # ensure check does not occur post-move
    # p_board = copy(board)
    # if len(move) == 2:
    #     movePiece(*move, p_board)
    # else:
    #     movePieceSpecial(move, p_board)

    # inCheck: bool = isInCheck(pieceColour(piece1), p_board)
    # if inCheck == None:
    #     if verbose: print("Is in check after the move!")
    #     return False

    # return not any([not inMoveSet, inCheck])

def legalMoves(moves: tuple[int], allPossibleMoves: list[tuple], board: array):
    legals: list[tuple] = []

    for move in moves:
        if legalMove(move, allPossibleMoves, [], board):
            legals.append(move)

    return legals

def movePiece(sqnum1: int, sqnum2: int, board: array) -> bool:
    board[sqnum2] = getPiece(sqnum1, board)
    board[sqnum1] = EMPTY

def movePieceSpecial(move: list[int], board: array):
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
    move: tuple[int] = getMove(squares[1:3], specialMoves, board)
    
    if legalMove(move, moves, specialMoves, board):
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

def hoverLogic(buttonClicked: str, mouseSqnum: int) -> None:
    """Serialised handler for hover logic. Runs per frame"""
    hover.clear()
    g.clearLayer(g.animationLayer)

    if buttonClicked == 'ldown':
        g.clearUserStyling()
        piece: int = getPiece(mouseSqnum, board)

        if isTurn(piece, turn) and playerTurn(player):
            hover.set(piece, mouseSqnum)
            sequence.clear()
            sequence.add(buttonClicked, mouseSqnum)

def handleUserInputs(mouse_buttons: tuple[int], mouse_IJ_rel: tuple[int]) -> None:
    global gameover
    if gameover: return

    if not clickInRange(mouse_IJ_rel):
        sequence.clear()
        hover.clear()
        g.clearLayer(g.animationLayer)
        return

    buttonClicked: str = getMouseButtonStr(mouse_buttons)
    mouseSqnum: int = getMouseSqnum(mouse_IJ_rel)

    if buttonClicked == None: return

    sequence.add(buttonClicked, mouseSqnum)
    
    # manage hovering pieces
    hoverLogic(buttonClicked, mouseSqnum)
        
    if sequence.active[0] in ['lup','rup']: sequence.clear()

    if any([sequence.match(seq) for seq in sequences]):
        if sequence.active == ['ldown', 'lup']:
            piece: int = getPiece(sequence.squares[0], board)

            if piece == EMPTY or not isTurn(piece, turn) or not playerTurn(player):
                sequence.clear()
            elif sequence.squares[0] != sequence.squares[1]:
                updateGame(sequence.squares)

                sequence.clear()

        # handle arrows and highlights
        elif sequence.active == ['rdown', 'rup']:
            if sequence.squares[0] == sequence.squares[1]:
                g.addSquareHighlight(sequence.squares[0])
            else:
                g.addArrow(*sequence.squares)
            
            sequence.clear()

        # animated piece moves
        elif sequence.active == ['ldown', 'lup', 'ldown', 'lup']:
            if isTurn(getPiece(sequence.squares[0], board), turn):
                animatedMove(tuple(sequence.squares))
                promotionLogic(sequence.squares[1:3], board)

            sequence.clear()
        else:
            pass # we do not clear sequence in this case!
    else:
        sequence.clear()

def updateGame(move: tuple[int]):
    moves, specialMoves = possibleMoves(move[0], board)
    move: tuple[int] = getMove(move, specialMoves, board)

    if legalMove(move, moves, specialMoves, board):
        if len(move) == 2:
            movePiece(*move, board)
        else:
            movePieceSpecial(move, board)

        moveLog.append((move))
        promotionLogic(move, board)
        nextTurn()
    else:
        print("ILLEGAL MOVE!")




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
player: Player = Player('player','w')

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


    def getMouseRel(win_dims: tuple[int]) -> tuple[int]:
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
                handleUserInputs(p.mouse.get_pressed(), getMouseRel((win_x, win_y)))
    
    
        screen = updateGraphics(getMouseRel((win_x, win_y)))
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