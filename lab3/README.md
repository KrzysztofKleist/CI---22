# Computational Intelligence

## Lab 3: Policy Search

The solution to the lab is based on Professor Giovanni Squillero's lectures and provided examples.

### Problem description

Write agents able to play [_Nim_](https://en.wikipedia.org/wiki/Nim), with an arbitrary number of rows and an upper bound $k$ on the number of objects that can be removed in a turn (a.k.a., _subtraction game_).

The player **taking the last object wins**.

- Task3.1: An agent using fixed rules based on _nim-sum_ (i.e., an _expert system_)
- Task3.2: An agent using evolved rules
- Task3.3: An agent using minmax
- Task3.4: An agent using reinforcement learning

## Solution and results

### Task 3.1 - fixed rules

In fixed rules solution (function `krzysztof`) I assumed that the player at the beggining is playing high numbers of sticks. When they reach 10 sticks left the player stars playing it safe - so they remove either one or two sticks depending if numer of sticks left is even (player takes 2) or odd (player takes 1).

#### Results

The results are quite promising. Games were played in following configurations: `for NIM_SIZE in [3, 4, 5, 8, 10, 15, 20]`, `for NUM_MATCHES in [10, 100, 1000]`, `for k in [None, 5, 3, 2]`.
Agent `krzysztof` was playing against `pure_random` and through all above configurations it reached average of 78% wins. Partial results can be seen in notebook file.

### Task 3.2 - evolved rules

In the solution for the task 3.2 I'm evolving scores used to determine which method will be implemented for current iteration. The options are:

- `pure_random` - presented at the lecture,
- `gabriele` - presented at the lecture,
- `longest_row` - takes random numer of sticks from the longest row,
- `shorterst_row` - takes random numer of sticks from the shortest row,
- `take_one` - takes one stick from the first non-empty row starting form the top,
- `krzysztof` - my strategy, presented above,
- `nim_sum` (`optimal_strategy`) - it's optional, the code was ran using both options - with and without `nim_sum`.

#### Fitness function

Fitness function was simply `evaluate` function that returned number of won matches divided by the number of all matches (`NUM_MATCHES`).

#### Evolution

For evolution 3 different approaches were used:

- `cross_over` - normal crossover taking some elements from one genome, and the rest from the other,
- `average_cross_o` - takes averages of genomes of two parents,
- `mutation` - normal mutation, chooses random gene and then inserts random value (between 0 and 1) there.

#### Results

The results for all combinations are better than expected.

Obviously agents that had an option of choosing `nim_sum` strategy were always eveolving towards it playing both against `pure_random` and `optimal_strategy`.

Agents without `nim_sum` on the other hand also perforemd well almost always winning against `pure_random` and having quite a chance against `nim_sum`. The reason for that is `nim_sum` tends to underperform when a fixed value of `k` is used, because it cannot always determine the optimal move.

##### Playing against `pure_random` without `nim_sum`

| NUM_GENERATIONS | NIM_SIZE | NUM_MATCHES | k   | win_rate |
| --------------- | -------- | ----------- | --- | -------- |
| 10              | 3        | 10          |     | 0.9      |
| 10              | 3        | 10          | 5   | 1.0      |
| 10              | 3        | 10          | 3   | 0.9      |
| 10              | 3        | 100         |     | 0.69     |
| 10              | 3        | 100         | 5   | 0.69     |
| 10              | 3        | 100         | 3   | 0.7      |
| 10              | 5        | 10          |     | 1.0      |
| 10              | 5        | 10          | 5   | 0.9      |
| 10              | 5        | 10          | 3   | 0.9      |
| 10              | 5        | 100         |     | 0.69     |
| 10              | 5        | 100         | 5   | 0.72     |
| 10              | 5        | 100         | 3   | 0.74     |
| 10              | 10       | 10          |     | 0.9      |
| 10              | 10       | 10          | 5   | 0.9      |
| 10              | 10       | 10          | 3   | 0.9      |
| 10              | 10       | 100         |     | 0.71     |
| 10              | 10       | 100         | 5   | 0.7      |
| 10              | 10       | 100         | 3   | 0.69     |
| 100             | 3        | 10          |     | 1.0      |
| 100             | 3        | 10          | 5   | 1.0      |
| 100             | 3        | 10          | 3   | 1.0      |
| 100             | 3        | 100         |     | 0.73     |
| 100             | 3        | 100         | 5   | 0.77     |
| 100             | 3        | 100         | 3   | 0.78     |
| 100             | 5        | 10          |     | 1.0      |
| 100             | 5        | 10          | 5   | 1.0      |
| 100             | 5        | 10          | 3   | 1.0      |
| 100             | 5        | 100         |     | 0.76     |
| 100             | 5        | 100         | 5   | 0.78     |
| 100             | 5        | 100         | 3   | 0.78     |
| 100             | 10       | 10          |     | 1.0      |
| 100             | 10       | 10          | 5   | 1.0      |
| 100             | 10       | 10          | 3   | 1.0      |
| 100             | 10       | 100         |     | 0.74     |
| 100             | 10       | 100         | 5   | 0.79     |
| 100             | 10       | 100         | 3   | 0.73     |

##### Playing against `pure_random` with `nim_sum`

| NUM_GENERATIONS | NIM_SIZE | NUM_MATCHES | k   | win_rate |
| --------------- | -------- | ----------- | --- | -------- |
| 10              | 3        | 10          |     | 1.0      |
| 10              | 3        | 10          | 5   | 1.0      |
| 10              | 3        | 10          | 3   | 1.0      |
| 10              | 3        | 100         |     | 0.8      |
| 10              | 3        | 100         | 5   | 0.8      |
| 10              | 3        | 100         | 3   | 0.78     |
| 10              | 5        | 10          |     | 0.9      |
| 10              | 5        | 10          | 5   | 0.9      |
| 10              | 5        | 10          | 3   | 0.9      |
| 10              | 5        | 100         |     | 0.84     |
| 10              | 5        | 100         | 5   | 0.76     |
| 10              | 5        | 100         | 3   | 0.77     |
| 10              | 10       | 10          |     | 1.0      |
| 10              | 10       | 10          | 5   | 1.0      |
| 10              | 10       | 10          | 3   | 1.0      |
| 10              | 10       | 100         |     | 0.81     |
| 10              | 10       | 100         | 5   | 0.78     |
| 10              | 10       | 100         | 3   | 0.85     |
| 100             | 3        | 10          |     | 1.0      |
| 100             | 3        | 10          | 5   | 1.0      |
| 100             | 3        | 10          | 3   | 1.0      |
| 100             | 3        | 100         |     | 0.87     |
| 100             | 3        | 100         | 5   | 0.95     |
| 100             | 3        | 100         | 3   | 0.87     |
| 100             | 5        | 10          |     | 1.0      |
| 100             | 5        | 10          | 5   | 1.0      |
| 100             | 5        | 10          | 3   | 1.0      |
| 100             | 5        | 100         |     | 0.84     |
| 100             | 5        | 100         | 5   | 0.89     |
| 100             | 5        | 100         | 3   | 0.8      |
| 100             | 10       | 10          |     | 1.0      |
| 100             | 10       | 10          | 5   | 1.0      |
| 100             | 10       | 10          | 3   | 1.0      |
| 100             | 10       | 100         |     | 0.89     |
| 100             | 10       | 100         | 5   | 0.98     |
| 100             | 10       | 100         | 3   | 0.86     |

##### Playing against `optimal_strategy` without `nim_sum`

| NUM_GENERATIONS | NIM_SIZE | NUM_MATCHES | k   | win_rate |
| --------------- | -------- | ----------- | --- | -------- |
| 10              | 3        | 10          |     | 0.6      |
| 10              | 3        | 10          | 5   | 0.6      |
| 10              | 3        | 10          | 3   | 0.6      |
| 10              | 3        | 100         |     | 0.41     |
| 10              | 3        | 100         | 5   | 0.5      |
| 10              | 3        | 100         | 3   | 0.42     |
| 10              | 5        | 10          |     | 0.6      |
| 10              | 5        | 10          | 5   | 0.7      |
| 10              | 5        | 10          | 3   | 0.5      |
| 10              | 5        | 100         |     | 0.46     |
| 10              | 5        | 100         | 5   | 0.33     |
| 10              | 5        | 100         | 3   | 0.31     |
| 10              | 10       | 10          |     | 0.5      |
| 10              | 10       | 10          | 5   | 0.6      |
| 10              | 10       | 10          | 3   | 0.9      |
| 10              | 10       | 100         |     | 0.45     |
| 10              | 10       | 100         | 5   | 0.51     |
| 10              | 10       | 100         | 3   | 0.68     |
| 100             | 3        | 10          |     | 0.8      |
| 100             | 3        | 10          | 5   | 0.9      |
| 100             | 3        | 10          | 3   | 0.6      |
| 100             | 3        | 100         |     | 0.91     |
| 100             | 3        | 100         | 5   | 0.69     |
| 100             | 3        | 100         | 3   | 0.82     |
| 100             | 5        | 10          |     | 0.7      |
| 100             | 5        | 10          | 5   | 0.8      |
| 100             | 5        | 10          | 3   | 0.7      |
| 100             | 5        | 100         |     | 0.69     |
| 100             | 5        | 100         | 5   | 0.85     |
| 100             | 5        | 100         | 3   | 0.82     |
| 100             | 10       | 10          |     | 0.8      |
| 100             | 10       | 10          | 5   | 0.9      |
| 100             | 10       | 10          | 3   | 0.8      |
| 100             | 10       | 100         |     | 0.71     |
| 100             | 10       | 100         | 5   | 0.84     |
| 100             | 10       | 100         | 3   | 0.86     |

##### Playing against `optimal_strategy` with `nim_sum`

| NUM_GENERATIONS | NIM_SIZE | NUM_MATCHES | k   | win_rate |
| --------------- | -------- | ----------- | --- | -------- |
| 10              | 3        | 10          |     | 0.5      |
| 10              | 3        | 10          | 5   | 0.6      |
| 10              | 3        | 10          | 3   | 0.5      |
| 10              | 3        | 100         |     | 0.47     |
| 10              | 3        | 100         | 5   | 0.28     |
| 10              | 3        | 100         | 3   | 0.36     |
| 10              | 5        | 10          |     | 0.4      |
| 10              | 5        | 10          | 5   | 0.5      |
| 10              | 5        | 10          | 3   | 0.6      |
| 10              | 5        | 100         |     | 0.33     |
| 10              | 5        | 100         | 5   | 0.42     |
| 10              | 5        | 100         | 3   | 0.38     |
| 10              | 10       | 10          |     | 0.6      |
| 10              | 10       | 10          | 5   | 0.6      |
| 10              | 10       | 10          | 3   | 0.5      |
| 10              | 10       | 100         |     | 0.43     |
| 10              | 10       | 100         | 5   | 0.37     |
| 10              | 10       | 100         | 3   | 0.51     |
| 100             | 3        | 10          |     | 0.8      |
| 100             | 3        | 10          | 5   | 0.9      |
| 100             | 3        | 10          | 3   | 0.7      |
| 100             | 3        | 100         |     | 0.58     |
| 100             | 3        | 100         | 5   | 0.86     |
| 100             | 3        | 100         | 3   | 0.83     |
| 100             | 5        | 10          |     | 0.9      |
| 100             | 5        | 10          | 5   | 0.8      |
| 100             | 5        | 10          | 3   | 0.8      |
| 100             | 5        | 100         |     | 0.59     |
| 100             | 5        | 100         | 5   | 0.74     |
| 100             | 5        | 100         | 3   | 0.79     |
| 100             | 10       | 10          |     | 0.7      |
| 100             | 10       | 10          | 5   | 0.9      |
| 100             | 10       | 10          | 3   | 1.0      |
| 100             | 10       | 100         |     | 0.64     |
| 100             | 10       | 100         | 5   | 0.74     |
| 100             | 10       | 100         | 3   | 0.87     |
