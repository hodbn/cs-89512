from funcs import get_predicted_fn, get_real_fn
from measurenet import main

PREDICTED_FN = get_predicted_fn(1)
REAL_FN = get_real_fn(1)


if __name__ == "__main__":
    main(PREDICTED_FN, REAL_FN)
