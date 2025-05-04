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

def draw_numbers():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            num = user_board[y][x]
            if num != 0:
                color = BLACK if board[y][x] != 0 else BLUE
                txt = font.render(str(num), True, color)
                screen.blit(txt, (x * CELL_SIZE + 20, y * CELL_SIZE + 10))

def draw_selection():
    x, y = selected
    pygame.draw.rect(screen, LIGHTBLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_timer():
    elapsed = int(time.time() - start_time)
    mins, secs = divmod(elapsed, 60)
    timer_text = small_font.render(f"Час: {mins:02}:{secs:02}", True, BLACK)
    screen.blit(timer_text, (WIDTH - 140, HEIGHT - 90))

def draw_check_button(hover=False):
    button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 70, 150, 40)
    color = (70, 70, 70) if hover else DARKGREY
    pygame.draw.rect(screen, color, button_rect, border_radius=8)
    text = small_font.render("Перевірити", True, WHITE)
    screen.blit(text, (button_rect.x + 25, button_rect.y + 8))
    return button_rect

def draw_message():
    if message:
        msg_surface = small_font.render(message, True, GREEN if "успішна" in message else RED)
        screen.blit(msg_surface, (20, HEIGHT - 130))

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_x = col // 3 * 3
    box_y = row // 3 * 3
    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if board[i][j] == num:
                return False
    return True

def generate_board(difficulty):
    from copy import deepcopy

    def fill_board(b):
        nums = list(range(1, 10))
        for y in range(9):
            for x in range(9):
                if b[y][x] == 0:
                    random.shuffle(nums)
                    for n in nums:
                        if is_valid(b, y, x, n):
                            b[y][x] = n
                            if fill_board(b):
                                return True
                            b[y][x] = 0
                    return False
        return True

    board = [[0] * 9 for _ in range(9)]
    fill_board(board)
    puzzle = deepcopy(board)

    if difficulty == "easy":
        empties = 35
    elif difficulty == "medium":
        empties = 45
    else:
        empties = 55

    while empties:
        y, x = random.randint(0, 8), random.randint(0, 8)
        if puzzle[y][x] != 0:
            puzzle[y][x] = 0
            empties -= 1

    return puzzle, board

def draw_menu(selected_option):
    screen.fill(WHITE)
    title = large_font.render("Вибери рівень", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    options = ["Легкий", "Середній", "Складний"]
    for i, text in enumerate(options):
        color = BLUE if i == selected_option else DARKGREY
        txt = font.render(text, True, color)
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 200 + i * 70))

    pygame.display.flip()

def show_difficulty_menu():
    option = 0
    while True:
        draw_menu(option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option = (option - 1) % 3
                elif event.key == pygame.K_DOWN:
                    option = (option + 1) % 3
                elif event.key == pygame.K_RETURN:
                    return ["easy", "medium", "hard"][option]

difficulty = show_difficulty_menu()
board, solution = generate_board(difficulty)
user_board = [[board[y][x] for x in range(9)] for y in range(9)]

running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    draw_selection()
    draw_numbers()
    draw_timer()

    mouse_pos = pygame.mouse.get_pos()
    hovering = False
    check_button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 70, 150, 40)
    if check_button_rect.collidepoint(mouse_pos):
        hovering = True

    check_button_rect = draw_check_button(hovering)
    draw_message()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if mx < WIDTH and my < WIDTH:
                selected = (mx // CELL_SIZE, my // CELL_SIZE)
            elif check_button_rect.collidepoint(mx, my):
                if user_board == solution:
                    message = "Перевірка успішна!"
                else:
                    message = "Є помилки!"

        elif event.type == pygame.KEYDOWN:
            x, y = selected
            if board[y][x] == 0:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    user_board[y][x] = 0
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    if is_valid(user_board, y, x, num):
                        user_board[y][x] = num

pygame.quit()
sys.exit()
