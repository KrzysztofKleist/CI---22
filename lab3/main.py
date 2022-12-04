from typing import Callable
from copy import deepcopy
from operator import xor
from itertools import accumulate
import random
from collections import namedtuple


Nimply = namedtuple("Nimply", "row, num_objects")


class Nim:
    # Nim class from the lecture
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def k(self) -> int:
        return self._k

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        # assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects


def pure_random(state: Nim) -> Nimply:
    # pure_random from the lecture
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    if state.k == None:
        num_objects = random.randint(1, state.rows[row])
    elif state.rows[row] < state.k:
        num_objects = random.randint(1, state.rows[row])
    else:
        num_objects = random.randint(1, state.k)
    return Nimply(row, num_objects)


def gabriele(state: Nim) -> Nimply:
    # gabriele's idea from the lecture
    # pick always the maximum possible number of the lowest row
    possible_moves = [(r, o) for r, c in enumerate(state.rows)
                      for o in range(1, c + 1)]
    if state.k != None:
        possible_moves = [p for p in possible_moves if p[1] <= state.k]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


def krzysztof(state: Nim) -> Nimply:
    # my strategy is to play high numbers at first, until, there are only 10 sticks left
    # and then to play 1 or 2 sticks each time, depending on how many are left
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


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, xor)
    return result


def optimal_strategy(state: Nim) -> Nimply:
    # optimal strategy using nim sum (a bit different implementation than the lecture)
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


def evaluate(NUM_MATCHES: int, NIM_SIZE: int, strategy0: Callable, strategy1: Callable, k=None) -> float:
    # games are ran NUM_MATCHES times to check the average result
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


# genetic algorithm
# with nim-sum
def ga_nim_sum(POPULATION_SIZE, OFFSPRING_SIZE, NUM_GENERATIONS, NUM_MATCHES, NIM_SIZE, EVALUATION_STRATEGY: Callable, k=None):

    population = list()
    Individual = namedtuple("Individual", ["genome", "fitness"])

    i = 0
    while i < POPULATION_SIZE:
        # genome is a tuple of probabilities of using: longest_row, shortest_row, take_one,
        # gabriele_strategy, pure_random_strategy, krzysztof_strategy or nim_sum strategies
        genome = tuple([round(random.random(), 2) for _ in range(7)])

        # prevents from creating duplicates
        if check_duplicates(genome, population):
            i -= 1
        else:
            population.append(
                Individual(
                    genome,
                    fitness(
                        genome,
                        NUM_MATCHES,
                        NIM_SIZE,
                        EVALUATION_STRATEGY,
                        make_strategy(
                            {"longest_row": genome[0], "shortest_row": genome[1], "take_one": genome[2],
                             "gabriele_strategy": genome[3], "pure_random_strategy": genome[4], "krzysztof_strategy": genome[5], "nim_sum": genome[6]}),
                        k
                    ),
                )
            )
        i += 1

    population = sorted(population, key=lambda i: -i.fitness)[:POPULATION_SIZE]

    for g in range(NUM_GENERATIONS):
        offspring = list()
        i = 0
        while i < OFFSPRING_SIZE:

            p1 = tournament(population)
            p2 = tournament(population)

            # randomly choose form of crossover
            if random.random() < 0.4:
                o = average_cross_over(p1.genome, p2.genome)
            else:
                o = cross_over(p1.genome, p2.genome)

            # mutate
            if random.random() < 0.5:
                o = mutation(o)

            # prevents from creating duplicates
            if check_duplicates(o, population) or check_duplicates(o, offspring):
                i -= 1
            else:
                f = fitness(
                    o,
                    NUM_MATCHES,
                    NIM_SIZE,
                    EVALUATION_STRATEGY,
                    make_strategy(
                        {"longest_row": o[0], "shortest_row": o[1], "take_one": o[2],
                         "gabriele_strategy": o[3], "pure_random_strategy": o[4], "krzysztof_strategy": o[5], "nim_sum": o[6]}),
                    k
                )
                offspring.append(Individual(o, f))
            i += 1

        population += offspring
        population = sorted(population, key=lambda i: -
                            i.fitness)[:POPULATION_SIZE]

    return population[0].fitness


# genetic algorithm
# without nim-sum
def ga(POPULATION_SIZE, OFFSPRING_SIZE, NUM_GENERATIONS, NUM_MATCHES, NIM_SIZE, EVALUATION_STRATEGY: Callable, k=None):

    population = list()
    Individual = namedtuple("Individual", ["genome", "fitness"])

    i = 0
    while i < POPULATION_SIZE:
        # genome is a tuple of probabilities of using: longest_row, shortest_row, take_one,
        # gabriele_strategy, pure_random_strategy or krzysztof_strategy strategies
        genome = tuple([round(random.random(), 2) for _ in range(6)])

        # prevents from creating duplicates
        if check_duplicates(genome, population):
            i -= 1
        else:
            population.append(
                Individual(
                    genome,
                    fitness(
                        genome,
                        NUM_MATCHES,
                        NIM_SIZE,
                        EVALUATION_STRATEGY,
                        make_strategy(
                            {"longest_row": genome[0], "shortest_row": genome[1], "take_one": genome[2],
                             "gabriele_strategy": genome[3], "pure_random_strategy": genome[4], "krzysztof_strategy": genome[5]}),
                        k
                    ),
                )
            )
        i += 1

    population = sorted(population, key=lambda i: -i.fitness)[:POPULATION_SIZE]

    for g in range(NUM_GENERATIONS):
        offspring = list()
        i = 0
        while i < OFFSPRING_SIZE:

            p1 = tournament(population)
            p2 = tournament(population)

            # randomly choose form of crossover
            if random.random() < 0.4:
                o = average_cross_over(p1.genome, p2.genome)
            else:
                o = cross_over(p1.genome, p2.genome)

            # mutate
            if random.random() < 0.5:
                o = mutation(o)

            # prevents from creating duplicates
            if check_duplicates(o, population) or check_duplicates(o, offspring):
                i -= 1
            else:
                f = fitness(
                    o,
                    NUM_MATCHES,
                    NIM_SIZE,
                    EVALUATION_STRATEGY,
                    make_strategy(
                        {"longest_row": o[0], "shortest_row": o[1], "take_one": o[2],
                         "gabriele_strategy": o[3], "pure_random_strategy": o[4], "krzysztof_strategy": o[5]}),
                    k
                )
                offspring.append(Individual(o, f))
            i += 1

        population += offspring
        population = sorted(population, key=lambda i: -
                            i.fitness)[:POPULATION_SIZE]

    return population[0].fitness


if __name__ == "__main__":

    import csv

    with open('pure_random_nim_sum.csv', 'w', newline='') as file:

        writer = csv.writer(file)
        fieldnames = ["NUM_GENERATIONS", "NIM_SIZE",
                      "NUM_MATCHES", "k", "win_rate"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # make_strategy with nim-sum
        EVALUATION_STRATEGY = pure_random
        POPULATION_SIZE = 20
        OFFSPRING_SIZE = 10

        for NUM_GENERATIONS in [10, 100]:
            for NIM_SIZE in [3, 5, 10]:
                for NUM_MATCHES in [10, 100]:
                    for k in [None, 5, 3]:
                        writer.writerow({"NUM_GENERATIONS": NUM_GENERATIONS, "NIM_SIZE": NIM_SIZE, "NUM_MATCHES": NUM_MATCHES, "k": k,
                                         "win_rate": ga_nim_sum(POPULATION_SIZE, OFFSPRING_SIZE,
                                                                NUM_GENERATIONS, NUM_MATCHES, NIM_SIZE,
                                                                EVALUATION_STRATEGY, k)})

        file.close()

    with open('optimal_strategy_nim_sum.csv', 'w', newline='') as file:

        writer = csv.writer(file)
        fieldnames = ["NUM_GENERATIONS", "NIM_SIZE",
                      "NUM_MATCHES", "k", "win_rate"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # make_strategy with nim-sum
        EVALUATION_STRATEGY = optimal_strategy
        POPULATION_SIZE = 20
        OFFSPRING_SIZE = 10

        for NUM_GENERATIONS in [10, 100]:
            for NIM_SIZE in [3, 5, 10]:
                for NUM_MATCHES in [10, 100]:
                    for k in [None, 5, 3]:
                        writer.writerow({"NUM_GENERATIONS": NUM_GENERATIONS, "NIM_SIZE": NIM_SIZE, "NUM_MATCHES": NUM_MATCHES, "k": k,
                                         "win_rate": ga_nim_sum(POPULATION_SIZE, OFFSPRING_SIZE,
                                                                NUM_GENERATIONS, NUM_MATCHES, NIM_SIZE,
                                                                EVALUATION_STRATEGY, k)})

        file.close()

    with open('pure_random_no_nim_sum.csv', 'w', newline='') as file:

        writer = csv.writer(file)
        fieldnames = ["NUM_GENERATIONS", "NIM_SIZE",
                      "NUM_MATCHES", "k", "win_rate"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # make_strategy with nim-sum
        EVALUATION_STRATEGY = pure_random
        POPULATION_SIZE = 20
        OFFSPRING_SIZE = 10

        for NUM_GENERATIONS in [10, 100]:
            for NIM_SIZE in [3, 5, 10]:
                for NUM_MATCHES in [10, 100]:
                    for k in [None, 5, 3]:
                        writer.writerow({"NUM_GENERATIONS": NUM_GENERATIONS, "NIM_SIZE": NIM_SIZE, "NUM_MATCHES": NUM_MATCHES, "k": k,
                                         "win_rate": ga(POPULATION_SIZE, OFFSPRING_SIZE,
                                                        NUM_GENERATIONS, NUM_MATCHES, NIM_SIZE,
                                                        EVALUATION_STRATEGY, k)})

        file.close()

    with open('optimal_strategy_no_nim_sum.csv', 'w', newline='') as file:

        writer = csv.writer(file)
        fieldnames = ["NUM_GENERATIONS", "NIM_SIZE",
                      "NUM_MATCHES", "k", "win_rate"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # make_strategy with nim-sum
        EVALUATION_STRATEGY = optimal_strategy
        POPULATION_SIZE = 20
        OFFSPRING_SIZE = 10

        for NUM_GENERATIONS in [10, 100]:
            for NIM_SIZE in [3, 5, 10]:
                for NUM_MATCHES in [10, 100]:
                    for k in [None, 5, 3]:
                        writer.writerow({"NUM_GENERATIONS": NUM_GENERATIONS, "NIM_SIZE": NIM_SIZE, "NUM_MATCHES": NUM_MATCHES, "k": k,
                                         "win_rate": ga(POPULATION_SIZE, OFFSPRING_SIZE,
                                                        NUM_GENERATIONS, NUM_MATCHES, NIM_SIZE,
                                                        EVALUATION_STRATEGY, k)})

        file.close()
