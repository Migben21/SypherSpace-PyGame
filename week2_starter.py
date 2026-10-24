import random
import pygame

# --- Setup -----------------------------------------------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame UI Lesson")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 34)
big_font = pygame.font.SysFont(None, 56)

PANEL_COLOUR = (36, 40, 54)
PLAYER_COLOUR = (232, 113, 74)
BUTTON_COLOUR = (60, 65, 82)
BUTTON_HOVER_COLOUR = (80, 86, 108)
TEXT_COLOUR = (250, 250, 245)
PLAYER_SIZE = 50
PLAYER_SPEED = 5
COIN_SIZE = 30

PANEL_X, PANEL_Y, PANEL_WIDTH = 64, 120, WIDTH - 128
LINE_HEIGHT = 54
BUTTON_W, BUTTON_H, BUTTON_GAP = 400, 64, 18

# --- Game states ---------------------------------------------------------
STATE_STORY = "story"
STATE_PLAYING = "playing"
STATE_WIN = "win"


# --- One "theme" per path, so the three mini-games look different without
# needing different rules and just have different colors ------
PATH_THEMES = {
    "forest": {"background": (18, 38, 26), "coin": (120, 210, 130)},
    "mountain": {"background": (34, 38, 52), "coin": (210, 212, 230)},
    # TODO: add a third entry here for "cave", copying the pattern of
    # "forest" and "mountain" above (pick any two colours you like -
    # colours are (red, green, blue), each from 0 to 255).
}


# --- The story, as a dictionary of scenes ---------------------------------
# Each scene has some text, and a list of buttons. A button's "next"
# tells us which scene to go to when it's clicked except for the three
# "Begin!" buttons, whose next is None, which means "start the game".
SCENES = {
    "intro1": {
        "text": "Somewhere in Pygametopia, a legendary trophy has gone missing...",
        "buttons": [{"label": "Continue", "next": "intro2"}],
    },
    "intro2": {
        "text": "You've been chosen to find it. Three paths lie ahead of you.",
        "buttons": [{"label": "Continue", "next": "choice"}],
    },
    "choice": {
        "text": "Which path will you take?",
        "buttons": [
            {"label": "The Forest Path", "next": "forest"},
            {"label": "The Mountain Path", "next": "mountain"},
            # TODO: add a third button here for the Cave path.
            # Copy the pattern above; its "next" should be "cave",
            # to match the scene you're about to add below.
        ],
    },
    "forest": {
        "text": "You step into the shadowy forest. Something glints up ahead...",
        "buttons": [{"label": "Begin!", "next": None}],
    },
    "mountain": {
        "text": "You climb the windswept mountain path, the trophy glinting somewhere above...",
        "buttons": [{"label": "Begin!", "next": None}],
    },
    # TODO: add a "cave" scene here, copying the pattern of "forest" and
    # "mountain" above. Give it its own "text" and a single "Begin!"
    # button with "next": None.
}

# The win screen isn't part of the story, but it reuses the exact same
# "list of buttons" idea - no "next" needed, we'll check the label instead.
WIN_BUTTONS = [{"label": "Play Again"}, {"label": "Exit"}]


# --- Story progress ---------------------------------------------------
current_scene = "intro1"
chosen_path = None
state = STATE_STORY

# These get filled in properly once a path is chosen (see the TODO in
# the event loop below) - for now they're just starting placeholders.
background_colour = (24, 26, 36)
coin_colour = (232, 113, 74)
coin_x = coin_y = 0


# --- Buttons -----------------------------------------------------------
def get_button_rects(buttons, start_y):
    """Lays out one rect per button, stacked and centred, starting at
    start_y. (Provided for you.)"""
    rects = []
    for i in range(len(buttons)):
        rect = pygame.Rect((WIDTH - BUTTON_W) // 2, start_y + i * (BUTTON_H + BUTTON_GAP), BUTTON_W, BUTTON_H)
        rects.append(rect)
    return rects


def draw_button(surface, rect, label):
    """Draws one button, highlighted if the mouse is over it. (Provided for you.)"""
    mouse_pos = pygame.mouse.get_pos()
    colour = BUTTON_HOVER_COLOUR if rect.collidepoint(mouse_pos) else BUTTON_COLOUR
    pygame.draw.rect(surface, colour, rect, border_radius=10)
    text = font.render(label, True, TEXT_COLOUR)
    surface.blit(text, text.get_rect(center=rect.center))


def wrap_text(text, font, max_width):
    """Breaks `text` into a list of lines that each fit within max_width.
    (Provided for you - word-wrapping isn't today's focus.)"""
    words = text.split(" ")
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def get_story_layout():
    """Works out this scene's wrapped text lines, panel height, and button
    rects. This is based on how much is actually in the scene, so a short
    scene with 3 buttons and a long scene with 1 button both fit on
    screen without overlapping."""
    scene = SCENES[current_scene]
    lines = wrap_text(scene["text"], big_font, PANEL_WIDTH - 60)
    panel_height = len(lines) * LINE_HEIGHT + 60
    panel = pygame.Rect(PANEL_X, PANEL_Y, PANEL_WIDTH, panel_height)
    button_start_y = panel.bottom + 30
    rects = get_button_rects(scene["buttons"], button_start_y)
    return scene, lines, panel, rects


# --- Player (from Week 1) ---------------------------------------------
player_x = WIDTH // 2
player_y = HEIGHT // 2


def draw_player(surface, x, y):
    pygame.draw.rect(surface, PLAYER_COLOUR, (x, y, PLAYER_SIZE, PLAYER_SIZE))


def clamp(value, lo, hi):
    return max(lo, min(value, hi))


# --- Game loop -----------------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and state == STATE_STORY:
            scene, _, _, rects = get_story_layout()
            for rect, button in zip(rects, scene["buttons"]):
                if rect.collidepoint(event.pos):
                    if button["next"] is None:
                        # The story's over for this path - set up its mini-game.
                        # TODO: replace None below with PATH_THEMES[chosen_path]
                        theme = None
                        background_colour = theme["background"]
                        coin_colour = theme["coin"]
                        coin_x = random.randint(0, WIDTH - COIN_SIZE)
                        coin_y = random.randint(0, HEIGHT - COIN_SIZE)
                        state = STATE_PLAYING
                    else:
                        current_scene = button["next"]
                        if button["next"] in PATH_THEMES:
                            chosen_path = button["next"]

        if event.type == pygame.MOUSEBUTTONDOWN and state == STATE_WIN:
            win_rects = get_button_rects(WIN_BUTTONS, 400)
            for rect, button in zip(win_rects, WIN_BUTTONS):
                if rect.collidepoint(event.pos):
                    if button["label"] == "Play Again":
                        # Jump straight back to the choice scene so players
                        # can try a different path without replaying the intro
                        current_scene = "choice"
                        chosen_path = None
                        state = STATE_STORY
                    elif button["label"] == "Exit":
                        running = False

    if state == STATE_PLAYING:
        # Movement, straight from Week 1
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
        coin_rect = pygame.Rect(coin_x, coin_y, COIN_SIZE, COIN_SIZE)
        # TODO: replace False below with a check for whether player_rect
        # and coin_rect are touching (hint: one Rect has a method for
        # checking if it overlaps another Rect)
        touching_coin = False
        if touching_coin:
            state = STATE_WIN

    # --- Draw everything ---
    if state == STATE_STORY:
        screen.fill((24, 26, 36))

        scene, lines, panel, rects = get_story_layout()
        pygame.draw.rect(screen, PANEL_COLOUR, panel, border_radius=16)
        for i, line in enumerate(lines):
            text = big_font.render(line, True, TEXT_COLOUR)
            screen.blit(text, (panel.x + 30, panel.y + 30 + i * LINE_HEIGHT))

        for rect, button in zip(rects, scene["buttons"]):
            draw_button(screen, rect, button["label"])

    elif state == STATE_PLAYING:
        screen.fill(background_colour)
        draw_player(screen, player_x, player_y)
        pygame.draw.circle(screen, coin_colour, (coin_x + COIN_SIZE // 2, coin_y + COIN_SIZE // 2), COIN_SIZE // 2)

        hud = font.render(f"Path: {chosen_path.title()} - find the coin!", True, TEXT_COLOUR)
        screen.blit(hud, (20, 20))

    elif state == STATE_WIN:
        screen.fill(background_colour)
        message = big_font.render("You found it!", True, TEXT_COLOUR)
        screen.blit(message, message.get_rect(center=(WIDTH // 2, 260)))

        win_rects = get_button_rects(WIN_BUTTONS, 400)
        for rect, button in zip(win_rects, WIN_BUTTONS):
            draw_button(screen, rect, button["label"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()