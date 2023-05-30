import math
import random

from genetic_algorithm import (GAParams, GeneticAlgorithm, Individual,
                               Population)


def init_population(ga: GeneticAlgorithm, size: int) -> Population:
    return [ga.generate_individual() for _ in range(size)]


def select(ga: GeneticAlgorithm, pop: Population, n: int) -> list[Individual]:
    weights = list(map(ga.fitness, pop))
    return random.choices(pop, weights=weights, k=n)


def spawn_offspring(ga: GeneticAlgorithm, pop: Population) -> Individual:
    parent1, parent2 = select(ga, pop, 2)
    offspring = random.choice(ga.crossover(parent1, parent2))
    return offspring


def copy(ga: GeneticAlgorithm, pop: Population, n: int) -> Population:
    return select(ga, pop, n)


def crossover(ga: GeneticAlgorithm, pop: Population, n: int) -> Population:
    return [spawn_offspring(ga, pop) for _ in range(n)]


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
        # top5 = {k: ga.fitness(k) for k in sorted(pop, key=ga.fitness)[:5]}
        # print(f"{gen}: top-5: {top5}")
        gen += 1
    return solution
