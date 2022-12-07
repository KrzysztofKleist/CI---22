from Nim import Nim
from Nim import Nimply
from random import random
from typing import Callable
from copy import deepcopy
from operator import xor
from itertools import accumulate
import random
from collections import namedtuple


# pure_random from the lecture
def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    if state.k == None:
        num_objects = random.randint(1, state.rows[row])
    elif state.rows[row] < state.k:
        num_objects = random.randint(1, state.rows[row])
    else:
        num_objects = random.randint(1, state.k)
    return Nimply(row, num_objects)


# gabriele's idea from the lecture
def gabriele(state: Nim) -> Nimply:
    # pick always the maximum possible number of the lowest row
    possible_moves = [(r, o) for r, c in enumerate(state.rows)
                      for o in range(1, c + 1)]
    if state.k != None:
        possible_moves = [p for p in possible_moves if p[1] <= state.k]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


# my strategy is to play high numbers at first, until, there are only 10 sticks left
# and then to play 1 or 2 sticks each time, depending on how many are left
def krzysztof(state: Nim) -> Nimply:
    sum_rows = sum(row for row in state.rows)

    if sum_rows > 10:
        row = max((x for x in enumerate(state.rows)
                   if x[1] > 0), key=lambda y: y[1])[0]
        if state.k == None:
            num_objects = state.rows[row]
        elif state.rows[row] < state.k:
            num_objects = state.rows[row]
        else:
            num_objects = state.k
        ply = Nimply(row, num_objects)

    elif (sum_rows % 2) == 0:
        # if the number of sticks is even I'm taking 2
        row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
        ply = Nimply(row, 2)

    else:
        # if the number of sticks is odd I'm taking 1
        row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
        ply = Nimply(row, 1)

    return ply


def longest_row(state: Nim) -> Nimply:
    # chooses rows with the most elements
    row = max((x for x in enumerate(state.rows)
              if x[1] > 0), key=lambda y: y[1])[0]
    if state.k == None:
        num_objects = random.randint(1, state.rows[row])
    elif state.rows[row] < state.k:
        num_objects = random.randint(1, state.rows[row])
    else:
        num_objects = random.randint(1, state.k)
    return Nimply(row, random.randint(1, num_objects))


def shortest_row(state: Nim) -> Nimply:
    # chooses rows with the least elements
    row = min((x for x in enumerate(state.rows)
              if x[1] > 0), key=lambda y: y[1])[0]
    if state.k == None:
        num_objects = random.randint(1, state.rows[row])
    elif state.rows[row] < state.k:
        num_objects = random.randint(1, state.rows[row])
    else:
        num_objects = random.randint(1, state.k)
    return Nimply(row, random.randint(1, num_objects))


def take_one(state: Nim) -> Nimply:
    # takes one element from the first non-empty row
    row = tuple((x for x in enumerate(state.rows) if x[1] > 0))[0][0]
    return Nimply(row, 1)


# optimal strategy using nim sum (a bit different implementation than the lecture)
def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, xor)
    return result


def optimal_strategy(state: Nim) -> Nimply:
    # retrieve the possible moves
    possible_moves = [(r, o) for r, c in enumerate(state.rows)
                      for o in range(1, c + 1)]
    if state.k != None:
        possible_moves = [p for p in possible_moves if p[1] <= state.k]

    # check the values of nim_sum after all possible moves
    possible_moves_optimal = list()

    for move in possible_moves:
        temp_state = deepcopy(state)
        temp_state.nimming(Nimply(move[0], move[1]))
        if nim_sum(temp_state) == 0:
            possible_moves_optimal.append(move)

    if possible_moves_optimal == []:
        chosen_move = random.choice(possible_moves)
    else:
        chosen_move = random.choice(possible_moves_optimal)

    return Nimply(chosen_move[0], chosen_move[1])


# function used to determine which partial strategy I'm using every iteration
# based on scores assigned for each strategy (longest_row, shortest_row ... etc.)
def choose_strategy(genome: dict) -> int:
    # multiply scores to get int values
    genome_100 = tuple(int(genome.get(g) * 100) for g in genome)

    # list of values of scores with numbers assigned to each strategy
    prob_list = list()
    # strategy value changing at each iteration
    strategy_value = 1
    for i in genome_100:
        for j in range(i):
            prob_list.append(strategy_value)
        strategy_value += 1

    # returned values are equivalent to:
    # longest_row: 1
    # shortest_row: 2
    # take_one: 3
    # gabriele_strategy: 4
    # pure_random_strategy: 5
    # krzysztof_strategy: 6
    # nim_sum: 7
    # at the end we choose random strategy but the distribution of them
    # in the list is weighted

    return random.choice(prob_list)


def make_strategy(genome: dict) -> Callable:
    # evolvable strategy that takes scores for different partial strategies as parameters
    def evolvable(state: Nim) -> Nimply:

        choice = choose_strategy(genome)

        if choice == 1:  # longest_row
            # chooses rows with the most elements
            ply = longest_row(state)

        if choice == 2:  # shortest_row
            # chooses rows with the least elements
            ply = shortest_row(state)

        if choice == 3:  # take_one
            # takes one element from the first non-empty row
            ply = take_one(state)

        if choice == 4:  # gabriele_strategy
            # implements gabriele_strategy
            ply = gabriele(state)

        if choice == 5:  # pure_random_strategy
            # implements pure_random_strategy
            ply = pure_random(state)

        if choice == 6:  # krzysztof_strategy
            # implements krzysztof_strategy
            ply = krzysztof(state)

        if choice == 7:  # nim_sum
            # implements nim_sum
            ply = optimal_strategy(state)

        return ply

    return evolvable


# games are ran NUM_MATCHES times to check the average result
def evaluate(NUM_MATCHES: int, NIM_SIZE: int, strategy0: Callable, strategy1: Callable, k=None) -> float:
    opponent = (strategy0, strategy1)
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE, k)
        player = 0
        while nim:
            ply = opponent[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 0:
            won += 1
    return won / NUM_MATCHES



def fitness(genome, NUM_MATCHES: int, NIM_SIZE: int, EVALUATION_STRATEGY: Callable, strategy: Callable, k=None):
    # calculates the fitness through evaluate function
    return evaluate(NUM_MATCHES, NIM_SIZE, EVALUATION_STRATEGY, strategy, k)


def check_duplicates(genome, population):
    # prevents from creating duplicates
    population_genome = [p.genome for p in population]
    return (genome in population_genome)


def tournament(population, tournament_size=2):
    # chooses two parents from the population
    return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)


def cross_over(g1, g2):
    # normal crossover
    cut = random.randint(0, len(g1))
    return g1[:cut] + g2[cut:]


def average_cross_over(g1, g2):
    # another way of crossover, takes averages of genomes of two parents
    g_new = tuple(round((g1[i] + g2[i])/2, 4) for i in range(len(g1)))
    return g_new


def mutation(g):
    # normal mutation
    point = random.randint(0, len(g) - 1)
    return g[:point] + (round(random.random(), 4),) + g[point + 1:]


def print_order_of_params(num):
    # helps in displaying results
    if num == 0:
        print("genome=(longest_row, shortest_row, take_one, gabriele_strategy, pure_random_strategy, krzysztof_strategy, nim_sum)")
    else:
        print("genome=(longest_row, shortest_row, take_one, gabriele_strategy, pure_random_strategy, krzysztof_strategy)")
