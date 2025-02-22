import os
import time
from collections import deque
import pygame
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from heuristic.run import Heuristic_search
from blind_search.dfs import Blind_search
class ChessGame:
    def __init__(self, state_init, mode):
        pygame.init()
        self.initial_state = state_init
        self.mode = mode
        self.current_step = 0
        self.last_move = None
        self.game_started = False  
        
        # Screen setup
        self.screen_size = 600
        self.square_size = self.screen_size // 8
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size + 50))
        pygame.display.set_caption(f'Chess ranger - {mode}')
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.HILIGHT = (255, 255, 0)
        self.GREEN = (34, 139, 34)  # Color for start button
        # Load game data
        self.steps = self.load_sol()
        self.board_state = {(piece.x,piece.y):piece.type for piece in self.initial_state}
        self.images = self.load_images()
        
        # Font
        self.font = pygame.font.Font(None, 36)

    def draw_start_button(self):
        button_width = 200
        button_height = 50
        button_x = (self.screen_size - button_width) //2
        button_y = (self.screen_size - button_height) //2
        
        start_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, self.GREEN, start_rect, border_radius=10)
        
        text = self.font.render('Start Solution', True, self.WHITE)
        text_rect = text.get_rect(center=start_rect.center)
        self.screen.blit(text, text_rect)
        
        return start_rect

    def draw_buttons(self):
        if not self.game_started:
            return None, None ,None
            
        # Only draw undo and next buttons if game has started
        undo_rect = pygame.Rect(200, self.screen_size + 10, 180, 30)
        pygame.draw.rect(self.screen, self.BLACK, undo_rect)
        undo_text = self.font.render('Undo', True, self.WHITE)
        undo_text_rect = undo_text.get_rect(center=undo_rect.center)
        self.screen.blit(undo_text, undo_text_rect)

        next_rect = pygame.Rect(self.screen_size - 190, self.screen_size + 10, 180, 30)
        pygame.draw.rect(self.screen, self.BLACK, next_rect)
        next_text = self.font.render('Next Step', True, self.WHITE)
        next_text_rect = next_text.get_rect(center=next_rect.center)
        self.screen.blit(next_text, next_text_rect)
        
        back_rect = pygame.Rect(10, self.screen_size + 10, 130, 30)
        pygame.draw.rect(self.screen, self.BLACK, back_rect)
        text = self.font.render('Back', True, self.WHITE)
        text_rect = text.get_rect(center=back_rect.center)
        self.screen.blit(text, text_rect)
        
        return  undo_rect,next_rect, back_rect

    # def draw_back_button(self):
    #     button_width = 150
    #     button_height = 50
    #     button_x = 10
    #     button_y = self.screen_size + 10
        
    #     back_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    #     pygame.draw.rect(self.screen, self.BLACK, back_rect, border_radius=10)
        
    #     text = self.font.render('Back', True, self.WHITE)
    #     text_rect = text.get_rect(center=back_rect.center)
    #     self.screen.blit(text, text_rect)
        
        # return back_rect
    def run(self):
        while True:
            if len(self.steps)==0:
                self.no_solution()
                return "repair"
            self.screen.fill(self.WHITE)
            self.draw_board()
            self.draw_pieces()
            # self.draw_back_button()
            if not self.game_started:
                start_button = self.draw_start_button()
            undo_button, next_button , back_button= self.draw_buttons()
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_started:
                        if start_button.collidepoint(event.pos):
                            self.game_started = True
                    else:
                        if undo_button and undo_button.collidepoint(event.pos):
                            self.undo_step()
                        elif next_button and next_button.collidepoint(event.pos):
                            self.next_step()
                        elif back_button and back_button.collidepoint(event.pos):
                            return "back"

    def load_sol(self):
        # initial_state = []
        print(self.mode)
        if self.mode == "heuristic":
            start = time.time()
            hs = Heuristic_search(self.initial_state)
           
           #print time with 0.2f format
           
        # with open(f'blind_search/output/{self.chess_num}_chess/{self.id}.txt', 'r') as input_file:
        #     lines = deque(input_file, maxlen=self.chess_num)
        # temp = lines[0].split('\t')[1:-1]
            step = hs.solve()
            end = time.time()
            print(f"Time: {end - start:.2f} seconds")
        else:
            start = time.time()
            bs = Blind_search(self.initial_state)
            step = bs.solve()
            end = time.time()
            print(f"Time: {end - start:.2f} seconds")
        print("Chess game: ", step)
        return step

    def load_images(self):
        pieces = ['Bishop', 'Knight', 'Rook', 'Pawn', 'Queen', 'King']
        images = {}
        for piece in pieces:
            images[piece] = pygame.transform.scale(
                pygame.image.load(f'images/{piece}.png'), 
                (self.square_size, self.square_size)
            )
        return images

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
        
        if self.last_move is not None:
            highlight_surface = pygame.Surface((self.square_size, self.square_size))
            highlight_surface.set_alpha(100)
            highlight_surface.fill(self.HILIGHT)
            for coord in self.last_move:
                x, y = coord
                self.screen.blit(highlight_surface, 
                               (x * self.square_size, (7 - y) * self.square_size))

    def draw_pieces(self):
        for position, piece in self.board_state.items():
            x, y = position
            self.screen.blit(self.images[piece], (x * self.square_size, (7 - y) * self.square_size))

    def no_solution(self):
        self.screen.fill(self.WHITE)
        text = self.font.render('No solution found', True, self.BLACK)
        text_rect = text.get_rect(center=(self.screen_size // 2, self.screen_size // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(5000)
    
    def next_step(self):
        if len(self.steps) == 0:
            self.no_solution()
            return False
        if self.current_step < len(self.steps):
            # print(self.steps[self.current_step])
            piece, x1, y1, target_piece, x2, y2 = self.steps[self.current_step]
            self.last_move = ((x1, y1), (x2, y2))
            
            if (x2, y2) in self.board_state:
                del self.board_state[(x2, y2)]
            self.board_state[(x2, y2)] = self.board_state.pop((x1, y1))
            self.current_step += 1

    def undo_step(self):
        if self.current_step > 0:
            piece, x1, y1, target_piece, x2, y2 = self.steps[self.current_step - 1]
            self.last_move = ((x1, y1), (x2, y2))
            self.current_step -= 1
            
            self.board_state[(x1, y1)] = self.board_state.pop((x2, y2))
            if target_piece != 'empty':
                self.board_state[(x2, y2)] = target_piece