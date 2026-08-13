import pygame

class SolitaryPlayer:
    def __init__(self, start_x, start_y):
        # Position and Movement Configurations
        self.pos = pygame.math.Vector2(start_x, start_y)
        self.speed = 5
        self.is_moving = False

        # Grid box dimensions matching our 32 * 32 pixel spritesheets
        self.frame_w = 32
        self.frame_h = 32
        self.scale_factor = 3.0     # Scales the sprite up to 3 times (96 * 96) visually on screen

        # Screen size configurations
        self.screen_width = 800
        self.screen_height = 600

        # State and Direction Tracking
        self.current_dir = "down"
        self.current_frame = 0

        # Independent Animation Speed Configurations (NB: Lower = Faster)
        self.idle_cooldown = 320
        self.walk_cooldown = 120
        self.last_update = pygame.time.get_ticks()

        # Load and cleanly split both animation sheets
        self.idle_animations, self.walk_animations = self._load_and_slice_assets()

        # Foundational physics box for our team's collision logic
        self.rect = pygame.Rect(
            self.pos.x,
            self.pos.y,
            int(self.frame_w * self.scale_factor),
            int(self.frame_h * self.scale_factor)
        )

    # FIXED INDENTATION: This method is now properly placed inside the class block
    def _load_and_slice_assets(self):
        try:
            walk_sheet = pygame.image.load("placeholder_sheet.png").convert_alpha()
            idle_sheet = pygame.image.load("idleholder_sheet.png").convert_alpha()
        except pygame.error as e:
            print(f"Asset Load Error inside player.py: {e}")
            walk_sheet = pygame.Surface((self.frame_w * 4, self.frame_h * 5), pygame.SRCALPHA)
            idle_sheet = pygame.Surface((self.frame_w * 4, self.frame_h * 5), pygame.SRCALPHA)

        # Map grid rows cleanly according to the canvas design
        row_map = {
            "down": 0,
            "right": 1,
            "up": 4
        }

        # Empty folders/groups to hold the sliced images
        idle_pool = {"down": [], "right": [], "up": []}
        walk_pool = {"down": [], "right": [], "up": []}

        # Cutting columns 0 to 3 out of each mapped horizontal
        for direction, row_index in row_map.items():
            new_size = (int(self.frame_w * self.scale_factor), int(self.frame_h * self.scale_factor))

            for col_index in range(4):
                # Calculates precise pixel coordinates where the current box starts
                x = col_index * self.frame_w
                y = row_index * self.frame_h
                rect = pygame.Rect(x, y, self.frame_w, self.frame_h)

                # Slices Canvas, Removes the black background, and scales it up
                frame_idle = pygame.Surface(rect.size, pygame.SRCALPHA)
                frame_idle.blit(idle_sheet, (0,0), rect)
                frame_idle.set_colorkey((0, 0, 0))
                frame_idle = pygame.transform.scale(frame_idle, new_size)
                idle_pool[direction].append(frame_idle)

                # FIXED TYPO: Changed Surfacw to Surface
                frame_walk = pygame.Surface(rect.size, pygame.SRCALPHA)
                frame_walk.blit(walk_sheet, (0, 0), rect)
                frame_walk.set_colorkey((0, 0, 0))
                frame_walk = pygame.transform.scale(frame_walk, new_size)
                walk_pool[direction].append(frame_walk)
            
        # FIXED INDENTATION: Moved return outside the loop so it slices all rows
        return idle_pool, walk_pool
    
    # FIXED: Added wall_rects parameter to accept the map data from main.py
    def update(self, wall_rects):
        # Handles keyboard tracking inputs and blocks movement into wall colliders 
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        
        # Calculate individual step movement increments
        move_x = 0
        move_y = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  move_x = -self.speed; self.current_dir = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: move_x = self.speed;  self.current_dir = "right"
        elif keys[pygame.K_w] or keys[pygame.K_UP]:    move_y = -self.speed; self.current_dir = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:  move_y = self.speed;  self.current_dir = "down"

        if move_x != 0 or move_y != 0:
            self.is_moving = True
            
            # 1. HORIZONTAL AXIS PHYSICS STEP
            self.pos.x += move_x
            self.rect.x = int(self.pos.x)
            for wall in wall_rects:
                if self.rect.colliderect(wall):
                    if move_x > 0: self.rect.right = wall.left
                    if move_x < 0: self.rect.left = wall.right
                    self.pos.x = self.rect.x

            # 2. VERTICAL AXIS PHYSICS STEP
            self.pos.y += move_y
            self.rect.y = int(self.pos.y)
            for wall in wall_rects:
                if self.rect.colliderect(wall):
                    if move_y > 0: self.rect.bottom = wall.top
                    if move_y < 0: self.rect.top = wall.bottom
                    self.pos.y = self.rect.y
        else:
            self.is_moving = False

        # Cycle animation frame tracks
        active_cooldown = self.walk_cooldown if self.is_moving else self.idle_cooldown
        if now - self.last_update >= active_cooldown:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 4

            
            # Both sheets have exactly 4 frames (0, 1, 2, 3), so it restarts at 0 after frame 3
            if self.current_frame >= 4:
                self.current_frame = 0

    # Uses the right image as the left image
    def draw(self, screen):
        lookup_dir = "right" if self.current_dir == "left" else self.current_dir

        # Fetches the active image from the walk/idle sheet based on movement state
        if self.is_moving:
            sprite_to_draw = self.walk_animations[lookup_dir][self.current_frame]
        else:
            sprite_to_draw = self.idle_animations[lookup_dir][self.current_frame]

        if self.current_dir == "left":
            sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)
        
        screen.blit(sprite_to_draw, self.rect)

if __name__ == "__main__":
    import sys
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    protagonist = SolitaryPlayer(352, 252)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        protagonist.update()
        screen.fill((50, 60, 75))
        protagonist.draw(screen)
        pygame.display.flip()
        clock.tick(60)

