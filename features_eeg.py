from EEGDataSplitMerge import EEGDataSplitMerge

sample_size=128

norma=0
blink=1
categ=2
 
# input_csv='eeg_train_025.csv'
# norma_start=1500
# norma_finish=7000
# blink_start=8000
# blink_finish=13500


input_csv='csv_eeg_ann/eeg_mik_raw.csv'
# input_csv='eeg_exec_045_test_mag.csv'
#input_csv='eeg_exec_045_test_mik.csv'

input_line_count = sum(1 for line in open(input_csv))

############################
# states start, states end #
############################
norma_start = 2000
norma_finish = 6000

blink_start = 20000
blink_finish = 24000

categ_start = 0
categ_finish = input_line_count

############################
#       MAIN PROGRAM       #
############################
eeg = EEGDataSplitMerge()
eeg.reset_data(0,1,2)
eeg.reset_data('data_eeg.data')
eeg.reset_data('data_category.data')


# eeg.csv_rows_split('eeg_exec_045.csv', sample_size, norma, \
#     norma_start, norma_finish)
# eeg.csv_rows_split('eeg_exec_045.csv', sample_size, blink, \
#     blink_start, blink_finish)
 
eeg.csv_rows_split(input_csv, sample_size, categ, \
    categ_start, categ_finish)


eeg.feature('data_eeg.data')
eeg.fann_category('data_category.data')


# eeg.csv_rows_split(1500,256,21,0)
# eeg.csv_rows_split(8000,256,21,1)
# eeg.csv_write_splitted()
# eeg.test('')
