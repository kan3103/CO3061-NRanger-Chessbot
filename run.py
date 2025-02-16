
from models.Menu import Menu
from models.ChessGame import ChessGame
from models.Repair import Repair
from models.chess import Rook, Bishop, Queen, Pawn, Knight, King

def main():
    repair = Repair()
    initial=repair.run()
    state_initial = []
    for position, piece in initial.items():
        x, y = position
        chessType = piece
        if chessType == "Rook": chess = Rook(x, y)
        elif chessType == "Pawn": chess = Pawn(x, y)
        elif chessType == "Bishop": chess = Bishop(x, y)
        elif chessType == "Queen": chess = Queen(x, y)
        elif chessType == "King": chess = King(x, y)
        else: chess = Knight(x, y)
        state_initial.append(chess)
    # Start with the menu
    menu = Menu()
    selected_mode = menu.run()
    
    # Initialize the game with the selected mode
    if selected_mode == "heuristic":
        game = ChessGame(state_initial,selected_mode)
    else:  # mode2
        game = ChessGame(state_initial,selected_mode)
    
    game.run()

if __name__ == "__main__":
    main()