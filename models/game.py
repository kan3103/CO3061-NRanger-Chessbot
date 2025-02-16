import pygame 
import sys
from collections import deque
import argparse

pygame.init()

screen_size = 600
square_size = screen_size // 8
screen = pygame.display.set_mode((screen_size, screen_size + 50))
pygame.display.set_caption('Chess ranger')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
HILIGHT = (255, 255, 0)  

def load_sol(chess_num, id):
    with open(f'blind_search/output/{chess_num}_chess/{id}.txt', 'r') as input_file:
        lines = deque(input_file, maxlen=chess_num)
    temp = lines[0].split('\t')[1:-1]
    initial_state = []
    steps = []
    for line in temp: 
        chess = line.split(',')
        initial_state.append( (str(chess[0]), int(chess[1]), int(chess[2])) )
    for i in range(1, chess_num):
        line = lines[i]
        step = line.split('\t')
        chess = step[1].strip().replace(',', '').split()
        temp = (str(chess[0]), int(chess[1]), int(chess[2]), str(chess[4]), int(chess[5]), int(chess[6]))
        steps.append(temp)
    return initial_state, steps
        
def draw_board():
    colors = [WHITE, GRAY]
    for y in range(8):
        for x in range(8):
            color = colors[(x + y) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(x * square_size, (7 - y) * square_size, square_size, square_size))
    
    if last_move is not None:
        highlight_surface = pygame.Surface((square_size, square_size))
        highlight_surface.set_alpha(100)  
        highlight_surface.fill(HILIGHT)
        for coord in last_move:
            x, y = coord
            screen.blit(highlight_surface, (x * square_size, (7 - y) * square_size))

def load_images():
    pieces = ['Bishop', 'Knight', 'Rook', 'Pawn', 'Queen', 'King']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (square_size, square_size))
    return images

def draw_pieces():
    for position, piece in board_state.items():
        x, y = position
        screen.blit(images[piece], (x * square_size, (7 - y) * square_size))

current_step = 0
last_move = None  

def next_step():
    global current_step, last_move
    if current_step < len(steps):

        piece, x1, y1, target_piece, x2, y2 = steps[current_step]

        last_move = ((x1, y1), (x2, y2))

        if (x2, y2) in board_state:
            del board_state[(x2, y2)]
        board_state[(x2, y2)] = board_state.pop((x1, y1))
        current_step += 1

def undo_step():
    global current_step, last_move
    if current_step > 0:

        piece, x1, y1, target_piece, x2, y2 = steps[current_step - 1]

        last_move = ((x1, y1), (x2, y2))
        current_step -= 1
        board_state[(x1, y1)] = board_state.pop((x2, y2))

        board_state[(x2, y2)] = target_piece

def draw_buttons():
    font = pygame.font.Font(None, 36)


    undo_rect = pygame.Rect(10, screen_size + 10, 180, 30)
    pygame.draw.rect(screen, BLACK, undo_rect)
    undo_text = font.render('Undo', True, WHITE)
    undo_text_rect = undo_text.get_rect(center=undo_rect.center)
    screen.blit(undo_text, undo_text_rect)
    

    next_rect = pygame.Rect(screen_size - 190, screen_size + 10, 180, 30)
    pygame.draw.rect(screen, BLACK, next_rect)
    next_text = font.render('Next Step', True, WHITE)
    next_text_rect = next_text.get_rect(center=next_rect.center)
    screen.blit(next_text, next_text_rect)
    
    return undo_rect, next_rect

images = load_images()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chess-num")
    parser.add_argument("--id")
    args = parser.parse_args()
    
    chess_num = int(args.chess_num)
    id = int(args.id)
    
    initial_state, steps = load_sol(chess_num, id)

    board_state = {(x, y): piece for piece, x, y in initial_state}

    while True:
        draw_board()
        draw_pieces()
        undo_button, next_button = draw_buttons()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if undo_button.collidepoint(event.pos):
                    undo_step()
                elif next_button.collidepoint(event.pos):
                    next_step()
