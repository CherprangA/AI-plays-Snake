import numpy as np
import pygame
from stable_baselines3 import PPO
from snake_env import SnakeEnv

# Load the trained CNN policy
model = PPO.load("snake_cnn_policy")
print("✅ Trained CNN policy loaded!")

# Initialize the Snake environment
env = SnakeEnv()

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = env.grid_size
# Scale down the rendering window
WIDTH = env.width // 2  # Reduce width by half
HEIGHT = env.height // 2  # Reduce height by half

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock to control FPS
clock = pygame.time.Clock()

# Main game loop
obs, _ = env.reset()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI-Plays-Snake")

print("Starting the game")
running = True
while running:
    pygame.event.pump()  # Ensure events are processed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the snake
    for segment in env.snake:
        pygame.draw.rect(
            screen,
            BLUE,
            (
                segment[0] * (GRID_SIZE // 2),  # Scale down the snake's position
                segment[1] * (GRID_SIZE // 2),
                GRID_SIZE // 2,  # Scale down the snake's size
                GRID_SIZE // 2,
            ),
        )

    # Draw the food
    pygame.draw.rect(
        screen,
        RED,
        (
            env.food[0] * (GRID_SIZE // 2),  # Scale down the food's position
            env.food[1] * (GRID_SIZE // 2),
            GRID_SIZE // 2,  # Scale down the food's size
            GRID_SIZE // 2,
        ),
    )

    # Predict the action using the policy
    action, _states = model.predict(obs, deterministic=True)

    # Step the environment
    obs, reward, terminated, truncated, info = env.step(action)

    # Check if the game is over
    if terminated or truncated:
        print("Game Over! Restarting...")
        obs, _ = env.reset()  # Reset the environment and continue

    # Display the score on the screen
    font_score = pygame.font.Font(None, 36)  # Font for the score
    score_text = font_score.render(f"Score: {env.score}", True, GREEN)
    screen.blit(score_text, (10, 10))  # Display the score at the top-left corner

    # Update display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(10)

pygame.quit()