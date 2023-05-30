import random

from genetic_algorithm import (GAParams, GeneticAlgorithm, Individual,
                               Population)


def init_population(ga: GeneticAlgorithm, size: int) -> Population:
    return [ga.generate_individual() for _ in range(size)]


def select_parents(ga: GeneticAlgorithm, pop: Population) -> list[Individual]:
    weights = list(map(ga.fitness, pop))
    return random.choices(pop, weights=weights, k=2)


def spawn_offspring(
    ga: GeneticAlgorithm, pop: Population, params: GAParams
) -> Individual:
    parent1, parent2 = select_parents(ga, pop)
    offspring = ga.crossover(parent1, parent2)
    mutated_offspring = ga.mutate(offspring, params.mutation_prob)
    return mutated_offspring


def next_generation(
    ga: GeneticAlgorithm, pop: Population, params: GAParams
) -> Population:
    return [spawn_offspring(ga, pop, params) for _ in range(params.pop_size_max)]


def run_algorithm(ga: GeneticAlgorithm, params: GAParams) -> Individual:
    pop = init_population(ga, params.pop_size_init)
    gen = 0
    while True:
        solution = ga.end_condition(pop, gen)
        if solution is not None:
            break
        pop = next_generation(ga, pop, params)
        gen += 1
    return solution
