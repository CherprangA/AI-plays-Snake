import pygame
import sys
import random
import time
import json
import pickle
from RL_agent import SimpleAgent

from scripts import snake_mechanics

# Load the action space
with open("action_space.json", "r") as f:
    action_space_data = json.load(f)
num_actions = action_space_data["num_actions"]
print(f"✅ Action space loaded: {num_actions} actions")

# Load the RL agent
with open("rl_agent.pkl", "rb") as f:
    agent = pickle.load(f)
print("✅ RL agent loaded successfully!")

# Initialize Pygame
pygame.init()

# Set up the screen

# small window for testing
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# snake moving distance in single step
MOVE_DISTANCE = 5

# detecte collision with food
COLLISION_WITH_FOOD = False


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
food_x = random.randint(0, WIDTH - 60)
food_y = random.randint(0, HEIGHT - 60)
current_direction = "right"

while running:
    pygame.event.pump()  # Ensure events are processed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)    
    
    
    # Draw the snake
    pygame.draw.rect(screen, BLUE, (x, y, 60, 60))
    
    # Draw the food
    if COLLISION_WITH_FOOD:
        food_x = random.randint(0, WIDTH - 60)
        food_y = random.randint(0, HEIGHT - 60)   
        COLLISION_WITH_FOOD = False 
    pygame.draw.rect(screen, RED, (food_x, food_y, 60, 60))
    
    # Simulate the agent's actions
    observation = [x / WIDTH, y / HEIGHT, food_x / WIDTH, food_y / HEIGHT]  # Normalize positions
    action = agent.predict(observation)
    print(f"Agent chose action: {action}")
    
    
    # Prevent the box from going out of bounds
    if x >= WIDTH - 60:
        x = WIDTH - 60
    if y >= HEIGHT - 60:
        y = HEIGHT - 60
    if x <= 0:
        x = 0
    if y <= 0:
        y = 0
    
        
    if current_direction == "right":
        x += MOVE_DISTANCE
    elif current_direction == "left":
        x -= MOVE_DISTANCE
    elif current_direction == "up":
        y -= MOVE_DISTANCE
    elif current_direction == "down":
        y += MOVE_DISTANCE
        
    COLLISION_WITH_FOOD = snake_mechanics.check_collision(x, y, food_x, food_y)
    
    keys = pygame.key.get_pressed()
    
    directions = [keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]]
    current_direction = snake_mechanics.get_direction(directions, current_direction)
    
    # Simulate the environment for 10 timesteps
    for step in range(10):
        observation = [0.0, 0.1, 0.2, 0.3]  # Dummy observation for testing
        action = agent.predict(observation)
        print(f"Step {step + 1}: Agent chose action {action}")

    # time.sleep(1)  # Slow down the loop for better visibility

    # Update display
    pygame.display.update()  # Use update instead of flip

    # Cap the frame rate
    clock.tick(60)
    
pygame.quit()
sys.exit()
