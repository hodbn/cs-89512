from dummy_impl import DummyImpl
from impl import Impl
from params import params
from runner import run_algorithm


def main():
    impl = Impl(1.0, 0.1, ciphertexts=[open("enc.txt", "r").read()])
    solution = run_algorithm(impl, params)
    print(f"solution={solution}")
    print(f"fitness={impl.fitness(solution)}")
    print(f"calls_to_fitness={impl.fitness_calls}")


if __name__ == "__main__":
    main()
