
import pygame as p
from numpy import array, sqrt, degrees
from lib import *
from math import atan2



# thinking of migrating these to a for relevance
def newArrow(square1: list[int], square2: list[int]) -> p.Surface | p.Rect:
    # offsets arrow extremities this many pixels from square centre
    centreOffset: int = -40

    v1 = array(square2pos(*square1))
    v2 = array(square2pos(*square2))
    
    u: array[int] = v2 - v1
    umag: int = round(sqrt(u.dot(u))) + centreOffset
    uhat: array = u/umag
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
    rotatedArrow: p.Surface = p.transform.rotate(arrow, -degrees(angle))
    width: int = rotatedArrow.get_width()
    height: int = rotatedArrow.get_height()

    cent_x, cent_y = v1 + uhat*umag/2
    rect = p.Rect(cent_y + (SQUARE_SIZE - width)/2, cent_x + (SQUARE_SIZE - height)/2, width, height)

    rotatedArrow.set_alpha(180)

    return rotatedArrow, rect
    
def newSquareHighlight(row: int, col: int) -> p.Surface | tuple:
    highlight: p.Surface = p.Surface((SQUARE_SIZE, SQUARE_SIZE), p.SRCALPHA, 32)
    highlightColour: tuple = blendColours(getSquareColour(row, col), HIGHLIGHT_PRIMARY, opacity=HIGHLIGHT_INTENSITY)

    pos = tuple(square2pos(col, row))
    highlight.fill(highlightColour)

    return highlight, pos

def pos2square(pos: tuple[int]) -> list[int]:
    row: int = pos[0] // SQUARE_SIZE
    col: int = pos[1] // SQUARE_SIZE

    return [col, row]

def square2pos(row: int, col: int) -> list[int]:
    i: int = row * SQUARE_SIZE
    j: int = col * SQUARE_SIZE

    return [i, j]

def squareIsDark(row: int, col: int) -> bool:
    return not(even(row) == even(col))

def squareNumber(row: int, col: int) -> int:
    return row*8 + col

def getSquareColour(row: int, col: int) -> tuple:
    return BOARD_COLOURS[squareIsDark(row, col)]



### Miscellaneous Helper Functions

def loadImages() -> list[p.Surface]:
    images: list[p.Surface] = []

    for code in ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]:
        images.append(loadImage(f"images/{code}.png"))

    return images

def arrowID(square1: list[int], square2: list[int]) -> str:
    return str(squareNumber(*square1)) + str(squareNumber(*square2))



### Graphics Functions

def updateScreen() -> None:
    drawUserStyling()

    for layer in layers: win.blit(layer, (0,0))
    p.display.update()

def drawBoard() -> None:
    for row in range(8):
        for col in range(8):
            drawSquare(boardLayer, row, col, BOARD_COLOURS[(row + col)%2])

def drawSprite(layer: p.Surface, image: p.Surface, i: int, j: int) -> None:
    layer.blit(image, p.Rect(j, i, SQUARE_SIZE, SQUARE_SIZE))

def drawPiece(layer: p.Surface, pieceInt: int, row: int, col: int) -> None:
    if pieceInt >= len(pieceImages): return
    
    i = row*SQUARE_SIZE
    j = col*SQUARE_SIZE

    drawSprite(layer, pieceImages[pieceInt], i, j)

def drawPieces(board: array) -> None:
    clearLayer(pieceLayer)

    for row in range(8):
        for col in range(8):
            piece = board[row,col]
            drawPiece(pieceLayer, piece, row, col)

def drawSquare(layer: p.Surface, row: int, col: int, colour: p.Color) -> None:
    i = col*SQUARE_SIZE
    j = row*SQUARE_SIZE

    p.draw.rect(layer, colour, p.Rect(i, j, SQUARE_SIZE, SQUARE_SIZE))

def drawUserStyling() -> None:
    clearLayer(arrowLayer)
    clearLayer(highlightsLayer)

    for highlight, rect in highlights.values(): highlightsLayer.blit(highlight, rect)
    for arrow,     rect in arrows.values():          arrowLayer.blit(arrow,     rect)

def clearUserStyling() -> None:
    highlights.clear()
    arrows.clear()

def pieceHover(pieceInt: int, target_IJ: tuple[int]) -> None:
    if pieceInt >= len(pieceImages): return # ignore empty squares

    clearSquareIJ(pieceLayer, *target_IJ)

    [i, j] = p.mouse.get_pos()
    offset = SQUARE_SIZE/2

    clearLayer(animationLayer)
    drawSprite(animationLayer, pieceImages[pieceInt], j - offset, i - offset)

def clearLayer(layer: p.Surface) -> None:
    layer.fill(TRANSPARENT)

def move_animate(image: p.Surface, point1: list[int], point2: list[int], dt=0.1, numPoints=20):
    direction = (p.math.Vector2(point2) - point1)/numPoints
    points = [p.math.Vector2(point1) + i*direction for i in range(numPoints)]
    frameRate = int(numPoints/dt)*2

    # hide the piece we are animating on the piece layer
    clearSquareIJ(pieceLayer, *point1)

    for i in range(numPoints):
        clearLayer(animationLayer)
        drawSprite(animationLayer, image, *points[i])
        updateScreen()

        clock.tick(frameRate)

    # animation is complete so wipe all animations
    clearLayer(animationLayer)

def clearSquareIJ(layer: p.Surface, i: int, j: int) -> None:
    erase_rect = p.Rect(j, i, SQUARE_SIZE, SQUARE_SIZE)
    layer.fill(TRANSPARENT, erase_rect)



# Core functions

def addArrow(square1: list[int], square2: list[int]) -> None:
    arrow, arrowRect = newArrow(square1, square2)
    arrID = arrowID(square1, square2)

    if arrID in arrows.keys():
        arrows.pop(arrID)
    else:
        arrows[arrID] = (arrow, arrowRect)

def addSquareHighlight(row: int, col: int) -> None:
    highlight, pos = newSquareHighlight(row, col)
    squareID = squareNumber(row, col)

    if squareID in highlights.keys():
        highlights.pop(squareID)
    else:
        highlights[squareID] = (highlight, pos)





SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SQUARE_SIZE = int(SCREEN_HEIGHT // 8)

BOARD_COLOURS: list[tuple] = [(255,215,183), (163,108,77)]
HIGHLIGHT_PRIMARY: tuple = (255,100,100)
HIGHLIGHT_SECONDARY: tuple = (252,247,189)
HIGHLIGHT_INTENSITY = 0.8
TRANSPARENT: p.Color = p.Color(0,0,0,0)

pieceImages: list[p.Surface] = loadImages()
clock = p.time.Clock()
arrows: dict[str, tuple[p.Surface, p.Rect]] = {}
highlights: list[str, tuple[p.Surface, p.Rect]] = {}

p.init()

win = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
boardLayer =      p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
highlightsLayer = p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), p.SRCALPHA, 32)
pieceLayer =      p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), p.SRCALPHA, 32)
arrowLayer =      p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), p.SRCALPHA, 32)
animationLayer =  p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), p.SRCALPHA, 32)
# blankSquare = p.Surface((SQUARE_SIZE, SQUARE_SIZE), p.SRCALPHA, 32)

highlightsLayer.convert_alpha()
pieceLayer.convert_alpha()
arrowLayer.convert_alpha()
animationLayer.convert_alpha()
# blankSquare.convert_alpha()

# drawBoard()

layers: list[p.Surface] = [boardLayer, highlightsLayer, pieceLayer, arrowLayer, animationLayer]