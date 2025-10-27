import pygame
from random import randint
from pygame.locals import KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT


# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Base class for all game objects."""
    
    def __init__(self, position=None, color=WHITE):
        """Initialize game object with position and color."""
        self.position = position or (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = color
    
    def draw(self, surface):
        """Abstract method to draw the object on the surface."""
        pass


class Apple(GameObject):
    """Apple object that snake can eat."""
    
    def __init__(self):
        """Initialize apple with red color and random position."""
        super().__init__(color=RED)
        self.randomize_position()
    
    def randomize_position(self):
        """Set apple to a random position on the grid."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
    
    def draw(self, surface):
        """Draw the apple on the surface."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Snake(GameObject):
    """Snake object that player controls."""
    
    def __init__(self):
        """Initialize snake with green color and starting position."""
        super().__init__(color=GREEN)
        self.reset()
    
    def reset(self):
        """Reset snake to initial state."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
    
    def update_direction(self):
        """Update direction based on next_direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def get_head_position(self):
        """Return the position of snake's head."""
        return self.positions[0]
    
    def move(self):
        """Move the snake one step in current direction."""
        self.update_direction()
        head = self.get_head_position()
        
        # Calculate new head position with wrap-around
        new_x = (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        
        # Check for self-collision (only if snake is long enough)
        if len(self.positions) > 3 and new_head in self.positions[3:]:
            self.reset()
            return
        
        # Store last position for cleaning
        if len(self.positions) == self.length:
            self.last = self.positions[-1]
        else:
            self.last = None
        
        # Add new head
        self.positions.insert(0, new_head)
        
        # Remove tail if not growing
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def draw(self, surface):
        """Draw the snake on the surface."""
        for position in self.positions:
            rect = pygame.Rect(
                (position[0], position[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)
        
        # Clean last position
        if self.last:
            rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BLACK, rect)


def handle_keys(snake):
    """
    Handle keyboard input for snake direction.
    
    Args:
        snake: Snake object to control
        
    Returns:
        bool: False if game should quit, True otherwise
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            return False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                return False
            elif event.key == K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
    return True


def main():
    """Main game function."""
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    
    snake = Snake()
    apple = Apple()
    running = True
    max_length = 1
    
    while running:
        running = handle_keys(snake)
        if not running:
            break
        
        snake.move()
        
        # Check if snake ate apple
        if snake.get_head_position() == apple.position:
            snake.length += 1
            max_length = max(max_length, snake.length)
            
            # Update window title with max length
            title = f'Изгиб Питона - Рекорд: {max_length}'
            pygame.display.set_caption(title)
            
            # Find new position for apple that's not on snake
            while True:
                apple.randomize_position()
                if apple.position not in snake.positions:
                    break
        
        # Draw everything
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        
        clock.tick(10)  # Control game speed


if __name__ == '__main__':
    main()
