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

def print_step(step, node, visited, output_path):
    res = f"\nLần duyệt thứ {len(visited)}\t{step}:\t"
    for i in range(len(node)):
        x = node[i]
        res += f"{x.type}, {x.x}, {x.y}\t"
    if (step == "After"): res += '\n'
    with open(output_path, "a", encoding="utf-8") as output_file:
        output_file.write(res)
        
def print_sol(sol):
    with open(output_path, "a", encoding= "utf-8") as output_file:
        count = 0
        for line in reversed(sol):
            if count == 0: step = line
            else: step = f"\nStep {count}: \t" + line
            output_file.write(step)
            count += 1 



def dfs_recursive(node, output_path, chess_num, sol=None, visited=None):
    if visited is None:
        visited = []
    if sol is None:
        sol = []
    initial_node = copy.deepcopy(node)
    visited.append(node)
    
    if(len(node) == 1):
        print_step("Goal", node, visited, output_path)
        return True
        
    print_step("Before", node, visited, output_path)
    
    child = []
    for i in range(len(node)):
        curr = node[i]
        for j in range(len(node)):
            if i == j: continue
            temp = node[j]
            if(curr.isValid(temp.x, temp.y, node)):
                original_x, original_y = curr.x, curr.y
                curr.move(temp.x, temp.y)
                child = node[:]
                child.remove(temp)
                if(len(child) != 0):
                    print_step("After", child, visited, output_path)
                    if dfs_recursive(child, output_path, chess_num, sol, visited): 
                        
                        temp = f"{curr.type}, {original_x}, {original_y} captures {temp.type}, {temp.x}, {temp.y}"
                        sol.append(temp)
                        if len(sol) == int(chess_num)-1: 
                            initial_state = "\nInitial state:\t"
                            for i in range(len(initial_node)):
                                x = initial_node[i]
                                initial_state += f"{x.type}, {x.x}, {x.y}\t"
                            sol.append(initial_state)
                            
                            print_sol(sol)
                        return True
                curr.move(original_x, original_y)  # backtracking
    return False

def get_mem():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss/ 10**6

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
    smem = get_mem()
    dfs_recursive(initial, output_path, chess_num)      
    end = time.time()
    emem = get_mem()
    
    time = (end - start)
    print(f"start mem: {smem}")
    print(f"end mem: {emem}")
    print(f"Time: {time:.2f} seconds")