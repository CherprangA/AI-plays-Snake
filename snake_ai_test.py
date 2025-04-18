import torch
import torch.nn as nn
import numpy as np
import pygame
import random
import json

# Define the policy architecture (same as used during training)
class SnakePolicy(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(SnakePolicy, self).__init__()
        self.mlp_extractor = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU()
        )
        self.action_net = nn.Linear(64, output_dim)

    def forward(self, x):
        x = self.mlp_extractor(x)
        x = self.action_net(x)
        return x

# Load the policy weights
input_dim = 5  # Observation space size
output_dim = 4  # Action space size
policy = SnakePolicy(input_dim, output_dim)
policy = torch.load("snake_policy_full.pth", weights_only=False)
policy.eval()
print("✅ Policy loaded successfully!")

# Load the action space
with open("snake_action_space.json", "r") as f:
    action_space = json.load(f)
print(f"✅ Action space loaded: {action_space['num_actions']} actions")

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 30
WIDTH = 1200
HEIGHT = 900
NUM_ROWS = HEIGHT // GRID_SIZE
NUM_COLS = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialize the game state
def reset_game():
    global snake, food, direction, score, running, game_over
    snake = [(5, 5)]
    food = (random.randint(0, NUM_COLS - 1), random.randint(0, NUM_ROWS - 1))
    direction = "right"
    score = 0
    running = True
    game_over = False

# Get the current observation
def get_observation():
    head_x, head_y = snake[0]
    food_x, food_y = food
    return np.array([head_x, head_y, food_x, food_y, len(snake)], dtype=np.float32)

# Render the game
def render():
    screen.fill(WHITE)

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, BLUE, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the food
    pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 255, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

def update_snake(action):
    global running, game_over, score, food, direction

    # Map action to direction
    if action == 0 and direction != "down":
        direction = "up"
    elif action == 1 and direction != "up":
        direction = "down"
    elif action == 2 and direction != "right":
        direction = "left"
    elif action == 3 and direction != "left":
        direction = "right"

    # Calculate new head position
    head_x, head_y = snake[0]
    if direction == "right":
        head_x += 1
    elif direction == "left":
        head_x -= 1
    elif direction == "up":
        head_y -= 1
    elif direction == "down":
        head_y += 1
        
    print(f"Predicted action: {action}")
    print(f"Current direction: {direction}")

    # Check for collisions
    if head_x < 0 or head_x >= NUM_COLS or head_y < 0 or head_y >= NUM_ROWS or (head_x, head_y) in snake:
        running = False
        game_over = True
        return

    # Add new head position
    snake.insert(0, (head_x, head_y))

    # Check for food
    if (head_x, head_y) == food:
        food = (random.randint(0, NUM_COLS - 1), random.randint(0, NUM_ROWS - 1))
        score += 1
    else:
        # Remove the tail
        snake.pop()
        
        
# Main game loop
reset_game()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

while True:
    while running:
        pygame.event.pump()

        # Get the current observation
        obs = get_observation()

        # Predict the action using the policy

        obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
        
        action, _, _ = policy(obs_tensor)  # Extract the first value (action)
        action = action.item()  # Convert to a Python integer

        # Update the snake's position based on the action
        update_snake(action)

        # Render the game
        render()

        # Cap the frame rate
        clock.tick(10)

    # Game over screen
    while game_over:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to Restart", True, BLUE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        # Handle events for restarting
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()