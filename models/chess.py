from abc import ABC, abstractmethod

class ChessPiece(ABC):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    @abstractmethod
    def move(self):
        pass

class King(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "King"
    
    def move(self):
        pass

class Queen(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Queen"
    def move(self):
        pass

class Bishop(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Bishop"
    def move(self):
        pass

class Knight(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Knight"
    def move(self):
        pass

class Rook(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Rook"
    def move(self):
        pass

class Pawn(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Pawn"
    def move(self):
        pass

