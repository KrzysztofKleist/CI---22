# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
from players import RandomPlayer, Agent, GAPlayer
from objects import Quarto
from tqdm import tqdm
import numpy as np
import random
from collections import namedtuple

import matplotlib.pyplot as plt


def RL_evaluate(player0, NUM_MATCHES=1000, PLOT_STEP=100):
    game = Quarto()
    agent = Agent(game)

    wins1 = 0
    wins1_check = 0

    x_axis = []
    y_axis = []

    for i in tqdm(range(NUM_MATCHES)):
        game.set_players((player0(game), agent))
        winner = game.run()

        if winner == 1:
            wins1 += 1
            wins1_check += 1

        if i % PLOT_STEP == 0 and i != 0:
            # print(i, "win rate:", wins1_check/1000)
            x_axis.append(i)
            y_axis.append(wins1_check/PLOT_STEP)
            wins1_check = 0

        game = Quarto()
        agent.reset(game)

    plt.plot(x_axis, y_axis)
    plt.show()

    return wins1/NUM_MATCHES


def ES_evaluate(NUM_MATCHES, genome):
    won = 0
    num_matches = int(NUM_MATCHES/2)
    for m in range(num_matches):
        # GA as the second player
        game = Quarto()
        game.set_players((RandomPlayer(game), GAPlayer(genome, game)))
        winner = game.run()
        if winner == 1:
            won += 1

        # GA as the first player
        game = Quarto()
        game.set_players((GAPlayer(genome, game), RandomPlayer(game)))
        winner = game.run()
        if winner == 0:
            won += 1

    return won / NUM_MATCHES


def fitness(NUM_MATCHES, genome):
    return ES_evaluate(NUM_MATCHES, genome)


def check_duplicates(genome, population):
    # prevents from creating duplicates
    population_genome = [p.genome for p in population]
    return (genome in population_genome)


def tournament(population):
    # chooses two parents from the population
    return max(random.choices(population), key=lambda i: i.fitness)


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


def modify_population(population, num_to_remove, Individual, NUM_MATCHES, POPULATION_SIZE, GENOME_CHOOSE_LEN, GENOME_PLACE_LEN):
    population = population[-num_to_remove:]

    for n in range(num_to_remove):
        genome_choose = tuple([round(random.random(), 2)
                              for _ in range(GENOME_CHOOSE_LEN)])
        genome_place = tuple([round(random.random(), 2)
                             for _ in range(GENOME_PLACE_LEN)])

        genome = genome_choose + genome_place
        if check_duplicates(genome, population):
            n -= 1
        else:
            population.append(Individual(genome, fitness(NUM_MATCHES, genome)))
        n += 1

    population = sorted(population, key=lambda i: -i.fitness)[:POPULATION_SIZE]


def explore(population, num_to_remove, Individual, NUM_MATCHES, POPULATION_SIZE, GENOME_CHOOSE_LEN, GENOME_PLACE_LEN):
    modify_population(population, num_to_remove, Individual,
                      NUM_MATCHES, POPULATION_SIZE, GENOME_CHOOSE_LEN, GENOME_PLACE_LEN)


def competition_evaluate(NUM_MATCHES, genome0, genome1):
    won = 0
    num_matches = int(NUM_MATCHES/2)
    for m in range(num_matches):
        # GA as the second player
        game = Quarto()
        game.set_players((GAPlayer(genome1, game), GAPlayer(genome0, game)))
        winner = game.run()
        if winner == 1:
            won += 1

        # GA as the first player
        game = Quarto()
        game.set_players((GAPlayer(genome0, game), GAPlayer(genome1, game)))
        winner = game.run()
        if winner == 0:
            won += 1

    return won / NUM_MATCHES


def ES_competition(population):
    result_table = np.zeros(shape=(10, 10))
    for i in range(10):
        for j in range(10):
            if i != j:
                result_table[j][i] = competition_evaluate(100, population[i].genome, population[j].genome)
    return result_table


def main():
    ########################### EVOLUTIONARY  STRATEGY ###########################

    # initial population
    print("----------------------------------------------------------------------")
    print("--------------------------INITIAL POPULATION--------------------------")
    print("----------------------------------------------------------------------")

    GENOME_CHOOSE_LEN = 5
    GENOME_PLACE_LEN = 7

    ### HYPERPARAMETERS ###
    POPULATION_SIZE = 20
    NUM_GENERATIONS = 500
    OFFSPRING_SIZE = 10
    NUM_MATCHES = 100
    #######################

    population = list()
    Individual = namedtuple(
        "Individual", ["genome", "fitness"])

    i = 0
    while i < POPULATION_SIZE:
        # genome is a tuple of probabilities of using certain strategies
        genome_choose = tuple([round(random.random(), 2)
                              for _ in range(GENOME_CHOOSE_LEN)])
        genome_place = tuple([round(random.random(), 2)
                             for _ in range(GENOME_PLACE_LEN)])

        genome = genome_choose + genome_place

        # prevents from creating duplicates
        if check_duplicates(genome, population):
            i -= 1
        else:
            population.append(Individual(genome, fitness(NUM_MATCHES, genome)))
        i += 1

    population = sorted(population, key=lambda i: -i.fitness)[:POPULATION_SIZE]

    for p in population:
        print(p)

    print("----------------------------------------------------------------------")

    # generating offspring

    print("-------------------------GENERATING OFFSPRING-------------------------")
    print("----------------------------------------------------------------------")

    ### HYPERPARAMETERS ###
    TOP_POPULATION_LENGTH = 5
    TOP_POPULATION_REPETITIONS = 5
    NUM_GENOMES_TO_REMOVE = 10
    EXPLORATION_RATE = 0.2
    MUTATION_RATE = 0.2
    CHOOSE_CROSSOVER_RATE = 0.4
    #######################
    total_offspring_counter = 0
    average_co_counter = 0
    normal_co_counter = 0
    mutation_counter = 0
    explore_counter = 0
    top_population_rep_counter = 0

    for g in tqdm(range(NUM_GENERATIONS)):
        offspring = list()
        # top_g = 0
        i = 0
        while i < OFFSPRING_SIZE:
            total_offspring_counter += 1

            p1 = tournament(population)
            p2 = tournament(population)

            # randomly choose form of crossover
            if random.random() < CHOOSE_CROSSOVER_RATE:
                o = average_cross_over(p1.genome, p2.genome)
                average_co_counter += 1
            else:
                o = cross_over(p1.genome, p2.genome)
                normal_co_counter += 1

            # mutate
            if random.random() < MUTATION_RATE:
                o = mutation(o)
                mutation_counter += 1

            # prevents from creating duplicates
            if check_duplicates(o, population) or check_duplicates(o, offspring):
                i -= 1
            else:
                f = fitness(NUM_MATCHES, o)
                offspring.append(Individual(o, f))
            i += 1

        population += offspring
        population = sorted(population, key=lambda i: -
                            i.fitness)[:POPULATION_SIZE]

        # modify the population based on the EXPLORATION_RATE
        if random.random() < EXPLORATION_RATE:
            explore(population, NUM_GENOMES_TO_REMOVE,
                    Individual, NUM_MATCHES, POPULATION_SIZE, GENOME_CHOOSE_LEN, GENOME_PLACE_LEN)
            explore_counter += 1

        # modify the population based on the numbers of repetitions of the best genome combinations
        if g == 0 or update_population == True:
            update_population = False
            top_population = population[:TOP_POPULATION_LENGTH]
            population_repetitions_counter = 0
        elif top_population != population[:5]:
            top_population = population[:TOP_POPULATION_LENGTH]
            population_repetitions_counter = 0
        elif top_population == population[:5]:
            population_repetitions_counter += 1

        if population_repetitions_counter == TOP_POPULATION_REPETITIONS:
            # print(" top population was the same 5 times")
            modify_population(population, NUM_GENOMES_TO_REMOVE,
                              Individual, NUM_MATCHES, POPULATION_SIZE, GENOME_CHOOSE_LEN, GENOME_PLACE_LEN)
            update_population = True
            top_population_rep_counter += 1

    for p in population:
        print(p)

    print("----------------------------------------------------------------------")
    print("----------------------------------------------------------------------")
    print("----------------------------------------------------------------------")

    print("STATS:")
    print("total_offspring_counter =", total_offspring_counter)
    print("average_co_counter =", average_co_counter)
    print("normal_co_counter =", normal_co_counter)
    print("mutation_counter =", mutation_counter)
    print("explore_counter =", explore_counter)
    print("top_population_rep_counter =", top_population_rep_counter)

    print("----------------------------------------------------------------------")
    print("----------------------------GA COMPETITION----------------------------")
    print("----------------------------------------------------------------------")

    final_table = ES_competition(population[:10])
    print(final_table)

    print("----------------------------------------------------------------------")
    print("----------------------------------------------------------------------")
    print("----------------------------------------------------------------------")        

    ##############################################################################

    ########################### REINFORCEMENT LEARNING ###########################
    # win_rate = RL_evaluate(RandomPlayer, 1000, 100)
    # logging.warning(f"main: Win rate for player 1: {win_rate}")
    ##############################################################################


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()
