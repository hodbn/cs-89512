from dummy_impl import DummyImpl
from params import params
from runner import run_algorithm


def main():
    run_algorithm(DummyImpl(), params)


if __name__ == "__main__":
    main()
