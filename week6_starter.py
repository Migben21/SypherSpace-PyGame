"""
CodeBots - Term 4 - Week 6 starter file
----------------------------------------------------------------------
Builds on Week 5's win screen, game over screen, and sound effects.
This week you'll add a high score that's saved to a file, so it
survives even after the game is closed and reopened.

Most TODOs are either adding one line you can see the shape of nearby,
or replacing a placeholder (False, 0, or a comment telling you what to
type)
"""

import json
import math
import os
import random

import pygame

# --- Setup -----------------------------------------------------------
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 34)
big_font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 26)

BACKGROUND_COLOUR = (24, 26, 36)
PLAYER_COLOUR = (232, 113, 74)
TREASURE_COLOUR = (230, 196, 90)
OBSTACLE_COLOUR = (196, 68, 68)
TEXT_COLOUR = (250, 250, 245)
HIGHLIGHT_COLOUR = (230, 196, 90)

PLAYER_SIZE = 50
PLAYER_SPEED = 5
START_X, START_Y = WIDTH // 2, HEIGHT // 2
player_x, player_y = START_X, START_Y

SAFE_MARGIN = 80
SAFE_ZONE = pygame.Rect(
    START_X - SAFE_MARGIN,
    START_Y - SAFE_MARGIN,
    PLAYER_SIZE + SAFE_MARGIN * 2,
    PLAYER_SIZE + SAFE_MARGIN * 2,
)

OBSTACLE_SIZE = 50
TREASURE_SIZE = 40
NUM_OBSTACLES = 5
NUM_TREASURES = 3
INVULNERABLE_FRAMES = 30  # half a second at 60 FPS

HIGH_SCORE_FILE = "high_score.json"


# --- Saving and loading the high score ---------------------------------
# These two functions are provided for you. load_high_score() runs once,
# right when the program starts. save_high_score() is called whenever
# the game ends with a new best score.
def load_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, "r") as f:
        data = json.load(f)
        return data["high_score"]


def save_high_score(value):
    with open(HIGH_SCORE_FILE, "w") as f:
        json.dump({"high_score": value}, f)


# --- Sound effects -----------------------------------------------------
# make_beep() builds a short tone entirely in code, so no sound files
# are needed. You don't need to understand every line of this to use
# it - just know it hands back a Sound you can call .play() on.
def make_beep(frequency=440, duration=0.15, volume=0.5, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    amplitude = int(32767 * volume)
    samples = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        value = int(amplitude * math.sin(2 * math.pi * frequency * t))
        samples += value.to_bytes(2, byteorder="little", signed=True)
    return pygame.mixer.Sound(buffer=bytes(samples))


TREASURE_SOUND = make_beep(frequency=880, duration=0.12, volume=0.4)
HIT_SOUND = make_beep(frequency=180, duration=0.25, volume=0.4)
HIGH_SCORE_SOUND = make_beep(frequency=1200, duration=0.2, volume=0.4)


def make_obstacle():
    """Returns a new obstacle Rect at a random position, trying again
    if it would land inside the safe zone."""
    while True:
        rect = pygame.Rect(
            random.randint(0, WIDTH - OBSTACLE_SIZE),
            random.randint(0, HEIGHT - OBSTACLE_SIZE),
            OBSTACLE_SIZE,
            OBSTACLE_SIZE,
        )
        if not rect.colliderect(SAFE_ZONE):
            return rect


def make_treasure():
    """Same idea as make_obstacle(), just sized and used for treasures."""
    while True:
        rect = pygame.Rect(
            random.randint(0, WIDTH - TREASURE_SIZE),
            random.randint(0, HEIGHT - TREASURE_SIZE),
            TREASURE_SIZE,
            TREASURE_SIZE,
        )
        if not rect.colliderect(SAFE_ZONE):
            return rect


def draw_player(surface, x, y):
    pygame.draw.rect(surface, PLAYER_COLOUR, (x, y, PLAYER_SIZE, PLAYER_SIZE))


def clamp(value, lo, hi):
    return max(lo, min(value, hi))


# TODO: set high_score by calling load_high_score() instead of just 0
high_score = 0

OBSTACLES = []
for _ in range(NUM_OBSTACLES):
    OBSTACLES.append(make_obstacle())

TREASURES = []
for _ in range(NUM_TREASURES):
    TREASURES.append({"rect": make_treasure(), "collected": False})

score = 0
lives = 3
treasures_found = 0
invulnerable_timer = 0
game_won = False
result_saved = False
new_high_score = False

# --- Game loop ---------------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_r:
                # Start a fresh game: new random layout, counters back
                # to their starting values
                player_x, player_y = START_X, START_Y
                OBSTACLES = []
                for _ in range(NUM_OBSTACLES):
                    OBSTACLES.append(make_obstacle())
                TREASURES = []
                for _ in range(NUM_TREASURES):
                    TREASURES.append({"rect": make_treasure(), "collected": False})
                score = 0
                lives = 3
                treasures_found = 0
                invulnerable_timer = 0
                game_won = False
                # TODO: reset result_saved and new_high_score back to
                # False here too, the same way the lines above reset
                # score, lives, and game_won

    game_over = lives <= 0

    if not game_over and not game_won:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += PLAYER_SPEED

        player_x = clamp(player_x, 0, WIDTH - PLAYER_SIZE)
        player_y = clamp(player_y, 0, HEIGHT - PLAYER_SIZE)
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

        for treasure in TREASURES:
            if not treasure["collected"] and player_rect.colliderect(treasure["rect"]):
                treasure["collected"] = True
                score += 1
                treasures_found += 1
                TREASURE_SOUND.play()

        if invulnerable_timer > 0:
            invulnerable_timer -= 1

        for obstacle in OBSTACLES:
            if invulnerable_timer <= 0 and player_rect.colliderect(obstacle):
                lives -= 1
                invulnerable_timer = INVULNERABLE_FRAMES
                player_x, player_y = START_X, START_Y
                HIT_SOUND.play()

        # Winning: every treasure found
        if treasures_found == NUM_TREASURES:
            game_won = True

    # The game has just ended (win or lose) and this result hasn't
    # been checked against the high score yet
    if (game_over or game_won) and not result_saved:
        # TODO: replace False with a condition that is True when the
        # current score beats the saved high score
        if False:
            high_score = score
            # TODO: call save_high_score(), passing it high_score, so
            # the new best actually gets written to the file
            new_high_score = True
            HIGH_SCORE_SOUND.play()
        result_saved = True

    # --- Draw everything ---
    screen.fill(BACKGROUND_COLOUR)

    for treasure in TREASURES:
        if not treasure["collected"]:
            pygame.draw.rect(screen, TREASURE_COLOUR, treasure["rect"])

    for obstacle in OBSTACLES:
        pygame.draw.rect(screen, OBSTACLE_COLOUR, obstacle)

    # Flash the player while invulnerable, instead of drawing it
    # solidly the whole time
    player_visible = True
    if invulnerable_timer > 0:
        player_visible = invulnerable_timer % 6 < 3
    if player_visible:
        draw_player(screen, player_x, player_y)

    # TODO: add "   Best: {high_score}" to the end of this f-string,
    # the same way "Treasures: ..." was added to the HUD in Week 4
    hud_text = f"Score: {score}   Lives: {lives}   Treasures: {treasures_found}/{NUM_TREASURES}"
    hud = font.render(hud_text, True, TEXT_COLOUR)
    screen.blit(hud, (20, 20))

    if game_won or game_over:
        if game_won:
            message = big_font.render("You found every treasure!", True, TEXT_COLOUR)
        else:
            message = big_font.render("No lives left!", True, TEXT_COLOUR)
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))

        if new_high_score:
            best = big_font.render(f"New best score: {score}!", True, HIGHLIGHT_COLOUR)
            screen.blit(best, best.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5)))

        hint = small_font.render("Press R to play again, or Q to quit", True, TEXT_COLOUR)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()