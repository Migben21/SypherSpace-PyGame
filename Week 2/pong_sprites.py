"""
pong_sprites.py  —  Pong reimplemented with sprites & images
=============================================================

What this adds over the basic Pong:
  • Loading PNG images with pygame.image.load() + .convert_alpha()
  • Blitting sprites instead of drawing shapes
  • A tiled/scaled background image
  • pygame.transform.scale() to resize loaded images
  • A glow/trail effect using a translucent overlay surface
  • An animated "flash" effect on score using sprite scaling
  • Graceful fallback: if image files are missing, draws coloured
    shapes instead so the game always runs

Controls:
  Left paddle  : W (up)  /  S (down)
  Right paddle : UP arrow / DOWN arrow
  Restart      : R
  Quit         : ESC or close window

Asset files expected in  assets/  folder (next to this script):
  background.png   — any image at least 800×600 px
  player.png       — left paddle sprite  (e.g. 20×90 px, transparent OK)
  enemy.png        — right paddle sprite (same size as player.png)
  ball.png         — ball sprite         (e.g. 20×20 px, transparent OK)

If any file is missing the game falls back to coloured rectangles/circles,
so you can always run it even without assets.
"""

import pygame
import sys
import os

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

WIDTH, HEIGHT = 900, 600
FPS           = 60

PADDLE_SPEED  = 6
PADDLE_MARGIN = 30

BALL_START_SPEED_X = 5
BALL_START_SPEED_Y = 4
BALL_SPEEDUP       = 0.3
BALL_MAX_SPEED     = 14

WINNING_SCORE      = 7

# Fallback colours (used when sprites are missing)
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
CYAN   = (40,  200, 220)
PINK   = (255,  80, 150)
ORANGE = (230, 120,  20)
GREY   = (80,  80,  80)

# Asset paths — all in the assets/ subfolder
ASSET_DIR  = os.path.join(os.path.dirname(__file__), 'assets')
BG_PATH    = os.path.join(ASSET_DIR, 'background.png')
LEFT_PATH  = os.path.join(ASSET_DIR, 'player.png')
RIGHT_PATH = os.path.join(ASSET_DIR, 'enemy.png')
BALL_PATH  = os.path.join(ASSET_DIR, 'ball.png')


# ─────────────────────────────────────────────────────────────────────────────
# SPRITE LOADING HELPER
# Returns a scaled Surface, or None if the file doesn't exist.
# This lets the rest of the code gracefully fall back to shapes.
# ─────────────────────────────────────────────────────────────────────────────

def load_sprite(path, size=None):
    """
    Load a PNG image and optionally scale it.

    path : file path to the PNG
    size : (width, height) tuple to scale to, or None to keep original size

    Returns a Surface with .convert_alpha() applied, or None on failure.
    """
    if not os.path.exists(path):
        print(f'[INFO] Asset not found, using shape fallback: {path}')
        return None
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            # Scale to the requested size — always from the original (not chained)
            img = pygame.transform.scale(img, size)
        return img
    except pygame.error as e:
        print(f'[WARN] Could not load {path}: {e}')
        return None


def load_background(path):
    """
    Load the background image scaled to fill the window.
    Uses .convert() (not .convert_alpha()) since the background
    doesn't need transparency — convert() is slightly faster.

    Returns a Surface scaled to (WIDTH, HEIGHT), or None on failure.
    """
    if not os.path.exists(path):
        print(f'[INFO] Background not found, using solid colour.')
        return None
    try:
        img = pygame.image.load(path).convert()
        # Scale to exactly fill the window — done once here, not every frame
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        return img
    except pygame.error as e:
        print(f'[WARN] Could not load background: {e}')
        return None


# ─────────────────────────────────────────────────────────────────────────────
# PADDLE CLASS
# ─────────────────────────────────────────────────────────────────────────────

class Paddle:
    """
    One player's paddle.
    Supports a sprite image OR a fallback coloured rectangle.
    """

    # Target size for paddle sprites — we scale loaded images to this
    SPRITE_W = 20
    SPRITE_H = 90

    def __init__(self, x, fallback_color, sprite_img=None):
        """
        x              : left edge x position
        fallback_color : RGB colour used if no sprite is available
        sprite_img     : Surface returned by load_sprite(), or None
        """
        self.color  = fallback_color
        self.sprite = sprite_img    # may be None
        self.score  = 0

        self.rect = pygame.Rect(x, HEIGHT // 2 - self.SPRITE_H // 2,
                                self.SPRITE_W, self.SPRITE_H)

    def move(self, up_key, down_key, keys_held):
        """Move the paddle up/down, clamped to the window."""
        if keys_held[up_key]:
            self.rect.y -= PADDLE_SPEED
        if keys_held[down_key]:
            self.rect.y += PADDLE_SPEED
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self, surface):
        """
        If a sprite is available, blit it.
        Otherwise, draw a coloured rectangle — same position/size.
        """
        if self.sprite:
            # blit() draws the image at the rect's top-left corner
            surface.blit(self.sprite, self.rect.topleft)
        else:
            # Fallback shape with a highlight stripe
            pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
            highlight = pygame.Rect(self.rect.x, self.rect.y, 3, self.rect.height)
            pygame.draw.rect(surface, WHITE, highlight, border_radius=2)


# ─────────────────────────────────────────────────────────────────────────────
# BALL CLASS
# ─────────────────────────────────────────────────────────────────────────────

class Ball:
    """
    The Pong ball.
    Supports a sprite image OR a fallback coloured circle.
    """

    SIZE = 20   # pixel width and height of the ball (square bounding box)

    def __init__(self, sprite_img=None):
        self.sprite = sprite_img
        self.rect   = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.vel_x  = 0
        self.vel_y  = 0
        self.reset(direction=1)

    def reset(self, direction=1):
        """Place ball at centre and give it a fresh velocity."""
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vel_x = BALL_START_SPEED_X * direction
        self.vel_y = BALL_START_SPEED_Y

    def update(self, left_paddle, right_paddle):
        """
        Move, bounce, detect scoring.
        Returns: 0 = in play | 1 = right scored | -1 = left scored
        """
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)

        # Wall bounces
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vel_y = abs(self.vel_y)
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = -abs(self.vel_y)

        # Paddle collisions
        for paddle in (left_paddle, right_paddle):
            if self.rect.colliderect(paddle.rect):
                self._bounce_off_paddle(paddle)
                break

        # Scoring
        if self.rect.right < 0:
            return 1    # right player scored
        if self.rect.left > WIDTH:
            return -1   # left player scored
        return 0

    def _bounce_off_paddle(self, paddle):
        """Reverse direction; angle depends on where the ball hit the paddle."""
        relative_hit = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        relative_hit = max(-1.0, min(1.0, relative_hit))

        speed = min(abs(self.vel_x) + BALL_SPEEDUP, BALL_MAX_SPEED)

        if self.vel_x > 0:
            self.vel_x = -speed
            self.rect.right = paddle.rect.left - 1
        else:
            self.vel_x = speed
            self.rect.left = paddle.rect.right + 1

        self.vel_y = relative_hit * speed * 0.9

    def draw(self, surface):
        """Blit sprite if available; otherwise draw a circle."""
        if self.sprite:
            surface.blit(self.sprite, self.rect.topleft)
        else:
            pygame.draw.circle(surface, ORANGE, self.rect.center, self.SIZE // 2)


# ─────────────────────────────────────────────────────────────────────────────
# TRAIL EFFECT
# A translucent black surface blitted each frame instead of a solid fill.
# Previous frames fade out gradually, leaving a motion trail.
# ─────────────────────────────────────────────────────────────────────────────

def make_trail_overlay(alpha=40):
    """
    Create a surface the size of the window filled with semi-transparent black.

    alpha : 0 = fully transparent (long trail), 255 = opaque (no trail)

    SRCALPHA flag tells PyGame this surface uses per-pixel alpha, which
    allows the (R, G, B, A) four-channel fill to work properly.
    """
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    return overlay


# ─────────────────────────────────────────────────────────────────────────────
# SCORE FLASH EFFECT
# When a point is scored we briefly scale the scorer's number up then back.
# ─────────────────────────────────────────────────────────────────────────────

class ScoreFlash:
    """Tracks a temporary scale-up animation for a score digit."""

    def __init__(self):
        self.scale   = 1.0    # current scale multiplier (1.0 = normal)
        self.active  = False

    def trigger(self):
        """Start the flash animation."""
        self.scale  = 2.2
        self.active = True

    def update(self):
        """Shrink back toward 1.0 each frame."""
        if self.active:
            self.scale -= 0.07
            if self.scale <= 1.0:
                self.scale  = 1.0
                self.active = False

    def current_scale(self):
        return self.scale


# ─────────────────────────────────────────────────────────────────────────────
# DRAWING HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def draw_background(surface, bg_img):
    """
    Draw the background.
    If a background image was loaded, blit it (already scaled to window size).
    Otherwise fill with a dark gradient approximation (two rects).
    """
    if bg_img:
        surface.blit(bg_img, (0, 0))
    else:
        surface.fill((15, 15, 30))   # dark navy fallback


def draw_net(surface):
    """Dashed centre line."""
    x    = WIDTH // 2 - 1
    y    = 0
    dash = 18
    gap  = 10
    while y < HEIGHT:
        pygame.draw.rect(surface, GREY, (x, y, 3, dash))
        y += dash + gap


def draw_scores(surface, font_large, left_paddle, right_paddle,
                left_flash, right_flash):
    """
    Render scores with the flash scale effect applied.
    The flash temporarily enlarges the score that just went up.
    """
    for paddle, flash, x_fraction in (
        (left_paddle,  left_flash,  0.25),
        (right_paddle, right_flash, 0.75),
    ):
        color = CYAN if paddle is left_paddle else PINK

        # Render at base size
        base_surf = font_large.render(str(paddle.score), True, color)

        # Scale up if flash is active
        s = flash.current_scale()
        if s != 1.0:
            w = int(base_surf.get_width()  * s)
            h = int(base_surf.get_height() * s)
            base_surf = pygame.transform.scale(base_surf, (w, h))

        # Centre the (possibly scaled) score in its half of the screen
        cx = int(WIDTH * x_fraction)
        rect = base_surf.get_rect(center=(cx, 45))
        surface.blit(base_surf, rect)


def draw_winner_screen(surface, big_font, small_font, winner_name, winner_color):
    """Semi-transparent winner overlay."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    msg = big_font.render(f'{winner_name} wins!', True, winner_color)
    sub = small_font.render('R to play again   |   ESC to quit', True, WHITE)
    surface.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
    surface.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 44)))


def draw_controls(surface, font):
    """Small key-hint labels in the bottom corners."""
    left  = font.render('W / S', True, CYAN)
    right = font.render('↑ / ↓', True, PINK)
    surface.blit(left,  (PADDLE_MARGIN + Paddle.SPRITE_W + 8, HEIGHT - 22))
    surface.blit(right, (WIDTH - PADDLE_MARGIN - Paddle.SPRITE_W - right.get_width() - 8,
                          HEIGHT - 22))


# ─────────────────────────────────────────────────────────────────────────────
# GAME STATE
# ─────────────────────────────────────────────────────────────────────────────

class GameState:
    """Owns all mutable game data and the update/draw cycle."""

    def __init__(self, left_sprite, right_sprite, ball_sprite):
        self.left_paddle  = Paddle(PADDLE_MARGIN, CYAN,  left_sprite)
        self.right_paddle = Paddle(WIDTH - PADDLE_MARGIN - Paddle.SPRITE_W, PINK, right_sprite)
        self.ball         = Ball(ball_sprite)
        self.game_over    = False
        self.winner_name  = ''
        self.winner_color = WHITE

        # One flash tracker per paddle
        self.left_flash  = ScoreFlash()
        self.right_flash = ScoreFlash()

        # Trail overlay — blitted every frame for the motion effect
        self.trail = make_trail_overlay(alpha=35)

    def reset(self):
        """Restart the match."""
        self.left_paddle.score  = 0
        self.right_paddle.score = 0
        self.left_paddle.rect.y  = HEIGHT // 2 - Paddle.SPRITE_H // 2
        self.right_paddle.rect.y = HEIGHT // 2 - Paddle.SPRITE_H // 2
        self.ball.reset(direction=1)
        self.game_over    = False
        self.winner_name  = ''
        self.winner_color = WHITE

    def update(self, keys_held):
        if self.game_over:
            return

        self.left_paddle.move(pygame.K_w, pygame.K_s, keys_held)
        self.right_paddle.move(pygame.K_UP, pygame.K_DOWN, keys_held)

        result = self.ball.update(self.left_paddle, self.right_paddle)

        if result == 1:
            self.right_paddle.score += 1
            self.right_flash.trigger()
            self._check_winner()
            if not self.game_over:
                self.ball.reset(direction=-1)

        elif result == -1:
            self.left_paddle.score += 1
            self.left_flash.trigger()
            self._check_winner()
            if not self.game_over:
                self.ball.reset(direction=1)

        self.left_flash.update()
        self.right_flash.update()

    def _check_winner(self):
        if self.right_paddle.score >= WINNING_SCORE:
            self.game_over    = True
            self.winner_name  = 'Right player'
            self.winner_color = PINK
        elif self.left_paddle.score >= WINNING_SCORE:
            self.game_over    = True
            self.winner_name  = 'Left player'
            self.winner_color = CYAN

    def draw(self, surface, bg_img, score_font, tiny_font):
        """
        Full draw pass each frame.

        Drawing order (back to front):
          1. Background image (or solid fill)
          2. Trail overlay  (semi-transparent black — fades previous frames)
          3. Net
          4. Scores
          5. Paddles
          6. Ball
          7. Controls hint
        """
        draw_background(surface, bg_img)
        # Trail overlay gives the motion blur / ghost effect
        surface.blit(self.trail, (0, 0))
        draw_net(surface)
        draw_scores(surface, score_font,
                    self.left_paddle, self.right_paddle,
                    self.left_flash, self.right_flash)
        self.left_paddle.draw(surface)
        self.right_paddle.draw(surface)
        self.ball.draw(surface)
        draw_controls(surface, tiny_font)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong — Sprites Edition')
    clock = pygame.time.Clock()

    # ── Load all assets ────────────────────────────────────────────────────
    # Each returns a Surface or None — None triggers shape fallback in draw()
    bg_img       = load_background(BG_PATH)
    left_sprite  = load_sprite(LEFT_PATH,  size=(Paddle.SPRITE_W, Paddle.SPRITE_H))
    right_sprite = load_sprite(RIGHT_PATH, size=(Paddle.SPRITE_W, Paddle.SPRITE_H))
    ball_sprite  = load_sprite(BALL_PATH,  size=(Ball.SIZE, Ball.SIZE))

    # ── Fonts ──────────────────────────────────────────────────────────────
    score_font = pygame.font.SysFont('consolas', 64, bold=True)
    win_font   = pygame.font.SysFont('consolas', 52, bold=True)
    sub_font   = pygame.font.SysFont('consolas', 22)
    tiny_font  = pygame.font.SysFont('consolas', 16)

    # ── Game state ─────────────────────────────────────────────────────────
    state = GameState(left_sprite, right_sprite, ball_sprite)

    # ── Game loop ──────────────────────────────────────────────────────────
    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    state.reset()

        # Update
        keys_held = pygame.key.get_pressed()
        state.update(keys_held)

        # Draw
        state.draw(screen, bg_img, score_font, tiny_font)
        if state.game_over:
            draw_winner_screen(screen, win_font, sub_font,
                               state.winner_name, state.winner_color)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
