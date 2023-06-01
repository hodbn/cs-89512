from dataclasses import dataclass, field
from typing import Optional, Protocol

Individual = tuple[int]
Population = list[Individual]


@dataclass
class GAMetrics:
    avg_fitness: list[float] = field(default_factory=list)
    best_fitness: list[float] = field(default_factory=list)
    avg_topn_fitness: list[float] = field(default_factory=list)
    avg_botn_fitness: list[float] = field(default_factory=list)
    diff_inds: list[float] = field(default_factory=list)
    fitness_calls: int = 0


class GeneticAlgorithm(Protocol):
    def generate_individual(self) -> Individual:
        ...

    def mutate(self, ind: Individual) -> Individual:
        ...

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        ...

    def fitness(self, ind: Individual) -> float:
        ...

    def end_condition(self, pop: Population, gen: int) -> Optional[Individual]:
        ...

    @property
    def metrics(self) -> GAMetrics:
        ...


@dataclass
class GAParams:
    pop_size_init: int
    pop_size_max: int
    mutation_prob: float
    crossover_prob: float
