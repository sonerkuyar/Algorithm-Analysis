# PROJECT 3- Knights Tour Solution with LasVegas Algorithms

This is a Python program that examines the Knights Tour Problem and its solution with probabilistic algorithms.

## Dependencies

This script requires Python 3.x and the following Python libraries (built-in) installed:

- math
- random
- sys

## How to run code

The script runs with an argument `part1` or `part2`.

Usage: `python3 main.py part1` or `python3 main.py part2`

### PART1 (Complete Probabilistic Approach)

In this part, the program uses a complete probabilistic approach to solve the Knights Tour Problem. The knight is placed on the board and moves randomly until it either covers all squares or cannot make a valid move.

### PART2 (Semi Deterministic Approach)

In this part, the program uses a semi-deterministic approach. The knight is placed on the board and moves through k random steps after that starts to search a path by backtracking based on the Warnsdorff's rule, which states that the knight should always move to an adjacent, unvisited square with the fewest onward moves.

## Output

The program will output the sequence of moves made by the knight to cover all squares on the chessboard. If the knight cannot cover all squares, the program will output the number of squares covered.
Also keeps the statistics over tries.
There is a high-detailed experiments with comments in the `KnightsTour_Report.pdf` file.
 