import pygame 
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 600

# Grid and Cell size dimensions
cell_size = 200
grid_width = 3
grid_height = 3

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Reflex AI Vacuum Cleaner')

# Load and scale the vacuum cleaner icon
vacuum_icon = pygame.image.load('vacuum_icon.png')
vacuum_icon = pygame.transform.scale(vacuum_icon, (cell_size, cell_size))
# dirt icon
dirt_icon = pygame.image.load('dust_icon.png')
dirt_icon = pygame.transform.scale(dirt_icon, (cell_size, cell_size))

# Initialize exactly three unique dirt positions
#Sets in Python are collections that are unordered, mutable, and do not allow duplicate elements. This characteristic makes sets ideal for storing the dirt positions because each position is unique, and you don't care about the order.
dirt_positions = set()
while len(dirt_positions) < 3:
    dirt_positions.add((random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)))

class VacuumCleaner:
    def __init__(self):
        self.position = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]
#Tuples are used because they are immutable, meaning they can't be changed once created, which is suitable for a simple access to the vacuum's position.    
    def location_sensor(self):
        """Returns the current position of the vacuum as a tuple."""
        return tuple(self.position)
    
    def dirt_sensor(self):
        """Checks if there is dirt at the current position."""
        return self.location_sensor() in dirt_positions
    
    def actuator(self):
        current_pos = self.location_sensor()
        label = str(self.position[1] * grid_width + self.position[0])
        
        if self.dirt_sensor():
            print(f'Vacuum is at: {label}, action: Suck')
            dirt_positions.remove(current_pos)
        else:
            # Enhanced movement logic with direction specific actions
            direction = random.choice(['left', 'right', 'up', 'down'])
            if direction == 'right' and self.position[0] < grid_width - 1:
                self.position[0] += 1
                print(f'Vacuum is at: {label}, action: Move Right')
            elif direction == 'down' and self.position[1] < grid_height - 1:
                self.position[1] += 1
                print(f'Vacuum is at: {label}, action: Move Down')
            elif direction == 'left' and self.position[0] > 0:
                self.position[0] -= 1
                print(f'Vacuum is at: {label}, action: Move Left')
            elif direction == 'up' and self.position[1] > 0:
                self.position[1] -= 1
                print(f'Vacuum is at: {label}, action: Move Up')

vacuum = VacuumCleaner()

def draw_grid_and_vacuum():
    for x in range(grid_height):
        for y in range(grid_width):
            rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, white, rect, 1) #The outline is set to be white and has a thickness of 1 pixel.
            if (x, y) in dirt_positions:
                screen.blit(dirt_icon, (y * cell_size, x * cell_size))

            # Adjusted label calculation for left-to-right labeling
            label = str(y + x * grid_width)
            font = pygame.font.SysFont("Arial", 24) #font type Arial and size 24
            text = font.render(label, True, white)
            
            # Adjusted blit position to match rect positioning
            screen.blit(text, (y * cell_size + cell_size / 2 - text.get_width() / 2, x * cell_size + cell_size / 2 - text.get_height() / 2))
    
    # Ensure vacuum position is correctly interpreted (assuming vacuum.position is [y, x])
    screen.blit(vacuum_icon, (vacuum.position[1] * cell_size, vacuum.position[0] * cell_size))


# Main game loop
running = True
clock = pygame.time.Clock()  #Used to control the framerate.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    draw_grid_and_vacuum()
    vacuum.actuator()
    
    pygame.display.flip()
    clock.tick(1)

pygame.quit()
