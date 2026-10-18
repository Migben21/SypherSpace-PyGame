"""
CodeBots - Term 4 - Week 1 EXTENSION scaffold (for fast finishers)
----------------------------------------------------------------------
Start from your working solution_week1.py (movement + clamping already
done), then fill in the TODOs below in order:

  STEP 1: add a target (trophy) the player can collect to WIN
  STEP 2 (bonus): add walls that block movement, turning it into a maze

Get Step 1 fully working first - test that reaching the target shows
"You win!" - before starting on Step 2.
"""

import pygame

# --- Setup -----------------------------------------------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game - reach the trophy!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 72)

BACKGROUND_COLOUR = (30, 30, 40)
PLAYER_COLOUR = (232, 113, 74)
TARGET_COLOUR = (240, 200, 80)
WALL_COLOUR = (90, 97, 110)
PLAYER_SIZE = 40
PLAYER_SPEED = 5

MAZE_MODE = False  # flip this to True once Step 1 works

player_x = 40
player_y = HEIGHT // 2

# TODO (Step 1): create target_rect - a pygame.Rect for the trophy,
# somewhere on the other side of the screen from the player, e.g.
# target_rect = pygame.Rect(WIDTH - 90, HEIGHT // 2 - 20, 40, 40)

# TODO (Step 1): add a game_won variable, starting as False

# TODO (Step 2, bonus): make a list called `walls` of pygame.Rect
# objects laid out to form a simple maze, e.g.
# walls = [
#     pygame.Rect(200, 0, 20, 400),
#     pygame.Rect(400, 200, 20, 400),
# ]


def draw_player(surface, x, y):
    pygame.draw.rect(surface, PLAYER_COLOUR, (x, y, PLAYER_SIZE, PLAYER_SIZE))


def clamp(value, lo, hi):
    return max(lo, min(value, hi))


# TODO (Step 2, bonus): write move_with_walls(rect, dx, dy, walls).
# Hint: try moving on the x-axis first - if the moved rect collides
# with any wall, cancel dx. Do the same for the y-axis with dy. Then
# apply whichever movement is left with rect.move_ip(dx, dy).
#
# def move_with_walls(rect, dx, dy, walls):
#     ...
#     return rect


# --- Game loop ---------------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # TODO: only move the player while the game hasn't been won yet
    # (hint: wrap this whole block in `if not game_won:`)

    dx = dy = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += PLAYER_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= PLAYER_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += PLAYER_SPEED

    player_x += dx
    player_y += dy
    player_x = clamp(player_x, 0, WIDTH - PLAYER_SIZE)
    player_y = clamp(player_y, 0, HEIGHT - PLAYER_SIZE)

    # TODO (Step 1): build a player_rect from player_x/player_y, then
    # check player_rect.colliderect(target_rect) - if True, set
    # game_won = True

    # TODO (Step 2, bonus): once move_with_walls() is written, use it
    # instead of the plain player_x += dx / player_y += dy lines above

    # --- Draw everything ---
    screen.fill(BACKGROUND_COLOUR)

    # TODO (Step 2, bonus): if MAZE_MODE, draw each wall in `walls`

    # TODO (Step 1): draw target_rect

    draw_player(screen, player_x, player_y)

    # TODO (Step 1): if game_won, render "You win!" text in the
    # middle of the screen with font.render(...) and screen.blit(...)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
