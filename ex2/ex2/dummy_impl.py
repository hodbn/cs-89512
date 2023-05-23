import functools

from genetic_algorithm import (GeneticAlgorithm, Individual, Optional,
                               Population)


class DummyImpl(GeneticAlgorithm):
    def __init__(self) -> None:
        super().__init__()
        self.calls = 0

    @property
    def bits(self):
        return 8

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
