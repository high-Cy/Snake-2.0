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

    def move_food(self, border1, border2):
        new_pos = self.position + self.direction
        if border1 <= new_pos.y < border2 and border1 <= new_pos.x < border2:
            self.position = new_pos


class SNAKE:
    def __init__(self):
        self.head_colour = (255, 0, 0)
        self.body_colour = (255, 255, 255)
        self.positions = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

    def draw_snake(self):
        for pos in self.positions:
            pos_x = int(pos.x * GRID_SIZE)
            pos_y = int(pos.y * GRID_SIZE)
            pos_rect = pygame.Rect(pos_x, pos_y, GRID_SIZE, GRID_SIZE)
            if pos == self.positions[0]:
                pygame.draw.rect(screen, self.head_colour, pos_rect)
            else:
                pygame.draw.rect(screen, self.body_colour, pos_rect)

    def move_snake(self, food_position, score_turn):
        global turn
        self.get_direction(food_position)

        if turn % score_turn != 0:
            self.positions = self.positions[:-1]
            self.positions.insert(0, self.positions[0] + self.direction)
        else:
            self.positions = self.positions[:]
            self.positions.insert(0, self.positions[0] + self.direction)

    def get_direction(self, food_position):
        x_diff = food_position.x - self.positions[0].x
        y_diff = food_position.y - self.positions[0].y

        if abs(y_diff) > abs(x_diff):
            if y_diff < 0 and self.direction != DOWN:
                self.direction = UP
            elif y_diff >=0 and self.direction != UP:
                self.direction = DOWN
            else:
                self.direction = RIGHT
        else:
            if x_diff <= 0 and self.direction != RIGHT:
                self.direction = LEFT
            elif x_diff > 0 and self.direction != LEFT:
                self.direction = RIGHT
            else:
                self.direction = DOWN


class MAIN:
    def __init__(self, t1, t2):
        self.food = FOOD()
        self.snake = SNAKE()
        self.score = 0
        self.score_turn = 7
        self.snake_turn = [t1, t2]  # snake moves 1 out of 2 times
        self.sped_up = False
        self.lose = False
        self.border1 = 0
        self.border2 = GRID_NUM

    def update(self):
        self.food.move_food(self.border1, self.border2)
        if turn % self.snake_turn[1] < self.snake_turn[0]:
            self.snake.move_snake(self.food.position, self.score_turn)

        self.check_collision()

    def draw(self):
        self.snake.draw_snake()
        self.food.draw_food()
        self.display_score()

    def check_collision(self):
        for snake_pos in self.snake.positions:
            if self.food.position == snake_pos:
                # self.lose = True
                self.food.direction = Vector2(0, 0)

        if not self.lose and turn % self.score_turn == 0:
            self.score += 1
            self.sped_up = False

    def shrink_display(self):
        if self.border1 <= 5:
            self.border1 += 1
            self.border2 -= 1

    def display_score(self):
        score_font = pygame.font.Font(None, 30)

        score = f'Score: {str(self.score), str(self.snake_turn[0])}'
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

T1 = 1
T2 = 2

MILLI = 1000
screen = pygame.display.set_mode(SIZE)

pygame.display.set_caption('Snake')
icon = pygame.image.load('img/snake.png').convert_alpha()
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
SPEEDUP_SNAKE = pygame.USEREVENT + 1
SLOWDOWN_SNAKE = pygame.USEREVENT + 2
SHRINK_DISPLAY = pygame.USEREVENT + 3
pygame.time.set_timer(SCREEN_UPDATE, 150)
pygame.time.set_timer(SHRINK_DISPLAY, 1*MILLI)

game = MAIN(T1, T2)

turn = 0
while True:
    turn += 1
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            game.update()

        if event.type == SHRINK_DISPLAY:
            game.shrink_display()

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
