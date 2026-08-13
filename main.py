import pygame
import sys

# Import your custom standalone modules
from environments import Environment
from player import SolitaryPlayer

class GameEngine:
    def __init__(self):
        pygame.init()
        # Use the exact screen boundaries from your environment test canvas
        self.screen_width = 864
        self.screen_height = 672
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Re:Human - Project Sandbox")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier New", 28, bold=True)
        self.title_font = pygame.font.SysFont("Courier New", 56, bold=True)

        # Global Application State Manager ("MENU", "GAME", "SETTINGS", "CREDITS")
        self.state = "MENU"

        # Initialize environment and spawn player on an open corridor floor tile
        self.level_env = Environment()
        self.player = SolitaryPlayer(96, 96)

        # Define menu button footprint tracking areas centered horizontally
        btn_w, btn_h = 240, 50
        start_x = (self.screen_width // 2) - (btn_w // 2)
        
        self.buttons = {
            "START": pygame.Rect(start_x, 260, btn_w, btn_h),
            "SETTINGS": pygame.Rect(start_x, 330, btn_w, btn_h),
            "CREDITS": pygame.Rect(start_x, 400, btn_w, btn_h),
            "QUIT": pygame.Rect(start_x, 470, btn_w, btn_h)
        }

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            # =====================================================================
            # 1. APPLICATION LEVEL EVENT CAPTURER
            # =====================================================================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "MENU":
                        if self.buttons["START"].collidepoint(mouse_pos):
                            self.state = "GAME"
                        elif self.buttons["SETTINGS"].collidepoint(mouse_pos):
                            self.state = "SETTINGS"
                        elif self.buttons["CREDITS"].collidepoint(mouse_pos):
                            self.state = "CREDITS"
                        elif self.buttons["QUIT"].collidepoint(mouse_pos):
                            pygame.quit(); sys.exit()
                            
                    elif self.state in ["SETTINGS", "CREDITS"]:
                        self.state = "MENU"

            # =====================================================================
            # 2. RUNTIME PHYSICS AND UPDATE STEP
            # =====================================================================
            if self.state == "GAME":
                # Only update player physics vectors when actively inside the game map
                self.player.update(self.level_env.wall_rects)

            # =====================================================================
            # 3. GRAPHICS PAINT LAYER MANAGER
            # =====================================================================
            if self.state == "MENU":
                self._draw_main_menu(mouse_pos)
            elif self.state == "SETTINGS":
                self._draw_sub_menu("SETTINGS", "Controls: WASD or Arrows.\n\nEsc to leave game loop.\n\nClick anywhere to return.")
            elif self.state == "CREDITS":
                self._draw_sub_menu("CREDITS", "Re:Human Thriller Project\n\nDeveloped Solo.\n\nClick anywhere to return.")
            elif self.state == "GAME":
                # Paint scene layout sequentially: Void -> Walls/Floors -> Player
                self.screen.fill((0, 0, 0))
                self.level_env.draw(self.screen)
                self.player.draw(self.screen)

                # Listen for Emergency Escape Key to slide cleanly back to menu loop
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self.state = "MENU"

            pygame.display.flip()
            self.clock.tick(60)

    def _draw_main_menu(self, mouse_pos):
        self.screen.fill((15, 18, 22))

        # Paint Title Text Elements
        title_surf = self.title_font.render("RE:HUMAN", True, (200, 210, 220))
        title_x = (self.screen_width // 2) - (title_surf.get_width() // 2)
        self.screen.blit(title_surf, (title_x, 120))

        # Render menu loop buttons matrix
        for name, rect in self.buttons.items():
            is_hovered = rect.collidepoint(mouse_pos)
            bg_color = (35, 45, 55) if is_hovered else (25, 30, 35)
            text_color = (100, 255, 100) if is_hovered else (150, 160, 170)

            pygame.draw.rect(self.screen, bg_color, rect, border_radius=4)
            pygame.draw.rect(self.screen, (50, 60, 75), rect, width=1, border_radius=4)

            text_surf = self.font.render(name, True, text_color)
            text_x = rect.centerx - (text_surf.get_width() // 2)
            text_y = rect.centery - (text_surf.get_height() // 2)
            self.screen.blit(text_surf, (text_x, text_y))

    def _draw_sub_menu(self, header, body_text):
        self.screen.fill((15, 18, 22))
        head_surf = self.title_font.render(header, True, (200, 210, 220))
        self.screen.blit(head_surf, (50, 80))
        
        lines = body_text.split("\n")
        for idx, line in enumerate(lines):
            body_surf = self.font.render(line, True, (140, 150, 160))
            self.screen.blit(body_surf, (50, 200 + (idx * 40)))

if __name__ == "__main__":
    game = GameEngine()
    game.run()
