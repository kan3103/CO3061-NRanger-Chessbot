import os
import sys
from queue import PriorityQueue
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tracemalloc
from models.chess import Rook, Bishop, Queen, Pawn, Knight, King


        
class Heuristic_search():
    def __init__(self,initial_state):
        self.step = 0
        self.initial = initial_state
        # self.initial = []
        # self.input_path = input_path
        # with open(input_path, "r") as input_file:
        #     for line in input_file:  
        #         line = line.strip()
        #         parts = line.split(",")  
        #         chessType, x, y = parts
        #         x, y = int(x), int(y)
        #         if chessType == "rook": chess = Rook(x, y)
        #         elif chessType == "pawn": chess = Pawn(x, y)
        #         elif chessType == "bishop": chess = Bishop(x, y)
        #         elif chessType == "queen": chess = Queen(x, y)
        #         elif chessType == "king": chess = King(x, y)
        #         else: chess = Knight(x, y)
        #         self.initial.append(chess)
                
        self.initial = (self.initial)
        self.visited = set()
        self.chess_num = len(self.initial)
        self.check_step = ""
        self.goal = []
    def copy(self, node):
        new_node = None
        if node.type == "Rook": new_node = Rook(node.x, node.y)
        elif node.type == "Pawn": new_node = Pawn(node.x, node.y)
        elif node.type == "Bishop": new_node = Bishop(node.x, node.y)
        elif node.type == "Queen": new_node = Queen(node.x, node.y)
        elif node.type == "King": new_node = King(node.x, node.y)
        else: new_node = Knight(node.x, node.y)
        return new_node
    
    def print_step(self,sol):
        with open("heuristic/output/1.txt", "w") as output_file:
            output_file.write(sol)
    
    def tostring(self,node):
        res = ""
        for i in range(len(node)):
            x = node[i]
            res += f"{x.type}, {x.x}, {x.y}\t"
        return res
    
    def run(self,node,sol=None):
        priority = PriorityQueue()
        if sol is None:
            sol = ([],[],[])
        else:
            self.check_step+=f"\nStep {self.step}: \t" + self.tostring(sol[0][-1])
        if self.check_goal(node):
            self.check_step+=f"\nGoal with {str(self.step)} \n"
            count = 1
            for s in sol[0]:
                self.check_step+="step "+ str(count) +': ' +self.tostring(s)+'\n'
                count += 1
            return True
        else:
            self.visited.add(frozenset(node))
            self.step += 1
            
            for chess in node:
                for chess2 in node:
                    if chess == chess2: continue
                    
                    if chess.isValid(chess2.x, chess2.y, node):
                        
                        tempchess = self.copy(chess)
                        tempchess.move(chess2.x, chess2.y)
                        temp = [chess3 for chess3 in node if chess3 != chess2 and chess3 != chess]
                        temp.append(tempchess)
                        temp = (temp)
                        s = chess.type + " " + str(chess.x) + " " + str(chess.y) + " eat " + chess2.type + " " + str(chess2.x) + " " + str(chess2.y)
                        goal_temp = chess.type, chess.x, chess.y, chess2.type, chess2.x, chess2.y
                        if(frozenset(temp) in self.visited):
                            continue
                        targets = self.check_target(temp)
                        length = len(temp)
                        if(targets == 0 and length != 1) :
                            self.visited.add(frozenset(temp))
                            continue
                            
                        if self.check_goal(temp):
                            sol[0].append(temp)
                            sol[1].append(goal_temp)
                            sol[2].append(s)
                            self.check_step+=f"\nStep {self.step}: \t" + self.tostring(temp)
                            self.check_step+=f"\nGoal with {str(self.step)} \n"
                            count = 1
                            for so in sol[2]:
                                self.check_step+="step "+ str(count) +': ' +so+'\n'
                                count += 1
                            self.goal = sol[1]
                            self.print_step(self.check_step)
                            # print(self.goal)
                            return True

                        value = -targets 
                            
                        priority.put((value, temp ,goal_temp ,s ))
                        
            while not priority.empty():
                temp=priority.get()
                sol[0].append(temp[1])
                sol[1].append(temp[2])
                sol[2].append(temp[3])
                if self.run(temp[1],sol):
                    return True
                else:
                    sol[0].pop()
                    sol[1].pop()
                    sol[2].pop()
        return False

    
    def check_target(self, node):
        if len(node) == 1:
            return 0
        targets = 0
        have_targets = 0
        for chess in node:
            target , have_target = chess.check_target(node)
            if (target == 0 and have_target == 0):
                return 0
            targets += target
        return targets 
            
    def check_goal(self, node):
        if len(node) == 1:
            return True
        return False

    def solve(self):
        if self.run(self.initial):
            return self.goal
        else:
            print("No solution")
            return []
    
if __name__ == "__main__":
    # tracemalloc.start()
    
    
    start = time.time()
    
    input_path = "heuristic/input/1.txt"
    hs = Heuristic_search(input_path)
    sol = hs.solve()
    hs.print_step(hs.check_step)    
    end = time.time()
    # current, peak = tracemalloc.get_traced_memory()
    # print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    # tracemalloc.stop()

    time = (end - start)
    print(f"Time: {time:.2f} seconds")