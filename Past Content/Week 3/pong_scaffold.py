"""
pong_scaffold.py — Build Pong in 90 minutes
============================================
Instructions: search for every # TODO comment and fill in the code.
Run the file after each phase to check your work.
Do NOT change anything outside a TODO block unless your teacher says so.
"""

import pygame
import sys

# ── Constants — do not change these ───────────────────────────────────
WIDTH, HEIGHT      = 800, 600
PADDLE_W, PADDLE_H = 12, 80
BALL_SIZE          = 14
SPEED              = 6

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
GREY  = (60,  60,  60)


# ══ PHASE 1 — INITIALISE ══════════════════════════════════════════════
pygame.init()

# TODO (Phase 1): create the window — 800 × 600
screen = _______________________________________________

# TODO (Phase 1): set the window title to "Pong"
________________________________________________

# TODO (Phase 1): create a clock to control frame rate
clock  = _______________________________________________

# Font for the score display (used in Phase 5)
pygame.font.init()
font = pygame.font.SysFont("consolas", 36, bold=True)


# ── Starting positions ────────────────────────────────────────────────
left_x,  left_y  = 30,          HEIGHT // 2 - PADDLE_H // 2
right_x, right_y = WIDTH - 42,  HEIGHT // 2 - PADDLE_H // 2

ball_x,     ball_y     = WIDTH // 2, HEIGHT // 2
ball_vel_x, ball_vel_y = 4, 3

left_score  = 0
right_score = 0


# ══ GAME LOOP ═════════════════════════════════════════════════════════
running = True
while running:

    # ── a) EVENTS ─────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    # ── b) UPDATE ─────────────────────────────────────────────────────

    # TODO (Phase 3a): read which keys are held down
    keys = _______________________________________________

    # TODO (Phase 3a): move left paddle with W (up) and S (down)
    if keys[_______________]: left_y  -= SPEED
    if keys[_______________]: left_y  += SPEED

    # TODO (Phase 3a): move right paddle with UP / DOWN arrow keys
    if keys[_______________]: right_y -= SPEED
    if keys[_______________]: right_y += SPEED

    # TODO (Phase 3a): clamp paddles so they can't leave the screen
    left_y  = max(0, min(left_y,  _______________))
    right_y = max(0, min(right_y, _______________))

    # TODO (Phase 3b): move the ball using its velocity variables
    ball_x _= _______________
    ball_y _= _______________

    # TODO (Phase 4): bounce ball off top and bottom walls
    if ball_y <= 0 or ball_y + BALL_SIZE >= HEIGHT:
        ball_vel_y = _______________

    # TODO (Phase 4): left paddle collision
    if (ball_x <= left_x + PADDLE_W and
            left_y <= ball_y + BALL_SIZE and
            ball_y <= left_y + PADDLE_H):
        ball_vel_x = _______________   # hint: use abs()

    # TODO (Phase 4): right paddle collision
    if (ball_x + BALL_SIZE >= right_x and
            right_y <= ball_y + BALL_SIZE and
            ball_y <= right_y + PADDLE_H):
        ball_vel_x = _______________   # hint: use -abs()

    # TODO (Phase 5): score when ball exits left — right player scores
    if ball_x + BALL_SIZE < 0:
        right_score += ___
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_vel_x = ___

    # TODO (Phase 5): score when ball exits right — left player scores
    if ball_x > WIDTH:
        left_score += ___
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_vel_x = ___


    # ── c) DRAW ───────────────────────────────────────────────────────
    screen.fill(BLACK)

    # Centre line (decorative — already done for you)
    for y in range(0, HEIGHT, 28):
        pygame.draw.rect(screen, GREY, (WIDTH // 2 - 1, y, 3, 14))

    # TODO (Phase 2): draw the left paddle
    pygame.draw.rect(screen, WHITE, (_________________________))

    # TODO (Phase 2): draw the right paddle
    pygame.draw.rect(screen, WHITE, (_________________________))

    # TODO (Phase 2): draw the ball
    pygame.draw.rect(screen, WHITE, (_________________________))

    # TODO (Phase 5): render and blit left score
    left_surf  = font.render(___________________________, True, WHITE)
    screen.blit(left_surf,  (WIDTH // 4,           20))

    # TODO (Phase 5): render and blit right score
    right_surf = font.render(___________________________, True, WHITE)
    screen.blit(right_surf, (WIDTH * 3 // 4 - 20,  20))

    pygame.display.flip()
    clock.tick(60)


# ══ QUIT ══════════════════════════════════════════════════════════════
pygame.quit()
sys.exit()
