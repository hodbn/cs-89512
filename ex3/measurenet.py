import itertools
import operator


def main(predicted_fn, real_fn):
    print("*** measuring success rate ***")
    predicted = open(predicted_fn, "r").readlines()
    real = open(real_fn, "r").readlines()
    print(f"predicted results fn = {predicted_fn}")
    print(f"real results fn = {real_fn}")
    assert len(predicted) == len(real)
    print(f"number of results = {len(real)}")
    eqs = list(itertools.starmap(operator.eq, zip(real, predicted)))
    print(f"success = {sum(eqs)}")
    print(f"error = {len(eqs) - sum(eqs)}")
    success_rate = sum(eqs) / float(len(eqs))
    print(f"success rate = {success_rate}")
