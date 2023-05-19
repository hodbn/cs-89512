from typing import Protocol

Individual = list[int]
Population = list[Individual]


class GeneticAlgorithm(Protocol):
    def fitness(self, ind: Individual) -> float:
        ...

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        ...

    def mutate(self, ind: Individual) -> Individual:
        ...

    def generate_individual(self) -> Individual:
        ...

    def end_condition(self, pop: Population, gen: int) -> bool:
        ...
