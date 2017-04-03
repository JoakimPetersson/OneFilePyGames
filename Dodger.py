import pygame
from pygame.locals import *
from enum import Enum
import random
import copy

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
SPAWN_SPEED = 300
ENEMY_MOVE_SPEED = 3
BORDER = 100
PLAYER_SIZE = 20
MOVE_SPEED = 5

# System
pygame.init()
pygame.font.init()
run = True
clock = pygame.time.Clock()
size = ( SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dodger")
font = pygame.font.SysFont("Arial", 20)
bigfont = pygame.font.SysFont("Arial", 72)
TICK = 60
run = True
score = 0
game_over = False
pygame.mouse.set_visible(False)

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(self.image, color, rect, 0)
        self.rect = self.image.get_rect()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(self.image, color, rect, 0)
        self.rect = self.image.get_rect()

# Events
SPAWN_EVENT = USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, SPAWN_SPEED)

# Objects
player = Player(WHITE, PLAYER_SIZE, PLAYER_SIZE)
player.rect.x = (SCREEN_WIDTH // 2)
player.rect.y = (SCREEN_HEIGHT // 2)

enemies = []

borderrect = pygame.Rect(BORDER,BORDER,GAME_AREA,GAME_AREA)

sprites = pygame.sprite.Group()
sprites.add(player)

# Main game loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if (event.type == SPAWN_EVENT) and (game_over == False):
            h = random.randint(5, 100)
            w = random.randint(5, 100)
            enemy = Enemy(RED, w, h)

            enemies.append(enemy)

            startx = random.randint(BORDER, GAME_AREA)
            enemy.rect.x = startx
            enemy.rect.y = BORDER
            sprites.add(enemy)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                run = False

            if game_over:
                if event.key == pygame.K_y:

                    player.kill()
                    del player
                    player = Player(WHITE, PLAYER_SIZE, PLAYER_SIZE)
                    player.rect.x = (SCREEN_WIDTH // 2)
                    player.rect.y = (SCREEN_HEIGHT // 2)
                    pygame.mouse.set_pos([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
                    sprites.add(player)
                    score = 0
                    ENEMY_MOVE_SPEED = 3
                    game_over = False
                    SPAWN_SPEED = 300
                    pygame.time.set_timer(SPAWN_EVENT, SPAWN_SPEED)

                    for e in enemies:
                        e.kill()
                        sprites.update()

                    del enemies[:]
                    enemies = []

                if event.key == pygame.K_n:
                    run = False

    keys = pygame.key.get_pressed()

    if not game_over:
        player.rect.center = pygame.mouse.get_pos()

        '''
        if keys[pygame.K_LEFT]:
            player.rect.move_ip(0 - MOVE_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            player.rect.move_ip(MOVE_SPEED, 0)
        if keys[pygame.K_DOWN]:
            player.rect.move_ip(0, MOVE_SPEED)
        if keys[pygame.K_UP]:
            player.rect.move_ip(0, 0 - MOVE_SPEED)
        '''


    for e in enemies:
        e.rect.y += ENEMY_MOVE_SPEED

        if player.rect.colliderect(e):
            game_over = True
            ENEMY_MOVE_SPEED = 0

        if not borderrect.contains(e.rect):
            e.kill()
            #sprites.remove(e)
            e = None
            score += 1

            if score % 20 == 0:
                ENEMY_MOVE_SPEED += 1
                SPAWN_SPEED -= 20
                pygame.time.set_timer(SPAWN_EVENT, SPAWN_SPEED)



    enemies[:] = [e for e in enemies if borderrect.contains(e.rect)]

    player.rect.clamp_ip(borderrect)
    # Drawing graphics
    screen.fill(BLACK)

    # Game border
    pygame.draw.rect(screen, WHITE, borderrect, 2)

    sprites.update()
    sprites.draw(screen)

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
