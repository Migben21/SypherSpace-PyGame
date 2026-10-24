"""
breakout_scaffold.py — Build Breakout in 90 minutes
====================================================
Find every # TODO and fill it in.
Run after each phase checkpoint to see your progress.
"""

import pygame
import sys

# ── Constants ──────────────────────────────────────────────────────────
WIDTH,  HEIGHT     = 800, 600
PADDLE_W, PADDLE_H = 90, 12
BALL_SIZE           = 12
SPEED               = 6

BRICK_ROWS   = 5
BRICK_COLS   = 10
BRICK_W      = 70
BRICK_H      = 22
BRICK_PAD    = 4
BRICK_COLOUR = (70, 130, 220)

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GREY   = (80,  80,  80)
RED    = (220, 50,  50)
YELLOW = (255, 220,  40)


# ── INITIALISE ─────────────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("consolas", 26, bold=True)
big    = pygame.font.SysFont("consolas", 52, bold=True)


# ══ PHASE 6 — BUTTON CLASS ════════════════════════════════════════════
class Button:
    def __init__(self, x, y, w, h, label, colour=(60, 100, 200)):
        self.rect   = pygame.Rect(x, y, w, h)
        self.label  = label
        self.colour = colour

    def draw(self, surface, fnt):
        # TODO (Phase 6): check if mouse is hovering using collidepoint
        hovered = _______________________________________________
        # TODO (Phase 6): make a lighter colour when hovered
        c = (min(self.colour[0]+40,255),
             min(self.colour[1]+40,255),
             min(self.colour[2]+40,255)) if hovered else self.colour
        pygame.draw.rect(surface, c, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        text = fnt.render(self.label, True, WHITE)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        # TODO (Phase 6): return True if this button was left-clicked
        return (event.type == _______________ and
                event.button == 1 and
                self.rect.collidepoint(_______________))


# ── Create buttons (used in Phase 6) ──────────────────────────────────
btn_start = Button(WIDTH//2 - 100, 340, 200, 50, "START")
btn_quit  = Button(WIDTH//2 - 100, 410, 200, 50, "QUIT",
                   colour=(140, 40, 40))


# ── Brick builder ──────────────────────────────────────────────────────
def build_bricks():
    result = []
    # TODO (Phase 1): nested loop — BRICK_ROWS rows, BRICK_COLS columns
    # x = col * (BRICK_W + BRICK_PAD) + 35
    # y = row * (BRICK_H + BRICK_PAD) + 60
    # append pygame.Rect(x, y, BRICK_W, BRICK_H)
    return result


# ── Menu screen ────────────────────────────────────────────────────────
def draw_menu(surface):
    surface.fill((10, 10, 25))
    title = big.render("BREAKOUT", True, YELLOW)
    surface.blit(title, title.get_rect(center=(WIDTH//2, 160)))
    sub = font.render("LEFT / RIGHT arrows to move", True, GREY)
    surface.blit(sub, sub.get_rect(center=(WIDTH//2, 240)))
    # TODO (Phase 6): draw btn_start and btn_quit
    _______________________________________________
    _______________________________________________


# ── Reset helper ───────────────────────────────────────────────────────
def reset_game():
    return {
        "bricks"    : build_bricks(),
        "paddle_x"  : WIDTH  // 2 - PADDLE_W // 2,
        "paddle_y"  : HEIGHT - 40,
        "ball_x"    : WIDTH  // 2,
        "ball_y"    : HEIGHT // 2,
        "ball_vel_x": 4,
        "ball_vel_y": -4,
        "score"     : 0,
        "lives"     : 3,
    }


# ── Starting state ─────────────────────────────────────────────────────
state = "menu"       # "menu" | "playing" | "game_over" | "you_win"
g     = None


# ══ GAME LOOP ═════════════════════════════════════════════════════════
running = True
while running:

    # ── a) Events ─────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Restart with R key on end screens
            if event.key == pygame.K_r and state in ("game_over", "you_win"):
                g     = reset_game()
                state = "playing"

        # TODO (Phase 6): detect btn_start and btn_quit clicks on menu


        # TODO (Phase 6): detect btn_start and btn_quit clicks on end screens


    # ── b) Update ─────────────────────────────────────────────────────
    if state == "playing" and g is not None:

        keys = pygame.key.get_pressed()

        # TODO (Phase 2): move paddle left/right with arrow keys
        # TODO (Phase 2): clamp paddle_x to screen

        # TODO (Phase 3): move ball
        # TODO (Phase 3): bounce left/right walls
        # TODO (Phase 3): bounce top wall
        # TODO (Phase 3): paddle collision with colliderect()
        # TODO (Phase 3): brick collision — loop bricks[:], colliderect(), remove, bounce, score

        # TODO (Phase 4): ball exits bottom — lives, reset, game_over state

        # TODO (Phase 5): win condition — len(bricks) == 0

    # ── c) Draw ───────────────────────────────────────────────────────
    if state == "menu":
        # TODO (Phase 6): call draw_menu(screen)
        pass

    elif state == "playing" and g is not None:
        screen.fill(BLACK)

        # TODO (Phase 1): draw all bricks with a for loop
        # TODO (Phase 2): draw paddle
        # TODO (Phase 3): draw ball
        # Already provided — score and lives HUD
        screen.blit(font.render(f"Score: {g['score']}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Lives: {g['lives']}", True, WHITE), (WIDTH-130, 10))

    elif state == "game_over":
        # TODO (Phase 5): draw game-over message
        # TODO (Phase 5): draw "Press R to restart"
        screen.fill(BLACK)

    elif state == "you_win":
        # TODO (Phase 5): draw win message
        # TODO (Phase 5): draw "Press R to restart"
        screen.fill(BLACK)

    pygame.display.flip()
    clock.tick(60)


# ══ QUIT ══════════════════════════════════════════════════════════════
pygame.quit()
sys.exit()
