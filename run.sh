#!/bin/sh
python test_without_preprocessing.py inde_3_10000.txt 2 3 topkgp > s_2_topkgp_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 3 3 topkgp > s_3_topkgp_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 4 3 topkgp > s_4_topkgp_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 5 3 topkgp > s_5_topkgp_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 6 3 topkgp > s_6_topkgp_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 2 3 topkgg pa > s_2_pa_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 3 3 topkgg pa > s_3_pa_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 4 3 topkgg pa > s_4_pa_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 5 3 topkgg pa > s_5_pa_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 6 3 topkgg pa > s_6_pa_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 2 3 topkgg ca > s_2_ca_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 3 3 topkgg ca > s_3_ca_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 4 3 topkgg ca > s_4_ca_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 5 3 topkgg ca > s_5_ca_inde
sleep 5
python test_without_preprocessing.py inde_3_10000.txt 6 3 topkgg ca > s_6_ca_inde
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 2 3 topkgp > s_2_topkgp_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 3 3 topkgp > s_3_topkgp_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 4 3 topkgp > s_4_topkgp_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 5 3 topkgp > s_5_topkgp_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 6 3 topkgp > s_6_topkgp_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 2 3 topkgg pa pa > s_2_pa_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 3 3 topkgg pa pa > s_3_pa_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 4 3 topkgg pa > s_4_pa_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 5 3 topkgg pa > s_5_pa_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 6 3 topkgg pa > s_6_pa_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 2 3 topkgg ca > s_2_ca_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 3 3 topkgg ca > s_3_ca_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 4 3 topkgg ca > s_4_ca_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 5 3 topkgg ca > s_5_ca_anti
sleep 5
python test_without_preprocessing.py anti_3_10000.txt 6 3 topkgg ca > s_6_ca_anti
sleep 5