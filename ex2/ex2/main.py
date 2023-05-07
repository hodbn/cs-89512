from dummy_impl import DummyImpl
from params import POP_SIZE_INIT, POP_SIZE_MAX
from runner import run_algorithm


def main():
    run_algorithm(DummyImpl(), POP_SIZE_INIT, POP_SIZE_MAX)


if __name__ == "__main__":
    main()
