import pygame
import numpy as np
import gradio as gr

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.Surface((WIDTH, HEIGHT))  # Create an off-screen surface for rendering

# Set up the font
font = pygame.font.Font(None, 36)


def render_frame():
    """
    Renders a single frame of the game and returns it as a NumPy array.
    """
    # Calculate seconds elapsed
    seconds_elapsed = pygame.time.get_ticks() // 1000

    # Clear the screen
    screen.fill((0, 0, 0))

    # Render the text
    text = font.render(f"Seconds Elapsed: {seconds_elapsed}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Convert the pygame surface to a NumPy array
    frame = pygame.surfarray.array3d(screen)
    return np.transpose(frame, (1, 0, 2))  # Transpose to match Gradio's expected format


def snake_game(action):
    """
    Handles user input (action) and returns the updated game frame.
    """
    if action == "Quit":
        pygame.quit()
        return "Game Over!", None

    # Render the current frame
    frame = render_frame()
    return None, frame


# Define Gradio interface
actions = ["Continue", "Quit"]
interface = gr.Interface(
    fn=snake_game,
    inputs=gr.Dropdown(choices=actions, label="Action"),
    outputs=[
        gr.Textbox(label="Game Status"),
        gr.Image(label="Game Screen"),
    ],
    live=True,
)

if __name__ == "__main__":
    interface.launch()