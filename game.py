import pygame
from constants import WIDTH, HEIGHT, BLACK, WHITE, GRAY, FPS, CELL_SIZE
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font       = pygame.font.SysFont("Arial", 24)
        self.font_large = pygame.font.SysFont("Arial", 48)
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food  = Food()
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset()
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
        return True

    def update(self):
        if self.game_over:
            return
        self.snake.move()
        if self.snake.check_collision():
            self.game_over = True
            return
        # Did the snake eat the food?
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.score += 1
            self.food.spawn()
            # Make sure food doesn't spawn on the snake
            while self.food.position in self.snake.body:
                self.food.spawn()

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.food.draw(self.screen)
        self.snake.draw(self.screen)

        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Game over screen
        if self.game_over:
            over_text    = self.font_large.render("GAME OVER", True, WHITE)
            restart_text = self.font.render(f"Score: {self.score}   |   Press R to restart", True, WHITE)
            self.screen.blit(over_text,    (WIDTH // 2 - over_text.get_width()    // 2, HEIGHT // 2 - 60))
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()