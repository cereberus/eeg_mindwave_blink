from EEGDataSplitMerge import EEGDataSplitMerge
import datetime

package_size=128

norma=0
blink=1
categ=2

input_csv='csv_eeg_ann/eeg_train.csv'
output_csv='csv_eeg_ann/splitted_train_'\
        + datetime.datetime.now().strftime("%y_%m_%d_%H_%M")\
        + '.csv'
output_csv_split = 'fann_eeg_learn/data_train.data'


input_line_count = sum(1 for line in open(input_csv))

############################
# states start, states end #
############################
categ_start = 0
categ_finish = input_line_count

############################
#       MAIN PROGRAM       #
############################
eeg = EEGDataSplitMerge()
eeg.reset_data(0,1,2)
eeg.reset_data('data_eeg.data')
eeg.reset_data('data_category.data')
eeg.reset_data(output_csv)
eeg.reset_data(output_csv_split)

eeg.fann_feature_train(\
        package_size,\
        output_csv_split,
        'psychopy_experiment/norma_raw.csv',\
        0,\
        'psychopy_experiment/blink_raw.csv',\
        1\
        )
