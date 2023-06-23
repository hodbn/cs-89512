#!/bin/sh
python3 buildnet1.py && python3 gentestnet1.py && python3 runnet1.py && python3 measurenet1.py
rm testnet1 testnet1_real testnet1_predicted
