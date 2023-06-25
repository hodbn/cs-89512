import sys
from pathlib import Path

from funcs import get_test_dataset_fn, get_train_dataset_fn


def open_dataset(fp: Path):
    return fp.open("r").readlines()


def split_dataset(dataset, ratio: float):
    n = int(len(dataset) * ratio)
    return dataset[:n], dataset[n:]


def write_dataset(dataset, fp: Path):
    return fp.open("w").writelines(dataset)


def main():
    dataset_fn = Path(sys.argv[1])
    dataset = open_dataset(dataset_fn)
    train, test = split_dataset(dataset, 0.75)
    print(f"dataset file = {dataset_fn}")
    print(f"dataset size = {len(dataset)}")

    train_dataset_fn = get_train_dataset_fn(dataset_fn)
    print(f"train dataset file = {train_dataset_fn}")
    print(f"train size = {len(train)}")
    write_dataset(train, train_dataset_fn)

    test_dataset_fn = get_test_dataset_fn(dataset_fn)
    print(f"test dataset file = {test_dataset_fn}")
    print(f"test size = {len(test)}")
    write_dataset(test, test_dataset_fn)


if __name__ == "__main__":
    main()
