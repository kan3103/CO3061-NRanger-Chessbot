from abc import ABC, abstractmethod

class ChessPiece(ABC):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y
        
    @abstractmethod
    # table is a list of chess object: [Rook, Queen]
    def isValid(self, x, y, table):
        pass

class King(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "King"
    
    def isValid(self, x, y, table):
        return ( abs(y - self.y)==1 and abs(x - self.x)==1) or ( (y == self.y and abs(x- self.x)==1) or (x == self.x and abs(y - self.y)==1) )

class Queen(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Queen"
    def isValid(self, x, y, table):
        if abs(x - self.x) == abs(y - self.y):
            for chess in table:
                if (chess.x == self.x and chess.y == self.y) or (chess.x == x and chess.y == y): continue
                if abs(chess.x - self.x) == abs(chess.y - self.y) and abs(chess.x - self.x) < abs(x - self.x): return False
            return True
        elif self.x == x or self.y == y:
            for chess in table:
                if (chess.x == self.x and chess.y == self.y) or (chess.x == x and chess.y == y): continue
                if ( 
                    self.x == chess.x and self.x == x and (min(self.y, y)<=chess.y<=max(self.y, y)) 
                ) or ( 
                    self.y == chess.y and self.y == y and (min(self.x, x)<=chess.x<=max(self.x, x)) 
                ): return False
            return True
        return False
        
class Bishop(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Bishop"
    def isValid(self, x, y, table):
        if abs(x - self.x) == abs(y - self.y):
            step_x = 1 if x > self.x else -1
            step_y = 1 if y > self.y else -1
            curr_x, curr_y = self.x + step_x, self.y + step_y
            while(curr_x != x and curr_y != y):
                for chess in table:
                    if(curr_x == chess.x and curr_y == chess.y): return False
                curr_x += step_x
                curr_y += step_y
            return True
        return False

class Knight(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Knight"
    def isValid(self, x, y, table):
        return ( abs(y - self.y)==1 and abs(x - self.x)==2 ) or ( abs(y - self.y)==2 and abs(x - self.x)==1 )

class Rook(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Rook"
    def isValid(self, x, y, table):
        if self.x == x or self.y == y:
            for chess in table:
                if (chess.x == self.x and chess.y == self.y) or (chess.x == x and chess.y == y): continue
                if ( 
                    self.x == chess.x and self.x == x and (min(self.y, y)<=chess.y<=max(self.y, y)) 
                ) or ( 
                    self.y == chess.y and self.y == y and (min(self.x, x)<=chess.x<=max(self.x, x)) 
                ): return False
            return True
        return False

class Pawn(ChessPiece): # ignore the vertical movement, just allow cross movement for capturing
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Pawn"
    def isValid(self, x, y, table):
        return y - self.y == 1 and abs(x- self.x) == 1

