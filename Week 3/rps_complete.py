"""
Rock, Paper, Scissors -- PyGame Complete Version
Includes the Tier 1 scoreboard extension from Phase 5.
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
    return random.choice(choices)


def decide_winner(player, computer):
    if player == computer:
        return "tie"
    wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    if wins[player] == computer:
        return "player"
    return "computer"


player_choice = None
computer_choice = None
result_text = "Click a shape to play!"
last_winner = None
player_score = 0
computer_score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for name, rect in boxes.items():
                if rect.collidepoint(event.pos):
                    player_choice = name
                    computer_choice = computer_move()
                    winner = decide_winner(player_choice, computer_choice)
                    last_winner = winner
                    if winner == "tie":
                        result_text = f"Both picked {name} — tie!"
                    elif winner == "player":
                        result_text = f"{name} beats {computer_choice} — you win!"
                        player_score += 1
                    else:
                        result_text = f"{computer_choice} beats {name} — computer wins!"
                        computer_score += 1

    screen.fill(WHITE)

    for name, rect in boxes.items():
        colour = GREY
        if name == player_choice:
            if last_winner == "player":
                colour = GREEN
            elif last_winner == "computer":
                colour = RED
        pygame.draw.rect(screen, colour, rect, border_radius=12)
        label = font.render(name, True, BLACK)
        screen.blit(label, (rect.centerx - label.get_width() // 2,
                             rect.centery - label.get_height() // 2))

    result_surface = big_font.render(result_text, True, BLACK)
    screen.blit(result_surface, (300 - result_surface.get_width() // 2, 60))

    score_surface = font.render(f"You: {player_score}   Computer: {computer_score}", True, BLACK)
    screen.blit(score_surface, (300 - score_surface.get_width() // 2, 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
