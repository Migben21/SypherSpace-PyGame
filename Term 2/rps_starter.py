"""
Rock, Paper, Scissors -- PyGame Starter
Fill in the blanks marked with ____ as you follow along in class.
"""
import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Rock Paper Scissors")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 50)

WHITE = (255, 255, 255)
GREY  = (210, 210, 210)
GREEN = (60, 170, 90)
RED   = (200, 70, 70)
BLACK = (20, 20, 20)

choices = ["rock", "paper", "scissors"]
boxes = {
    "rock":     pygame.Rect(40,  250, 150, 120),
    "paper":    pygame.Rect(225, 250, 150, 120),
    "scissors": pygame.Rect(410, 250, 150, 120),
}


def computer_move():
    # TODO: return a random choice from `choices`
    pass


def decide_winner(player, computer):
    # TODO: return "tie", "player", or "computer"
    pass


player_choice = None
computer_choice = None
result_text = "Click a shape to play!"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for name, rect in boxes.items():
                if rect.collidepoint(event.pos):
                    player_choice = name
                    # TODO: call computer_move() and decide_winner()
                    # TODO: set result_text based on who won

    screen.fill(WHITE)

    for name, rect in boxes.items():
        colour = GREY
        # TODO: colour the box green/red if it was the player's choice
        pygame.draw.rect(screen, colour, rect, border_radius=12)
        label = font.render(name, True, BLACK)
        screen.blit(label, (rect.centerx - label.get_width() // 2,
                             rect.centery - label.get_height() // 2))

    result_surface = big_font.render(result_text, True, BLACK)
    screen.blit(result_surface, (300 - result_surface.get_width() // 2, 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
