from abc import ABC, abstractmethod

class ChessPiece(ABC):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y
        
    @abstractmethod
    def isValid(self, x, y):
        pass

class King(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "King"
    
    def isValid(self, x, y):
        return ( abs(y - self.y)==1 and abs(x - self.x)==1) or ( (y == self.y and abs(x- self.x)==1) or (x == self.x and abs(y - self.y)==1) )

class Queen(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Queen"
    def isValid(self, x, y):
        return (abs(x - self.x) == abs(y - self.y)) or (self.x == x or self.y == y)

class Bishop(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Bishop"
    def isValid(self, x, y):
        return (abs(x - self.x) == abs(y - self.y))

class Knight(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Knight"
    def isValid(self, x, y):
        return ( abs(y - self.y)==1 and abs(x - self.x)==2 ) or ( abs(y - self.y)==2 and abs(x - self.x)==1 )

class Rook(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Rook"
    def isValid(self, x, y):
        return self.x == x or self.y == y

class Pawn(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Pawn"
    def isValid(self, x, y):
        return y - self.y == 1 and abs(x- self.x) == 1

