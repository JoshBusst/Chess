
import pygame as p
import numpy, copy, random, time
from lib import *
from math import sqrt, cos, sin, atan2
from numpy import degrees



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
    [body_i, body_j] = square2pos(*square1)
    [head_i, head_j] = square2pos(*square2)
    
    # Calculate the angle of the line
    angle = atan2(body_i - head_i, body_j - head_j)
    width = 30

    # Find the perpendicular vector to the line
    perp_x = sin(angle) * width / 2
    perp_y = -cos(angle) * width / 2

    v1 = numpy.array((body_i, body_j))
    v2 = numpy.array((head_i, head_j))

    offset = 40

    u = v2 - v1
    umag = numpy.sqrt(u.dot(u))
    uhat = u/umag

    start = v1 + offset*uhat + SQUARE_SIZE/2
    end = v2 - offset*uhat + SQUARE_SIZE/2

    # Calculate the four corners of the rectangle (thick line)
    points = numpy.array([
        (start[1] - perp_x, start[0] - perp_y),  # Corner 1
        (start[1] + perp_x, start[0] + perp_y),  # Corner 2
        (end[1] + perp_x, end[0] + perp_y),      # Corner 3
        (end[1] - perp_x, end[0] - perp_y)       # Corner 4
    ])

    # points = points + SQUARE_SIZE/2
    
    head_x: int = SQUARE_SIZE*2/6
    head_y: int = SQUARE_SIZE/3
    arrowHead: p.Surface = p.Surface((head_x, head_y), p.SRCALPHA)
    p.draw.polygon(arrowHead, HIGHLIGHT_SECONDARY, ((0,0),(0,head_y),(head_x,head_y/2),(0,0)))

    # Draw the polygon (rectangle) to represent the thick line
    p.draw.polygon(arrowLayer, HIGHLIGHT_SECONDARY, points)
    rotated_head = p.transform.rotate(arrowHead, 180 - degrees(angle))
    head_rect = rotated_head.get_rect(center=(head_j + SQUARE_SIZE/2, head_i + SQUARE_SIZE/2))

    
    arrowLayer.blit(rotated_head, head_rect)
    # arrowLayer.blit(rotated_body, body_rect)

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
arrowHead, arrowBody = getArrowGraphic()
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