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
        self.RED = (144, 238, 144)
        
        # Font
        self.font = pygame.font.Font(None, 48)
        
        # Button dimensions
        self.button_width = 300
        self.button_height = 60
        self.button_margin = 40
        
        # Create buttons
        center_x = self.screen_size // 2 - self.button_width // 2
        center_y = self.screen_size // 2 - self.button_height - self.button_margin
        
        self.heuristic_rect = pygame.Rect(center_x, center_y, 
                                        self.button_width, self.button_height)
        self.blind_rect = pygame.Rect(center_x, 
                                    center_y + self.button_height + self.button_margin,
                                    self.button_width, self.button_height)
        
        # Back button
        self.back_button = pygame.Rect(10, 10, 100, 40)
        
        # Track button hover state
        self.heuristic_hover = False
        self.blind_hover = False
        self.back_hover = False

    def draw_back_button(self):
        color = self.HOVER_COLOR if self.back_hover else self.GRAY
        pygame.draw.rect(self.screen, color, self.back_button, border_radius=5)
        text = self.font.render('Back', True, self.WHITE)
        text_rect = text.get_rect(center=self.back_button.center)
        self.screen.blit(text, text_rect)

    def draw_buttons(self):
        # Draw back button
        self.draw_back_button()
        
        # Mode buttons
        color = self.HOVER_COLOR if self.heuristic_hover else self.GRAY
        pygame.draw.rect(self.screen, color, self.heuristic_rect, border_radius=10)
        text = self.font.render('Heuristic', True, self.WHITE)
        text_rect = text.get_rect(center=self.heuristic_rect.center)
        self.screen.blit(text, text_rect)
        
        color = self.HOVER_COLOR if self.blind_hover else self.GRAY
        pygame.draw.rect(self.screen, color, self.blind_rect, border_radius=10)
        text = self.font.render('Blind Search', True, self.WHITE)
        text_rect = text.get_rect(center=self.blind_rect.center)
        self.screen.blit(text, text_rect)

    def check_hover(self, mouse_pos):
        self.heuristic_hover = self.heuristic_rect.collidepoint(mouse_pos)
        self.blind_hover = self.blind_rect.collidepoint(mouse_pos)
        self.back_hover = self.back_button.collidepoint(mouse_pos)

    def run(self):
        while True:
            self.screen.fill(self.WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                    
                if event.type == pygame.MOUSEMOTION:
                    self.check_hover(event.pos)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        return "back"
                    elif self.heuristic_rect.collidepoint(event.pos):
                        return "heuristic"
                    elif self.blind_rect.collidepoint(event.pos):
                        return "blind"
            
            self.draw_buttons()
            pygame.display.flip()