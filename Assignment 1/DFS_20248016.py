import pygame
import random
from collections import deque  
from collections import OrderedDict

pygame.init()

# Screen dimensions
screen_width = 300
screen_height = 300

# Grid and Cell size dimensions
cell_size = 60  # Adjusted for 20x20 grid to fit in the 600x600 window
grid_width = 5
grid_height = 5

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
light_blue = (173, 216, 230) 
yellow = (255, 255, 0)  

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Vacuum Cleaner')

# Load and scale the vacuum cleaner icon
vacuum_icon = pygame.image.load('vacuum_icon.png')
vacuum_icon = pygame.transform.scale(vacuum_icon, (cell_size, cell_size))
# Load and scale the dirt icon
dirt_icon = pygame.image.load('dust_icon.png')
dirt_icon = pygame.transform.scale(dirt_icon, (cell_size, cell_size))

# Initialize exactly eight unique dirt positions
dirt_positions = set()
cleaned_positions = set()  
while len(dirt_positions) < 5:
    dirt_positions.add((random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)))


class VacuumCleaner:
    def __init__(self):
        self._position = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
        
        self.visited = OrderedDict()

    def location_sensor(self):
        """Returns the current position of the vacuum as a tuple, acting as the location sensor."""
        return self._position

    def dirt_sensor(self):
        """Checks if there is dirt at the vacuum's current position, acting as the dirt sensor."""
        return self.location_sensor() in dirt_positions

    def position_to_label(self, position):
        row, col = position
        return col + 1 + row * grid_width

    def actuator_DFS(self):
        starting_label = self.position_to_label(self.location_sensor())
        print(f"Starting position: {starting_label}")

        screen.fill(black)  # Clear screen
        draw_grid_and_vacuum()  # Redraw grid with new vacuum position
        pygame.display.flip()  # Update display
        pygame.time.delay(1000) # Slow down the movement for visualization
        
        # TODO 
        # You only need to fill out actuator_DFS part.
        # You don't need to use other libraries because every library you need is already implemented. 
        # Use OrderedDict() to store visited location.
        
        # For each iteration, you should update screen.
        # You must use below code snippet for EVERY ITERATION to successfully implement Coding Assignment.
        '''
            screen.fill(black)
            draw_grid_and_vacuum()
            pygame.display.flip()
            pygame.time.delay(500)
        '''
        
        # Also, You need to print out Current Vacuum Position, Whether you sucked dirt, etc. Below is code snippet related to them.
        '''
            print(f"Current Vacuum Position: {self.position_to_label({current Position of Vacuum})}")
        '''
        '''
            print(f"Sucked dirt at: {self.position_to_label({current Position of Vacuum})}")
        '''
        
        # Write your code below here
        
        # Stack for DFS 
        stack = []
        stack.append((self.location_sensor(), []))  # Each stack item stores a position and its path
        
        while stack:
            current_position, current_path = stack.pop()  # Pop a cell and its path from the stack
            
           # Check if the current position
            if current_position in self.visited:
                continue
            
            self.visited[current_position] = True  # Mark cell as goal
            
            # Get target coordinates for the current position
            target_x = current_position[1]
            target_y = current_position[0]
            
            # Move the vacuum cleaner one square at a time towards the target position
            while self._position != current_position:
                current_x, current_y = self._position[1], self._position[0]
                dx, dy = 0, 0

                # Calculate the direction of movement
                if current_x < target_x:
                    dx = 1
                elif current_x > target_x:
                    dx = -1
                elif current_y < target_y:
                    dy = 1
                elif current_y > target_y:
                    dy = -1

                # Update the vacuum cleaner's position
                current_x += dx
                current_y += dy
                self._position = (current_y, current_x)  # Update vacuum position
                
                # Print each move of the cleaner
                move_label = self.position_to_label((current_y, current_x))
                # print(f"Moving to square {move_label}")
                print(f"Current Vacuum Position: {move_label} -> Target Position: {self.position_to_label(current_position)}")
                
                # Redraw the grid and vacuum cleaner
                screen.fill(black)
                draw_grid_and_vacuum()  
                pygame.display.flip()
                pygame.time.delay(800)  

            # Show the target square where the vacuum cleaner should visit
            current_pos_label = self.position_to_label(current_position)
            # print(f"Current Vacuum Position: {current_pos_label}")

            # Check if the current position has dirt
            if current_position in dirt_positions and current_position in self.visited:
                dirt_positions.remove(current_position)  # Clean dirt
                cleaned_positions.add(current_position)  # Add to cleaned positions
                print(f"Sucked dirt at: {current_pos_label}")

            # Check if all dirt has been cleaned
            if not dirt_positions:
                print("All dirty squares visited. Cleaning complete.")
                return current_path  # Return the shortest path
            
            # Push neighboring cells onto the stack
            row, col = current_position
            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            for neighbor in neighbors:
                if 0 <= neighbor[0] < grid_height and 0 <= neighbor[1] < grid_width:
                    if neighbor not in self.visited:  # Check neighbor
                        stack.append((neighbor, current_path + [current_position]))  # Push onto stack with updated path

        print("No solution found.")
        return None
        
        # Write your code above here.

def draw_grid_and_vacuum():
    for x in range(grid_height):
        for y in range(grid_width):
            rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
            if (x, y) in cleaned_positions:  # Check if the cell has been cleaned
                pygame.draw.rect(screen, yellow, rect)  # Fill cleaned cell with yellow
            elif (x, y) in vacuum.visited:  # Check if the cell is visited
                pygame.draw.rect(screen, light_blue, rect)  # Fill visited cell with light blue
            else:
                pygame.draw.rect(screen, white, rect, 1)  # Draw border for unvisited cells
            if (x, y) in dirt_positions:
                screen.blit(dirt_icon, (y * cell_size, x * cell_size))
    
    vacuum_pos = vacuum.location_sensor()
    screen.blit(vacuum_icon, (vacuum_pos[1] * cell_size, vacuum_pos[0] * cell_size))

vacuum = VacuumCleaner()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    vacuum.actuator_DFS()
    if not dirt_positions:
        break

pygame


