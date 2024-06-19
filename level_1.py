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
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    PLAYER_WIDTH, PLAYER_HEIGHT = 70, 70  # Increased size to make the player larger
    PLAYER_SPEED = 3
    JUMP_VELOCITY = -5
    GRAVITY = 0.1
    FRAME_RATE = 60
    WORLD_WIDTH = 1600
    PLAYER_HEALTH = 100  # Initial health value
    HEALTH_BAR_DISPLAY_TIME = 2000  # Time in milliseconds to show the health bar after being attacked
    MOB_ATTACK_COOLDOWN = 1000  # Cooldown time in milliseconds for mob attacks

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
            self.speed = 0.5  # Adjust speed as needed
            self.attack_damage = 10  # Damage inflicted on the player per attack
            self.frame_index = 0
            self.animation_speed = 0.1
            self.last_update = pygame.time.get_ticks()
            self.health = 50  # Initial health value
            self.max_health = 50  # Maximum health value
            self.last_attacked_time = 0  # Time when the mob was last attacked
            self.last_attack_time = 0  # Time when the mob last attacked

        def update(self, player):
            # Check if player is nearby
            if self.is_player_nearby(player):
                # Move towards the player
                if self.rect.x < player.rect.x:
                    self.rect.x += self.speed
                elif self.rect.x > player.rect.x:
                    self.rect.x -= self.speed

                # Attack the player if within range and cooldown period has passed
                if self.rect.colliderect(player.rect):
                    now = pygame.time.get_ticks()
                    if now - self.last_attack_time > MOB_ATTACK_COOLDOWN:
                        player.decrease_health(self.attack_damage)
                        self.last_attack_time = now

            # Update animation
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 / (FRAME_RATE * self.animation_speed):
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.frames):
                    self.frame_index = 0
                self.image = self.frames[self.frame_index]

        def is_player_nearby(self, player):
            # Define a distance threshold for "nearby"
            distance_threshold = 200  # Adjust as needed
            return abs(self.rect.centerx - player.rect.centerx) < distance_threshold

        def decrease_health(self, amount):
            self.health -= amount
            self.last_attacked_time = pygame.time.get_ticks()
            if self.health <= 0:
                self.kill()  # Remove the mob from all sprite groups

        def draw_health_bar(self, surface):
            now = pygame.time.get_ticks()
            if now - self.last_attacked_time < HEALTH_BAR_DISPLAY_TIME:
                # Calculate width of health bar
                bar_length = 50
                bar_height = 5
                fill = (self.health / self.max_health) * bar_length
                outline_rect = pygame.Rect(self.rect.x, self.rect.y - 10, bar_length, bar_height)
                fill_rect = pygame.Rect(self.rect.x, self.rect.y - 10, fill, bar_height)
                pygame.draw.rect(surface, (255, 0, 0), fill_rect)
                pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

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

    # Sprite group for mobs
    mob_sprites = pygame.sprite.Group()
    mob_sprites.add(mob1)

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
            self.attack_cooldown = 500  # Cooldown time in milliseconds
            self.last_attack_time = 0  # Time when the player last attacked

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

            if keys[pygame.K_SPACE]:
                self.jump()

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

        def jump(self):
            if self.on_ground:
                self.velocity_y = JUMP_VELOCITY
                self.on_ground = False
        
        def attack(self):
            now = pygame.time.get_ticks()
            if now - self.last_attack_time > self.attack_cooldown:
                self.last_attack_time = now
                return True
            return False

        def decrease_health(self, amount):
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.game_over()

        def game_over(self):
            global running
            running = False
            show_game_over_screen()

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

    def show_game_over_screen():
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main()  # Restart the game
                    elif event.key == pygame.K_ESCAPE:
                        import menu
                        menu.main_menu()  # Go back to main menu

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_x, mouse_y = event.pos
                        # Check if the restart button is clicked
                        if 540 <= mouse_x <= 740 and 400 <= mouse_y <= 440:
                            main()  # Restart the game
                        elif 540 <= mouse_x <= 740 and 460 <= mouse_y <= 500:
                            import menu
                            menu.main_menu()  # Go back to main menu

            screen.fill((0, 0, 0))  # Fill the screen with black
            draw_text(screen, 'You Died', 74, (255, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

            # Draw restart button
            pygame.draw.rect(screen, (0, 255, 0), (540, 400, 200, 40))  # Restart button
            pygame.draw.rect(screen, (255, 0, 0), (540, 460, 200, 40))  # Main menu button

            draw_text(screen, 'Restart', 36, (0, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
            draw_text(screen, 'Restart', 36, (0, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

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
                elif event.key == pygame.K_SPACE:
                    if player.attack():
                        for mob in mob_sprites:
                            if player.rect.colliderect(mob.rect):
                                mob.decrease_health(10)  # Adjust damage as needed

        # Update all sprites
        all_sprites.update()
        mob_sprites.update(player)

        # Remove killed mobs from sprite group
        for mob in mob_sprites:
            if not mob.alive():
                mob_sprites.remove(mob)

        # Check if player is alive
        if player.health <= 0:
            player.game_over()

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
            mob.draw_health_bar(screen)

        # Draw health bar
        player.draw_health_bar(screen, 50, 30)

        pygame.display.flip()
        clock.tick(FRAME_RATE)  # Limit the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
