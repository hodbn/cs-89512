import random

from genetic_algorithm import (GAParams, GeneticAlgorithm, Individual,
                               Population)


def generate_individual(ga: GeneticAlgorithm) -> Individual:
    num = random.randint(0, 2**ga.bits - 1)
    return str(bin(num))[2:].zfill(ga.bits)


def init_population(ga: GeneticAlgorithm, size: int) -> Population:
    return [generate_individual(ga) for _ in range(size)]


def mutate(ind: Individual, params: GAParams) -> Individual:
    flip_bit = lambda b: str(1 - int(b))
    mutate_bit = lambda b: b if random.random() > params.mutation_prob else flip_bit(b)
    return "".join(map(mutate_bit, ind))


def crossover(
    ga: GeneticAlgorithm, parent1: Individual, parent2: Individual
) -> Individual:
    pos = random.randint(0, ga.bits - 1)
    return parent1[:pos] + parent2[pos + 1 :]


def select(ga: GeneticAlgorithm, pop: Population) -> Individual:
    weights = list(map(ga.fitness, pop))
    return random.choices(pop, weights=weights, k=1)[0]


def spawn_offspring(
    ga: GeneticAlgorithm, pop: Population, params: GAParams
) -> Individual:
    parent1 = select(ga, pop)
    parent2 = select(ga, pop)
    offspring = crossover(ga, parent1, parent2)
    mutated_offspring = mutate(offspring, params)
    return mutated_offspring


def next_generation(
    ga: GeneticAlgorithm, pop: Population, params: GAParams
) -> Population:
    return [spawn_offspring(ga, pop, params) for _ in range(params.pop_size_max)]


def run_algorithm(ga: GeneticAlgorithm, params: GAParams) -> Individual:
    pop = init_population(ga, params.pop_size_init)
    gen = 0
    while not ga.end_condition(pop, gen):
        pop = next_generation(ga, pop, params)
    return max(pop, key=ga.fitness)
