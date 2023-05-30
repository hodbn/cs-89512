import functools
import random

from genetic_algorithm import (GeneticAlgorithm, Individual, Optional,
                               Population)


class DummyImpl(GeneticAlgorithm):
    def __init__(self, bits: int) -> None:
        super().__init__()
        self.calls = 0
        self.bits = bits

    def generate_individual(self) -> Individual:
        return [random.randint(0, 1) for _ in range(self.bits)]

    def mutate(self, ind: Individual, mutation_prob: float) -> Individual:
        return [b if random.random() < mutation_prob else 1 - b for b in ind]

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        pos = random.randint(0, self.bits - 1)
        opt1 = parent1[:pos] + parent2[pos:]
        opt2 = parent2[:pos] + parent1[pos:]
        return random.choice([opt1, opt2])

    @functools.cache
    def fitness(self, ind: Individual) -> float:
        self.calls += 1
        n = 0
        prev = None
        for b in ind:
            if b != prev and prev is not None:
                n += 1
            prev = b
        return n

    @property
    def fitness_calls(self) -> int:
        return self.calls

    def end_condition(self, pop: Population, gen: int) -> Optional[Individual]:
        if gen == 100:
            return max(pop, key=self.fitness)
        return None
