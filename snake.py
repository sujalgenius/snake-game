import pygame
from constants import CELL_SIZE, GREEN, WIDTH, HEIGHT

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        # Snake starts as 3 blocks in the middle of the screen
        self.body = [
            (10, 15),
            (9,  15),
            (8,  15),
        ]
        self.direction = (1, 0)  # Moving right at start
        self.grow = False

    def change_direction(self, new_direction):
        # Prevent the snake from reversing into itself
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def move(self):
        head_x, head_y = self.body[0]
        dir_x,  dir_y  = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        self.body.insert(0, new_head)  # Add new head at front
        if not self.grow:
            self.body.pop()  # Remove tail (snake moves forward)
        else:
            self.grow = False  # Keep tail this turn (snake grows)

    def draw(self, surface):
        for segment in self.body:
            x, y = segment
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, (0, 100, 0), rect, 1)  # Dark border

    def check_collision(self):
        head = self.body[0]
        # Hit a wall?
        if not (0 <= head[0] < WIDTH // CELL_SIZE and 0 <= head[1] < HEIGHT // CELL_SIZE):
            return True
        # Hit itself?
        if head in self.body[1:]:
            return True
        return False