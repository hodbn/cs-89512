import random
import sys

from funcs import get_real_fn, get_test_fn

func0 = lambda x: str(int(x.count("1") >= 8))
func1 = lambda x: str(int(x.count("1") <= 7))
funcs = [func0, func1]


def main():
    print("*** generating test dataset ***")

    n = int(sys.argv[1])
    real_fn = get_real_fn(n)
    test_fn = get_test_fn(n)

    xs = []
    ys = []
    for _ in range(100000):
        x = "".join(map(str, (random.randint(0, 1) for _ in range(16))))
        y = funcs[n](x)
        xs.append(x)
        ys.append(y)

    open(test_fn, "w").write("\n".join(xs))
    print(f"test dataset written to {test_fn}")
    open(real_fn, "w").write("\n".join(ys))
    print(f"real test results written to {real_fn}")


if __name__ == "__main__":
    main()
