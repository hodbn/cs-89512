import pickle

import numpy as np
from funcs import (get_predicted_fn, get_test_fn, get_wnet_fn, mse, mse_prime,
                   tanh, tanh_prime)
from network import ActivationLayer, FCLayer, Network
from utils import concrete_predict

NETWORK_FN = get_wnet_fn(0)
PREDICTED_FN = get_predicted_fn(0)
TEST_FN = get_test_fn(0)


def open_testset(fn):
    return open(fn, "r").readlines()


def read_testset(testset: list[str]):
    def load_entry(fentry: str):
        return ([[int(c, 2) for c in fentry.strip()]],)

    return list(map(np.array, zip(*map(load_entry, testset))))


def main():
    print("*** running network on test dataset ***")
    print(f"loading network from {NETWORK_FN}...")
    net = pickle.load(open(NETWORK_FN, "rb"))

    print(f"loading test dataset from {TEST_FN}...")
    testset = open_testset(TEST_FN)
    (x,) = read_testset(testset)

    print("predicting...")
    out_probs = net.predict(x)
    out = concrete_predict(out_probs)

    open(PREDICTED_FN, "w").writelines("\n".join("".join(map(str, y)) for y in out))
    print(f"predictions written to {PREDICTED_FN}")


if __name__ == "__main__":
    main()
