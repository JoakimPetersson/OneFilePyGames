import pygame
from pygame.locals import *
from enum import Enum
import random
import copy

# TODO
# Set speed value

# Colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

# "Constants"
SCREEN_WIDTH = 800;
SCREEN_HEIGHT = 800;
GAME_AREA = 600
GRID_SIZE = 60
SQUARE_SIDE = GAME_AREA // GRID_SIZE
SPEED = 75
BORDER = 100

# System
pygame.init()
pygame.font.init()
run = True
clock = pygame.time.Clock()
size = ( SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")
font = pygame.font.SysFont("Arial", 20)
bigfont = pygame.font.SysFont("Arial", 72)
TICK = 60
run = True


# Events
MOVE_EVENT = USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, SPEED)

# Grid System
class Pos():
    def __init__(self, x, y):
        self.x = x
        self.y = y

grid = [[(0,0) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
tempx = BORDER
tempy = BORDER
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        grid[row][col] = Pos(tempx, tempy)
        tempx += SQUARE_SIDE
    tempy += SQUARE_SIDE
    tempx = BORDER

STARTPOS = Pos((GRID_SIZE // 2), (GRID_SIZE // 2))

def get_x(x, y):
    return grid[y][x].x

def get_y(x, y):
    return grid[y][x].y

def get_random_pos():
    rand_x = random.randint(0, GRID_SIZE -1)
    rand_y = random.randint(0, GRID_SIZE -1)

    return Pos(rand_x, rand_y)

# Game variables
score = 0
game_over = False

# Classes
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Food(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.pos = get_random_pos()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(self.image, color, rect, 0)
        self.rect = self.image.get_rect()
        self.rect.x = get_x(self.pos.x, self.pos.y)
        self.rect.y = get_y(self.pos.x, self.pos.y)

    def RespawnFood(self):
        self.pos = get_random_pos()
        self.rect.x = get_x(self.pos.x, self.pos.y)
        self.rect.y = get_y(self.pos.x, self.pos.y)

class BodySegment(pygame.sprite.Sprite):
    def __init__(self, color, width, height, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(self.image, color, rect, 0)
        self.rect = self.image.get_rect()
        self.rect.x = get_x(self.pos.x, self.pos.y)
        self.rect.y = get_y(self.pos.x, self.pos.y)

class Head(pygame.sprite.Sprite):
    def __init__(self, color, width, height, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(self.image, color, rect, 0)
        self.rect = self.image.get_rect()
        self.rect.x = get_x(self.pos.x, self.pos.y)
        self.rect.y = get_y(self.pos.x, self.pos.y)

class Snake():
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.length = 0
        self.head = Head(WHITE, SQUARE_SIDE, SQUARE_SIDE, copy.deepcopy(STARTPOS))
        self.body = []
        self.food = Food(WHITE, SQUARE_SIDE, SQUARE_SIDE)

        self.sprites.add(self.food)
        self.sprites.add(self.head)

        for idx in range(0, 4, 1):
            self.body.append(BodySegment(WHITE, SQUARE_SIDE, SQUARE_SIDE, Pos(self.head.pos.x, self.head.pos.y - idx)))
            self.sprites.add(self.body[idx - 1])

        self.dir = Direction.DOWN

    def move(self, direction, auto):
        allowmove = False
        oldpos = copy.deepcopy(self.head.pos)
        global game_over

        if (auto == 0) and (self.dir == direction):
            return

        if(direction == Direction.LEFT) and not (self.dir == Direction.RIGHT) :
            self.head.pos.x -= 1
            allowmove = True
        if(direction == Direction.RIGHT) and not (self.dir == Direction.LEFT):
            self.head.pos.x += 1
            allowmove = True
        if(direction == Direction.UP) and not (self.dir == Direction.DOWN):
            self.head.pos.y -= 1
            allowmove = True
        if(direction == Direction.DOWN) and not (self.dir == Direction.UP):
            self.head.pos.y += 1
            allowmove = True

        if((self.head.pos.x < 0) or (self.head.pos.x > (GRID_SIZE - 1))) or ((self.head.pos.y < 0) or (self.head.pos.y > (GRID_SIZE - 1))):
            game_over = True
        elif allowmove:

            for seg in self.body:
                if (seg.pos.x == self.head.pos.x) and (seg.pos.y == self.head.pos.y):
                    game_over = True
                    return

            if(self.head.pos.x == self.food.pos.x) and (self.head.pos.y == self.food.pos.y):
                global score
                score += 1
                self.body.insert(0, BodySegment(WHITE, SQUARE_SIDE, SQUARE_SIDE, oldpos))
                self.sprites.add(self.body[0])

                self.head.rect.x = get_x(self.head.pos.x, self.head.pos.y)
                self.head.rect.y = get_y(self.head.pos.x, self.head.pos.y)
                self.food.RespawnFood()
                self.dir = direction

            else:
                self.dir = direction

                self.body[0].rect.x = self.head.rect.x
                self.body[0].rect.y = self.head.rect.y
                self.body[0].pos.x = self.head.pos.x
                self.body[0].pos.y = self.head.pos.y

                self.head.rect.x = get_x(self.head.pos.x, self.head.pos.y)
                self.head.rect.y = get_y(self.head.pos.x, self.head.pos.y)

                for idx in range(len(self.body) -1, 0, -1):
                    self.body[idx].rect.x = self.body[idx - 1].rect.x
                    self.body[idx].rect.y = self.body[idx - 1].rect.y
                    self.body[idx].pos.x = self.body[idx -1].pos.x
                    self.body[idx].pos.y = self.body[idx -1].pos.y




    def draw_snake(self, screen):
        self.sprites.update()
        self.sprites.draw(screen)



# Objects
snake = Snake()

# Main game loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if (event.type == MOVE_EVENT) and (game_over == False):
            snake.move(snake.dir, 1)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                run = False
            if not game_over:
                if event.key == pygame.K_LEFT:
                    snake.move(Direction.LEFT, 0)
                if event.key == pygame.K_RIGHT:
                    snake.move(Direction.RIGHT, 0)
                if event.key == pygame.K_DOWN:
                    snake.move(Direction.DOWN, 0)
                if event.key == pygame.K_UP:
                    snake.move(Direction.UP, 0)
            if game_over:
                if event.key == pygame.K_y:
                    del snake.head
                    del snake.body
                    snake = Snake()
                    score = 0
                    game_over = False
                if event.key == pygame.K_n:
                    run = False


    # Drawing graphics
    screen.fill(BLACK)

    # Game border
    rect = pygame.Rect(BORDER,BORDER,GAME_AREA,GAME_AREA)
    pygame.draw.rect(screen, WHITE, rect, 2)

    #rect = pygame.Rect(get_x(STARTPOS.x, STARTPOS.y), get_y(STARTPOS.x, STARTPOS.y), SQUARE_SIDE,SQUARE_SIDE)
    #pygame.draw.rect(screen, WHITE, rect, 0)

    snake.draw_snake(screen)
    scorestring = "Score: " + str(score)
    scoretext = font.render(scorestring, True, WHITE)
    screen.blit(scoretext, (((SCREEN_WIDTH // 2) - (scoretext.get_width() // 2)), ((BORDER // 2) + scoretext.get_height())))

    if game_over:
        gameovertext = bigfont.render("Game Over", True, WHITE)
        gameoversubtext = font.render("Play again? Y/N", True, WHITE)
        screen.blit(gameovertext, ((SCREEN_WIDTH // 2) - (gameovertext.get_width() // 2), (SCREEN_HEIGHT // 2 ) - (gameovertext.get_height() // 2)))
        screen.blit(gameoversubtext, ((SCREEN_WIDTH // 2) - (gameoversubtext.get_width() // 2), ((SCREEN_HEIGHT // 2 ) + (gameovertext.get_height() // 2))))

    pygame.display.update()
    clock.tick(TICK)

pygame.quit()
