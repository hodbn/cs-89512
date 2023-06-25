#!/bin/sh
python3 buildnet1.py && python3 gentestnet.py 1 && python3 runnet1.py && python3 measurenet.py 1
rm testnet1 testnet1_real testnet1_predicted
