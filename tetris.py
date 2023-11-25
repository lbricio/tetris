import pygame
import random

game_is_running = True

FPS = 60
GRID_SIZE = 30
WIDTH = 10 * GRID_SIZE
HEIGHT = 20 * GRID_SIZE

WHITE = (155, 155, 155)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
CYAN = (100, 225, 225)
MAGENTA = (255, 100, 255)
YELLOW = (255, 255, 150)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
ORANGE = (255, 180, 100)

SHAPES = [
    [[1, 1], 
     [1, 1]],

    [[1, 1, 1], 
     [0, 1, 0], 
     [0, 0, 0]],

    [[0, 0, 0], 
     [1, 1, 0], 
     [0, 1, 1]],

    [[0, 0, 0], 
     [0, 1, 1], 
     [1, 1, 0]],

    [[0, 0, 0, 0], 
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],

    [[0, 0, 0, 0],
     [1, 1, 1, 0], 
     [1, 0, 0, 0], 
     [0, 0, 0, 0]],

    [[0, 0, 0, 0],
     [1, 1, 1, 0], 
     [0, 0, 1, 0], 
     [0, 0, 0, 0]],
]

class Piece():
    def __init__(self):
        rand_value = random.choice(range(6))
        colors = [RED, CYAN, MAGENTA, YELLOW, GREEN, BLUE, ORANGE]

        self.type = SHAPES[rand_value]
        self.color = colors[rand_value]
        self.x = WIDTH // GRID_SIZE // 2 - len(self.type[0]) // 2
        self.y = -2
        self.speed = 0.1

    def rotate(self, piece):
        return [[piece[j][i] for j in range(len(piece))] for i in range(len(piece) - 1, -1, -1)]

    def check_collision(self, current_shape, grid, new_position):
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if int(cell) == 1:
                    grid_y = int(y + new_position[1])
                    if (grid_y >= len(grid)
                            or x + new_position[0] < 0
                            or x + new_position[0] >= len(grid[0])
                            or (grid_y >= 0 and grid[grid_y][x + new_position[0]])):
                        return True
        return False

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.stack = self.create_empty_stack()
        self.current_piece = None
        self.overtime = 0

    def create_empty_stack(self):
        return [[0] * (WIDTH // GRID_SIZE) for _ in range(HEIGHT // GRID_SIZE)]

    def handle_event(self):
        if self.current_piece is None:
            self.current_piece = Piece()
        current_position = [self.current_piece.x, self.current_piece.y]
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                global game_is_running
                game_is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_position = [current_position[0] - 1, current_position[1]]
                    if not self.current_piece.check_collision(self.current_piece.type, self.stack, new_position):
                        self.current_piece.x = new_position[0]

                elif event.key == pygame.K_RIGHT:
                    new_position = [current_position[0] + 1, current_position[1]]
                    if not self.current_piece.check_collision(self.current_piece.type, self.stack, new_position):
                        self.current_piece.x = new_position[0]

                elif event.key == pygame.K_DOWN:
                    self.current_piece.speed = 0.2

                elif event.key == pygame.K_UP:
                    rotated_piece = self.current_piece.rotate(self.current_piece.type)
                    if not self.current_piece.check_collision(rotated_piece, self.stack, current_position):
                        self.current_piece.type = rotated_piece

    def game_update(self):
        new_position = [self.current_piece.x, self.current_piece.y + self.current_piece.speed]

        if not self.current_piece.check_collision(self.current_piece.type, self.stack, new_position):
            self.current_piece.x = new_position[0]
            self.current_piece.y = new_position[1]
            self.overtime = 0.5 * FPS
        elif self.overtime > 0:
            self.overtime -= 1
        else:
            # adiciona a peça ao entulho
            for y, row in enumerate(self.current_piece.type):
                for x, cell in enumerate(row):
                    if self.current_piece.type[y][x] == 1:
                        self.stack[y + int(self.current_piece.y)][x + int(self.current_piece.x)] = self.current_piece.color
            self.current_piece = None
            # destroi linhas horizontal completas
            delete_line = []
            for y, row in enumerate(self.stack):
                for x, cell in enumerate(row):
                    if cell == 0:
                        break
                    if x == len(row)-1:
                        delete_line.append(y)
            for line in delete_line:
                for y, x in enumerate(self.stack[line], -1):
                    self.stack[line][y] = 0
                # atualizar linhas acima da deletada
                for y, row in reversed(list(enumerate(self.stack))):
                    if y > 0 and y <= line:
                        self.stack[y] = self.stack[y-1]
            delete_line.clear()

    def render_screen(self):
        self.screen.fill(BLACK)

        # draw current piece
        if self.current_piece:
            for y, row in enumerate(self.current_piece.type):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.current_piece.color,
                            (x * GRID_SIZE + self.current_piece.x * GRID_SIZE,
                            (y-1) * GRID_SIZE + self.current_piece.y * GRID_SIZE,
                            GRID_SIZE, GRID_SIZE))
        # draw grid lines
        for y, row in enumerate(self.stack):
            for x, cell in enumerate(row):
                pygame.draw.rect(self.screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
        # draw block stack
        for y, row in enumerate(self.stack):
            for x, cell_color in enumerate(row):
                if cell_color:
                    pygame.draw.rect(self.screen, cell_color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        quit()

def main():
    game = Game()

    while game_is_running is True:
        game.handle_event()
        game.game_update()
        game.render_screen()
        game.clock.tick(FPS)
    game.quit()

if __name__ == "__main__":
    main()
