import pygame
import random
import numpy as np
import gym
from gym import spaces

class SnakeEnv(gym.Env):
    def __init__(self, grid_size=30, width=1200, height=900):
        super(SnakeEnv, self).__init__()
        self.grid_size = grid_size
        self.width = width
        self.height = height
        self.num_rows = height // grid_size
        self.num_cols = width // grid_size

        # Define the action space (0: up, 1: down, 2: left, 3: right)
        self.action_space = spaces.Discrete(4)

        # Define the observation space
        # Observation: [head_x, head_y, food_x, food_y, snake_length]
        self.observation_space = spaces.Box(
            low=0,
            high=max(self.num_cols, self.num_rows),
            shape=(5,),
            dtype=np.int32
        )

        self.reset()

    def reset(self):
        # Reset the game state
        self.snake = [(5, 5)]
        self.food = (random.randint(0, self.num_cols - 1), random.randint(0, self.num_rows - 1))
        self.direction = "right"
        self.score = 0
        self.done = False
        return self._get_observation()

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
            return self._get_observation(), -10, self.done, {}  # Negative reward for dying

        # Add new head position
        self.snake.insert(0, (head_x, head_y))

        # Check for food
        if (head_x, head_y) == self.food:
            self.food = (random.randint(0, self.num_cols - 1), random.randint(0, self.num_rows - 1))
            self.score += 1
            reward = 10  # Positive reward for eating food
        else:
            self.snake.pop()  # Remove tail
            reward = -0.1  # Neutral reward for moving

        return self._get_observation(), reward, self.done, {}

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
        # Return the state as a numpy array
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        return np.array([head_x, head_y, food_x, food_y, len(self.snake)], dtype=np.int32)