import pygame

def run_snake_game():
    # initialize pygame
    pygame.init()

    # set up the display
    WIDTH, HEIGHT = 800, 600

    # set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Snake Game")

    # set up the font
    font = pygame.font.Font(None, 36)

    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        # calculate seconds elapsed
        seconds_elapsed = pygame.time.get_ticks() // 1000

        # clear the screen
        screen.fill((0, 0, 0))

        # render the text
        text = font.render(f"Seconds Elapsed: {seconds_elapsed}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # update the display
        pygame.display.flip()

    # quit pygame
    pygame.quit()