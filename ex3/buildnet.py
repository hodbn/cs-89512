import pickle

import numpy as np
from funcs import (concrete_predict, get_dataset_fn, get_wnet_fn, mse,
                   mse_prime, tanh, tanh_prime)
from network import ActivationLayer, FCLayer, Network


def show_metrics(fn, error_rates):
    try:
        import matplotlib.pyplot as plt
    except:
        return
    ypoints = np.array(error_rates)
    plt.plot(ypoints, linestyle="dotted", label="error_rate")
    plt.ylim([0, 1])
    plt.xlabel("epochs")
    plt.title(fn)
    plt.legend()
    plt.show()


def open_dataset(fn):
    return open(fn, "r").readlines()


def split_dataset(dataset, ratio: float):
    n = int(len(dataset) * ratio)
    return dataset[:n], dataset[n:]


def read_dataset(dataset: list[str]):
    def load_entry(fentry: str):
        strx, stry = fentry.split("   ")
        x = [[int(c, 2) for c in strx]]
        y = [int(stry, 2)]
        return (x, y)

    return list(map(np.array, zip(*map(load_entry, dataset))))


def measure(out, y_test):
    results = np.equal(out, y_test).all(axis=1)
    return results.sum() / float(results.size)


def main(n):
    print("*** building network ***")
    dataset_fn = get_dataset_fn(n)
    output_fn = get_wnet_fn(n)
    dataset = open_dataset(dataset_fn)
    print(f"dataset file = {dataset_fn}")
    print(f"dataset size = {len(dataset)}")
    print("splitting dataset...")

    train, test = split_dataset(dataset, 0.75)
    print(f"train size = {len(train)}")
    print(f"test size = {len(test)}")
    x_train, y_train = read_dataset(train)
    x_test, y_test = read_dataset(test)

    # network
    net = Network()
    net.add(FCLayer(16, 16))
    net.add(ActivationLayer(tanh, tanh_prime))
    net.add(FCLayer(16, 1))
    net.add(ActivationLayer(tanh, tanh_prime))

    print("network structure:")
    print(net)

    print("training...")

    # train
    net.use(mse, mse_prime)
    error_rates = net.fit(x_train, y_train, epochs=10, learning_rate=0.1)

    print("testing...")

    # test
    out_probs = net.predict(x_test)
    out = concrete_predict(out_probs)

    # get success rate
    success_rate = measure(out, y_test)
    print(f"success rate = {success_rate}")

    # save network
    pickle.dump(net, open(output_fn, "wb"))
    print(f"network saved to {output_fn}")

    show_metrics(dataset_fn, error_rates)
