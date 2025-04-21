import json
import numpy as np
import pygame
import random

# Load the policy weights from the JSON file
with open("snake_policy_weights.json", "r") as f:
    policy_weights = json.load(f)
policy_weights = {k: np.array(v) for k, v in policy_weights.items()}
print("✅ Policy weights loaded successfully!")

# Load the action space
with open("snake_action_space.json", "r") as f:
    action_space = json.load(f)
print(f"✅ Action space loaded: {action_space['num_actions']} actions")

# Define a lightweight policy class
class SnakePolicy:
    def __init__(self, weights):
        self.weights = weights

        # Transpose the weights for the first layer to match the expected input shape
        self.weights["mlp_extractor.policy_net.0.weight"] = np.array(self.weights["mlp_extractor.policy_net.0.weight"]).T

        # Transpose the weights for the final layer to match the expected input shape
        self.weights["action_net.weight"] = np.array(self.weights["action_net.weight"]).T

    def forward(self, x):
        # Implement the forward pass manually using numpy
        x = np.dot(x, self.weights["mlp_extractor.policy_net.0.weight"]) + self.weights["mlp_extractor.policy_net.0.bias"]
        x = np.maximum(0, x)  # ReLU
        x = np.dot(x, self.weights["mlp_extractor.policy_net.2.weight"]) + self.weights["mlp_extractor.policy_net.2.bias"]
        x = np.maximum(0, x)  # ReLU
        x = np.dot(x, self.weights["action_net.weight"]) + self.weights["action_net.bias"]
        return x
    
policy = SnakePolicy(policy_weights)

# Preprocess the observation to match the input size of the policy network
# Preprocess the observation to match the input size of the policy network
def preprocess_observation(observation):
    # No padding is needed; return the observation as is
    return np.expand_dims(observation, axis=0)  # Add batch dimension

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
GREEN = (0, 255, 0)

# Clock to control FPS
clock = pygame.time.Clock()

# Initialize the game state
def reset_game():
    global snake, food_x, food_y, direction, score, running, game_over
    snake = [(5, 5)]
    food_x = random.randint(0, NUM_COLS - 1)
    food_y = random.randint(0, NUM_ROWS - 1)
    direction = "right"
    score = 0
    running = True
    game_over = False

# Main game loop
reset_game()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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

        # Get the current observation
        head_x, head_y = snake[0]
        observation = np.array([head_x, head_y, food_x, food_y, len(snake)], dtype=np.float32)

        # Preprocess the observation
        observation = preprocess_observation(observation)

        # Predict the action using the policy
        action_probs = policy.forward(observation)
        action = np.argmax(action_probs)  # Get the action with the highest probability
        
        print(f"Action: {action}")
        
        # Update snake position based on direction
        if action == 0 and direction != "down":
            direction = "up"
        elif action == 1 and direction != "up":
            direction = "down"
        elif action == 2 and direction != "right":
            direction = "left"
        elif action == 3 and direction != "left":
            direction = "right"

        # Calculate new head position
        if direction == "right":
            head_x += 1
        elif direction == "left":
            head_x -= 1
        elif direction == "up":
            head_y -= 1
        elif direction == "down":
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
            exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()