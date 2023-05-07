from genetic_algorithm import GeneticAlgorithm, Individual, Population


class DummyImpl(GeneticAlgorithm):
    def fitness(self, ind: Individual) -> float:
        raise NotImplementedError()

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        raise NotImplementedError()

    def mutate(self, ind: Individual) -> Individual:
        raise NotImplementedError()

    def init_population(self, size: int) -> Population:
        raise NotImplementedError()

    def end_condition(self, pop: Population, gen: int) -> bool:
        raise NotImplementedError()
