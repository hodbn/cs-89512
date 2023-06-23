import numpy as np


def mse(y_true, y_pred):
    return np.mean(np.power(y_true - y_pred, 2))


def mse_prime(y_true, y_pred):
    return 2 * (y_pred - y_true) / y_true.size


def tanh(x):
    return np.tanh(x)


def tanh_prime(x):
    return 1 - np.tanh(x) ** 2


def get_predicted_fn(n):
    return f"testnet{n}_predicted"


def get_real_fn(n):
    return f"testnet{n}_real"


def get_test_fn(n):
    return f"testnet{n}"


def get_wnet_fn(n):
    return f"wnet{n}"


def get_dataset_fn(n):
    return f"nn{n}.txt"
