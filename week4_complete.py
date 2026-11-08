import random
import pygame

# --- Setup -----------------------------------------------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame Lesson: Scores & Objects")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 34)
big_font = pygame.font.SysFont(None, 48)

BACKGROUND_COLOUR = (24, 26, 36)
PLAYER_COLOUR = (232, 113, 74)
TREASURE_COLOUR = (230, 196, 90)
OBSTACLE_COLOUR = (196, 68, 68)
TEXT_COLOUR = (250, 250, 245)

PLAYER_SIZE = 50
PLAYER_SPEED = 5
START_X, START_Y = WIDTH // 2, HEIGHT // 2
player_x, player_y = START_X, START_Y

# A safe zone around the player's starting spot, so nothing spawns
# right on top of them
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


# Build the lists by looping and appending, instead of typing out
# each Rect by hand like last week
OBSTACLES = []
for _ in range(NUM_OBSTACLES):
    OBSTACLES.append(make_obstacle())

TREASURES = []
for _ in range(NUM_TREASURES):
    TREASURES.append({"rect": make_treasure(), "collected": False})

score = 0
lives = 3
treasures_found = 0
INVULNERABLE_FRAMES = 30  # half a second at 60 FPS
invulnerable_timer = 0


def draw_player(surface, x, y):
    pygame.draw.rect(surface, PLAYER_COLOUR, (x, y, PLAYER_SIZE, PLAYER_SIZE))


def clamp(value, lo, hi):
    return max(lo, min(value, hi))


# --- Game loop ---------------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if lives > 0:
        # Movement, same as Week 1
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

        # Loop through every treasure in the list, same combined
        # condition as Week 3, just checked once per treasure now
        for treasure in TREASURES:
            if not treasure["collected"] and player_rect.colliderect(treasure["rect"]):
                treasure["collected"] = True
                score += 1
                treasures_found += 1

        if invulnerable_timer > 0:
            invulnerable_timer -= 1

        for obstacle in OBSTACLES:
            if invulnerable_timer <= 0 and player_rect.colliderect(obstacle):
                lives -= 1
                invulnerable_timer = INVULNERABLE_FRAMES
                player_x, player_y = START_X, START_Y

    # --- Draw everything ---
    screen.fill(BACKGROUND_COLOUR)

    for treasure in TREASURES:
        if not treasure["collected"]:
            pygame.draw.rect(screen, TREASURE_COLOUR, treasure["rect"])

    for obstacle in OBSTACLES:
        pygame.draw.rect(screen, OBSTACLE_COLOUR, obstacle)

    draw_player(screen, player_x, player_y)

    hud_text = f"Score: {score}   Lives: {lives}   Treasures: {treasures_found}/{NUM_TREASURES}"
    hud = font.render(hud_text, True, TEXT_COLOUR)
    screen.blit(hud, (20, 20))

    if lives <= 0:
        message = big_font.render("No lives left! Movement stopped.", True, TEXT_COLOUR)
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()