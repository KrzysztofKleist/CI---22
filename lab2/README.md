# Computational Intelligence

## Lab 2: Set Covering - Genetic Algorithm

The solution to the lab is based on Professor Giovanni Squillero's lectures and provided examples, especially onemax problem.

>

### Problem description

The goal of the task was given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$, determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$, such that each number between $0$ and $N-1$ appears in at least one list.

## Solution

I provided one posible solution with one fitness function. `Genome` is a set of 0s and 1s, that are mapped to the `all_lists`. Only `genome` is modified, `all_lists` stay the same. The length of the `genome` is the same as the length of `all_lists`. The size of `population` and number of `offspring` vary depending on `N`.

### Fitness function

The fitness function calculates the length of current solution and evaluates if current solution contains all the needed numbers (0 if contains, 1 if doesn't, to make it easier to sort). The result of the fitness function is a tuple with the 0 or 1 indicating if the solution is valid and with the calculated length.

### Results

| N    | w      | Number of generations |
| ---- | ------ | --------------------- |
| 5    | 5      | 95                    |
| 10   | 14     | 10000                 |
| 20   | 35     | 20000                 |
| 100  | 224    | 76552                 |
| 500  | 50944  | 514                   |
| 1000 | 486819 | 23                    |

The results for values 5, 10, 20, 100 are acceptable, but the solution is not scalable as it doesn't find good results for 500 and 1000.

### After the deadline

The population and the offspring size were limited for the bigger values of N.
Prevention from creating duplicates both in the offspring and the initial population.

The results are way better, especially for N = 500. 

| N    | w      | Number of generations |
| ---- | ------ | --------------------- |
| 5    | 5      | 17                    |
| 10   | 11     | 10000                 |
| 20   | 24     | 10000                 |
| 100  | 229    | 10000                 |
| 500  | 1651   | 10000                 |
| 1000 | 335162 | 662                   |
