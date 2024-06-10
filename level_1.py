import pygame
import sys

# Define the Portal class
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 100))  # Dimensions of the portal
        self.image.fill((255, 0, 0))  # Color of the portal (red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define the function to load levels
def load_level(level_number):
    if level_number == 1:
        background_image = pygame.image.load("images/background1.png")
        background_image = pygame.transform.scale(background_image, (1600, 600))  # Use WORLD_WIDTH, WORLD_HEIGHT directly here
        portal = Portal(1600 - 100, 600 - 150)  # Place portal at the end of the level
    elif level_number == 2:
        background_image = pygame.image.load("images/background2.png")
        background_image = pygame.transform.scale(background_image, (1600, 600))
        portal = Portal(1600 - 100, 600 - 150)
    else:
        print(f"Level {level_number} not implemented.")
        pygame.quit()
        sys.exit()
    return background_image, portal

def main():
    # Initialize Pygame
    pygame.init()

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    WORLD_WIDTH, WORLD_HEIGHT = 1600, 600
    PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
    PLAYER_COLOR = (0, 0, 255)
    BACKGROUND_COLOR = (0, 0, 0)
    PLAYER_SPEED = 5
    JUMP_VELOCITY = -10
    GRAVITY = 0.5

    # Set up the display in fullscreen mode
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Neon Veil")

    # Update constants based on actual screen size
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill(PLAYER_COLOR)
            self.rect = self.image.get_rect()
            self.rect.x = 100
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100
            self.velocity_y = 0
            self.on_ground = False

        def update(self, platforms):
            # Apply gravity
            self.velocity_y += GRAVITY

            # Check for player input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.rect.x += PLAYER_SPEED
            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = JUMP_VELOCITY
                self.on_ground = False

            # Update vertical position
            self.rect.y += self.velocity_y

            # Boundary checks within the world
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WORLD_WIDTH:
                self.rect.right = WORLD_WIDTH
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.velocity_y = 0
                self.on_ground = True

    def draw_text(screen, text, size, color, x, y, font_name='Arial'):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

    def pause_menu():
        paused = True
        menu_items = ["Resume", "Main Menu"]
        selected_item = 0

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False  # Resume the game
                    elif event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        if selected_item == 0:  # Resume
                            paused = False
                        elif selected_item == 1:  # Quit
                            pygame.quit()
                            sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    mouse_y = event.pos[1]
                    for i, item in enumerate(menu_items):
                        text_rect = pygame.Rect(0, 0, 200, 50)
                        text_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60)
                        if text_rect.collidepoint(event.pos):
                            selected_item = i
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_y = event.pos[1]
                        for i, item in enumerate(menu_items):
                            text_rect = pygame.Rect(0, 0, 200, 50)
                            text_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60)
                            if text_rect.collidepoint(event.pos):
                                if i == 0:  # Resume
                                    paused = False
                                elif i == 1:  # Quit
                                    pygame.quit()
                                    sys.exit()

            screen.fill((0, 0, 0))  # Fill the screen with black
            draw_text(screen, 'Paused', 74, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

            for i, item in enumerate(menu_items):
                if i == selected_item:
                    color = (255, 255, 0)  # Yellow when selected or hovered
                else:
                    color = (255, 255, 255)  # White when not selected
                draw_text(screen, item, 50, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60)

            pygame.display.flip()
            clock.tick(15)  # Limit the loop to 15 frames per second

    # Create player
    player = Player()

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Camera position
    camera_x = 0

    # Main game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

        # Update sprites
        all_sprites.update([])

        # Adjust camera position to follow the player
        camera_x = player.rect.x - SCREEN_WIDTH // 2
        camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, camera_x))

        # Draw background image relative to camera position
        screen.blit(background_image, (-camera_x, 0))

        # Draw everything relative to camera position
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()