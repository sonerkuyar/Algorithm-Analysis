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
