import random

from genetic_algorithm import GeneticAlgorithm, Population


def init_population(ga: GeneticAlgorithm, size: int):
    return [ga.generate_individual() for _ in range(size)]


def select(ga: GeneticAlgorithm, pop: Population):
    weights = list(map(ga.fitness, pop))
    return random.choices(pop, weights=weights, k=1)[0]


def spawn_offspring(ga: GeneticAlgorithm, pop: Population):
    parent1 = select(ga, pop)
    parent2 = select(ga, pop)
    offspring = ga.crossover(parent1, parent2)
    mutated_offspring = ga.mutate(offspring)
    return mutated_offspring


def next_generation(ga: GeneticAlgorithm, pop: Population, pop_size: int):
    return [spawn_offspring(ga, pop) for _ in range(pop_size)]


def run_algorithm(ga: GeneticAlgorithm, pop_size_init: int, pop_size_max: int):
    pop = init_population(ga, pop_size_init)
    gen = 0
    while not ga.end_condition(pop, gen):
        pop = next_generation(ga, pop, pop_size_max)
    return max(pop, key=ga.fitness)
