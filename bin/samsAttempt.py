import pygame
import main

# Initialize pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
FPS = 60
COLORS = [pygame.Color("white"), pygame.Color("gray")]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess AI")

# Load images from the ImagesChess folder
def load_images():
    pieces = {}
    # Load each piece image from the ImagesChess folder, scaled to fit the square size
    for name in ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]:
        pieces[name] = pygame.transform.scale(pygame.image.load(f"images/{name}.png"), (SQUARE_SIZE, SQUARE_SIZE))
    return pieces

pieces = load_images()

# Function to draw the chess board
def draw_board(screen):
    for r in range(8):
        for c in range(8):
            color = COLORS[(r + c) % 2]
            pygame.draw.rect(screen, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw the pieces on the board
def draw_pieces(screen, board):
    for square in main.SQUARES:
        piece = board.piece_at(square)
        if piece:
            column, row = main.square_file(square), main.square_rank(square)
            # Determine the name of the piece to find the correct image
            piece_name = f"{('w' if piece.color == main.WHITE else 'b')}{piece.symbol().upper()}"
            screen.blit(pieces[piece_name], (column * SQUARE_SIZE, (7 - row) * SQUARE_SIZE))

# Main function to handle the game loop
def main():
    clock = pygame.time.Clock()
    board = main.Board()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(screen)
        draw_pieces(screen, board)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()