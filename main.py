import pygame
import sys
from pygame.math import Vector2


class FOOD:
    def __init__(self):
        self.image = pygame.image.load('img/apple.png')
        self.position = Vector2(GRID_NUM / 2, GRID_NUM - 5)
        self.direction = Vector2(0, 0)

    def draw_food(self):
        food_rect = pygame.Rect(int(self.position.x * GRID_SIZE),
                                int(self.position.y * GRID_SIZE),
                                GRID_SIZE, GRID_SIZE)
        screen.blit(self.image, food_rect)

    def move_food(self):
        new_pos = self.position + self.direction
        if 0 <= new_pos.y < GRID_NUM and 0 <= new_pos.x < GRID_NUM:
            self.position = new_pos


class SNAKE:
    def __init__(self, food_pos):
        self.head_colour = (255, 0, 0)
        self.body_colour = (255, 255, 255)
        self.positions = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = self.get_direction(food_pos)

    def draw_snake(self):
        for pos in self.positions:
            pos_x = int(pos.x * GRID_SIZE)
            pos_y = int(pos.y * GRID_SIZE)
            pos_rect = pygame.Rect(pos_x, pos_y, GRID_SIZE, GRID_SIZE)
            if pos == self.positions[0]:
                pygame.draw.rect(screen, self.head_colour, pos_rect)
            else:
                pygame.draw.rect(screen, self.body_colour, pos_rect)

    def move_snake(self, food_position, turn):
        self.direction = self.get_direction(food_position)

        if turn % 7 != 0:
            self.positions = self.positions[:-1]
            self.positions.insert(0, self.positions[0] + self.direction)
        else:
            self.positions = self.positions[:]
            self.positions.insert(0, self.positions[0] + self.direction)

    def get_direction(self, food_position):
        x_diff = food_position.x - self.positions[0].x
        y_diff = food_position.y - self.positions[0].y

        if abs(y_diff) > abs(x_diff):
            if y_diff < 0:
                preferred_direction = UP
            else:
                preferred_direction = DOWN
        else:
            if x_diff <= 0:
                preferred_direction = LEFT
            else:
                preferred_direction = RIGHT

        return preferred_direction


class MAIN:
    def __init__(self):
        self.food = FOOD()
        self.snake = SNAKE(self.food.position)
        self.score = 0
        self.lose = False

    def update(self, turn):
        self.food.move_food()
        if turn % 2 == 0:
            self.snake.move_snake(self.food.position, turn)

        self.check_collision()

    def draw(self):
        self.snake.draw_snake()
        self.food.draw_food()
        self.display_score()

    def check_collision(self):
        for snake_pos in self.snake.positions:
            if self.food.position == snake_pos:
                self.lose = True
                self.food.direction = Vector2(0, 0)

    def display_score(self):
        score_font = pygame.font.Font(None, 30)

        score = f'Score: {str(self.score)}'
        score_surface = score_font.render(score, True, (250, 250, 250))
        score_x = int(SCREEN_WIDTH - 60)
        score_y = int(SCREEN_HEIGHT - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        screen.blit(score_surface, score_rect)


pygame.init()

GRID_SIZE = 32
GRID_NUM = 20
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = GRID_SIZE * GRID_NUM, GRID_SIZE * GRID_NUM

UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

screen = pygame.display.set_mode(SIZE)

pygame.display.set_caption('Snake')
icon = pygame.image.load('img/snake.png').convert_alpha()
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game = MAIN()

i = 0
while True:
    i += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            game.update(i)

        if not game.lose and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.food.direction = UP

            if event.key == pygame.K_DOWN:
                game.food.direction = DOWN

            if event.key == pygame.K_LEFT:
                game.food.direction = LEFT

            if event.key == pygame.K_RIGHT:
                game.food.direction = RIGHT

    screen.fill((0, 0, 0))

    game.draw()

    pygame.display.update()
    clock.tick(60)
