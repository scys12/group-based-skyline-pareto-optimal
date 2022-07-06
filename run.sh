#!/bin/sh
python test_without_preprocessing.py anti_2_10000.txt 2 3 pwa
sleep 5
python test_without_preprocessing.py anti_2_10000.txt 4 3 pwa
sleep 5
python test_without_preprocessing.py anti_2_10000.txt 6 3 pwa
sleep 5
python test_without_preprocessing.py anti_2_10000.txt 8 3 pwa
sleep 5