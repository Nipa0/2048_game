# 2048 implementation using pygame

import copy
import pygame
import random

pygame.init()

# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 24)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
board_values = [[4 for _ in range(4)] for _ in range(4)]

full = False
immovable = False
spawn_new = True
initialized = 0  # responsible for the initial 2 tiles
direction = ""
score = 0
file = open("high_score", "r")  # read out the last high score from the according text file
high_score = int(file.readline())
file.close()


def draw_board():
    """Draws the background rectangle for the game board."""

    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f"Score: {score}", True, "black")
    high_score_text = font.render(f"High-Score: {high_score}", True, "black")
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))


def draw_over():
    """If the game is failed, this function will display a game over screen."""

    pygame.draw.rect(screen, "black", [50, 50, 300, 100], 0, 10)
    game_over_text = font.render("Game Over!", True, "white")
    game_over_text2 = font.render("Press Enter to Restart", True, "white")
    screen.blit(game_over_text, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# draw game tiles
def draw_values(board):
    """Draws the values of a surpassed board into the screen"""

    for i in range(4):
        for j in range(4):  # decide the color of every tile by reading out it's value and setting a new one if required
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75])  # draw the new tile
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font("freesansbold.ttf",
                                        48 - (5 * value_len))  # decide fontsize based on value length
                value_text = font.render(str(value), True, value_color)
                text_rec = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rec)
                pygame.draw.rect(screen, "black", [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


def new_piece(board):
    """Spawn a new piece on the board in a random empty tile.
    If the board is not full, the function returns false as second parameter, if it is, the function returns true."""

    if any(0 in row for row in board):  # if there is any tile in the board, which value equals 0
        optional_tiles = []
        for j in range(4):
            for i in range(4):
                if board[i][j] == 0:
                    optional_tiles.append((i, j))  # pick all tiles which value equals 0
        tile = random.choice(optional_tiles)  # choose a random tile of the optional tiles
        optional_tiles.remove(tile)
        board[tile[0]][tile[1]] = int(random.choices((2, 4), (0.9, 0.1))[0])  # pick 2 in 90% & 4 in 10% of the cases
        return board, len(optional_tiles) == 0  # return the new board, if there is a 0 left, return false
    return board, True


def move(direction, board, check_directions=True):  # check_directions is a recursion anchor for move-ability checks
    """The function takes in the direction which is pressed (up, down, left, right)
    and repositions and merges the tiles accordingly"""

    global score
    merged = [[False for _ in range(4)] for _ in range(4)]  # no piece has been merged so far
    clone = copy.deepcopy(board)  # clone the board to check if any updates have occurred afterward
    if direction == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:  # If you are not in the highest row,
                    for q in range(i):  # count the empty tiles until you reach the top in the current column
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]  # Move the current tile into the highest possible place
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:  # Check if two pieces are merge-able and weren't merged
                        board[i - shift - 1][j] *= 2  # "merge"
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direction == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]  # Move the current tile into the lowest possible place
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:  # Check if two pieces are merge-able and weren't merged
                        board[3 - i + shift][j] *= 2  # "merge"
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direction == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]  # Move the current tile into the leftest possible place
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:  # Check if two pieces are merge-able and weren't merged
                    board[i][j - shift - 1] *= 2  # "merge"
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direction == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]  # Move the current tile into the rightest possible place
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:  # Check if two pieces are merge-able and weren't merged
                        board[i][4 - j + shift] *= 2  # "merge"
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True

    immovable = False
    equal = True
    for i in range(4):
        for j in range(4):
            if board[i][j] != clone[i][j]:
                equal = False
    if equal and check_directions:
        immovable = check_other_directions(direction, board)
    if equal and not check_directions:  # Is only ever reached, when check_other_directions calls move()
        immovable = True
    return board, immovable


def check_other_directions(direction, board):  # If you couldn't move
    """helper function to the move function, checks if there's movement possible in any other direction than the current
    one, if there is no such, the function will set the immovable variable in move to true"""

    res = True
    if direction != "UP":
        res = res and move("UP", copy.deepcopy(board), False)[1]
    if direction != "DOWN":
        res = res and move("DOWN", copy.deepcopy(board), False)[1]
    if direction != "LEFT":
        res = res and move("LEFT", copy.deepcopy(board), False)[1]
    if direction != "RIGHT":
        res = res and move("RIGHT", copy.deepcopy(board), False)[1]
    return res


# game loop
running = True
while running:
    timer.tick(fps)
    screen.fill("gray")
    draw_board()
    draw_values(board_values)
    if spawn_new or initialized < 2:
        board_values, full = new_piece(board_values)
        spawn_new = False
        initialized += 1
    if direction != "":
        board_values, immovable = move(direction, board_values)
        direction = ""
        spawn_new = True
    if full and immovable:
        draw_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # red X is pressed (alt + F4)
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = "UP"
            if event.key == pygame.K_DOWN:
                direction = "DOWN"
            if event.key == pygame.K_LEFT:
                direction = "LEFT"
            if event.key == pygame.K_RIGHT:
                direction = "RIGHT"

            if full and immovable:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    initialized = 0
                    score = 0
                    direction = ""
                    full = False
                    immovable = False

    pygame.display.flip()
if score > high_score:  # write the high score to the according text file, if the last high score was cracked
    file = open("high_score", "w")
    file.write(f"{score}")
    file.close()
pygame.quit()
