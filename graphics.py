
import pygame as p
from numpy import array, sqrt, degrees
from lib import *
from math import atan2


DEBUG = True


TRANSPARENT: p.Color = p.Color(0,0,0,0)
WHITE: p.Color = p.Color('azure')
BLACK: p.Color = p.Color('black')
RED:   p.Color = p.Color('red')
GREEN:   p.Color = p.Color('green')
BLUE:  p.Color = p.Color('blue')
BROWN: p.Color = p.Color('antiquewhite2')

# static screen dimensions. Constantly used but the final surface is scaled dynamically
SCREEN_HEIGHT = 800
SCREEN_DIMS = (SCREEN_HEIGHT, SCREEN_HEIGHT)
SQUARE_SIZE = SCREEN_HEIGHT // 8

# dynamic screen size
screen_height = SCREEN_HEIGHT


BOARD_COLOURS: list[tuple] = [(255,215,183), (163,108,77)]
HIGHLIGHT_PRIMARY: tuple = (255,100,100)
HIGHLIGHT_SECONDARY: tuple = (252,247,189)
HIGHLIGHT_INTENSITY = 0.8



# thinking of migrating these to a different file for relevance
def newArrow(sqnum1: int, sqnum2: int) -> p.Surface | p.Rect:
    # offsets arrow extremities this many pixels from square centre
    centreOffset: int = -40

    v1 = array(num2pos(sqnum1))
    v2 = array(num2pos(sqnum2))

    u: array[int] = v2 - v1
    umag: int = round(sqrt(u.dot(u))) + centreOffset
    angle: float = atan2(*u)

    head_x: int = SQUARE_SIZE//3
    head_y: int = SQUARE_SIZE*3//5
    body_x: int = umag - head_x
    body_y: int = SQUARE_SIZE*2//7

    # right facing arrow, points are drawn anti-clockwise from top-left
    points = array([
        (0, (head_y - body_y)//2),
        (body_x, (head_y - body_y)//2),
        (body_x, 0),
        (umag, head_y//2),
        (body_x, head_y),
        (body_x, (head_y + body_y)//2),
        (0, (head_y + body_y)//2),
    ])

    arrow = p.Surface((umag, head_y), p.SRCALPHA, 32)
    p.draw.polygon(arrow, HIGHLIGHT_SECONDARY, points)
    
    # arrow head graphics
    rotatedArrow: p.Surface = p.transform.rotate(arrow, degrees(angle) - 90)
    width: int = rotatedArrow.get_width()
    height: int = rotatedArrow.get_height()

    cent_x, cent_y = v1 + u/2
    rect = p.Rect(cent_x + (SQUARE_SIZE - width)/2, cent_y + (SQUARE_SIZE - height)/2, width, height)

    rotatedArrow.set_alpha(180)

    return rotatedArrow, rect
    
def newSquareHighlight(sqnum: int) -> p.Surface | tuple:
    highlight: p.Surface = p.Surface((SQUARE_SIZE, SQUARE_SIZE), p.SRCALPHA, 32)
    highlightColour: tuple = blendColours(getSquareColour(sqnum), HIGHLIGHT_PRIMARY, opacity=HIGHLIGHT_INTENSITY)

    pos: tuple = num2pos(sqnum)
    highlight.fill(highlightColour)

    return highlight, pos

def num2square(sqnum: int) -> tuple:
    return (sqnum // 8, sqnum % 8)

def square2num(square: tuple) -> int:
    return int(square[0]*8 + square[1])

def pos2num(pos: tuple[int]) -> int:
    row: int = pos[1] // SQUARE_SIZE
    col: int = pos[0] // SQUARE_SIZE

    assert(row in list(range(8)) and col in list(range(8)))

    return int(row*8 + col)

def num2pos(sqnum: int) -> tuple[float]:
    row, col = num2square(sqnum)
    i: int = col * SQUARE_SIZE
    j: int = row * SQUARE_SIZE

    return (i, j)

def pos2num_dyna(pos: tuple[int]) -> int:
    row: int = pos[1] // (screen_height//8)
    col: int = pos[0] // (screen_height//8)

    # assert(row in list(range(8)) and col in list(range(8)))

    return int(row*8 + col)

def num2pos_dyna(sqnum: int) -> list[int]:
    row, col = num2square(sqnum)
    i: int = col * (screen_height//8)
    j: int = row * (screen_height//8)

    return [i, j]

def squareIsDark(sqnum: int) -> bool:
    return bool(sqnum % 2)

def getSquareColour(sqnum: int) -> tuple:
    return BOARD_COLOURS[squareIsDark(sqnum)]

def arrowID(sqnum1: int, sqnum2: int) -> str:
    return str(sqnum1) + str(sqnum2)

def loadImages() -> list[p.Surface]:
    images: list[p.Surface] = []

    for code in ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]:
        images.append(loadImage(f"images/{code}.png"))

    return images



### Graphics Functions

def updateScreen(new_screen_height: int) -> p.Surface:
    clearLayer(arrowLayer)
    clearLayer(highlightsLayer)

    for highlight, rect in highlights.values(): highlightsLayer.blit(highlight, rect)
    for arrow,     rect in arrows.values():          arrowLayer.blit(arrow, rect)

    for layer in layers: win.blit(layer, (0,0))

    global screen_height
    screen_height = new_screen_height

    return p.transform.scale(win, (new_screen_height, new_screen_height))

def drawBoard(screenDims: tuple[int]) -> p.Surface:
    boardLayer: p.Surface = p.Surface(screenDims)

    # needs to be this way or the squares wont alternate colour correctly
    for row in range(8):
        for col in range(8):
            sqnum: int = int(row*8 + col)
            drawSquare(boardLayer, sqnum, BOARD_COLOURS[(row + col) % 2])

    # draw square number in the top right corner of each square
    if DEBUG:
        for i in range(64):
            ij = array(num2pos(i)) + array([SQUARE_SIZE*0.05, SQUARE_SIZE*0.85])
            drawSprite(boardLayer, textSprite(str(i), 10), ij)

    return boardLayer 

def drawSprite(layer: p.Surface, image: p.Surface, sprite_ij: tuple[int]) -> None:
    layer.blit(image, p.Rect(*sprite_ij, SQUARE_SIZE, SQUARE_SIZE))

def drawPiece(layer: p.Surface, pieceInt: int, sqnum: int) -> None:
    if pieceInt >= len(pieceImages): return
    
    row, col = num2square(sqnum)
    i = col*SQUARE_SIZE
    j = row*SQUARE_SIZE

    drawSprite(layer, pieceImages[pieceInt], (i,j))

def drawPieces(board: array) -> None:
    clearLayer(pieceLayer)

    for sqnum in range(64):
        piece = board[sqnum]
        drawPiece(pieceLayer, piece, sqnum)

def drawSquare(layer: p.Surface, sqnum: int, colour: p.Color) -> None:
    row, col = num2square(sqnum)
    i = int(col)*SQUARE_SIZE
    j = int(row)*SQUARE_SIZE

    p.draw.rect(layer, colour, p.Rect(j, i, SQUARE_SIZE, SQUARE_SIZE))

def clearUserStyling() -> None:
    highlights.clear()
    arrows.clear()

def pieceHover(pieceInt: int, target_IJ: tuple[int], mouseIJ: tuple[int]) -> None:
    if pieceInt >= len(pieceImages): return # ignore empty squares

    clearSquareIJ(pieceLayer, *target_IJ)

    scale: float = SCREEN_HEIGHT/screen_height
    [i, j] = mouseIJ
    i *= scale
    j *= scale
    offset = SQUARE_SIZE//2

    clearLayer(animationLayer)
    drawSprite(animationLayer, pieceImages[pieceInt], (i - offset, j - offset))

def clearLayer(layer: p.Surface) -> None:
    layer.fill(TRANSPARENT)

def move_animate(image: p.Surface, point1: list[int], point2: list[int], dt=0.1, numPoints=20):
    assert(False)
    #TODO: serialise this function to deprecate use of updateScreen and prevent a bloxking implementation

    direction = (p.math.Vector2(point2) - point1)/numPoints
    points = [p.math.Vector2(point1) + i*direction for i in range(numPoints)]
    frameRate = int(numPoints/dt)*2

    # hide the piece we are animating on the piece layer
    clearSquareIJ(pieceLayer, *point1)

    for i in range(numPoints):
        clearLayer(animationLayer)
        drawSprite(animationLayer, image, points[i])
        updateScreen()

        clock.tick(frameRate)

    # animation is complete so wipe all animations
    clearLayer(animationLayer)

def clearSquareIJ(layer: p.Surface, i: int, j: int) -> None:
    erase_rect = p.Rect(i, j, SQUARE_SIZE, SQUARE_SIZE)
    layer.fill(TRANSPARENT, erase_rect)

def textSprite(text: str, fontSize: int=12, colour: p.Color=BLACK, font: str='calibri') -> p.Surface:
    lines: list[str] = text.split('\n')

    sprite_X: int = max([len(l) for l in lines])*fontSize/2
    sprite_Y: int = len(lines) * (fontSize + 2)

    sprite: p.Surface = p.Surface((sprite_X, sprite_Y), p.SRCALPHA).convert_alpha()

    for i, line in enumerate(lines):
        pygameFont: p.font.Font = p.font.SysFont(font, fontSize)
        text: p.Surface = pygameFont.render(line, True, colour)

        sprite.blit(text, (0, i*fontSize + 2))

    return sprite



# Core functions

def addArrow(sqnum1: int, sqnum2: int) -> None:
    arrow, arrowRect = newArrow(sqnum1, sqnum2)
    arrID = arrowID(sqnum1, sqnum2)

    if arrID in arrows.keys():
        arrows.pop(arrID)
    else:
        arrows[arrID] = (arrow, arrowRect)

def addSquareHighlight(sqnum: int) -> None:
    highlight, pos = newSquareHighlight(sqnum)

    if sqnum in highlights.keys():
        highlights.pop(sqnum)
    else:
        highlights[sqnum] = (highlight, pos)

def init() -> None:
    global pieceImages, win, boardLayer, highlightsLayer, pieceLayer, arrowLayer, animationLayer, extrasLayer, layers

    pieceImages = loadImages()

    win = p.Surface(SCREEN_DIMS)
    boardLayer = drawBoard(SCREEN_DIMS)
    highlightsLayer = p.Surface(SCREEN_DIMS, p.SRCALPHA, 32)
    pieceLayer = p.Surface(SCREEN_DIMS, p.SRCALPHA, 32)
    arrowLayer = p.Surface(SCREEN_DIMS, p.SRCALPHA, 32)
    animationLayer  = p.Surface(SCREEN_DIMS, p.SRCALPHA, 32)
    extrasLayer  = p.Surface(SCREEN_DIMS, p.SRCALPHA, 32)

    highlightsLayer.convert_alpha()
    pieceLayer.convert_alpha()
    arrowLayer.convert_alpha()
    animationLayer.convert_alpha()

    layers = [boardLayer, highlightsLayer, pieceLayer, arrowLayer, animationLayer, extrasLayer]



pieceImages: list[p.Surface] = []
clock = p.time.Clock()
arrows: dict[str, tuple[p.Surface, p.Rect]] = {}
highlights: list[str, tuple[p.Surface, p.Rect]] = {}

win: p.Surface
boardLayer: p.Surface
highlightsLayer: p.Surface
pieceLayer: p.Surface
arrowLayer: p.Surface
animationLayer: p.Surface
extrasLayer: p.Surface

layers: list[p.Surface] = []