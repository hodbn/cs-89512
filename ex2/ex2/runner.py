import math
import random

import numpy as np
from genetic_algorithm import (GAParams, GeneticAlgorithm, Individual,
                               Population)


def init_population(ga: GeneticAlgorithm, size: int) -> Population:
    return [ga.generate_individual() for _ in range(size)]


def select(ga: GeneticAlgorithm, pop: Population, n: int) -> list[Individual]:
    weights = list(map(ga.fitness, pop))
    return random.choices(pop, weights=weights, k=n)


def spawn_offspring(ga: GeneticAlgorithm, pop: Population) -> Individual:
    parent1, parent2 = select(ga, pop, 2)
    offspring = ga.crossover(parent1, parent2)
    return offspring


def copy(ga: GeneticAlgorithm, pop: Population, n: int) -> Population:
    return select(ga, pop, n)


def crossover(ga: GeneticAlgorithm, pop: Population, n: int) -> Population:
    # return [spawn_offspring(ga, pop) for _ in range(n)]

    elite = select(ga, pop, n)
    return [spawn_offspring(ga, elite) for _ in range(n)]

    # elite = select(ga, pop, n)
    # random.shuffle(elite)
    # elite_pairs = zip(elite[::2], elite[1::2])
    # return [spawn_offspring_pair(ga, pair) for pair in elite_pairs]


def mutate(ga: GeneticAlgorithm, pop: Population, mutation_prob: float):
    return [ind if random.random() < mutation_prob else ga.mutate(ind) for ind in pop]


def next_generation(
    ga: GeneticAlgorithm, pop: Population, params: GAParams
) -> Population:
    copied = copy(ga, pop, math.ceil(len(pop) * (1 - params.crossover_prob)))
    offsprings = crossover(ga, pop, math.floor(len(pop) * params.crossover_prob))
    next_gen = mutate(ga, copied + offsprings, params.mutation_prob)
    return next_gen


def run_algorithm(ga: GeneticAlgorithm, params: GAParams) -> Individual:
    pop = init_population(ga, params.pop_size_init)
    gen = 0
    while True:
        solution = ga.end_condition(pop, gen)
        if solution is not None:
            break
        pop = next_generation(ga, pop, params)
        topn = list(sorted(pop, key=ga.fitness, reverse=True)[:10])
        botn = list(sorted(pop, key=ga.fitness)[:10])
        print(f"{gen}")
        avg_fitness = sum(map(ga.fitness, pop)) / len(pop)
        avg_topn_fitness = sum(map(ga.fitness, topn)) / len(topn)
        avg_botn_fitness = sum(map(ga.fitness, botn)) / len(botn)
        best_fitness = ga.fitness(topn[0])
        ga.metrics.avg_fitness.append(avg_fitness)
        ga.metrics.avg_topn_fitness.append(avg_topn_fitness)
        ga.metrics.avg_botn_fitness.append(avg_botn_fitness)
        ga.metrics.diff_inds.append(len(set(pop)))
        ga.metrics.best_fitness.append(best_fitness)
        gen += 1
        if gen == 600:
            break
    return solution
