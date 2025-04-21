import pygame

        
def get_direction(directions, current_direction):


    current_direction = current_direction # Default direction
    if directions[0]:
        current_direction = "left"
        
    if directions[1]:
        current_direction = "right"
        
    if directions[2]:
        current_direction = "up"
        
    if directions[3]:            
        current_direction = "down"
    
    return current_direction

def check_collision(x, y, food_x, food_y):
    if x < food_x + 60 and x + 60 > food_x and y < food_y + 60 and y + 60 > food_y:
        return True
    return False
