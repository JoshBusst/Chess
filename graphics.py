
import pygame as p
import numpy, copy, random, time
from lib import *
from math import sqrt, atan2 as ang



### Miscellaneous Helper Functions


### Graphics Functions

def loadImages() -> list[p.Surface]:
    images: list[p.Surface] = []

    for code in ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]:
        images.append(loadImage(f"images/{code}.png"))

    return images

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

def getSquareColour(row: int, col: int) -> tuple:
    return BOARD_COLOURS[squareIsDark(row, col)]

def drawBoard() -> None:
    for row in range(8):
        for col in range(8):
            drawSquare(boardLayer, row, col, BOARD_COLOURS[(row + col)%2])

def drawSprite(layer: p.Surface, image: p.Surface, i: int, j: int) -> None:
    layer.blit(image, p.Rect(j, i, SQUARE_SIZE, SQUARE_SIZE))

def clearSquareIJ(layer: p.Surface, i: int, j: int) -> None:
    erase_rect = p.Rect(j, i, SQUARE_SIZE, SQUARE_SIZE)
    layer.fill(TRANSPARENT, erase_rect)

def drawPiece(layer: p.Surface, pieceInt: int, row: int, col: int) -> None:
    if pieceInt >= len(pieceImages): return
    
    i = row*SQUARE_SIZE
    j = col*SQUARE_SIZE

    drawSprite(layer, pieceImages[pieceInt], i, j)

def drawPieces(board: numpy.array) -> None:
    clearLayer(pieceLayer)

    for row in range(8):
        for col in range(8):
            piece = board[row,col]
            drawPiece(pieceLayer, piece, row, col)

def drawSquare(layer: p.Surface, row: int, col: int, colour: p.Color) -> None:
    i = col*SQUARE_SIZE
    j = row*SQUARE_SIZE

    p.draw.rect(layer, colour, p.Rect(i, j, SQUARE_SIZE, SQUARE_SIZE))

def highlightSquare(row: int, col: int) -> None:
    squareColour: tuple = getSquareColour(row, col)
    highlightColour: tuple = blendColours(squareColour, HIGHLIGHT_PRIMARY, opacity=HIGHLIGHT_INTENSITY)

    drawSquare(boardLayer, row, col, highlightColour)  

def clearHighlights() -> None:
    drawBoard()

def drawArrow(square1: list[int], square2: list[int]) -> None:
    print(f"Drawing arrow from {square1} to {square2}!")
    diff_vector: numpy.array = numpy.subtract(square1, square2)
    length: float = sqrt(diff_vector.dot(diff_vector))
    angle: float = ang(diff_vector[1], diff_vector[0])
    
    # scaled_rotated_body = p.transform.rotate(p.transform.scale_by(arrowBody, (length,1)), angle)
    # rotated_head = p.transform.rotate(arrowHead, angle)

    # staticScreen.blit(rotated_head, (10,100))
    # staticScreen.blit(scaled_rotated_body, (10,10))

def updateScreen() -> None:
    for layer in layers: win.blit(layer, (0,0))
    p.display.update()

def pieceHover(pieceInt: int, row: int, col: int) -> None:
    if pieceInt >= len(pieceImages): return

    print(f"Piece {[row, col]} is hovering!")

    clearSquareIJ(pieceLayer, *square2pos(row, col))
    target_fps = 50
    keepRunning = True

    while keepRunning:
        for e in p.event.get():
            if e.type in [p.QUIT, p.MOUSEBUTTONDOWN, p.MOUSEBUTTONUP]:
                clearLayer(animationLayer)
                p.event.post(e)
                return

        [i, j] = p.mouse.get_pos()
        offset = SQUARE_SIZE/2

        clearLayer(animationLayer)
        drawSprite(animationLayer, pieceImages[pieceInt], j - offset, i - offset)
        updateScreen()

        clock.tick(target_fps)

def getArrowGraphic() -> list[p.Surface]:
    arrowBody: p.Surface = p.Surface((SQUARE_SIZE, SQUARE_SIZE/3))
    arrowBody.fill(HIGHLIGHT_SECONDARY)

    head_x: int = SQUARE_SIZE*2/3
    head_y: int = SQUARE_SIZE/2
    arrowHead: p.Surface = p.Surface((head_x, head_y), p.SRCALPHA)
    p.draw.polygon(arrowHead, HIGHLIGHT_SECONDARY, ((0,0),(0,head_y),(head_x,head_y/2),(0,0)))

    return arrowHead, arrowBody

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

p.init()

win = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
boardLayer = p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pieceLayer = p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), p.SRCALPHA, 32)
arrowLayer = p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), p.SRCALPHA, 32)
animationLayer = p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), p.SRCALPHA, 32)
blankSquare = p.Surface((SQUARE_SIZE, SQUARE_SIZE), p.SRCALPHA, 32)

pieceLayer.convert_alpha()
arrowLayer.convert_alpha()
animationLayer.convert_alpha()
blankSquare.convert_alpha()

drawBoard()

layers: list[p.Surface] = [boardLayer, pieceLayer, arrowLayer, animationLayer]