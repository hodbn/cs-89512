from dummy_impl import DummyImpl
from params import params
from runner import run_algorithm


def main():
    impl = DummyImpl()
    solution = run_algorithm(impl, params)
    print(f"solution={solution}")
    print(f"fitness={impl.fitness(solution)}")
    print(f"calls_to_fitness={impl.fitness_calls}")


if __name__ == "__main__":
    main()
