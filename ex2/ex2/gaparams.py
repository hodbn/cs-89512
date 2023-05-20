from dataclasses import dataclass


@dataclass
class GAParams:
    pop_size_init: int
    pop_size_max: int
    mutation_prob: float
