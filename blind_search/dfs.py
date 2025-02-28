import argparse
import os
import time
import copy
from models.chess import Rook, Bishop, Queen, Pawn, Knight, King
import psutil

def creare_initial(input_path):
        initial = []
        with open(input_path, "r") as input_file:
            for line in input_file:  
                line = line.strip()
                parts = line.split(",")  
                chessType, x, y = parts
                x, y = int(x), int(y)
                if chessType == "rook": chess = Rook(x, y)
                elif chessType == "pawn": chess = Pawn(x, y)
                elif chessType == "bishop": chess = Bishop(x, y)
                elif chessType == "queen": chess = Queen(x, y)
                elif chessType == "king": chess = King(x, y)
                else: chess = Knight(x, y)

                initial.append(chess)
        return initial

class Blind_search():
    def __init__(self, initial_state):
        self.initial_state = copy.deepcopy(initial_state)
        self.chess_num = len(self.initial_state)
        
        os.makedirs(f"blind_search/output/{self.chess_num}_chess", exist_ok=True)
        
        self.id = 1
        self.output_path = f"blind_search/output/11_chess/1.txt"

    def print_step(self, step, node, visited, output_path):
        res = f"\nLần duyệt thứ {len(visited)}\t{step}:\t"
        for i in range(len(node)):
            x = node[i]
            res += f"{x.type}, {x.x}, {x.y}\t"
        if (step == "After"): res += '\n'
        with open(output_path, "a", encoding="utf-8") as output_file:
            output_file.write(res)
            
    def print_sol(self, sol):
        print(sol)



    def dfs_recursive(self, node, output_path, chess_num, sol=None, visited=None):
        if visited is None:
            visited = []
        if sol is None:
            sol = []
        initial_node = copy.deepcopy(node)
        visited.append(node)
        
        if(len(node) == 1):
            # self.print_step("Goal", node, visited, output_path)
            return True
            
        # self.print_step("Before", node, visited, output_path)
        
        child = []
        for i in range(len(node)):
            curr = node[i]
            for j in range(len(node)):
                if i == j: continue
                temp = node[j]
                if(curr.isValid(temp.x, temp.y, node)):
                    original_x, original_y = curr.x, curr.y
                    curr.move(temp.x, temp.y)
                    child = copy.deepcopy(node)
                    child.remove(temp)
                    if(len(child) != 0):
                        # self.print_step("After", child, visited, output_path)
                        if self.dfs_recursive(child, output_path, chess_num, sol, visited): 
                            
                            temp_str = f"{curr.type}, {original_x}, {original_y} captures {temp.type}, {temp.x}, {temp.y}"
                            sol.append( (curr.type, int(original_x), int(original_y), temp.type, int(temp.x), int(temp.y)) )
                            # print(sol)
                            if len(sol) == int(chess_num)-1: 
                                initial_state = "\nInitial state:\t"
                                for i in range(len(initial_node)):
                                    x = initial_node[i]
                                    initial_state += f"{x.type}, {x.x}, {x.y}\t"
                                # sol.append(initial_state)
                                
                                # self.print_sol(sol)
                            return True
                    curr.move(original_x, original_y)  # backtracking
        return False

    def get_mem(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss/ 10**6
    
    def run(self, initial_state):
        sol = []
        if self.dfs_recursive(initial_state, self.output_path, self.chess_num, sol=sol):  
            self.goal = sol[::-1]
            return True
        return False
    
    def solve(self):
        if self.run(self.initial_state):
            # print(self.goal)
            return self.goal
        else:
            print("No solution")
            return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chess-num")
    parser.add_argument("--id")
    args = parser.parse_args()
    
    chess_num = args.chess_num
    id = args.id
    
    input_path = f"blind_search/input/{chess_num}_chess/{id}.txt"

    os.makedirs(f"blind_search/output/{chess_num}_chess", exist_ok=True)
    output_path = f"blind_search/output/{chess_num}_chess/{id}.txt"
    with open(output_path, "w", encoding="utf-8") as file:
        pass
    
    initial = creare_initial(input_path)
    
    start = time.time()
    # smem = get_mem()
    bs = Blind_search(initial)
    goal = bs.solve()
    end = time.time()
    # emem = get_mem()
    
    time = (end - start)
    # print(f"start mem: {smem}")
    # print(f"end mem: {emem}")
    print(f"Time: {time:.2f} seconds")