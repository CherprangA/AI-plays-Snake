import pygame
import sys
import random
import time
import json
import pickle

# pygbag only degbug statemtents
# Uncomment the following line if you want to use pygbag for debugging
# import js

# js.console.log("This is a debug message")

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

#------------------define all the mechanics------------------#
def reset_game():
    global snake, food_x, food_y, current_direction, running, game_over, score
    snake = [(5, 5)]
    food_x = random.randint(0, NUM_COLS - 1)
    food_y = random.randint(0, NUM_ROWS - 1)
    current_direction = "right"
    running = True
    game_over = False
    score = 0


#----------------END of defining all the mechanics------------------#


#------------------define all the variables------------------#

# Set up the screen
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# grid mechanics
GRID_SIZE = 30  # Size of each grid cell in pixels
NUM_ROWS = HEIGHT // GRID_SIZE
NUM_COLS = WIDTH // GRID_SIZE


# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock to control FPS
clock = pygame.time.Clock()


# Snake and food initial positions
snake = [(5, 5)] # list to track snake body positions
score = 0
food_x = random.randint(0, NUM_COLS - 1)
food_y = random.randint(0, NUM_ROWS - 1)

current_direction = "right"


# Initialize game sate
game_over = False
running = True
#----------------END of defining all variables------------------#




# Full screen for deployment
# screen_info = pygame.display.Info()
# screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
pygame.display.set_caption("AI-Plays-Snake")




print("Starting the game")
while True:
    while running:
        pygame.event.pump()  # Ensure events are processed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with white
        screen.fill(WHITE)    
        
        
        # Draw the snake
        for segment in snake:
            pygame.draw.rect(screen, BLUE, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
        # Draw the food
        pygame.draw.rect(screen, RED, (food_x * GRID_SIZE, food_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # # Simulate the agent's actions
        observation = [segment[0] * GRID_SIZE / WIDTH, segment[0] * GRID_SIZE / HEIGHT, food_x / WIDTH, food_y / HEIGHT]  # Normalize positions
        action = agent.predict(observation)
        print(f"Agent chose action: {action}")
        keys = pygame.key.get_pressed()
        
        directions = [keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]]
        current_direction = snake_mechanics.get_direction(directions, current_direction)
        
        # Update snake position based on direction
        head_x, head_y = snake[0]
        if current_direction == "right":
            head_x += 1
        elif current_direction == "left":
            head_x -= 1
        elif current_direction == "up":
            head_y -= 1
        elif current_direction == "down":
            head_y += 1
        
        # Check for collision with the edges (Game Over)
        if head_x < 0 or head_x >= NUM_COLS or head_y < 0 or head_y >= NUM_ROWS:
            running = False
            game_over = True
            
        # Check for collision with the snake's own body (Game Over)
        if (head_x, head_y) in snake:
            running = False
            game_over = True
  
        # Add the new head position to the snake
        snake.insert(0, (head_x, head_y))

        

        # # Simulate the environment for 10 timesteps
        # for step in range(10):
        #     observation = [0.0, 0.1, 0.2, 0.3]  # Dummy observation for testing
        #     action = agent.predict(observation)
        #     # print(f"Step {step + 1}: Agent chose action {action}")

        # time.sleep(1)  # Slow down the loop for better visibility

        
        
        # Check for collision with food
        if head_x == food_x and head_y == food_y:
            food_x = random.randint(0, NUM_COLS - 1)
            food_y = random.randint(0, NUM_ROWS - 1)
            score += 1  # Increment the score
        else:
            # Remove the last segment of the snake to maintain its length
            snake.pop()

        
        # Display the score on the screen
        font_score = pygame.font.Font(None, 36)  # Font for the score
        score_text = font_score.render(f"Score: {score}", True, GREEN)
        screen.blit(score_text, (10, 10))  # Display the score at the top-left corner
        
        # Update display
        pygame.display.update()  # Use update instead of flip

        # Cap the frame rate
        clock.tick(10)
    
    # Handle game over state
    while game_over:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to Restart", True, BLUE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.update()

        # Handle events for restarting or quitting
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Restart the game
            reset_game()
        
        if keys[pygame.K_q]:  # Quit the game
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
