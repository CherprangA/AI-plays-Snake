import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen

# small window for testing
screen = pygame.display.set_mode((800, 600))

# Full screen for deployment
# screen_info = pygame.display.Info()
# screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
pygame.display.set_caption("AI-Plays-Snake")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock to control FPS
clock = pygame.time.Clock()

print("Starting the game")

# Game loop
running = True
x = 100
y = 100
current_direction = "right"
    
while running:
    pygame.event.pump()  # Ensure events are processed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)    
    
    # Draw a moving blue rectangle
    pygame.draw.rect(screen,BLUE, (x, y, 60, 60))
    if x > 640:
        x = -60
    if y > 480:
        y = -60
        
    if current_direction == "right":
        x += 2
    elif current_direction == "left":
        x -= 2
    elif current_direction == "up":
        y -= 2
    elif current_direction == "down":
        y += 2

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Move up
        y -= 2
        current_direction = "up"
    if keys[pygame.K_s]:  # Move down
        y += 2
        current_direction = "down"
    if keys[pygame.K_a]:  # Move left
        x -= 2
        current_direction = "left"
    if keys[pygame.K_d]:  # Move right
        x += 2
        current_direction = "right"

    # Update display
    pygame.display.update()  # Use update instead of flip

    # Cap the frame rate
    clock.tick(60)
    
pygame.quit()
sys.exit()
