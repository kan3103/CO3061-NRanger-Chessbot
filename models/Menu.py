import pygame 
import sys
class Menu:
    def __init__(self):
        pygame.init()
        self.screen_size = 600
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption('Chess Game Menu')
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.HOVER_COLOR = (100, 100, 100)
        
        # Font
        self.font = pygame.font.Font(None, 48)
        
        # Button dimensions
        self.button_width = 300
        self.button_height = 60
        self.button_margin = 40
        
        # Create buttons
        center_x = self.screen_size // 2 - self.button_width // 2
        center_y = self.screen_size // 2 - self.button_height
        
        self.mode1_rect = pygame.Rect(center_x, center_y, self.button_width, self.button_height)
        self.mode2_rect = pygame.Rect(center_x, center_y + self.button_height + self.button_margin, 
                                    self.button_width, self.button_height)
        
        # Track button hover state
        self.mode1_hover = False
        self.mode2_hover = False

    def draw_title(self):
        title = self.font.render('Chess Game', True, self.BLACK)
        title_rect = title.get_rect(center=(self.screen_size // 2, self.screen_size // 4))
        self.screen.blit(title, title_rect)

    def draw_buttons(self):
        # Mode 1 button
        color = self.HOVER_COLOR if self.mode1_hover else self.GRAY
        pygame.draw.rect(self.screen, color, self.mode1_rect, border_radius=10)
        text = self.font.render('Mode 1', True, self.WHITE)
        text_rect = text.get_rect(center=self.mode1_rect.center)
        self.screen.blit(text, text_rect)
        
        # Mode 2 button
        color = self.HOVER_COLOR if self.mode2_hover else self.GRAY
        pygame.draw.rect(self.screen, color, self.mode2_rect, border_radius=10)
        text = self.font.render('Mode 2', True, self.WHITE)
        text_rect = text.get_rect(center=self.mode2_rect.center)
        self.screen.blit(text, text_rect)

    def check_hover(self, mouse_pos):
        self.mode1_hover = self.mode1_rect.collidepoint(mouse_pos)
        self.mode2_hover = self.mode2_rect.collidepoint(mouse_pos)

    def run(self):
        while True:
            self.screen.fill(self.WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEMOTION:
                    self.check_hover(event.pos)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mode1_rect.collidepoint(event.pos):
                        return "blind"
                    elif self.mode2_rect.collidepoint(event.pos):
                        return "heuristic"
            
            self.draw_title()
            self.draw_buttons()
            pygame.display.flip()