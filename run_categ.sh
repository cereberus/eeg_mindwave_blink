#!/bin/bash

################################################################
# Script for blinking/not-blinking categorization              #
# I dont't know yet why, but it should be run twice            #
################################################################

rm -r -f data_category.data
rm -r -f fann_eeg_learn/data_category.data
rm -r -f csv_eeg_ann/categorized_blink

# python psychopy_experiment/expe_eeg.py

python features_categ.py
# cp data_category.data fann_eeg_learn/

cd fann_eeg_learn

./fann_categ.sh

cd ../plotting_data

python plot_eeg_blink_categ.py
