from genetic_algorithm import GeneticAlgorithm, Individual, Population


class DummyImpl(GeneticAlgorithm):
    @property
    def bits(self):
        raise NotImplementedError()

    def fitness(self, ind: Individual) -> float:
        raise NotImplementedError()

    def end_condition(self, pop: Population, gen: int) -> bool:
        raise NotImplementedError()