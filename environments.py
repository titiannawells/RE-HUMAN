import pygame
import sys

class Environment:
    def __init__(self):
        # Grid sizes scaled up to 96x96 pixels to fit your screen boundaries
        self.tile_size = 96  
        
        # Deep, unsettling dark atmospheric concrete tones
        self.wall_color = (25, 30, 35)      
        self.floor_color = (12, 14, 16)     
        self.grid_line_color = (20, 24, 28) 

        # =====================================================================
        # BALANCED MAP MATRIX LAYOUT (1 = Solid Wall Block, 0 = Walkway Corridor)
        # =====================================================================
        self.map_grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        # Container array to keep track of wall bounds for collision physics checks
        self.wall_rects = []
        self._build_collision_matrix()

    def _build_collision_matrix(self):
        """ Loops through map grid to generate physical coordinate boxes for walls """
        self.wall_rects.clear()
        for row_idx, row in enumerate(self.map_grid):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    x = col_idx * self.tile_size
                    y = row_idx * self.tile_size
                    rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                    self.wall_rects.append(rect)

    def draw(self, screen):
        """ Renders the base environment tiles and solid structures """
        for row_idx, row in enumerate(self.map_grid):
            for col_idx, tile in enumerate(row):
                x = col_idx * self.tile_size
                y = row_idx * self.tile_size
                tile_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

                if tile == 1:
                    pygame.draw.rect(screen, self.wall_color, tile_rect)
                    pygame.draw.rect(screen, (40, 48, 56), tile_rect, width=1)
                else:
                    pygame.draw.rect(screen, self.floor_color, tile_rect)
                    pygame.draw.rect(screen, (20, 24, 28), tile_rect, width=1)


# =====================================================================
# STANDALONE LOCAL ENVIRONMENT VISUAL TESTER
# =====================================================================
if __name__ == "__main__":
    pygame.init()
    
    # Grid math setup: 9 columns wide, 7 rows high * 96 pixels = 864x672 screen window
    screen = pygame.display.set_mode((864, 672))
    pygame.display.set_caption("Re:Human - Environment Test Canvas")
    clock = pygame.time.Clock()
    
    # Initialize the level system
    level_environment = Environment()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Draw the scene layout
        screen.fill((0, 0, 0))
        level_environment.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
