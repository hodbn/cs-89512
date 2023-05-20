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
