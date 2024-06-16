import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    pygame.mixer.init()
    click_sound = pygame.mixer.Sound("assets/enterface_click_2.mp3")

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 720, 720
    PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
    PLAYER_SPEED = 5
    JUMP_VELOCITY = -10
    GRAVITY = 0.1
    FRAME_RATE = 60

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Animated Sprite Sheet Example")

    # Load sprite sheet
    try:
        sprite_sheet = pygame.image.load("mc/mc_idle.png").convert_alpha()
    except pygame.error:
        print("Error loading sprite sheet. Please check the path.")
        pygame.quit()
        sys.exit()

    # Function to extract frames from the sprite sheet
    def extract_frames(sheet, frame_width, frame_height, num_frames):
        frames = []
        sheet_width, sheet_height = sheet.get_size()
        for i in range(num_frames):
            x = (i * frame_width) % sheet_width
            y = (i * frame_width) // sheet_width * frame_height
            frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frames.append(frame)
        return frames

    # Extract frames from the sprite sheet
    frame_width, frame_height = 48, 48  # Size of each frame in the sprite sheet
    num_frames = 4  # Number of frames in the animation
    frames = extract_frames(sprite_sheet, frame_width, frame_height, num_frames)

    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = frames[0]
            self.rect = self.image.get_rect()
            self.rect.x = 100
            self.rect.y = SCREEN_HEIGHT - frame_height - 100
            self.velocity_y = 0
            self.on_ground = False
            self.frame_index = 0
            self.animation_speed = 0.1  # Control the speed of the animation
            self.last_update = pygame.time.get_ticks()

        def update(self):
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
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.velocity_y = 0
                self.on_ground = True

            # Update animation
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 / FRAME_RATE:
                self.last_update = now
                self.frame_index += self.animation_speed
                if self.frame_index >= len(frames):
                    self.frame_index = 0
                self.image = frames[int(self.frame_index)]

    def draw_text(surface, text, size, color, x, y):
        font = pygame.font.Font("assets/cyb3.ttf", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

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
                            import menu
                            menu.main_menu()
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
                                import menu
                                click_sound.play()
                                if i == 0:  # Resume
                                    paused = False
                                elif i == 1:  # Quit
                                    import menu
                                    menu.main_menu()

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
        all_sprites.update()

        # Draw background color
        screen.fill((0, 0, 0))

        # Draw all sprites
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FRAME_RATE)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()