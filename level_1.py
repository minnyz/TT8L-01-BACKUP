import pygame
import sys
import random
import math
from pygame import mixer

def main():
    # Initialize Pygame
    pygame.init()

    pygame.mixer.init()
    click_sound = pygame.mixer.Sound("assets/enterface_click_2.mp3")
    explosion_sound = pygame.mixer.Sound("assets/explosion.mp3")
    jump_sound = pygame.mixer.Sound("assets/jump.wav")
    #running_sound = pygame.mixer.Sound("assets/running.mp3")
    punch_sound = pygame.mixer.Sound("assets/punch.wav")
    die_sound = pygame.mixer.Sound("assets/die.wav")
    
    
    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    POPUP_WIDTH, POPUP_HEIGHT = 1280, 720
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

    # Load sprite sheets 
    try:
        idle_sprite_sheet = pygame.image.load("assets/Mc/mc_idle.png").convert_alpha()
        idle_left_sprite_sheet = pygame.transform.flip(idle_sprite_sheet, True, False)  # Flipped version for idle left
        running_sprite_sheet = pygame.image.load("assets/Mc/mc_run.png").convert_alpha()
        running_left_sprite_sheet = pygame.transform.flip(running_sprite_sheet, True, False)  # Flipped version for running left
        jump_sprite_sheet = pygame.image.load("assets/Mc/mc_jump.png").convert_alpha()
        jump_left_sprite_sheet = pygame.transform.flip(jump_sprite_sheet, True, False)  # Flipped version for jumping left
        punch_sprite_sheet = pygame.image.load("assets/Mc/mc_punch.png").convert_alpha()
        punch_left_sprite_sheet = pygame.transform.flip(punch_sprite_sheet, True, False)  # Flipped version for punching left
        death_sprite_sheet = pygame.image.load("assets/Mc/mc_death.png").convert_alpha()
        mob_sprite_sheet = pygame.image.load("assets/mobsLow/1/Scan.png").convert_alpha()
        bullet_image = pygame.image.load('assets/mobsLow/1/c4.png').convert_alpha()
        mob_death_sprite_sheet = pygame.image.load("assets/mobsLow/1/Death.png").convert_alpha()
        boss_sprite_sheet = pygame.image.load("assets/mobsHigh/Idle.png").convert_alpha()
        boss_death_sprite_sheet = pygame.image.load("assets/mobsHigh/Death.png").convert_alpha()
        boss_attack_sprite_sheet = pygame.image.load("assets/mobsHigh/Attack2.png").convert_alpha()
    except pygame.error as e:
        print(f"Error loading sprite sheets: {e}")
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
    death_frames = extract_frames(death_sprite_sheet, 48, 48, 6, 10, 10)
    mob_frames = extract_frames(mob_sprite_sheet, 48, 48, 8, 120, 120) 
    mob_death_frames = extract_frames(mob_death_sprite_sheet, 48, 48, 8, 120, 120)  
    boss_idle_frames = extract_frames(boss_sprite_sheet, 72, 72, 4, 100, 100)
    boss_death_frames = extract_frames(boss_death_sprite_sheet, 72, 72, 6, 100, 100)
    boss_attack_frames = extract_frames(boss_attack_sprite_sheet, 72, 72, 6, 100, 100)
    
    # Boss Class
    class Boss(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.idle_frames = boss_idle_frames  # Replace with actual frames
            self.attack_frames = boss_attack_frames  # Replace with actual frames
            self.death_frames = boss_death_frames  # Replace with actual frames
            self.image = self.idle_frames[0]
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.attack_distance = 300  # Example distance at which boss starts attacking
            self.attack_delay = 3000  # Example delay between attacks in milliseconds
            self.last_attack = pygame.time.get_ticks()
            self.last_update = pygame.time.get_ticks()
            self.velocity = pygame.math.Vector2(0, 0)  # Adjust if boss moves
            self.frame_index = 0
            self.animation_speed = 0.1
            self.health = 200  # Example boss health
            self.is_dead = False
            self.death_time = 0

        def update(self, player):
            if self.is_dead:
                # Handle death animation
                now = pygame.time.get_ticks()
                if now - self.last_update > 1000 * self.animation_speed:
                    self.last_update = now
                    self.frame_index += 1
                    if self.frame_index < len(self.death_frames):
                        self.image = self.death_frames[self.frame_index]
                    else:
                        self.kill()  # Remove the boss after death animation finishes
                return
            
            # Example: Boss attacks player within a certain distance
            if abs(self.rect.centerx - player.rect.centerx) < self.attack_distance:
                self.shoot(player)

            # Example: Update animation
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 * self.animation_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.idle_frames):
                    self.frame_index = 0
                self.image = self.idle_frames[self.frame_index]

        def shoot(self, player):
            now = pygame.time.get_ticks()
            if now - self.last_attack > self.attack_delay:
                self.last_attack = now
                # Implement shooting logic towards the player
                pass  # Placeholder for shooting logic

        def take_damage(self, damage):
            self.health -= damage
            if self.health <= 0:
                self.die()

        def die(self):
            if not self.is_dead:
                self.is_dead = True
                self.death_time = pygame.time.get_ticks()
                self.frame_index = 0
                self.last_update = pygame.time.get_ticks()
                self.image = self.death_frames[self.frame_index]
                # Add sound or any other effects on boss death
                self.kill()  # Remove the boss after death animation finishes

        def draw_health_bar(self, surface):
            if not self.is_dead:
                BAR_WIDTH = 200
                BAR_HEIGHT = 25
                fill = BAR_WIDTH * (self.health / 500)  # Adjust as per boss's max health
                border_color = (255, 255, 255)
                fill_color = (0, 255, 0)

                health_bar_x = self.rect.centerx - BAR_WIDTH // 2
                health_bar_y = self.rect.top - 10

                border_rect = pygame.Rect(health_bar_x, health_bar_y, BAR_WIDTH, BAR_HEIGHT)
                fill_rect = pygame.Rect(health_bar_x, health_bar_y, fill, BAR_HEIGHT)

                pygame.draw.rect(surface, fill_color, fill_rect)
                pygame.draw.rect(surface, border_color, border_rect, 2)

    # Bullet class
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, target_x, target_y):
            super().__init__()
            self.image = bullet_image
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.speed = 4

            # Calculate direction towards the player
            direction = pygame.math.Vector2(target_x - x, target_y - y).normalize()
            self.velocity = direction * self.speed

        def update(self):
            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y

            # Remove the bullet if it moves off the screen
            if self.rect.right < 0 or self.rect.left > WORLD_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
                self.kill()

    # Class Mob
    class Mob(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.idle_frames = mob_frames  # Use the frames loaded from mob sprite sheet
            self.death_frames = mob_death_frames  # Add death frames
            self.image = self.idle_frames[0]
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.shooting_distance = 200  # Distance at which the mob starts shooting
            self.shoot_delay = 2000  # Delay between shots in milliseconds
            self.last_shot = pygame.time.get_ticks()
            self.last_update = pygame.time.get_ticks()  # Initialize last_update here
            self.velocity = pygame.math.Vector2(0, 0)  # Add velocity if needed for movement
            self.frame_index = 0  # Initialize frame index for animation
            self.animation_speed = 0.1  # Animation speed
            self.health = 100
            self.is_dead = False  # Flag to check if the mob is dead
            self.death_time = 0  # Time when the mob died
            self.mobs_died_sound = pygame.mixer.Sound("assets/mob_die.wav")
            
        def update(self, *args):
            if self.is_dead:
                # Handle death animation
                print(f"Death animation: frame_index={self.frame_index}, len(death_frames)={len(self.death_frames)}")
                now = pygame.time.get_ticks()
                if now - self.last_update > 1000 * self.animation_speed:
                    self.last_update = now
                    self.frame_index += 1
                    if self.frame_index < len(self.death_frames):
                        self.image = self.death_frames[self.frame_index]
                    else:
                        print("Removing mob after death animation.")
                        self.kill()  # Remove the mob after the death animation finishes
                return

            if args and isinstance(args[0], pygame.sprite.Sprite):
                player = args[0]
                # Check distance to player
                if abs(self.rect.centerx - player.rect.centerx) < self.shooting_distance:
                    self.shoot(player)

            # Update animation
            now = pygame.time.get_ticks()
            if now - self.last_update > 1000 * self.animation_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.idle_frames):
                    self.frame_index = 0
                self.image = self.idle_frames[self.frame_index]

        def shoot(self, player):
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                # Calculate direction towards the player
                direction = pygame.math.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery).normalize()

                # Adjust the starting point of the bullet's trajectory towards the player's position
                start_x = self.rect.centerx + direction.x * 10  # Adjust '20' as needed for deeper hits
                start_y = self.rect.centery + direction.y * 10  # Adjust '20' as needed for deeper hits

                bullet = Bullet(start_x, start_y, player.rect.centerx, player.rect.centery)
                bullet.velocity = direction * bullet.speed  # Update bullet's velocity towards the player
                all_sprites.add(bullet)
                bullets.add(bullet)

        def take_damage(self, damage):
            self.health -= damage
            if self.health <= 0:
                self.die()  # Switch to die method when health drops to zero

        def die(self):
            if not self.is_dead:
                self.is_dead = True  # Flag to indicate the mob is dead
                self.death_time = pygame.time.get_ticks()  # Record the time of death
                self.frame_index = 0  # Reset frame index for death animation
                self.last_update = pygame.time.get_ticks()  # Reset the last update time for death animation
                self.image = self.death_frames[self.frame_index]  # Start with the first death frame
                self.mobs_died_sound.play() 
            
        def draw_health_bar(self, surface):
            if not self.is_dead:  # Only draw health bar if the mob is not dead
                BAR_WIDTH = 40
                BAR_HEIGHT = 6
                fill = BAR_WIDTH * (self.health / 100)
                border_color = (255, 255, 255)
                fill_color = (0, 255, 0)

                # Fixed position on the screen
                health_bar_x = self.rect.centerx - BAR_WIDTH // 2
                health_bar_y = self.rect.top - 10

                # Draw the border of the health bar
                border_rect = pygame.Rect(health_bar_x - camera_x, health_bar_y, BAR_WIDTH, BAR_HEIGHT)
                fill_rect = pygame.Rect(health_bar_x - camera_x, health_bar_y, fill, BAR_HEIGHT)

                pygame.draw.rect(surface, fill_color, fill_rect)
                pygame.draw.rect(surface, border_color, border_rect, 1)

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
            self.death_frames = death_frames
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
            self.is_punching = False  # Add a flag to track punching state
            self.punch_duration = 500  # Duration of the punch animation in milliseconds
            self.punch_start_time = 0  # Time when the punch animation started
            self.facing_left = False
            self.health = PLAYER_MAX_HEALTH
            self.is_dead = False 
            self.death_time = 0 
        
        def attack(self, mobs):
            attack_hitbox = pygame.sprite.Sprite()  # Create a sprite for attack hitbox
            attack_hitbox.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width + 50, self.rect.height + 20)
            
            # Check for collisions with mobs
            hits = pygame.sprite.spritecollide(attack_hitbox, mobs, False)
            
            # Deal damage to each mob hit
            for mob in hits:
                mob.take_damage(10)  # Adjust damage as needed
  
        def update(self):
            # Apply gravity
            self.velocity_y += GRAVITY
            
        # Check for player input
            keys = pygame.key.get_pressed()

            if keys[pygame.K_z] and self.on_ground:
                punch_sound.play()
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
                    jump_sound.play() # jump sound 
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
           
            # Check if player health drops to zero
            if self.is_dead:
                return  # If dead, do not update further

            # Check conditions for dying
            if self.health <= 0:
                self.die()
        
        def die(self):
            die_sound.play()  # Call the play method correctly
            self.current_frames = death_frames  # Switch to death frames
            self.frame_index = 0  # Reset frame index for death animation
            self.is_dead = True  # Flag to track if player is dead
            self.death_time = pygame.time.get_ticks()  # Record time of death


        # Wait for 2 seconds before showing game over popup
        pygame.time.set_timer(pygame.USEREVENT, 3000)  # 3000 milliseconds (3 seconds)
        
        def handle_event(self, event):
            if event.type == pygame.USEREVENT and self.is_dead:
                show_death_popup()  # Show game over popup after delay
    
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
    
    
    # Function to show death popup and handle restart/main menu options
    def show_death_popup():
        pygame.init()
        die_sound.play()
        screen = pygame.display.set_mode((POPUP_WIDTH, POPUP_HEIGHT),pygame.FULLSCREEN)
        popup_rect = screen.get_rect()
        
        # Larger font size for the "You Died!" text
        popup_font_large = pygame.font.Font("assets/cyb3.ttf", 80) 
        # Regular font size for the options
        popup_font = pygame.font.Font("assets/cyb3.ttf", 40)  
        
        popup_color = pygame.Color(50, 50, 50, 150)
        option_color = (255, 0, 0)
        options = ["Restart", "Main Menu"]
        selected_option = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        click_sound.play()
                        if selected_option == 0:  # Restart
                            main()  # Restart the game
                        elif selected_option == 1:  # Main Menu
                            import menu
                            menu.main_menu()  # Go back to main menu

            # Draw popup background
            popup_surface = pygame.Surface((popup_rect.width, popup_rect.height), pygame.SRCALPHA)  # Create a surface with alpha channel
            popup_surface.fill(popup_color)  # Fill the surface with the transparent gray color
            screen.blit(popup_surface, (0,0))  # Blit the popup surface onto the screen

            # Draw popup text
            popup_text_large = popup_font_large.render("You Died!", True, option_color)
            screen.blit(popup_text_large, (popup_rect.centerx - popup_text_large.get_width() // 2, popup_rect.top + 20))

            # Draw options with regular font size, adjusted lower
            options_start_y = popup_rect.top + 300  # Increase this value to lower the options
            for i, option in enumerate(options):
                text = popup_font.render(option, True, option_color if i == selected_option else (150, 150, 150))
                screen.blit(text, (popup_rect.centerx - text.get_width() // 2, options_start_y + i * 50))

            pygame.display.flip()
    
    # Sprite groups
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    # Create player
    player = Player()
    all_sprites.add(player)

    # Add mobs to the game
    mob_positions = [(400, SCREEN_HEIGHT - PLAYER_HEIGHT - 100), (800, SCREEN_HEIGHT - PLAYER_HEIGHT - 100)]
    for pos in mob_positions:
        mob = Mob(pos[0], pos[1])
        all_sprites.add(mob)
        mobs.add(mob)
    
    # Add boss to the game
    boss = Boss(1200, SCREEN_HEIGHT - PLAYER_HEIGHT - 100)  # Example position
    all_sprites.add(boss)
    mobs.add(boss)
    
    # Load the background image
    try:
        background_image = pygame.image.load("assets/Background1.png")
        background_image = pygame.transform.scale(background_image, (WORLD_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        pygame.quit()
        sys.exit()

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
                elif event.key == pygame.K_z:
                    player.attack(mobs)
            # Handle player event to check for delayed game over popup
            player.handle_event(event)
        
        # Update all sprites
        for sprite in all_sprites:
            if isinstance(sprite, Boss):
                sprite.update(player)
            else:
                sprite.update()  # Pass player object to update mobsa
        
        # Check for bullet collisions with the player
        hits = pygame.sprite.spritecollide(player, bullets, True)
        for hit in hits:
            player.health -= 10  # Reduce player health by 10 on hit
            explosion_sound.play()  # Play explosion sound
            if player.health <= 0:
                show_death_popup() # End the game if health reachaes zero
        
        # Allow mobs to shoot
        for mob in mobs:
            mob.update(player)
        
        # Check mob health and remove dead mobs
        for mob in mobs.copy():  
            if mob.health <= 0:
                mob.kill()
        
        # Scroll the camera with the player
        camera_x = max(0, min(player.rect.centerx - SCREEN_WIDTH // 2, WORLD_WIDTH - SCREEN_WIDTH))

        # Draw everything
        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(background_image, (0 - camera_x, 0))  # Draw background
        
        # Draw all sprites
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
            if isinstance(sprite, Mob):
                sprite.draw_health_bar(screen)
            elif isinstance(sprite, Boss):
                sprite.draw_health_bar(screen)
        
        # Draw boss
        screen.blit(boss.image, boss.rect)
        
        # Check boss health and remove if dead
        if boss.health <= 0:
            boss.kill()
        
        # Draw health bars for mobs
        for mob in mobs:
            mob.draw_health_bar(screen)
        
        # Draw the health bar for players
        draw_health_bar(screen, 10, 10, player.health)
        
        # Draw health bar for boss
        boss.draw_health_bar(screen)
        
        pygame.display.flip()
        clock.tick(FRAME_RATE)  # Limit the frame rate

    pygame.quit()

def show_death_popup():
    # Existing code for game over popup
    pass

if __name__ == "__main__":
    main()
show_death_popup()
