from funcs import get_predicted_fn, get_test_fn, get_wnet_fn
from runnet import main

NETWORK_FN = get_wnet_fn(1)
PREDICTED_FN = get_predicted_fn(1)
TEST_FN = get_test_fn(1)


if __name__ == "__main__":
    main(NETWORK_FN, PREDICTED_FN, TEST_FN)
