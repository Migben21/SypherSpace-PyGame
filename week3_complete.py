import pygame

# --- Setup -----------------------------------------------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame Lesson: Collisions")
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

# --- The treasure (one collectible) ---------------------------------
TREASURE_SIZE = 40
TREASURE_RECT = pygame.Rect(650, 80, TREASURE_SIZE, TREASURE_SIZE)
treasure_collected = False

# --- The obstacles, stored as a list so we can loop over them --------
OBSTACLE_SIZE = 50
OBSTACLES = [
    pygame.Rect(200, 250, OBSTACLE_SIZE, OBSTACLE_SIZE),
    pygame.Rect(400, 150, OBSTACLE_SIZE, OBSTACLE_SIZE),
    pygame.Rect(550, 400, OBSTACLE_SIZE, OBSTACLE_SIZE),
]

score = 0
lives = 3
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

        # Treasure: a combined condition - only counts if it hasn't
        # already been collected AND the player is touching it
        if not treasure_collected and player_rect.colliderect(TREASURE_RECT):
            treasure_collected = True
            score += 1

        # Count down the brief safety window after getting hit
        if invulnerable_timer > 0:
            invulnerable_timer -= 1

        # Obstacles: loop over the list, same combined condition each time
        for obstacle in OBSTACLES:
            if invulnerable_timer <= 0 and player_rect.colliderect(obstacle):
                lives -= 1
                invulnerable_timer = INVULNERABLE_FRAMES
                player_x, player_y = START_X, START_Y

    # --- Draw everything ---
    screen.fill(BACKGROUND_COLOUR)

    if not treasure_collected:
        pygame.draw.rect(screen, TREASURE_COLOUR, TREASURE_RECT)

    for obstacle in OBSTACLES:
        pygame.draw.rect(screen, OBSTACLE_COLOUR, obstacle)

    draw_player(screen, player_x, player_y)

    hud_text = f"Score: {score}   Lives: {lives}"
    hud = font.render(hud_text, True, TEXT_COLOUR)
    screen.blit(hud, (20, 20))

    if lives <= 0:
        message = big_font.render("You're out of lives :(", True, TEXT_COLOUR)
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()