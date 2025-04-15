import pygame
import sys

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygbag Test")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Clock to control FPS
clock = pygame.time.Clock()

# Game loop
running = True
x = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw a moving blue rectangle
    pygame.draw.rect(screen, BLUE, (x, 200, 60, 60))
    x += 2
    if x > 640:
        x = -60

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
