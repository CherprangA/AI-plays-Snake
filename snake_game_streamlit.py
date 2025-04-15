import pygame

def run_snake_game():
    # Initialize pygame
    pygame.init()

    # Set up the display
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Snake Game")

    # Set up the font
    font = pygame.font.Font(None, 36)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        # Calculate seconds elapsed
        seconds_elapsed = pygame.time.get_ticks() // 1000

        # Clear the screen
        screen.fill((0, 0, 0))

        # Render the text
        text = font.render(f"Seconds Elapsed: {seconds_elapsed}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    run_snake_game()