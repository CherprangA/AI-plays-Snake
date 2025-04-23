import pygame
import random
import numpy as np
import gymnasium as gym  # Use Gymnasium instead of Gym
from gymnasium import spaces  # Update spaces import

class SnakeEnv(gym.Env):  # Inherit from gymnasium.Env
    def __init__(self, grid_size=25, width=900, height=900):  # Adjust grid_size and dimensions
        super(SnakeEnv, self).__init__()
        self.grid_size = grid_size
        self.width = width
        self.height = height
        self.num_rows = height // grid_size
        self.num_cols = width // grid_size

        # Define the action space (0: up, 1: down, 2: left, 3: right)
        self.action_space = spaces.Discrete(4)

        # Define the observation space (normalized to [0, 1])
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(1, self.num_rows, self.num_cols),  # Add channel dimension
            dtype=np.uint8  # Change dtype to uint8
        )

        self.reset()

    def reset(self, seed=None, options=None):
        # Handle the seed for reproducibility
        super().reset(seed=seed)  # Call the parent class's reset method
        self.np_random, seed = gym.utils.seeding.np_random(seed)

        # Reset the game state
        self.snake = [(5, 5)]
        self.food = (
            self.np_random.integers(0, self.num_cols),  # Use integers instead of randint
            self.np_random.integers(0, self.num_rows)   # Use integers instead of randint
        )
        self.direction = "right"
        self.score = 0
        self.done = False

        return self._get_observation(), {}

    def step(self, action):
        # Map action to direction
        if action == 0 and self.direction != "down":
            self.direction = "up"
        elif action == 1 and self.direction != "up":
            self.direction = "down"
        elif action == 2 and self.direction != "right":
            self.direction = "left"
        elif action == 3 and self.direction != "left":
            self.direction = "right"

        # Update snake position
        head_x, head_y = self.snake[0]
        if self.direction == "right":
            head_x += 1
        elif self.direction == "left":
            head_x -= 1
        elif self.direction == "up":
            head_y -= 1
        elif self.direction == "down":
            head_y += 1

        # Check for collisions
        if head_x < 0 or head_x >= self.num_cols or head_y < 0 or head_y >= self.num_rows or (head_x, head_y) in self.snake:
            self.done = True
            return self._get_observation(), -10, True, False, {}  # Terminated = True, Truncated = False

        # Add new head position
        self.snake.insert(0, (head_x, head_y))

        # Check for food
        if (head_x, head_y) == self.food:
            self.food = (
                self.np_random.integers(0, self.num_cols),
                self.np_random.integers(0, self.num_rows)
            )
            self.score += 1
            reward = 10  # Positive reward for eating food
        else:
            self.snake.pop()  # Remove tail
            reward = -0.1  # Neutral reward for moving

        return self._get_observation(), reward, False, False, {}  # Terminated = False, Truncated = False

    def render(self, mode="human"):
        # Render the game using Pygame
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        screen.fill((255, 255, 255))  # White background

        # Draw the snake
        for segment in self.snake:
            pygame.draw.rect(screen, (0, 0, 255), (segment[0] * self.grid_size, segment[1] * self.grid_size, self.grid_size, self.grid_size))

        # Draw the food
        pygame.draw.rect(screen, (255, 0, 0), (self.food[0] * self.grid_size, self.food[1] * self.grid_size, self.grid_size, self.grid_size))

        pygame.display.flip()

    def _get_observation(self):
        # Create a grid representation of the environment
        grid = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)

        # Mark the snake's body
        for segment in self.snake:
            grid[segment[1], segment[0]] = 255  # Snake body as max value

        # Mark the food
        food_x, food_y = self.food
        grid[food_y, food_x] = 128  # Food as mid value

        # Add a channel dimension (1, num_rows, num_cols)
        return grid[np.newaxis, :, :]