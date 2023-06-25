import pickle

import numpy as np
from funcs import (get_predicted_fn, get_test_fn, get_wnet_fn, mse, mse_prime,
                   tanh, tanh_prime)
from network import ActivationLayer, FCLayer, Network
from utils import concrete_predict


def open_testset(fn):
    return open(fn, "r").readlines()


def read_testset(testset: list[str]):
    def load_entry(fentry: str):
        return ([[int(c, 2) for c in fentry.strip()]],)

    return list(map(np.array, zip(*map(load_entry, testset))))


def main(n):
    network_fn = get_wnet_fn(n)
    predicted_fn = get_predicted_fn(n)
    test_fn = get_test_fn(n)
    print("*** running network on test dataset ***")
    print(f"loading network from {network_fn}...")
    net = pickle.load(open(network_fn, "rb"))

    print(f"loading test dataset from {test_fn}...")
    testset = open_testset(test_fn)
    (x,) = read_testset(testset)

    print("predicting...")
    out_probs = net.predict(x)
    out = concrete_predict(out_probs)

    open(predicted_fn, "w").writelines("\n".join("".join(map(str, y)) for y in out))
    print(f"predictions written to {predicted_fn}")
