# Soner Kuyar 2021400297
# Yunus Kağan Aydın 2021400123

import random
import sys
import math

class KnightsTour: # In this class we defined the basics of the KnightsTour class.
    def __init__(self, n, p): # This is the initialization function for our code.
        self.n = n
        self.p = p
        self.board = [[-1 for _ in range(n)] for _ in range(n)]

    def is_valid_move(self, row, col): # This function checks if the given move is valid inside the board boundaries.
        return 0 <= row < self.n and 0 <= col < self.n and self.board[row][col] == -1

    def random_tour(self, row, col, file): # This is the function for random tour algorithm. It returns the status of success and the number of steps
        row, col = row, col
        self.board[row][col] = 0
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

        success_threshold = math.ceil(self.p * self.n * self.n)  # Calculate the success threshold
        
        for step in range(2, self.n * self.n):
            possible_moves = [(row + r, col + c) for r, c in moves if self.is_valid_move(row + r, col + c)]

            if not possible_moves:
                return False, step

            row, col = random.choice(possible_moves)
            self.board[row][col] = step
            print(f"Stepping into ({row},{col})", file=file)
            if step >= success_threshold:
                return True, step

        return True, self.n * self.n - 1

    def backtrack(self, move_count, row, col, step): # This is the function for backgrounding algorithm to find a knight's tour. Returns true when successful and returns true when it is unsuccessful.
        if move_count >= math.ceil(self.p * self.n * self.n):
            return True
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        possible_moves = [(row + r, col + c) for r, c in moves if self.is_valid_move(row + r, col + c)]
        # if next step has few option, try it first
        possible_moves.sort(key=lambda x: len([(x[0] + r, x[1] + c) for r, c in moves if self.is_valid_move(x[0] + r, x[1] + c)]))
        for move in possible_moves:
            row, col = move
            self.board[row][col] = step + 1
            if self.backtrack(move_count + 1, row, col, step + 1):
                return True
            self.board[row][col] = -1
        
        return False

    def backtracking_tour(self, k,total_try=1):# This function performs multiple attempts of backtracking tours and returns the number of successful attempts.

        success_count = 0
        for run in range(total_try):
            step, (row, col) = self.random_walk(random.randint(0, self.n - 1), random.randint(0, self.n - 1), k)
            
            if(step != -1 and self.backtrack(step, row, col, k) ):
                success_count += 1
                
               
                
                
            self.reset_board()

        return success_count

    

    def random_walk(self, row, col, k): 
        '''random_walk is the helper function for generating a random walk which is going to be used in backtracking_tour. 
        This function returns the number of steps and the final position.'''
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        self.board[row][col] = 0
        for step in range(k):
            possible_moves = [(row + r, col + c) for r, c in moves if self.is_valid_move(row + r, col + c)]

            if not possible_moves:
                return -1, (-1, -1)

            row, col = random.choice(possible_moves)
            self.board[row][col] = step + 1
        return k + 1, (row, col)

    def board_complete(self): #This function checks if a board is completed or not. If it's completed it returns true, if it is not completed it return false.
        for row in self.board:
            if -1 in row:
                return False
        return True

    def reset_board(self):#This function resets board as making all the values -1 in the board.
        self.board = [[-1 for _ in range(self.n)] for _ in range(self.n)]



def run_part1(): #This is the function to run the part1
    try_count = 100000
    probabilities = [0.7, 0.8, 0.85]

    for p in probabilities:
        with open(f"2021400297_results_{p}.txt", "w") as file:
            kt = KnightsTour(8, p)
            successful_tours = 0

            for i in range(try_count): 
                kt.reset_board()  # Reset the board before each run
                row_start, col_start = random.randint(0, 7), random.randint(0, 7)
                print(f"Run {i+1}: starting from ({row_start}, {col_start})", file=file)
                success, tour_length = kt.random_tour(row_start, col_start,file)

                if success:
                    successful_tours += 1
                    print(f"Successful - Tour length: {tour_length}", file=file)
                else:
                    print(f"Unsuccessful - Tour length: {tour_length}", file=file)
                    pass

                for row in kt.board:
                    print(" ".join(map(lambda x: str(x) if x != -1 else "-1", row)), file=file)
                print("", file=file)        

            probability = successful_tours / try_count 
            print(f"Number of successful tours: {successful_tours}", file=file)
            print(f"Number of trials: 100000",file=file)  
            print(f"Probability of a successful tour: {probability}", file=file)
        file.close()

def run_part2():#This is the function to run the part2
    total_try = 100000
    probabilities = [0.7, 0.8, 0.85]
    k_values = [0, 2, 3]

    for p in probabilities:
        print(f"--- p = {p} ---")

        for k in k_values:
            print(f"LasVegas Algorithm With p = {p}, k = {k}")
            kt = KnightsTour(8, p)
            successful_tours = kt.backtracking_tour(k,total_try)
            probability = successful_tours / total_try

            print(f"Number of successful tours: {successful_tours}")
            print(f"Number of trials: {total_try}")
            print(f"Probability of a successful tour: {probability}")
            print()


if len(sys.argv) != 2 or sys.argv[1] not in ['part1', 'part2']:
    sys.exit(1)

if sys.argv[1] == 'part1':
    run_part1()
else:
    run_part2()

