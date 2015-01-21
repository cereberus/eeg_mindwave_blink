#!/bin/bash

################################################################
# Script for blinking/not-blinking fann training               #
# I dont't know yet why, but it should be run twice            #
################################################################

rm -r -f data_category.data
rm -r -f fann_eeg_learn/data_category.data
rm -r -f csv_eeg_ann/categorized_blink

# python psychopy_experiment/expe_eeg.py

python features_train.py

cd fann_eeg_learn

./fann_train.sh

echo ../cat csv_eeg_ann/categorized_blink
cat csv_eeg_ann/categorized
