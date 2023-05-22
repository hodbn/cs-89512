from dataclasses import dataclass
from typing import Protocol

Individual = str
Population = list[Individual]


class GeneticAlgorithm(Protocol):
    @property
    def bits(self) -> int:
        ...

    def fitness(self, ind: Individual) -> float:
        ...

    def end_condition(self, pop: Population, gen: int) -> bool:
        ...


@dataclass
class GAParams:
    pop_size_init: int
    pop_size_max: int
    mutation_prob: float
