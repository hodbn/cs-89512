import numpy as np
from network import ActivationLayer, FCLayer, Network

DATASET_FN = "nn0.txt"
OUTPUT_FN = "wnet"


def mse(y_true, y_pred):
    return np.mean(np.power(y_true - y_pred, 2))


def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / y_true.size


def tanh(x):
    return np.tanh(x)


def tanh_prime(x):
    return 1 - np.tanh(x) ** 2


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


def measure(out_probs, y_test):
    # choose binary outputs (true iff >= 0.5)
    out = [(item[0] > 0.5).astype(int) for item in out_probs]
    results = np.equal(out, y_test).all(axis=1)
    return results.sum() / float(results.size)


def main():
    dataset = open_dataset(DATASET_FN)
    train, test = split_dataset(dataset, 0.75)
    print(f"dataset file = {DATASET_FN}")
    print(f"dataset size = {len(dataset)}")
    print(f"train size = {len(train)}")
    print(f"test size = {len(test)}")
    x_train, y_train = read_dataset(train)
    x_test, y_test = read_dataset(test)

    # network
    net = Network()
    net.add(FCLayer(16, 50))
    net.add(ActivationLayer(tanh, tanh_prime))
    net.add(FCLayer(50, 1))
    net.add(ActivationLayer(tanh, tanh_prime))

    print("network structure:")
    print(net)

    print("training...")

    # train
    net.use(mse, mse_prime)
    net.fit(x_train, y_train, epochs=10, learning_rate=0.1)

    print("testing...")

    # test
    out = net.predict(x_test)

    # get success rate
    success_rate = measure(out, y_test)
    print(f"success rate = {success_rate}")

    # training, test = split_dataset(15000)
    # buildnet0(training, test)
    # pass


if __name__ == "__main__":
    main()
