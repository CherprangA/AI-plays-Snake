import pygame

class Movement:
    def __init__(self, x, y, keys):
        self.x = x
        self.y = y
        self.keys = keys
        
    def new_position(self, x, y, keys, current_direction):
        if keys[pygame.K_LEFT]:
            x -= 2
            current_direction = "left"
        if keys[pygame.K_RIGHT]:
            x += 2
            current_direction = "right"
        if keys[pygame.K_UP]:
            y -= 2
            current_direction = "up"
        if keys[pygame.K_DOWN]:
            y += 2
            current_direction = "down"
        
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if current_direction == "left":
                x -= 2
            elif current_direction == "right":
                x += 2
            elif current_direction == "up":
                y -= 2
            elif current_direction == "down":
                y += 2
        
            
        if x > 640:
            x = -60
        if y > 480:
            y = -60
            
        print(x, y, current_direction, "*")
        
        return (x, y, current_direction)