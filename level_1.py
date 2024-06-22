import pygame
import sys
import random
from pygame import mixer

def main():
    # Initialize Pygame
    pygame.init()

    pygame.mixer.init()
    click_sound = pygame.mixer.Sound("assets/enterface_click_2.mp3")

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 720, 720
    PLAYER_WIDTH, PLAYER_HEIGHT = 200, 200
    PLAYER_SPEED = 5
    JUMP_VELOCITY = -15
    GRAVITY = 0.5
    FRAME_RATE = 60
    WORLD_WIDTH = 1600
    PLAYER_MAX_HEALTH = 100

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Neon Veil")

    # Update constants based on actual screen size
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

    # Function to extract frames from the sprite sheet and scale them
    def extract_frames(sheet, frame_width, frame_height, num_frames, scale_width, scale_height):
        frames = []
        sheet_width, sheet_height = sheet.get_size()
        for i in range(num_frames):
            x = (i * frame_width) % sheet_width
            y = (i * frame_width) // sheet_width * frame_height
            if x + frame_width > sheet_width or y + frame_height > sheet_height:
                print(f"Skipping frame {i} as it goes out of bounds.")
                continue
            frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (scale_width, scale_height))
            frames.append(frame)
        return frames

    # Load sprite sheets for idle, running, jumping, and punching animations
    try:
        idle_sprite_sheet = pygame.image.load("mc/mc_idle.png").convert_alpha()
        idle_left_sprite_sheet = pygame.transform.flip(idle_sprite_sheet, True, False)  # Flipped version for idle left
        running_sprite_sheet = pygame.image.load("mc/mc_run.png").convert_alpha()
        running_left_sprite_sheet = pygame.transform.flip(running_sprite_sheet, True, False)  # Flipped version for running left
        jump_sprite_sheet = pygame.image.load("mc/mc_jump.png").convert_alpha()
        jump_left_sprite_sheet = pygame.transform.flip(jump_sprite_sheet, True, False)  # Flipped version for jumping left
        punch_sprite_sheet = pygame.image.load("mc/mc_punch.png").convert_alpha()
        punch_left_sprite_sheet = pygame.transform.flip(punch_sprite_sheet, True, False)  # Flipped version for punching left
        death_sprite_sheet = pygame.image.load("mc/mc_death.png").convert_alpha()
    except pygame.error:
        print("Error loading sprite sheets. Please check the path.")
        pygame.quit()
        sys.exit()

    # Extract and scale frames from the sprite sheets
    idle_frames = extract_frames(idle_sprite_sheet, 48, 48, 4, PLAYER_WIDTH, PLAYER_HEIGHT)
    idle_frames_left = extract_frames(idle_left_sprite_sheet, 48, 48, 4, PLAYER_WIDTH, PLAYER_HEIGHT)
    running_frames = extract_frames(running_sprite_sheet, 48, 48, 6, PLAYER_WIDTH, PLAYER_HEIGHT)
    running_frames_left = extract_frames(running_left_sprite_sheet, 48, 48, 6, PLAYER_WIDTH, PLAYER_HEIGHT)
    jump_frames = extract_frames(jump_sprite_sheet, 48, 48, 4, PLAYER_WIDTH, PLAYER_HEIGHT)
    jump_frames_left = extract_frames(jump_left_sprite_sheet, 48, 48, 4, PLAYER_WIDTH, PLAYER_HEIGHT)
    punch_frames = extract_frames(punch_sprite_sheet, 48, 48, 6, PLAYER_WIDTH, PLAYER_HEIGHT)
    punch_frames_left = extract_frames(punch_left_sprite_sheet, 48, 48, 6, PLAYER_WIDTH, PLAYER_HEIGHT)
    death_frames = extract_frames(death_sprite_sheet, 48, 48, 6, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.idle_frames = idle_frames
            self.idle_frames_left = idle_frames_left
            self.running_frames = running_frames
            self.running_frames_left = running_frames_left
            self.jump_frames = jump_frames
            self.jump_frames_left = jump_frames_left
            self.punch_frames = punch_frames
            self.punch_frames_left = punch_frames_left
            self.image = self.idle_frames[0]
            self.rect = self.image.get_rect()
            self.rect.x = 100
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100
            self.velocity_y = 0
            self.on_ground = False
            self.frame_index = 0
            self.animation_speed = 0.1  # Control the speed of the animation
            self.last_update = pygame.time.get_ticks()
            self.current_frames = self.idle_frames
            self.facing_left = False
            self.health = PLAYER_MAX_HEALTH
            self.is_punching = False  # Add a flag to track punching state
            self.punch_duration = 500  # Duration of the punch animation in milliseconds
            self.punch_start_time = 0  # Time when the punch animation started

        def update(self):
        # Apply gravity
            self.velocity_y += GRAVITY

        # Check for player input
            keys = pygame.key.get_pressed()

            if keys[pygame.K_z] and self.on_ground:
                self.is_punching = True
                self.punch_start_time = pygame.time.get_ticks()
                self.current_frames = self.punch_frames if not self.facing_left else self.punch_frames_left

            if self.is_punching:
                if pygame.time.get_ticks() - self.punch_start_time > self.punch_duration:
                    self.is_punching = False
                    self.frame_index = 0  # Reset the frame index after punching

            if not self.is_punching:
                if keys[pygame.K_LEFT]:
                    self.rect.x -= PLAYER_SPEED
                    self.facing_left = True
                    if self.on_ground:
                        self.current_frames = self.running_frames_left
                    else:
                        self.current_frames = self.jump_frames_left
                elif keys[pygame.K_RIGHT]:
                    self.rect.x += PLAYER_SPEED
                    self.facing_left = False
                    if self.on_ground:
                        self.current_frames = self.running_frames
                    else:
                        self.current_frames = self.jump_frames
                else:
                    if self.on_ground:
                        self.current_frames = self.idle_frames_left if self.facing_left else self.idle_frames
                    else:
                        self.current_frames = self.jump_frames if not self.facing_left else self.jump_frames_left

                if keys[pygame.K_SPACE] and self.on_ground:
                    self.velocity_y = JUMP_VELOCITY
                    self.on_ground = False
                    self.current_frames = self.jump_frames if not self.facing_left else self.jump_frames_left

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

                # Reset to idle or running animation after landing
                if self.current_frames in [self.jump_frames, self.jump_frames_left]:
                    self.current_frames = self.idle_frames_left if self.facing_left else self.idle_frames if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) else (self.running_frames_left if keys[pygame.K_LEFT] else self.running_frames)

            # Update animation
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 / (FRAME_RATE * self.animation_speed):
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.current_frames):
                    self.frame_index = 0
                self.image = self.current_frames[self.frame_index]

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

    def draw_health_bar(surface, x, y, percentage):
        BAR_WIDTH = 200
        BAR_HEIGHT = 25
        fill = percentage * BAR_WIDTH / 100
        border_color = (255, 255, 255)
        fill_color = (0, 255, 0)

        border_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

        pygame.draw.rect(surface, fill_color, fill_rect)
        pygame.draw.rect(surface, border_color, border_rect, 2)

    # Create player
    player = Player()
    
    # Load the background image
    try:
        background_image = pygame.image.load("assets/Background1.png")
        background_image = pygame.transform.scale(background_image, (WORLD_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        print("Error loading background image. Please check the path.")
        pygame.quit()
        sys.exit()

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

        # Update all sprites
        all_sprites.update()

        # Scroll the camera with the player
        camera_x = max(0, min(player.rect.centerx - SCREEN_WIDTH // 2, WORLD_WIDTH - SCREEN_WIDTH))

        # Draw everything
        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(background_image, (0 - camera_x, 0))  # Draw background
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect.topleft - pygame.Vector2(camera_x, 0))

        # Draw the health bar
        draw_health_bar(screen, 10, 10, player.health)

        pygame.display.flip()
        clock.tick(FRAME_RATE)  # Limit the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()