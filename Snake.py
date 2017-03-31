import pygame
from pygame.locals import *
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
GRID_HEIGHT = 20
GRID_WIDTH = 20
SQUARE = SCREEN_HEIGHT // GRID_HEIGHT
SPEED = 0

# System
pygame.init()
pygame.font.init()
run = True
clock = pygame.time.Clock()
size = ( SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")
font = pygame.font.SysFont("Arial", 20)

# Game variables
score = 0
game_over = False

# Events
MOVE_EVENT = USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, SPEED)

# Game functions

# Main game loop

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

		#if event.type == DROP_EVENT and not game_over:
		#		drop()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                run = False
            if not game_over:
                if event.key == pygame.K_LEFT:
                    print("left")
                if event.key == pygame.K_RIGHT:
                    print("right")
                if event.key == pygame.K_DOWN:
                    print("down")
                if event.key == pygame.K_UP:
                    print("up")

    # Drawing graphics
    screen.fill(BLACK)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
