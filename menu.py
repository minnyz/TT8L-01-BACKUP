import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 74)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Button class
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BUTTON_COLOR

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = FONT.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(event.pos):
            return True
        return False

# Create play button
play_button = Button("Play", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100)

# Main loop
running = True
menu = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if menu:
            if play_button.handle_event(event):
                menu = False  # Switch to game

    screen.fill(WHITE)

    if menu:
        # Draw play button
        mouse_pos = pygame.mouse.get_pos()
        if play_button.is_hovered(mouse_pos):
            play_button.color = BUTTON_HOVER_COLOR
        else:
            play_button.color = BUTTON_COLOR
        play_button.draw(screen)
    else:
        # Transition to the game
        import main  # Replace with the actual game code module name
        main.main()  # Call the main function of the game code

    pygame.display.flip()

pygame.quit()
sys.exit()
