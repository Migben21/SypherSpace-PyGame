import pygame

pygame.init()

WIDTH, HEIGHT = 900, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sypher Space Explorer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 34)

BACKGROUND_COLOUR = (10, 12, 26)
PANEL_COLOUR = (26, 30, 48)
BUTTON_COLOUR = (60, 65, 82)
BUTTON_HOVER_COLOUR = (80, 86, 108)
TEXT_COLOUR = (250, 250, 245)

PANEL_X, PANEL_Y, PANEL_WIDTH = 64, 70, WIDTH - 128
LINE_HEIGHT = 40
BUTTON_W, BUTTON_H, BUTTON_GAP = 650, 60, 16

STATE_STORY = "story"
STATE_END = "end"

SCENES = {
    "start": {
        "text": (
            "Welcome to the Sypher Space Explorer! You are the captain of a starship: "
            "The Sypher Shuttle. The Sypher Shuttle has stopped by a planet on its "
            "journey. The planet is blue yet filled with golden glimmers, hinting at "
            "possible treasures. Or at the very least, valuable minerals."
        ),
        "buttons": [
            {"label": "Land on the planet!", "next": "planet"},
            {"label": "I'm hungry! Cosmic Cravings.", "next": "cravings"},
        ],
    },
    "planet": {
        "text": (
            "You land on the planet - it appears to be filled with mostly deep blue "
            "waters. Several landmarks dot the horizon; there are islands in view. "
            "Your ship is now floating on the ocean, but you can easily sail it to "
            "other islands. One of the closer islands has what appears to be an alien "
            "temple. You could also use your antennas to scan for signals from where "
            "you are."
        ),
        "buttons": [
            {"label": "Go to the alien temple", "next": "temple"},
            {"label": "Scan for signals first!", "next": "scan"},
        ],
    },
    "temple": {
        "text": "Inside the alien temple, you find ancient alien technology. It hums with power.",
        "buttons": [
            {"label": "Touch it", "next": "temple_touch"},
            {"label": "Take a sample, return to Earth", "next": "temple_sample"},
        ],
    },
    "temple_touch": {
        "text": "You gain super space powers! You're now a Sypher Space Super Hero!",
        "buttons": [{"label": "The End", "next": None}],
    },
    "temple_sample": {
        "text": "When you bring it back to Earth, scientists are amazed! You're a hero of science now.",
        "buttons": [{"label": "The End", "next": None}],
    },
    "scan": {
        "text": "Your antenna is picking up a strange signal...",
        "buttons": [
            {"label": "Respond to it!", "next": "scan_respond"},
            {"label": "Ignore it - too risky!", "next": "scan_ignore"},
        ],
    },
    "scan_respond": {
        "text": "It turns out to be a friendly alien! They share cool knowledge. New friend achieved!",
        "buttons": [{"label": "The End", "next": None}],
    },
    "scan_ignore": {
        "text": (
            "You head back home and ignore the signal. Sounds like future space "
            "peoples' problem. For now, it's eepy time."
        ),
        "buttons": [{"label": "The End", "next": None}],
    },
    "cravings": {
        "text": (
            "Yummers. Cosmic Cravings. You proceed to eat tons of Big Burgers and "
            "Comet Chips. You got so full that you're starting to pass out into a "
            "food coma. Space exploration can wait for another day. For now, it's "
            "eepy time."
        ),
        "buttons": [{"label": "The End", "next": None}],
    },
}

END_BUTTONS = [{"label": "Play Again"}, {"label": "Exit"}]

current_scene = "start"
state = STATE_STORY


# Buttons
def get_button_rects(buttons, start_y):
    """Lays out one rect per button, stacked and centred, starting at start_y."""
    rects = []
    for i in range(len(buttons)):
        rect = pygame.Rect((WIDTH - BUTTON_W) // 2, start_y + i * (BUTTON_H + BUTTON_GAP), BUTTON_W, BUTTON_H)
        rects.append(rect)
    return rects


def draw_button(surface, rect, label):
    mouse_pos = pygame.mouse.get_pos()
    colour = BUTTON_HOVER_COLOUR if rect.collidepoint(mouse_pos) else BUTTON_COLOUR
    pygame.draw.rect(surface, colour, rect, border_radius=10)
    text = font.render(label, True, TEXT_COLOUR)
    surface.blit(text, text.get_rect(center=rect.center))


def wrap_text(text, font, max_width):
    """Breaks `text` into a list of lines that each fit within max_width."""
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
    scene = SCENES[current_scene]
    lines = wrap_text(scene["text"], big_font, PANEL_WIDTH - 60)
    panel_height = len(lines) * LINE_HEIGHT + 60
    panel = pygame.Rect(PANEL_X, PANEL_Y, PANEL_WIDTH, panel_height)
    button_start_y = panel.bottom + 30
    rects = get_button_rects(scene["buttons"], button_start_y)
    return scene, lines, panel, rects


# Game loop
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
                        state = STATE_END
                    else:
                        current_scene = button["next"]

        if event.type == pygame.MOUSEBUTTONDOWN and state == STATE_END:
            end_rects = get_button_rects(END_BUTTONS, 440)
            for rect, button in zip(end_rects, END_BUTTONS):
                if rect.collidepoint(event.pos):
                    if button["label"] == "Play Again":
                        current_scene = "start"
                        state = STATE_STORY
                    elif button["label"] == "Exit":
                        running = False

    screen.fill(BACKGROUND_COLOUR)

    if state == STATE_STORY:
        scene, lines, panel, rects = get_story_layout()
        pygame.draw.rect(screen, PANEL_COLOUR, panel, border_radius=16)
        for i, line in enumerate(lines):
            text = big_font.render(line, True, TEXT_COLOUR)
            screen.blit(text, (panel.x + 30, panel.y + 30 + i * LINE_HEIGHT))
        for rect, button in zip(rects, scene["buttons"]):
            draw_button(screen, rect, button["label"])

    elif state == STATE_END:
        message = big_font.render("Thanks for playing!", True, TEXT_COLOUR)
        screen.blit(message, message.get_rect(center=(WIDTH // 2, 300)))
        end_rects = get_button_rects(END_BUTTONS, 440)
        for rect, button in zip(end_rects, END_BUTTONS):
            draw_button(screen, rect, button["label"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()