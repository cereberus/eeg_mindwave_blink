#!/bin/bash

################################################################
# Script for blinking/not-blinking categorization              #
# I dont't know yet why, but it should be run twice            #
################################################################

rm -r -f data_category.data
rm -r -f fann_eeg_learn/data_category.data
rm -r -f csv_eeg_ann/categorized_blink

# python psychopy_experiment/expe_eeg.py

python features_eeg.py
cp data_category.data fann_eeg_learn/

echo 'data_category.data length in main folder:'
cat data_category.data | wc -l

cd fann_eeg_learn

echo 'data_category.data length in fann_eeg_learn folder:'
cat data_category.data | wc -l

./fann_compile.sh
# gcc -lfann -l m *_train.c -o fann_eeg_learn/eeg_learn_prog_train
# ./*_prog_train

echo cat csv_eeg_ann/categorized_blink

cd ../plotting_data

python plot_eeg_blink_categ.py
