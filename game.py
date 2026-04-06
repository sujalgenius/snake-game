import pygame
from constants import WIDTH, HEIGHT, BLACK, WHITE, GRAY, FPS, CELL_SIZE
from snake import Snake
from food import Food
from scores import save_score, get_high_score, get_history


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
                    if event.key == pygame.K_w:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_s:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_a:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_d:
                        self.snake.change_direction((1, 0))
        return True

    def update(self):
        if self.game_over:
            return
        self.snake.move()
        if self.snake.check_collision():
            self.game_over = True
            save_score(self.score)
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
        high_text  = self.font.render(f"Best: {get_high_score()}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_text,  (WIDTH - high_text.get_width() - 10, 10))

        # Game over screen
        if self.game_over:
            history = get_history()
            high    = get_high_score()

            over_text    = self.font_large.render("GAME OVER", True, WHITE)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            high_text    = self.font.render(f"High Score: {high}", True, WHITE)
            hist_label   = self.font.render("Last 5 Scores:", True, WHITE)

            self.screen.blit(over_text,    (WIDTH // 2 - over_text.get_width()    // 2, HEIGHT // 2 - 120))
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - 60))
            self.screen.blit(high_text,    (WIDTH // 2 - high_text.get_width()    // 2, HEIGHT // 2 - 20))
            self.screen.blit(hist_label,   (WIDTH // 2 - hist_label.get_width()   // 2, HEIGHT // 2 + 30))

            for i, s in enumerate(reversed(history)):
                entry = self.font.render(f"Round {len(history) - i}: {s}", True, WHITE)
                self.screen.blit(entry, (WIDTH // 2 - entry.get_width() // 2, HEIGHT // 2 + 60 + i * 28))   

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()