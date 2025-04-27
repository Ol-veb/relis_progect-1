import pygame
import sys
import time
import random

WIDTH, HEIGHT = 600, 700
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (173, 216, 230)
GREY = (200, 200, 200)
DARKGREY = (100, 100, 100)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Судоку")
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)

selected = (0, 0)
start_time = time.time()
message = ""

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GREY, rect, 1)

    for i in range(10):
        width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), width)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), width)
