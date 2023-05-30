from dummy_impl import DummyImpl
from genetic_algorithm import GAParams
from impl import Impl
from runner import run_algorithm


def main():
    params = GAParams(
        pop_size_init=80, pop_size_max=50, mutation_prob=0.2, crossover_prob=0.8
    )
    impl = Impl(1.0, 0.1, ciphertexts=[open("enc.txt", "r").read()])
    solution = run_algorithm(impl, params)
    print(f"solution={solution}")
    print(f"fitness={impl.fitness(solution)}")
    print(f"calls_to_fitness={impl.fitness_calls}")


if __name__ == "__main__":
    main()
