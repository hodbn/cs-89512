import itertools
import operator

from funcs import get_predicted_fn, get_real_fn

PREDICTED_FN = get_predicted_fn(0)
REAL_FN = get_real_fn(0)


def main():
    print("*** measuring success rate ***")
    predicted = open(PREDICTED_FN, "r").readlines()
    real = open(REAL_FN, "r").readlines()
    print(f"predicted results fn = {PREDICTED_FN}")
    print(f"real results fn = {REAL_FN}")
    assert len(predicted) == len(real)
    print(f"number of results = {len(real)}")
    eqs = list(itertools.starmap(operator.eq, zip(real, predicted)))
    print(f"success = {sum(eqs)}")
    print(f"error = {len(eqs) - sum(eqs)}")
    success_rate = sum(eqs) / float(len(eqs))
    print(f"success rate = {success_rate}")


if __name__ == "__main__":
    main()
