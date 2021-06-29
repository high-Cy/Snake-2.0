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
        self.position = self.position + self.direction


class SNAKE(FOOD):
    def __init__(self, food_class):
        super().__init__()
        self.head_colour = (255, 0, 0)
        self.body_colour = (255, 255, 255)
        self.positions = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = self.get_direction(food_class.position)

    def draw_snake(self):
        for pos in self.positions:
            pos_x = int(pos.x * GRID_SIZE)
            pos_y = int(pos.y * GRID_SIZE)
            pos_rect = pygame.Rect(pos_x, pos_y, GRID_SIZE, GRID_SIZE)
            if pos == self.positions[0]:
                pygame.draw.rect(screen, self.head_colour, pos_rect)
            else:
                pygame.draw.rect(screen, self.body_colour, pos_rect)

    def move_snake(self, food_position):
        self.direction = self.get_direction(food_position)

        self.positions = self.positions[:-1]
        self.positions.insert(0, self.positions[0] + self.direction)

    def get_direction(self, food_position):
        x_diff = food_position.x - self.positions[0].x
        y_diff = food_position.y - self.positions[0].y

        if abs(y_diff) > abs(x_diff):
            if y_diff <= 0:
                direction = UP
            else:
                direction = DOWN
        else:
            if x_diff <= 0:
                direction = LEFT
            else:
                direction = RIGHT

        return direction


class MAIN:
    def __init__(self):
        self.food = FOOD()
        self.snake = SNAKE(self.food)

    def update(self):
        self.food.move_food()
        self.snake.move_snake(self.food.position)

    def draw(self):
        self.snake.draw_snake()
        self.food.draw_food()


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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN:
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
