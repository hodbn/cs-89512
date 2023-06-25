#!/bin/sh
python3 buildnet0.py && python3 gentestnet.py 0 && python3 runnet0.py && python3 measurenet.py 0
rm testnet0 testnet0_real testnet0_predicted
