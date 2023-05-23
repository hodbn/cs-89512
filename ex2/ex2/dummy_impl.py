import functools

from genetic_algorithm import (GeneticAlgorithm, Individual, Optional,
                               Population)


class DummyImpl(GeneticAlgorithm):
    @property
    def bits(self):
        return 8

    @functools.cache
    def fitness(self, ind: Individual) -> float:
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
