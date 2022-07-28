#!/bin/sh
python test_without_preprocessing.py inde_3_1000.txt 2 3 topkgp > s_2_topkgp_inde
sleep 5
python test_without_preprocessing.py inde_3_1000.txt 3 3 topkgp > s_3_topkgp_inde
sleep 5
python test_without_preprocessing.py inde_3_1000.txt 4 3 topkgp > s_4_topkgp_inde
sleep 5
python test_without_preprocessing.py inde_3_1000.txt 5 3 topkgp > s_5_topkgp_inde
sleep 5