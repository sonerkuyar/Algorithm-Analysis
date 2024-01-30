import random
import sys
import math

from KnightsTour import KnightsTour

def random_policy(): 
    '''
    This function tries to find a knight's tour using completely a random policy. 
    It runs 100000 times for each probability and writes the results to a file.
    '''
    try_count = 100000
    probabilities = [0.7, 0.8, 0.85]

    for p in probabilities:
        with open(f"results_{p}.txt", "w") as file:
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

def deterministic_policy():
    '''
    Deterministic policy consist of a semi-deterministic approach. First it takes random k steps and then tries to find a
    path by using recursive backtracking. 
    Deterministic approach applies Warnsdorf's rule while choosing the first forwardtracking leaf.
    '''
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


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['part1', 'part2']:
        print("Usage: python main.py part1|part2")
        sys.exit(1)

    if sys.argv[1] == 'part1':
        random_policy()
    else:
        deterministic_policy()



