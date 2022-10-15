# Computational Intelligence

## Lab 1: Set Covering

The solution to the lab is based on Professor Giovanni Squillero's lectures and provided examples, especially 8-puzzle problem.
While completing the task I was working with Diego Gasco, Amine Hamdi, Enrico Magliano and Giovanni Genna.
They all are enrolled in Computational Intelligence course.

### Problem description

The goal of the task was given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$, determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$, such that each number between $0$ and $N-1$ appears in at least one list.

### Solution

The solution to the task is based on the earlier mentioned example. I implemented all the algorithms presented in the example: Breadth-First, Depth-First, Gready Best-First, A\*.
The only problem that I came across is the time of the calculations - when N is 50 calculations start to be too long. I limited the N to values: 5, 10, 20.

### Results

#### Breadth-First

- N = 5: 3 steps; number of elements: 5; visited 32 states, [{0}, {1, 3}, {2, 4}]
- N = 10: 3 steps; number of elements: 12; visited 772 states, [{9, 6}, {0, 1, 3, 4, 5}, {3, 4, 5, 6, 8}]
- N = 20: 5 steps; number of elements: 28; visited 13,580 states, [{8, 4, 7}, {2, 18, 6, 8, 10, 12, 15}, {16, 9, 19, 6}, {0, 16, 17, 5, 11}, {0, 3, 5, 8, 9, 10, 13, 14, 17}]

#### Depth-First

- N = 5: 3 steps; number of elements: 5; visited 16 states, [{2, 3}, {0, 1}, {4}]
- N = 10: 5 steps; number of elements: 15; visited 97 states, [{5, 6}, {1, 3, 6, 7}, {0, 9, 3}, {2, 3, 4}, {8, 9, 3}]
- N = 20: 7 steps; number of elements: 45; visited 129 states, [{0, 1, 2, 3, 5, 7, 14, 17}, {5, 7, 8, 13, 14}, {17, 3, 6, 7, 10, 14}, {3, 6, 7, 13, 15}, {17, 6, 9, 11, 12}, {4, 5, 8, 13, 15, 16, 17, 19}, {0, 1, 2, 3, 6, 13, 17, 18}]

#### Gready Best-First

- N = 5: 3 steps; number of elements: 5; visited 17 states, [{0, 1}, {2, 3}, {4}]
- N = 10: 3 steps; number of elements: 12; visited 62 states, [{0, 1, 3, 4, 5}, {9, 2, 6}, {8, 2, 3, 7}]
- N = 20: 4 steps; number of elements: 29; visited 74 states [{0, 3, 5, 8, 9, 10, 13, 14, 17}, {16, 18, 4, 7, 11, 12, 15}, {0, 1, 2, 3, 6, 13, 17, 18}, {0, 16, 17, 19, 6}]

#### A\*

- N = 5: 3 steps; number of elements: 5; visited 21 states, [{0, 1}, {2, 3}, {4}]
- N = 10: 4 steps; number of elements: 10; visited 750 states, [{0, 1}, {8, 2, 7}, {4, 5, 6}, {9, 6}]
- N = 20: 5 steps; number of elements: 26; visited 15,286 states, [{0, 16, 17, 5, 11}, {1, 3, 13, 14}, {2, 18, 6, 8, 10, 12, 15}, {8, 4, 7}, {2, 18, 6, 8, 10, 12, 15}]
