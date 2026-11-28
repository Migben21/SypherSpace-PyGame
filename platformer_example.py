"""
CodeBots Platformer
====================
HOW THE GAME IS ORGANISED
--------------------------
1. SETTINGS -> numbers we might want to tweak (screen size, gravity...)
2. LEVEL DATA -> a list of levels. Each level is a dictionary describing
   its platforms, coins, hazards and goal flag.
3. HELPER FUNCTIONS -> small functions that each do ONE job (move the
   player, check collisions, draw the menu, etc).
4. MAIN LOOP -> ties everything together and runs forever until the
   player quits.

CONTROLS
--------
  Left / Right arrow keys (or A / D)  -> move
  Space / Up arrow                    -> jump
  Mouse click                         -> choose a level in the menu
  Esc                                 -> back to the menu / quit
"""

import sys
import pygame

# ---------------------------------------------------------------------------
# 1. SETTINGS
# ---------------------------------------------------------------------------

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
FPS = 60

GRAVITY = 0.6          # how fast the player falls (pixels per frame, per frame)
MOVE_SPEED = 5          # how fast the player walks left/right
JUMP_STRENGTH = -11     # negative = upwards. Bigger (more negative) = higher jump

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 40

# A dictionary of colours so we only have to change a colour in ONE place.
COLORS = {
    "sky": (135, 206, 250),
    "ground": (90, 60, 40),
    "platform": (120, 85, 60),
    "player": (220, 60, 60),
    "coin": (255, 215, 0),
    "goal": (40, 200, 90),
    "hazard": (230, 30, 30),
    "text": (20, 20, 20),
    "white": (255, 255, 255),
    "menu_bg": (25, 25, 40),
    "button": (70, 130, 180),
    "button_hover": (100, 160, 210),
    "button_locked": (90, 90, 90),
}

# ---------------------------------------------------------------------------
# 2. LEVEL DATA
# Each level is a dictionary. "platforms" and "hazards" are lists of
# pygame.Rect(x, y, width, height). Feel free to add more levels using the
# same pattern -- that's the whole point of building it this way!
# ---------------------------------------------------------------------------

def build_levels():
    """Creates and returns the list of all levels in the game.

    We build this with a function (instead of writing it directly at the
    top of the file) so that pygame.Rect is only created after pygame has
    started up properly.
    """
    levels = [
        {
            "name": "Level 1",
            "player_start": (40, 300),
            "platforms": [
                pygame.Rect(0, 400, 800, 50),      # the main ground
                pygame.Rect(250, 320, 120, 20),
                pygame.Rect(450, 250, 120, 20),
                pygame.Rect(650, 180, 120, 20),
            ],
            "coins": [(290, 280), (490, 210), (690, 140)],
            "hazards": [],  # no hazards yet -- nice and safe!
            "goal": pygame.Rect(700, 120, 40, 60),
        },
        {
            "name": "Level 2",
            "player_start": (40, 300),
            "platforms": [
                pygame.Rect(0, 400, 250, 50),
                pygame.Rect(350, 400, 450, 50),
                pygame.Rect(150, 300, 100, 20),
                pygame.Rect(350, 230, 100, 20),
                pygame.Rect(550, 160, 100, 20),
            ],
            "coins": [(180, 260), (380, 190), (580, 120)],
            # a "hazard" is a pit of lava drawn as a red rectangle.
            # if the player touches it, they go back to the start.
            "hazards": [pygame.Rect(250, 420, 100, 30)],
            "goal": pygame.Rect(600, 100, 40, 60),
        },
        {
            "name": "Level 3",
            "player_start": (40, 300),
            "platforms": [
                pygame.Rect(0, 400, 180, 50),
                pygame.Rect(260, 400, 120, 50),
                pygame.Rect(460, 400, 120, 50),
                pygame.Rect(660, 400, 140, 50),
                pygame.Rect(130, 300, 90, 20),
                pygame.Rect(330, 260, 90, 20),
                pygame.Rect(530, 220, 90, 20),
            ],
            "coins": [(160, 260), (360, 220), (560, 180), (700, 350)],
            "hazards": [
                pygame.Rect(180, 420, 80, 30),
                pygame.Rect(380, 420, 80, 30),
                pygame.Rect(580, 420, 80, 30),
            ],
            "goal": pygame.Rect(740, 340, 40, 60),
        },
    ]
    return levels


# ---------------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# Each function below does ONE small job. Breaking a big problem into small
# functions like this makes the code much easier to read and fix!
# ---------------------------------------------------------------------------

def make_player(start_pos):
    """Creates a new player dictionary at the given (x, y) position."""
    x, y = start_pos
    return {
        "rect": pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT),
        "vel_y": 0,          # vertical speed (how fast falling/jumping)
        "on_ground": False,  # is the player currently standing on something?
    }


def handle_player_input(player, keys):
    """Looks at which keys are held down and moves the player left/right,
    and starts a jump if the player is on the ground and presses jump."""

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player["rect"].x -= MOVE_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player["rect"].x += MOVE_SPEED

    jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
    if jump_pressed and player["on_ground"]:
        player["vel_y"] = JUMP_STRENGTH
        player["on_ground"] = False


def apply_gravity_and_collisions(player, platforms):
    """Makes the player fall, then checks if they land on any platform.

    This is the trickiest part of any platformer, so here is the plan:
      1. Add gravity to the player's vertical speed (they fall faster
         and faster, just like in real life).
      2. Move the player down by that speed.
      3. Check every platform: if the player is now overlapping it AND
         was falling (not jumping up through it), snap the player to
         stand right on top of the platform and stop falling.
    """
    player["vel_y"] += GRAVITY
    player["rect"].y += player["vel_y"]
    player["on_ground"] = False

    for platform in platforms:
        if player["rect"].colliderect(platform):
            # Only land on top of a platform if we were moving downward
            # and our feet are near the top edge of that platform.
            falling_onto_top = player["vel_y"] >= 0
            feet_near_top = player["rect"].bottom - player["vel_y"] <= platform.top + 10

            if falling_onto_top and feet_near_top:
                player["rect"].bottom = platform.top
                player["vel_y"] = 0
                player["on_ground"] = True


def keep_player_on_screen(player):
    """Stops the player from walking off the left/right edges of the window."""
    if player["rect"].left < 0:
        player["rect"].left = 0
    if player["rect"].right > SCREEN_WIDTH:
        player["rect"].right = SCREEN_WIDTH


def collect_coins(player, coins, score):
    """Checks if the player is touching any coins. Collected coins are
    removed from the list and the score goes up by 10.
    Returns the (possibly smaller) coins list and the (possibly bigger) score.
    """
    remaining_coins = []
    for coin_pos in coins:
        coin_rect = pygame.Rect(coin_pos[0] - 10, coin_pos[1] - 10, 20, 20)
        if player["rect"].colliderect(coin_rect):
            score += 10  # got it!
        else:
            remaining_coins.append(coin_pos)
    return remaining_coins, score


def touching_hazard(player, hazards):
    """Returns True if the player's rectangle overlaps any hazard rectangle."""
    for hazard in hazards:
        if player["rect"].colliderect(hazard):
            return True
    return False


def reached_goal(player, goal_rect):
    """Returns True if the player has touched the level's goal flag."""
    return player["rect"].colliderect(goal_rect)


def draw_text(surface, text, size, color, x, y, center=False):
    """A shortcut for drawing text, so the rest of the code stays short."""
    font = pygame.font.SysFont("arial", size, bold=True)
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, rect)
    else:
        surface.blit(text_surface, (x, y))


# ---------------------------------------------------------------------------
# DRAWING THE GAMEPLAY SCREEN
# ---------------------------------------------------------------------------

def draw_level(surface, level, player, coins, score):
    """Draws everything for one frame of gameplay: background, platforms,
    coins, hazards, the goal flag, the player, and the score/HUD text."""

    surface.fill(COLORS["sky"])

    for platform in level["platforms"]:
        pygame.draw.rect(surface, COLORS["platform"], platform)

    for hazard in level["hazards"]:
        pygame.draw.rect(surface, COLORS["hazard"], hazard)

    for coin_pos in coins:
        pygame.draw.circle(surface, COLORS["coin"], coin_pos, 10)

    pygame.draw.rect(surface, COLORS["goal"], level["goal"])

    pygame.draw.rect(surface, COLORS["player"], player["rect"])

    draw_text(surface, level["name"], 22, COLORS["text"], 16, 12)
    draw_text(surface, f"Score: {score}", 22, COLORS["text"], 16, 40)
    draw_text(surface, "Esc = menu", 16, COLORS["text"], 16, SCREEN_HEIGHT - 28)


# ---------------------------------------------------------------------------
# MENU SCREEN
# A "button" here is just a dictionary holding a pygame.Rect and a label 
# ---------------------------------------------------------------------------

def build_menu_buttons(num_levels):
    """Creates one button dictionary per level, stacked in the middle of
    the screen."""
    buttons = []
    button_width = 300
    button_height = 60
    gap = 20
    total_height = num_levels * button_height + (num_levels - 1) * gap
    start_y = (SCREEN_HEIGHT - total_height) // 2

    for i in range(num_levels):
        rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + i * (button_height + gap),
            button_width,
            button_height,
        )
        buttons.append({"rect": rect, "level_index": i})
    return buttons


def draw_menu(surface, levels, buttons, unlocked_levels, mouse_pos):
    """Draws the level-select menu, including which levels are locked."""
    surface.fill(COLORS["menu_bg"])

    draw_text(surface, "CODEBOTS PLATFORMER", 40, COLORS["white"],
               SCREEN_WIDTH // 2, 60, center=True)
    draw_text(surface, "Choose a level", 22, COLORS["white"],
               SCREEN_WIDTH // 2, 100, center=True)

    for button in buttons:
        level_index = button["level_index"]
        is_unlocked = level_index in unlocked_levels
        is_hovered = button["rect"].collidepoint(mouse_pos)

        if not is_unlocked:
            color = COLORS["button_locked"]
        elif is_hovered:
            color = COLORS["button_hover"]
        else:
            color = COLORS["button"]

        pygame.draw.rect(surface, color, button["rect"], border_radius=10)

        label = levels[level_index]["name"]
        if not is_unlocked:
            label += "  (locked)"

        draw_text(surface, label, 20, COLORS["white"],
                   button["rect"].centerx, button["rect"].centery, center=True)

    draw_text(surface, "Beat a level to unlock the next one!", 16,
               COLORS["white"], SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, center=True)


def get_clicked_level(buttons, mouse_pos, unlocked_levels):
    """Checks every button to see if the mouse click landed on one that is
    unlocked. Returns the level index that was clicked, or None."""
    for button in buttons:
        if button["rect"].collidepoint(mouse_pos):
            if button["level_index"] in unlocked_levels:
                return button["level_index"]
    return None


# ---------------------------------------------------------------------------
# "LEVEL COMPLETE" SCREEN
# ---------------------------------------------------------------------------

def draw_level_complete(surface, level_name, score, has_next_level):
    surface.fill(COLORS["menu_bg"])
    draw_text(surface, "LEVEL COMPLETE!", 40, COLORS["goal"],
               SCREEN_WIDTH // 2, 140, center=True)
    draw_text(surface, level_name, 24, COLORS["white"],
               SCREEN_WIDTH // 2, 190, center=True)
    draw_text(surface, f"Score: {score}", 24, COLORS["white"],
               SCREEN_WIDTH // 2, 230, center=True)

    if has_next_level:
        draw_text(surface, "Press SPACE for the next level", 20, COLORS["white"],
                   SCREEN_WIDTH // 2, 300, center=True)
    else:
        draw_text(surface, "You beat every level! Nice work!", 20, COLORS["white"],
                   SCREEN_WIDTH // 2, 300, center=True)

    draw_text(surface, "Press ESC to return to the menu", 18, COLORS["white"],
               SCREEN_WIDTH // 2, 340, center=True)


# ---------------------------------------------------------------------------
# 4. MAIN LOOP
# This is where everything comes together. The game is always in exactly
# one "state": "menu", "playing", or "level_complete". Each time through
# the loop we check which state we're in and act accordingly.
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CodeBots Platformer")
    clock = pygame.time.Clock()

    levels = build_levels()
    menu_buttons = build_menu_buttons(len(levels))

    # Which levels can the player click on in the menu? Level 0 always
    # starts unlocked. We use a list (like a mini save-file in memory) and
    # add a level index to it once the player beats the level before it
    unlocked_levels = [0]

    # These variables describe "what is happening right now" and get reset
    # every time a new level starts.
    state = "menu"              # "menu", "playing", or "level_complete"
    current_level_index = 0
    player = None
    coins = []
    score = 0

    def start_level(index):
        """Resets everything needed to begin playing a level from scratch."""
        nonlocal player, coins, score, current_level_index, state
        current_level_index = index
        level = levels[index]
        player = make_player(level["player_start"])
        coins = list(level["coins"])  # copy the list so we don't lose the
                                       # original coin positions forever
        score = 0
        state = "playing"

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # ---- 1. HANDLE EVENTS (things that happened since last frame) ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state in ("playing", "level_complete"):
                        state = "menu"
                    else:
                        running = False

                elif event.key == pygame.K_SPACE and state == "level_complete":
                    next_index = current_level_index + 1
                    if next_index < len(levels):
                        start_level(next_index)
                    else:
                        state = "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN and state == "menu":
                clicked_index = get_clicked_level(menu_buttons, mouse_pos, unlocked_levels)
                if clicked_index is not None:
                    start_level(clicked_index)

        # ---- 2. UPDATE (make things move / change, based on the state) ----
        if state == "playing":
            level = levels[current_level_index]
            keys = pygame.key.get_pressed()

            handle_player_input(player, keys)
            apply_gravity_and_collisions(player, level["platforms"])
            keep_player_on_screen(player)

            coins, score = collect_coins(player, coins, score)

            if touching_hazard(player, level["hazards"]):
                # Send the player back to the start of the level.
                player = make_player(level["player_start"])

            elif reached_goal(player, level["goal"]):
                state = "level_complete"
                next_index = current_level_index + 1
                if next_index < len(levels) and next_index not in unlocked_levels:
                    unlocked_levels.append(next_index)

            # Falling off the bottom of the screen also resets the player.
            if player["rect"].top > SCREEN_HEIGHT:
                player = make_player(level["player_start"])

        # ---- 3. DRAW (show the current state on screen) ----
        if state == "menu":
            draw_menu(screen, levels, menu_buttons, unlocked_levels, mouse_pos)

        elif state == "playing":
            level = levels[current_level_index]
            draw_level(screen, level, player, coins, score)

        elif state == "level_complete":
            level_name = levels[current_level_index]["name"]
            has_next_level = current_level_index + 1 < len(levels)
            draw_level_complete(screen, level_name, score, has_next_level)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


# This makes sure the game only runs when we execute this file directly
# (and not if, for example, we ever import it from another file).
if __name__ == "__main__":
    main()