import functools
import random

from genetic_algorithm import (GAMetrics, GeneticAlgorithm, Individual,
                               Optional, Population)


class DummyImpl(GeneticAlgorithm):
    def __init__(self, bits: int) -> None:
        super().__init__()
        self.bits = bits
        self._metrics = GAMetrics()

    def generate_individual(self) -> Individual:
        return tuple(random.randint(0, 1) for _ in range(self.bits))

    def mutate(self, ind: Individual) -> Individual:
        pos = random.randint(0, self.bits - 1)
        return tuple(b if i != pos else 1 - b for i, b in enumerate(ind))

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        pos = random.randint(0, self.bits - 1)
        return random.choice(
            [parent1[:pos] + parent2[pos:], parent2[:pos] + parent1[pos:]]
        )

    @functools.cache
    def fitness(self, ind: Individual) -> float:
        self.metrics.fitness_calls += 1
        n = 0
        prev = None
        for b in ind:
            if b != prev and prev is not None:
                n += 1
            prev = b
        return n

    def end_condition(self, pop: Population, gen: int) -> Optional[Individual]:
        if gen == 100:
            return max(pop, key=self.fitness)
        return None

    @property
    def metrics(self) -> GAMetrics:
        return self._metrics
