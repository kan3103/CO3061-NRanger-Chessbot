
from models.Menu import Menu
from models.ChessGame import ChessGame
from models.Repair import Repair
from models.chess import Rook, Bishop, Queen, Pawn, Knight, King

class ScreenManager:
    def __init__(self):
        self.current_screen = "repair"  # Initial screen
        self.board_state = None
        self.selected_mode = None
        
    def run(self):
        while True:
            if self.current_screen == "repair":
                repair = Repair()
                self.board_state = repair.run()
                if self.board_state is None:  # User clicked exit
                    return None
                self.current_screen = "menu"
                
            elif self.current_screen == "menu":
                menu = Menu()
                self.selected_mode = menu.run()
                if self.selected_mode == "back":
                    self.current_screen = "repair"
                    continue
                elif self.selected_mode is None:  # User clicked exit
                    return None
                    
                # Convert board state to chess pieces
                state_initial = []
                for position, piece in self.board_state.items():
                    x, y = position
                    chessType = piece
                    if chessType == "Rook": chess = Rook(x, y)
                    elif chessType == "Pawn": chess = Pawn(x, y)
                    elif chessType == "Bishop": chess = Bishop(x, y)
                    elif chessType == "Queen": chess = Queen(x, y)
                    elif chessType == "King": chess = King(x, y)
                    else: chess = Knight(x, y)
                    state_initial.append(chess)
                
                # Start game
                game = ChessGame(state_initial, self.selected_mode)
                result = game.run()
                if result == "back":
                    self.current_screen = "menu"
                elif result == "repair":
                    self.current_screen = "repair"

def main():
    screen_manager = ScreenManager()
    screen_manager.run()

if __name__ == "__main__":
    main()