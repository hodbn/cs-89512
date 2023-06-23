#!/bin/sh
python3 buildnet0.py && python3 gentestnet0.py && python3 runnet0.py && python3 measurenet0.py
rm testnet0 testnet0_real testnet0_predicted
