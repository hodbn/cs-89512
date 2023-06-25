from pathlib import Path

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
    return f"wnet{n}.txt"


def get_dataset_fn(n):
    return f"nn{n}.txt"


def get_train_dataset_fn(dataset_fn: Path):
    return Path(f"{dataset_fn.stem}_train").with_suffix(dataset_fn.suffix)


def get_test_dataset_fn(dataset_fn: Path):
    return Path(f"{dataset_fn.stem}_test").with_suffix(dataset_fn.suffix)


def concrete_predict(out_probs):
    # choose binary outputs (true iff >= 0.5)
    return [(item[0] > 0.5).astype(int) for item in out_probs]
