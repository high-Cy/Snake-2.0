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
        self.head_colour = GREEN
        self.body_colour = WHITE
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
            elif y_diff >= 0 and self.direction != UP:
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
        self.draw_borders()
        self.display_score()

    def check_collision(self):
        for snake_pos in self.snake.positions:
            if self.food.position == snake_pos:
                self.lose = True
                self.food.direction = Vector2(0, 0)

        if self.border1 > self.food.position.y or \
                self.food.position.y >= self.border2 or \
                self.border1 > self.food.position.x or \
                self.food.position.x >= self.border2:
            self.lose = True

        if not self.lose and turn % self.score_turn == 0:
            self.score += 1

    def shrink_display(self):
        if self.border1 <= 5:
            self.border1 += 1
            self.border2 -= 1

    def draw_borders(self):
        for i in range(self.border1):
            i = i * GRID_SIZE
            pygame.draw.rect(screen, GREY, [i, 0, GRID_SIZE, SCREEN_HEIGHT])
            pygame.draw.rect(screen, GREY, [0, i, SCREEN_WIDTH, GRID_SIZE])

        for j in range(self.border2, GRID_NUM):
            j = j * GRID_SIZE
            pygame.draw.rect(screen, GREY, [j, 0, GRID_SIZE, SCREEN_HEIGHT])
            pygame.draw.rect(screen, GREY, [0, j, SCREEN_WIDTH, GRID_SIZE])

    def display_score(self):
        score_font = pygame.font.Font(None, 30)

        score = f'Score: {str(self.score), str(self.border1)}'
        score_surface = score_font.render(score, True, WHITE)
        score_x = int(SCREEN_WIDTH - 60)
        score_y = int(SCREEN_HEIGHT - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        screen.blit(score_surface, score_rect)

    @staticmethod
    def game_over_menu():
        lose_font = pygame.font.Font(None, 60)
        lose_surface = lose_font.render('GAME OVER!', True, RED)
        lose_x = int(SCREEN_WIDTH / 2)
        lose_y = int(SCREEN_HEIGHT / 2 - 2 * GRID_SIZE)
        lose_rect = lose_surface.get_rect(center=(lose_x, lose_y))

        restart_font = pygame.font.Font(None, 32)
        restart_surface = restart_font.render('Restart with Spacebar', True,
                                              WHITE)
        restart_x = lose_x
        restart_y = lose_y + 2 * GRID_SIZE
        restart_rect = restart_surface.get_rect(center=(restart_x, restart_y))

        bg_rect = pygame.Rect(restart_rect.left - 5, restart_rect.top - 5,
                              restart_rect.width + 10, restart_rect.height + 5)

        pygame.draw.rect(screen, GREY, bg_rect)
        screen.blit(restart_surface, restart_rect)
        screen.blit(lose_surface, lose_rect)

    def reset(self):
        self.food.position = Vector2(GRID_NUM / 2, GRID_NUM - 5)
        self.snake.positions = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.snake.direction = Vector2(1, 0)
        self.score = 0
        self.border1 = 0
        self.border2 = GRID_NUM
        self.lose = False


# --- Constants ----------------------------------------------------------------
MILLI = 1000

GRID_SIZE = 32
GRID_NUM = 20
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = GRID_SIZE * GRID_NUM, GRID_SIZE * GRID_NUM

GREY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (144, 238, 144)

UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

T1 = 1
T2 = 2

# ------------------------------------------------------------------------------

pygame.init()

screen = pygame.display.set_mode(SIZE)

pygame.display.set_caption('Snake')
icon = pygame.image.load('img/snake.png').convert_alpha()
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

SHRINK_TIME = 10 * MILLI
SHRINK_DISPLAY = pygame.USEREVENT + 1
pygame.time.set_timer(SHRINK_DISPLAY, SHRINK_TIME)

game = MAIN(T1, T2)

turn = 0
while True:
    turn += 1
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game.lose:
            if event.type == SCREEN_UPDATE:
                game.update()

            if event.type == SHRINK_DISPLAY:
                game.shrink_display()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.food.direction = UP

                if event.key == pygame.K_DOWN:
                    game.food.direction = DOWN

                if event.key == pygame.K_LEFT:
                    game.food.direction = LEFT

                if event.key == pygame.K_RIGHT:
                    game.food.direction = RIGHT

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.reset()

    screen.fill(BLACK)

    game.draw()

    if game.lose:
        game.game_over_menu()

    pygame.display.update()
