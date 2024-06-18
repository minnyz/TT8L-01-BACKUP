import pygame
import sys
from pygame import mixer

def main():
    # Initialize Pygame
    pygame.init()

    pygame.mixer.init()
    click_sound = pygame.mixer.Sound("assets/enterface_click_2.mp3")

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    PLAYER_WIDTH, PLAYER_HEIGHT = 70, 70  # Increased size to make the player larger
    PLAYER_SPEED = 5
    JUMP_VELOCITY = -10
    GRAVITY = 0.1
    FRAME_RATE = 60
    WORLD_WIDTH = 1600
    PLAYER_HEALTH = 100  # Initial health value

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

    # Load sprite sheets for idle and running animations
    try:
        idle_sprite_sheet = pygame.image.load("assets/Mc/mc_idle.png").convert_alpha()
        running_sprite_sheet = pygame.image.load("assets/Mc/mc_run.png").convert_alpha()
    except pygame.error:
        print("Error loading sprite sheets. Please check the path.")
        pygame.quit()
        sys.exit()

    # Extract and scale frames from the sprite sheets
    idle_frames = extract_frames(idle_sprite_sheet, 48, 48, 4, PLAYER_WIDTH, PLAYER_HEIGHT)
    running_frames = extract_frames(running_sprite_sheet, 48, 48, 6, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Define Mob class
    class Mob(pygame.sprite.Sprite):
        def __init__(self, x, y, frames):
            super().__init__()
            self.frames = frames
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = 3  # Adjust speed as needed
            self.attack_damage = 10  # Damage inflicted on the player per attack
            self.frame_index = 0
            self.animation_speed = 0.1
            self.last_update = pygame.time.get_ticks()

        def update(self, player):
            # Move towards the player
            if self.rect.x < player.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.speed

            # Update animation
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 / (FRAME_RATE * self.animation_speed):
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.frames):
                    self.frame_index = 0
                self.image = self.frames[self.frame_index]

    # Load sprite sheet for mobs
    try:
        mob_sprite_sheet = pygame.image.load("assets/mobsLow/1/Idle.png").convert_alpha()
    except pygame.error:
        print("Error loading mobs sprite sheet. Please check the path.")
        pygame.quit()
        sys.exit()

    # Extract and scale frames from the sprite sheet for mobs
    mob_frames = extract_frames(mob_sprite_sheet, 48, 48, 4, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Create mobs
    mob1 = Mob(500, SCREEN_HEIGHT - PLAYER_HEIGHT - 100, mob_frames)
    mob2 = Mob(800, SCREEN_HEIGHT - PLAYER_HEIGHT - 100, mob_frames)

    # Sprite group for mobs
    mob_sprites = pygame.sprite.Group()
    mob_sprites.add(mob1, mob2)

    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.idle_frames = idle_frames
            self.running_frames = running_frames
            self.image = self.idle_frames[0]
            self.rect = self.image.get_rect()
            self.rect.x = 100
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100
            self.velocity_y = 0
            self.on_ground = False
            self.frame_index = 0
            self.animation_speed = 0.1
            self.last_update = pygame.time.get_ticks()
            self.current_frames = self.idle_frames
            self.direction = "right"
            self.health = PLAYER_HEALTH  # Initialize health
            self.max_health = PLAYER_HEALTH  # Maximum health

        def update(self):
            # Apply gravity
            self.velocity_y += GRAVITY

            # Check for player input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= PLAYER_SPEED
                self.current_frames = self.running_frames
                self.direction = "left"
            elif keys[pygame.K_RIGHT]:
                self.rect.x += PLAYER_SPEED
                self.current_frames = self.running_frames
                self.direction = "right"
            else:
                self.current_frames = self.idle_frames

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

            # Update animation
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 / (FRAME_RATE * self.animation_speed):
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.current_frames):
                    self.frame_index = 0
                if self.direction == "right":
                    self.image = self.current_frames[self.frame_index]
                elif self.direction == "left":
                    self.image = pygame.transform.flip(self.current_frames[self.frame_index], True, False)

        def decrease_health(self, amount):
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                # Implement game over logic here if needed

        def draw_health_bar(self, surface, x, y):
            # Calculate width of health bar
            bar_length = 100
            bar_height = 10
            fill = (self.health / self.max_health) * bar_length
            outline_rect = pygame.Rect(x, y, bar_length, bar_height)
            fill_rect = pygame.Rect(x, y, fill, bar_height)
            pygame.draw.rect(surface, (255, 0, 0), fill_rect)
            pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)

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
        mob_sprites.update(player)

        # Scroll the camera with the player
        camera_x = max(0, min(player.rect.centerx - SCREEN_WIDTH // 2, WORLD_WIDTH - SCREEN_WIDTH))

        # Draw everything
        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(background_image, (0 - camera_x, 0))  # Draw background

        # Draw sprites
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect.topleft - pygame.Vector2(camera_x, 0))
        for mob in mob_sprites:
            screen.blit(mob.image, mob.rect.topleft - pygame.Vector2(camera_x, 0))

        # Draw health bar
        player.draw_health_bar(screen, 50, 30)

        pygame.display.flip()
        clock.tick(FRAME_RATE)  # Limit the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
