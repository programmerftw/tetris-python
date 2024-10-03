import pygame
import random
import sys

# Define constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255),  # Cyan
]

# Define Tetrimino shapes
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1], [1, 1]],        # O shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1], [1], [1], [1]],    # I shape
    [[1, 1, 1], [1, 0, 0]],  # L shape
    [[1, 1, 1], [0, 0, 1]],  # J shape
]

def log_error(message):
    print(f"ERROR: {message}", file=sys.stderr)

class Tetris:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.next_piece()
        self.score = 0
        self.game_over = False

    def next_piece(self):
        self.current_piece = Piece()

    def rotate_piece(self):
        self.current_piece.rotate()
        if self.check_collision():
            self.current_piece.rotate()  # rotate back if collision occurs

    def move_piece(self, dx):
        self.current_piece.x += dx
        if self.check_collision():
            self.current_piece.x -= dx

    def drop_piece(self):
        self.current_piece.y += 1
        if self.check_collision():
            self.current_piece.y -= 1
            self.merge_piece()
            if self.current_piece.y < 0:
                self.game_over = True
            else:
                self.clear_lines()
                self.next_piece()

    def check_collision(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece.x + x
                    board_y = self.current_piece.y + y
                    if (board_x < 0 or board_x >= BOARD_WIDTH or
                        board_y >= BOARD_HEIGHT or
                        (board_y >= 0 and self.board[board_y][board_x])):
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_y = self.current_piece.y + y
                    board_x = self.current_piece.x + x
                    if 0 <= board_y < BOARD_HEIGHT and 0 <= board_x < BOARD_WIDTH:
                        self.board[board_y][board_x] = self.current_piece.color_index + 1
                    else:
                        log_error(f"Attempted to merge piece outside board: x={board_x}, y={board_y}")

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(row)]
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        self.score += len(lines_to_clear)

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color_index = random.randint(0, len(COLORS) - 1)
        self.color = COLORS[self.color_index]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = -len(self.shape)

    def rotate(self):
        self.shape = list(zip(*reversed(self.shape)))

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                try:
                    color = COLORS[cell - 1]
                except IndexError:
                    log_error(f"Invalid color index: {cell} at position x={x}, y={y}")
                    color = WHITE  # fallback color
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), border_radius=3)

def draw_piece(screen, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, 
                                 piece.color, 
                                 ((piece.x + x) * BLOCK_SIZE, 
                                  (piece.y + y) * BLOCK_SIZE, 
                                  BLOCK_SIZE, 
                                  BLOCK_SIZE), 
                                 border_radius=3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Tetris()

    running = True
    while running:
        screen.fill(BLACK)
        draw_board(screen, game.board)
        if game.current_piece:
            draw_piece(screen, game.current_piece)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1)
                elif event.key == pygame.K_DOWN:
                    game.drop_piece()
                elif event.key == pygame.K_UP:
                    game.rotate_piece()

        game.drop_piece()

        if game.game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()
        clock.tick(5)  # Slow down the game for debugging

    pygame.quit()

if __name__ == "__main__":
    main()