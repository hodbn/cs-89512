import math
import string

from genetic_algorithm import GeneticAlgorithm, Individual, Population

ALEPHBET = string.ascii_lowercase
N = math.factorial(len(ALEPHBET))
BITS = math.ceil(math.log2(N))


class Impl(GeneticAlgorithm):
    @property
    def bits(self):
        return BITS

    def fitness(self, ind: Individual) -> float:
        raise NotImplementedError()

    def end_condition(self, pop: Population, gen: int) -> bool:
        raise NotImplementedError()
