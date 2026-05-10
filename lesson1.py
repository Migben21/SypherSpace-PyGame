import pygame, sys
 
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")
clock = pygame.time.Clock()
 
BLACK  = (0, 0, 0)
ORANGE = (230, 120, 20)
 
ball_x, ball_y = 400, 300
ball_r = 30
vel_x,  vel_y  = 4, 3
 
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    # Update
    ball_x += vel_x
    ball_y += vel_y
    if ball_x - ball_r <= 0 or ball_x + ball_r >= WIDTH:
        vel_x = -vel_x
    if ball_y - ball_r <= 0 or ball_y + ball_r >= HEIGHT:
        vel_y = -vel_y
 
    # Draw
    screen.fill(BLACK)
    pygame.draw.circle(screen, ORANGE, (ball_x, ball_y), ball_r)
    pygame.display.flip()
    clock.tick(60)
 
pygame.quit()
sys.exit()
