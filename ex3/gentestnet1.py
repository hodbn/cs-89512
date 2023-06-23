import random

from funcs import get_real_fn, get_test_fn

REAL_FN = get_real_fn(1)
TEST_FN = get_test_fn(1)


def main():
    print("*** generating test dataset ***")
    xs = []
    ys = []
    for _ in range(100000):
        x = "".join(map(str, (random.randint(0, 1) for _ in range(16))))
        y = str(int(x.count("1") <= 7))
        xs.append(x)
        ys.append(y)

    open(TEST_FN, "w").write("\n".join(xs))
    print(f"test dataset written to {TEST_FN}")
    open(REAL_FN, "w").write("\n".join(ys))
    print(f"real test results written to {REAL_FN}")


if __name__ == "__main__":
    main()
