from dataclasses import dataclass
from typing import Optional, Protocol

Individual = list[int]
Population = list[Individual]


class GeneticAlgorithm(Protocol):
    def generate_individual(self) -> Individual:
        ...

    def mutate(self, ind: Individual, mutation_prob: float) -> Individual:
        ...

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        ...

    def fitness(self, ind: Individual) -> float:
        ...

    def end_condition(self, pop: Population, gen: int) -> Optional[Individual]:
        ...

    @property
    def fitness_calls(self) -> int:
        ...


@dataclass
class GAParams:
    pop_size_init: int
    pop_size_max: int
    mutation_prob: float
    crossover_prob: float
