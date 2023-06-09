from dummy_impl import DummyImpl
from genetic_algorithm import GAParams
from runner import run_algorithm


def test_dummy_impl():
    for i in range(10):
        params = GAParams(
            pop_size_init=100, pop_size_max=100, mutation_prob=0.7, crossover_prob=0.8
        )
        impl = DummyImpl(8)
        solution = run_algorithm(impl, params)
        assert impl.fitness(solution) == 7
