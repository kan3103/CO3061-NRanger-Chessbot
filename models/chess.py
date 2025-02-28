from abc import ABC, abstractmethod

class ChessPiece(ABC):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash((self.x, self.y, self.type))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.type == other.type
    
    def __lt__(self, other):  
        return (self.x, self.y) < (other.x, other.y)
        
    @abstractmethod
    # table is a list of chess object: [Rook, Queen]
    def isValid(self, x, y, table):
        pass
    
    def check_target(self, table):
        target = 0
        have_target = 0
        for chess in table:
            if chess.x == self.x and chess.y == self.y: continue
            else: 
                if self.isValid(chess.x,chess.y , table): target += 1
                if chess.simulation(self.x, self.y, table) and have_target == 0: have_target += 1
        return target,have_target

    def simulation(self, x, y, table):
        pass
    


class King(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "King"
        self.target = 0
    
    def isValid(self, x, y, table):
        return ( abs(y - self.y)==1 and abs(x - self.x)==1) or ( (y == self.y and abs(x- self.x)==1) or (x == self.x and abs(y - self.y)==1) )
    
    def simulation(self, x, y, table):
        if self.isValid(x, y, table):
            return True
        for chess in table:
            if chess.x == x and chess.y == y: continue
            if chess.x == self.x and chess.y == self.y: continue
            
            temp = King(chess.x,chess.y)
            if temp.isValid(x, y, table):
                return True
        return False
    

class Queen(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Queen"
        self.target = 0
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
    
    def simulation(self, x, y, table):
        if self.isValid(x, y, table):
            return True
        for chess in table:
            if chess.x == x and chess.y == y: continue
            if chess.x == self.x and chess.y == self.y: continue
            
            temp = Queen(chess.x,chess.y)
            if temp.isValid(x, y, table):
                return True
        return False
        
class Bishop(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Bishop"
        self.target = 0
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
    
    def simulation(self, x, y, table):
        if (abs(x-y)%2 != abs(self.x-self.y)%2):
            return False
        if self.isValid(x, y, table):
            return True
        for chess in table:
            if chess.x == x and chess.y == y: continue
            if chess.x == self.x and chess.y == self.y: continue
            
            temp = Bishop(chess.x,chess.y)
            if temp.isValid(x, y, table):
                return True
        return False


class Knight(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Knight"
        self.target = 0
    def isValid(self, x, y, table):
        return ( abs(y - self.y)==1 and abs(x - self.x)==2 ) or ( abs(y - self.y)==2 and abs(x - self.x)==1 )
    
    def simulation(self, x, y, table):
        if self.isValid(x, y, table):
            return True
        for chess in table:
            if chess.x == x and chess.y == y: continue
            if chess.x == self.x and chess.y == self.y: continue
            
            temp = Knight(chess.x,chess.y)
            if temp.isValid(x, y, table):
                return True
        return False

class Rook(ChessPiece):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Rook"
        self.target = 0
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
    
    def simulation(self, x, y, table):
        if self.isValid(x, y, table):
            return True
        for chess in table:
            if chess.x == x and chess.y == y: continue
            if chess.x == self.x and chess.y == self.y: continue
            
            temp = Rook(chess.x,chess.y)
            if temp.isValid(x, y, table):
                return True
        return False


class Pawn(ChessPiece): # ignore the vertical movement, just allow cross movement for capturing
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.type = "Pawn"
        self.target = 0
    def isValid(self, x, y, table):
        return y - self.y == 1 and abs(x- self.x) == 1
    
    def simulation(self, x, y, table):
        if (self.y>=y):
            return False
        if self.isValid(x, y, table):
            return True
        for chess in table:
            if chess.x == x and chess.y == y: continue
            if chess.x == self.x and chess.y == self.y: continue
            
            temp = Pawn(chess.x,chess.y)
            if temp.isValid(x, y, table):
                return True
        return False


