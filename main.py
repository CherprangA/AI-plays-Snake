import pygame
import random
import heapq  # For priority queue used in A* search

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20  # Size of each grid cell
GRID_WIDTH = 20  # Number of cells horizontally
GRID_HEIGHT = 20  # Number of cells vertically
WIDTH = GRID_SIZE * GRID_WIDTH  # Screen width
HEIGHT = GRID_SIZE * GRID_HEIGHT  # Screen height

# Colors
WHITE = (255, 255, 255)  # Background color
BLUE = (0, 0, 255)  # Snake color
RED = (255, 0, 0)  # Food color
GREEN = (0, 255, 0)  # Score text color

# Clock to control FPS
clock = pygame.time.Clock()

# Snake and food initialization
snake = [(10, 10)]  # Snake starts in the middle of the grid
direction = (0, -1)  # Initial direction (up)
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))  # Random food position
score = 0  # Initial score

# Heuristic function for A* (Manhattan distance)
def heuristic(a, b):
    """Calculate Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Get valid neighbors for a given position
def get_neighbors(node):
    """Return valid neighbors of a node (up, down, left, right)."""
    neighbors = [
        (node[0] + 1, node[1]),  # Right
        (node[0] - 1, node[1]),  # Left
        (node[0], node[1] + 1),  # Down
        (node[0], node[1] - 1),  # Up
    ]
    # Filter out neighbors that are out of bounds or part of the snake's body
    valid_neighbors = [
        n for n in neighbors
        if 0 <= n[0] < GRID_WIDTH and 0 <= n[1] < GRID_HEIGHT and n not in snake
    ]
    return valid_neighbors

# A* search algorithm to find the shortest path
def a_star_search(start, goal):
    """Find the shortest path from start to goal using A*."""
    open_set = []  # Priority queue for nodes to explore
    heapq.heappush(open_set, (0, start))  # Add the start node with priority 0
    came_from = {}  # Track the path
    g_score = {start: 0}  # Cost from start to each node
    f_score = {start: heuristic(start, goal)}  # Estimated total cost (g + h)

    while open_set:
        _, current = heapq.heappop(open_set)  # Get the node with the lowest f_score

        if current == goal:  # If we reached the goal, reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()  # Reverse the path to get it from start to goal
            return path

        for neighbor in get_neighbors(current):  # Explore neighbors
            tentative_g_score = g_score[current] + 1  # Cost to reach the neighbor
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                # Update the path and scores if this path is better
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))  # Add to queue

    return None  # Return None if no path is found

# Flood fill algorithm to check if a move is safe
def flood_fill(snake, start):
    """Simulate flood fill to determine reachable area."""
    visited = set()  # Track visited nodes
    stack = [start]  # Stack for DFS

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                stack.append(neighbor)

    return len(visited)  # Return the size of the reachable area

# Function to generate new food
def generate_food(snake):
    """Generate a new food position that is not on the snake."""
    while True:
        new_food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if new_food not in snake:
            return new_food

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI-Plays-Snake")

print("Starting the game")
running = True

while running:
    pygame.event.pump()  # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(
            screen,
            BLUE,
            (
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            ),
        )

    # Draw the food
    pygame.draw.rect(
        screen,
        RED,
        (
            food[0] * GRID_SIZE,
            food[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        ),
    )

    # Use A* to find the path to the food
    path = a_star_search(snake[0], food)

    if path and len(path) > 0:
        # If a path is found, calculate the direction to the next step
        next_step = path[0]
        direction = (next_step[0] - snake[0][0], next_step[1] - snake[0][1])
    else:
        # If no path is found, fallback to the current direction
        pass

    # Simulate the move and check if it's safe using flood fill
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    if flood_fill(snake, new_head) < len(snake):
        # If the move is unsafe, fallback to the current direction
        direction = (0, -1)  # Default to moving up

    # Move the snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    # Check if the snake eats the food
    if new_head == food:
        score += 1
        food = generate_food(snake)  # Generate new food
    else:
        snake.pop()  # Remove the tail if no food is eaten

    # Check for collisions
    if new_head in snake[1:] or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
        print(f"Game Over! Final Score: {score}")
        running = False

    # Display the score on the screen
    font_score = pygame.font.Font(None, 36)
    score_text = font_score.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()