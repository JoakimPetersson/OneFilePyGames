import pygame
import copy
import random
from pygame.locals import *

# Class to represent one tetromino
class Block():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.map = []

		nr = random.randint(1, 7)

		if nr == 1:
			self.map = copy.deepcopy(I_BLOCK)
		elif nr == 2:
			self.map = copy.deepcopy(O_BLOCK)
		elif nr == 3:
			self.map = copy.deepcopy(T_BLOCK)
		elif nr == 4:
			self.map = copy.deepcopy(S_BLOCK)
		elif nr == 5:
			self.map = copy.deepcopy(Z_BLOCK)
		elif nr == 6:
			self.map = copy.deepcopy(J_BLOCK)
		elif nr == 7:
			self.map = copy.deepcopy(L_BLOCK)

# Colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

# Tetrominos
I_BLOCK = [
	[0, 0, 1, 0],
	[0, 0, 1, 0],
	[0, 0, 1, 0],
	[0, 0, 1, 0]
	]

O_BLOCK = [
	[1, 1],
	[1, 1]
	]

T_BLOCK = [
	[0, 1, 0],
	[1, 1, 1],
	[0, 0, 0]]

S_BLOCK = [
	[0, 1, 1],
	[1, 1, 0],
	[0, 0, 0]]

Z_BLOCK = [
	[1, 1, 0],
	[0, 1, 1],
	[0, 0, 0]]

J_BLOCK = [
	[1, 0, 0],
	[1, 1, 1],
	[0, 0, 0]]

L_BLOCK = [
	[0, 0, 1],
	[1, 1, 1],
	[0, 0, 0]]

# Setup
SCREEN_WIDTH = 550;
SCREEN_HEIGHT = 800;
GRID_HEIGHT = 20
GRID_WIDTH = 10
SQUARE = SCREEN_HEIGHT // GRID_HEIGHT
INITIAL_DROP_TIMER = 500

# System
pygame.init()
pygame.font.init()
run = True
clock = pygame.time.Clock()
size = ( SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")


# Game variables
grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT + 2)]
DROP_EVENT = USEREVENT + 1
droptimer = INITIAL_DROP_TIMER
pygame.time.set_timer(DROP_EVENT, droptimer)
active_block = Block()
next_block = Block()
game_over = False
lines_cleared = 0
level = 0
font = pygame.font.SysFont("Arial", 20)

# Game functions
def new_block():
	global next_block
	global active_block

	next_block.x = SQUARE * 4
	next_block.y = SQUARE * -2
	active_block = next_block
	next_block = Block()
	next_block.x = (GRID_WIDTH * SQUARE) + 20
	next_block.y = SQUARE

def rotate(block):
	temp_block = copy.deepcopy(block)

	for row in range(len(block.map)):
		i = len(block.map[0]) -1
		for col in range(len(block.map[0])):
			temp_block.map[row][col] = block.map[i][row]
			i -= 1

	return temp_block

def drop():
	global active_block
	collide = False

	for row in range(len(active_block.map)):
		for col in range(len(active_block.map[0])):
			if(active_block.map[row][col] == 1):
				if (active_block.y + ((row + 1) * SQUARE)) >= SCREEN_HEIGHT:
					collide = True

	if collide or (check_board_collision(active_block, 0, 1)):
		lock_piece()
		check_lines()
		return False
	else:
		active_block.y += SQUARE
		return True

def try_move(dir_x):
	global active_block
	temp_block = copy.deepcopy(active_block)

	temp_block.x += dir_x * SQUARE

	if check_edge_collision(temp_block) or check_board_collision(temp_block, 0, 0):
		return active_block

	return temp_block


# Check if rotation is possible
def try_rotate(block):
	global active_block
	temp_block = copy.deepcopy(block)
	temp_block = rotate(temp_block)

	if (check_edge_collision(temp_block)):
		return active_block

	if (check_board_collision(temp_block, 0, 0)):
		return active_block

	return temp_block

# Check collision with edges of play area
def check_edge_collision(block):
	for row in range(len(block.map)):
		for col in range(len(block.map[0])):
			if(block.map[row][col] == 1):
				if (block.x + ((col + 1) * SQUARE)) > (GRID_WIDTH * SQUARE):
					return True
				if (block.x + (col * SQUARE)) < 0:
					return True
				if (block.y + (row * SQUARE)) > SCREEN_HEIGHT:
					return True

	return False

# Check collision with already places blocks
def check_board_collision(block, x, y):
	gridx = (block.x // SQUARE) + x
	gridy = (block.y // SQUARE) + y
	for row in range(len(block.map)):
		for col in range(len(block.map[0])):
			if(block.map[row][col] == 1):
				if (grid[gridy + row][gridx + col] ==  1):
					return True
	return False

def lock_piece():
	global active_block
	global next_block
	global game_over
	gridx = (active_block.x // SQUARE)
	gridy = (active_block.y // SQUARE)

	if active_block.y < 0:
		game_over = True
		print("Game over")

	for row in range(len(active_block.map)):
		for col in range(len(active_block.map[0])):
			if(active_block.map[row][col] == 1):
				grid[gridy + row][gridx + col] = active_block.map[row][col]

	if not game_over:
		new_block()

def check_lines():
	for row in range(len(grid)):
		counter = 0
		for col in range(len(grid[0])):
			if(grid[row][col] == 1):
				counter += 1

		if(counter == GRID_WIDTH):
			remove_line(row)

def remove_line(start_row):
	global lines_cleared, level, droptimer
	for row in range(start_row, -1, -1):
		grid[row] = grid[row-1]

	grid[0] = [0 for x in range(GRID_WIDTH)]
	lines_cleared += 1
	if(lines_cleared % 5 == 0):
		level += 1
		droptimer += -25
		pygame.time.set_timer(DROP_EVENT, droptimer)

def fast_drop():
	loop = True
	while loop:
		loop = drop()

def draw_block(block):
	blockpos_y = block.y
	for row in range(len(block.map)):
		blockpos_x = 0 + block.x
		for col in range(len(block.map[0])):
			if block.map[row][col] == 1:
				pygame.draw.rect(screen, RED, (blockpos_x, blockpos_y, SQUARE, SQUARE), 0)
			blockpos_x += SQUARE
		blockpos_y += SQUARE

# Game loop
new_block()
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == DROP_EVENT and not game_over:
				drop()

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_x:
				run = False

			if not game_over:
				if event.key == pygame.K_LEFT:
						active_block = try_move(-1)

				if event.key == pygame.K_RIGHT:
						active_block = try_move(1)

				if event.key == pygame.K_DOWN:
						drop()

				if event.key == pygame.K_UP:
						fast_drop()

				if event.key == pygame.K_LCTRL:
						active_block = try_rotate(active_block)

	linestr = "Lines: " + str(lines_cleared)
	levelstr = "Level: " + str(level)
	linetext = font.render(linestr, True, WHITE)
	leveltext = font.render(levelstr, True, WHITE)

    # Drawing graphics
	screen.fill(BLACK)

	rowpos = 0
	for row in range(GRID_HEIGHT +2):
		colpos = 0
		for col in range(GRID_WIDTH):
			if grid[row][col] == 0:
				pygame.draw.rect(screen, WHITE, (colpos, rowpos, SQUARE, SQUARE), 0)
			elif grid[row][col] == 1:
				pygame.draw.rect(screen, GREEN, (colpos, rowpos, SQUARE, SQUARE), 0)
			colpos += SQUARE
		rowpos += SQUARE

	draw_block(next_block)
	draw_block(active_block)

	screen.blit(linetext, ((GRID_WIDTH * SQUARE) + 20 , 400))
	screen.blit(leveltext, ((GRID_WIDTH * SQUARE) + 20 , 430))

	if game_over:
		bigfont = pygame.font.SysFont("Arial", 72)
		gameovertext = bigfont.render("Game Over", True, RED)
		screen.blit(gameovertext, (((GRID_WIDTH * SQUARE // 2)) - (gameovertext.get_width() // 2), ((GRID_HEIGHT * SQUARE) // 2 ) - (gameovertext.get_height() // 2)))

	pygame.display.update()
	clock.tick(60)

pygame.quit()
