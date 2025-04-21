import random
import numpy as np
import gym
from gym import spaces

# Constants for reward values
BASE_REWARD_FOOD = 10
BASE_PENALTY_DEATH = -20
TIME_PENALTY = -0.01

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

        # Initialize step counter for time penalty
        self.steps_taken = 0

        self.reset()

    def reset(self):
        """ Resets the game to its initial state. """
        self.snake = [(5, 5)]  # Starting position of the snake
        self.food = (random.randint(0, self.num_cols - 1), random.randint(0, self.num_rows - 1))  # Random food placement
        self.direction = "right"  # Default starting direction
        self.score = 0
        self.done = False
        self.steps_taken = 0
        return self._get_observation()

    def step(self, action):
        """ Executes a single step in the game. """
        self.steps_taken += 1

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

        # Calculate distances for distance-based reward
        previous_distance_to_food = abs(self.snake[0][0] - self.food[0]) + abs(self.snake[0][1] - self.food[1])
        new_distance_to_food = abs(head_x - self.food[0]) + abs(head_y - self.food[1])

        # Check for collisions
        if self._check_collision(head_x, head_y):
            self.done = True
            # Game over penalty scaling based on snake length
            game_over_penalty = BASE_PENALTY_DEATH - len(self.snake) * 2
            return self._get_observation(), game_over_penalty, self.done, {}

        # Add new head position
        self.snake.insert(0, (head_x, head_y))

        # Check for food
        if (head_x, head_y) == self.food:
            self.food = (random.randint(0, self.num_cols - 1), random.randint(0, self.num_rows - 1))
            self.score += 1

            # Variable reward for food based on difficulty
            difficulty_multiplier = self._calculate_food_difficulty()
            reward = BASE_REWARD_FOOD * difficulty_multiplier
        else:
            self.snake.pop()  # Remove tail

            # Distance-based reward formula
            distance_reward = 1 / (new_distance_to_food + 1) - 1 / (previous_distance_to_food + 1)

            # Time-based penalty
            time_penalty = TIME_PENALTY * self.steps_taken

            reward = distance_reward + time_penalty

        return self._get_observation(), reward, self.done, {}

    def _get_observation(self):
        """ Returns the current state of the environment. """
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        return np.array([head_x, head_y, food_x, food_y, len(self.snake)], dtype=np.int32)

    def _check_collision(self, head_x, head_y):
        """ Checks if the snake collides with the walls or itself. """
        return (
            head_x < 0 or head_x >= self.num_cols or
            head_y < 0 or head_y >= self.num_rows or
            (head_x, head_y) in self.snake
        )

    def _calculate_food_difficulty(self):
        """ Calculates a difficulty multiplier for food based on its position. """
        food_x, food_y = self.food
        # Calculate proximity to walls
        wall_distances = [
            food_x,  # Distance to left wall
            self.num_cols - food_x - 1,  # Distance to right wall
            food_y,  # Distance to top wall
            self.num_rows - food_y - 1  # Distance to bottom wall
        ]
        min_wall_distance = min(wall_distances)

        # Calculate difficulty multiplier (closer to walls = higher difficulty)
        difficulty_multiplier = 1 + (1 / (min_wall_distance + 1))
        return difficulty_multiplier