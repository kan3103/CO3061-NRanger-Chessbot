import pygame 
import sys


class Repair:
    def __init__(self):
        pygame.init()

        self.placing_piece = False
        self.selected_piece = None
        self.board_state = {}  # Empty board initially
        
        # Screen setup with extra height for piece selection and buttons
        self.screen_size = 600
        self.square_size = self.screen_size // 8
        self.piece_list_height = 100
        self.button_height = 50
        self.total_height = self.screen_size + self.piece_list_height + self.button_height
        self.screen = pygame.display.set_mode((self.screen_size, self.total_height))
        pygame.display.set_caption(f'Chess ranger')
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.HILIGHT = (255, 255, 0)
        self.GREEN = (34, 139, 34)
        self.LIGHT_BLUE = (173, 216, 230)
        self.RED = (220, 20, 60)
        
        # Piece types and images
        self.piece_types = ['King', 'Queen', 'Bishop', 'Knight', 'Rook', 'Pawn']
        self.images = self.load_images()
        
        # Font
        self.font = pygame.font.Font(None, 36)
        
        # Piece selection area
        self.piece_buttons = self.create_piece_buttons()

    def draw_reset_button(self):
        button_width = 150
        button_x = 10  # Left side position
        button_y = self.screen_size + self.piece_list_height + 10
        
        reset_rect = pygame.Rect(button_x, button_y, button_width, self.button_height - 20)
        pygame.draw.rect(self.screen, self.RED, reset_rect, border_radius=10)
        
        text = self.font.render('Reset Board', True, self.WHITE)
        text_rect = text.get_rect(center=reset_rect.center)
        self.screen.blit(text, text_rect)
        
        return reset_rect

    def reset_board(self):
        self.board_state = {}
        self.selected_piece = None
        self.placing_piece = False
        self.game_started = False

    def run(self):
        while True:
            self.screen.fill(self.WHITE)
            self.draw_board()
            self.draw_pieces()
            self.draw_piece_selection()
            
            # Only show reset and start buttons before game starts
            reset_button = self.draw_reset_button()
            start_button = self.draw_start_button()
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    

                        # Check for piece selection/placement
                    if pos[1] >= self.screen_size and pos[1] < self.screen_size + self.piece_list_height:
                        self.handle_piece_selection(pos)
                    elif pos[1] < self.screen_size:
                        self.handle_piece_placement(pos)
                    # Check for reset button
                    elif reset_button.collidepoint(pos):
                        self.reset_board()
                    # Check for start button
                    elif start_button.collidepoint(pos):
                        return self.board_state

    # Previous methods remain the same
    def load_images(self):
        images = {}
        for piece in self.piece_types:
            images[piece] = pygame.transform.scale(
                pygame.image.load(f'images/{piece}.png'), 
                (self.square_size, self.square_size)
            )
        return images

    def create_piece_buttons(self):
        buttons = {}
        piece_width = self.screen_size // len(self.piece_types)
        for i, piece in enumerate(self.piece_types):
            buttons[piece] = pygame.Rect(
                i * piece_width,
                self.screen_size,
                piece_width,
                self.piece_list_height
            )
        return buttons

    def draw_piece_selection(self):
        pygame.draw.rect(self.screen, self.GRAY, 
                        (0, self.screen_size, self.screen_size, self.piece_list_height))
        
        for piece, rect in self.piece_buttons.items():
            if self.selected_piece == piece:
                pygame.draw.rect(self.screen, self.LIGHT_BLUE, rect)
            self.screen.blit(self.images[piece], 
                           (rect.centerx - self.square_size//2, 
                            rect.centery - self.square_size//2))

    def draw_board(self):
        colors = [self.GRAY, self.WHITE]
        for y in range(8):
            for x in range(8):
                color = colors[(x + y) % 2]
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    pygame.Rect(x * self.square_size, (7 - y) * self.square_size, 
                              self.square_size, self.square_size)
                )
                
                if self.placing_piece:
                    mouse_pos = pygame.mouse.get_pos()
                    board_x = mouse_pos[0] // self.square_size
                    board_y = 7 - (mouse_pos[1] // self.square_size)
                    if 0 <= board_x < 8 and 0 <= board_y < 8:
                        pygame.draw.rect(
                            self.screen,
                            self.HILIGHT,
                            pygame.Rect(board_x * self.square_size,
                                      (7 - board_y) * self.square_size,
                                      self.square_size,
                                      self.square_size),
                            3
                        )

    def draw_pieces(self):
        for position, piece in self.board_state.items():
            x, y = position
            self.screen.blit(self.images[piece], 
                           (x * self.square_size, (7 - y) * self.square_size))

    def draw_start_button(self):
        button_width = 150
        button_x = self.screen_size - button_width - 10  # Right side position
        button_y = self.screen_size + self.piece_list_height + 10
        
        start_rect = pygame.Rect(button_x, button_y, button_width, self.button_height - 20)
        pygame.draw.rect(self.screen, self.GREEN, start_rect, border_radius=10)
        
        text = self.font.render('Start Solution', True, self.WHITE)
        text_rect = text.get_rect(center=start_rect.center)
        self.screen.blit(text, text_rect)
        
        return start_rect

    def handle_piece_selection(self, pos):
        for piece, rect in self.piece_buttons.items():
            if rect.collidepoint(pos):
                self.selected_piece = piece
                self.placing_piece = True
                return True
        return False

    def handle_piece_placement(self, pos):
        if not self.placing_piece or self.selected_piece is None:
            return
            
        board_x = pos[0] // self.square_size
        board_y = 7 - (pos[1] // self.square_size)
        
        if 0 <= board_x < 8 and 0 <= board_y < 8:
            self.board_state[(board_x, board_y)] = self.selected_piece
            
        self.placing_piece = False
        self.selected_piece = None
