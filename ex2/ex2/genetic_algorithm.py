from typing import Protocol

Individual = dict[int, int]
Population = list[Individual]


class GeneticAlgorithm(Protocol):
    def fitness(self, ind: Individual) -> float:
        ...

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        ...

    def mutate(self, ind: Individual) -> Individual:
        ...

    def init_population(self, size: int) -> Population:
        ...

    def end_condition(self, pop: Population, gen: int) -> bool:
        ...
