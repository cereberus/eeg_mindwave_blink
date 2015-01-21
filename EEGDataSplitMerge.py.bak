#!/usr/bin/env python
'''
Class to manage MindWave Mobile EEG data.
    It alows to:
    * split csv file with EEG data to categories,
    * combine splitted files into one, *.data file for fann (C fann),

    Normal state: 0
    Blinking:     1

# # #

    Function csv_rows_split() splits main csv file into smaller ones.
    USAGE:
    %csv_rows_split(self, \
                    input_file_name, \
                    input_file_size, \
                    norm_or_blink, \
                    sample_num_begin, \
                    sample_num_end)
# # #

    Function fann_category()
    Generates file with EEG signal features. 
    File *.data for FANN recognition.
    One feature per row.
    Use the file later in C script for FANN.

# # #

    Function eeg.feature()
    Generates file with EEG signal features. 
    File *.data for FANN train.
    Tree feature per row. In next row wheather it is blinking or not.
    Use the file later in C script for FANN.
# # #
    '''

import csv
import os
from os import listdir
from os.path import isfile, join
import shutil

from statlib import stats

import random

class EEGDataSplitMerge:
    paths=['norma','blink','categ']
    if not os.path.exists(paths[0]):
        os.makedirs(paths[0])
        print(paths[0]+' empty directory created')
    if not os.path.exists(paths[1]):
        os.makedirs(paths[1])
        print(paths[1]+' empty directory created')
    if not os.path.exists(paths[2]):
        os.makedirs(paths[2])
        print(paths[2]+' empty directory created')
    blink = [ f for f in listdir(paths[0]) if isfile(join(paths[0],f)) ]
    norma = [ f for f in listdir(paths[1]) if isfile(join(paths[1],f)) ]
    categ = [ f for f in listdir(paths[2]) if isfile(join(paths[2],f)) ]
    both_list=[blink, norma, categ]

    #   INIT function
    def __init__(self):
        self.eegdata = self.run()
        self.value='bob'
    
    #   RESET function
    def reset_data(self, *args):
        reseted_dirs = []
        reseted_files = []
        for data_reseted in args:
            if data_reseted==0: 
                shutil.rmtree(self.paths[0], ignore_errors=True)
                os.makedirs(self.paths[0])
                reseted_dirs.append(self.paths[0])
            if data_reseted==1:
                shutil.rmtree(self.paths[1], ignore_errors=True)
                os.makedirs(self.paths[1])
                reseted_dirs.append(self.paths[1])
            if data_reseted==2:
                shutil.rmtree(self.paths[2], ignore_errors=True)
                os.makedirs(self.paths[2])
                reseted_dirs.append(self.paths[2])
            if type(data_reseted)==str:
                if os.path.isdir(data_reseted):
                    shutil.rmtree(data_reseted, ignore_errors=True)
                    os.makedirs(data_reseted)
                    reseted_dirs.append(data_reseted)
                elif os.path.isfile(data_reseted):
                    os.remove(data_reseted)
                    reseted_files.append(data_reseted)
                    

        print('################################')
        print('# reset_data()                 #')
        if len(reseted_dirs)==0 and len(reseted_files)==0:
            print('# status: error: no file       #')
            print('# nor dir has this name        #')
        else:
            print('# status: finished             #')
        print('# director(y/ies) reseted:     #')
        for i in reseted_dirs:
            print('#  * '+i+(32-6-len(i))*' '+'#')
        if len(reseted_dirs)==0:
            print('#  * none                      #')
        print('# file(s) reseted:             #')
        for i in reseted_files:
            print('#  * '+i+(32-6-len(i))*' '+'#')
        if len(reseted_files)==0:
            print('#  * none                      #')

        print('################################')
        print('')

    #   UPDATE_DIRS function
    def update_dirs(self):
        blink = [ f for f in listdir(self.paths[0]) \
            if isfile(join(self.paths[0],f)) ]
        norma = [ f for f in listdir(self.paths[1]) \
            if isfile(join(self.paths[1],f)) ]
        categ = [ f for f in listdir(self.paths[2]) \
            if isfile(join(self.paths[2],f)) ]
        both_list=[blink, norma, categ]
        return both_list

    #   SPLIT function
    def csv_rows_split(self, input_csv, s, e, x, y):
        files_num_current = len(listdir(self.paths[e]))
        with open(input_csv, 'r') as f:
            rows = list(csv.reader(f))
            # floor of state_end - state_begin
            files_num_add=(y-x)//s
            for i in range(files_num_add):
                j=x
                while(j<x+s):
                    with open (\
                        self.paths[e]+'/'+\
                        'eeg_'+self.paths[e]+'_'+'{0:03}'.\
                        format(files_num_current+i)+\
                        '.csv','a') as f:
                        
                        save=csv.writer(f)
                        save.writerow([j, rows[j][0]])
                    j+=1
                x+=s
        print('################################')
        print('# csv_rows_split()             #')
        print('# status:          finished    #')
        print('# output directory:            #')
        print('#  * ' + self.paths[e] + (32-6-len(self.paths[e]))*' ' +'#')
        print('# samples in file: ' + str(s)+(32-20-len(str(s)))*' ' +'#')
        print('# files added:     ' + str(files_num_add)+\
            (32-20-len(str(files_num_add)))*' ' + '#')
        print('# files total num: '+str(files_num_add+files_num_current)\
            +(32-20-len(str(files_num_add+files_num_current)))*' ' + '#')
        print('################################')
        print('') 

    #  ROW_NUM function
    def numbers_of_rows(self):
        for i in self.both_list:
            if len(i) != 0:
                return sum(1 for line in open(self.paths[0]+'/'+i[0]))
            elif len(i) != 0:
                return sum(1 for line in open(self.paths[1]+'/'+i[0]))
            else:
                return 'no_files'

    #   FANN_CATEGORY function
    def fann_category(self,output_data_file):
        for i in range(len(self.both_list)):
            for j in range(len(self.both_list[i])):
                eeg_data_list = []
                sliced_sample_begin = ''
                sliced_sample_end = ''
                eeg_stdev = 0.0
                eeg_data_positive = 0
                eeg_data_negative = 0
                eeg_data_sum = 0
                eeg_data_zero_crossed = 0
                with open (\
                    self.paths[i]+'/'+\
                    self.both_list[i][j] ,'r') as f:
                    rows = list(csv.reader(f))
                    sliced_sample_begin = rows[0][0]
                    sliced_sample_end = rows[len(rows)-1][0]
#                     print(str(i)+' '+str(j))
                    for k in range(len(rows)):
                        eeg_data_list.append(float(rows[k][1]))
                        if float(rows[k][1])>0:
                            eeg_data_positive += float(rows[k][1])
                            if k!=len(rows)-1:
                                if float(rows[k+1][1])<0:
                                    eeg_data_zero_crossed += 1
                        else:
                            eeg_data_negative += float(rows[k][1])
                            if k!=len(rows)-1:
                                if float(rows[k+1][1])>0:
                                    eeg_data_zero_crossed += 1
                    eeg_stdev = stats.stdev(eeg_data_list)
                    f = open(output_data_file,'a')
                    f.write(sliced_sample_begin+'\n')
                    f.write(sliced_sample_end+'\n')
                    f.write(str(eeg_stdev)+'\n')
                    f.write(str(eeg_data_negative)+'\n')
                    f.write(str(eeg_data_zero_crossed)+'\n')
                    f.close()
        
    #   FAETURE function
    def feature(self, output_data_file):
        if not os.path.isfile(output_data_file):
            f = open(output_data_file,'a')
            f.write(str(len(self.both_list[0])+\
                len(self.both_list[1]))+' '+str(3)+' '+str(1)+'\n')
        for i in range(len(self.both_list)):
            for j in range(len(self.both_list[i])):
                eeg_data_list = []
                eeg_data_positive = 0
                eeg_data_negative = 0
                eeg_data_sum = 0
                eeg_data_zero_crossed = 0
                with open (\
                    self.paths[i]+'/'+\
                    self.both_list[i][j] ,'r') as f:
                    rows = list(csv.reader(f))
#                     print(str(i)+' '+str(j))
                    for k in range(len(rows)):
                        eeg_data_list.append(float(rows[k][1]))
                        if float(rows[k][1])>0:
                            eeg_data_positive += float(rows[k][1])
                            if k!=len(rows)-1:
                                if float(rows[k+1][1])<0:
                                    eeg_data_zero_crossed += 1
                        else:
                            eeg_data_negative += float(rows[k][1])
                            if k!=len(rows)-1:
                                if float(rows[k+1][1])>0:
                                    eeg_data_zero_crossed += 1
                    eeg_stdev = stats.stdev(eeg_data_list)
                    f = open(output_data_file,'a')
                    f.write(
                         str(eeg_stdev)+' '\
                         #+ str(eeg_data_positive)+' '\
                         + str(eeg_data_negative)+' '\
                         + str(eeg_data_zero_crossed)+' '\
                        )
                    f.write('\n'+str(i)+'.0'+'\n')
                    f.close()

    #   MERGE function
    def csv_write_splitted(self):
        self.both_list = update_dirs()        
        output_data_file = 'data_eeg.data'
        samples_num = self.numbers_of_rows()
#         print (44*'#'+str(samples_num))
        if samples_num!='no_files':
            if os.path.isfile(output_data_file):
                os.remove(output_data_file)
            f = open(output_data_file,'a')
            f.write(\
                       str(len(self.both_list[0])+\
                       len(self.both_list[1]))+' '+\
                       str(samples_num)+' '+str(1)+'\n'\
                   )
            f.close()
            for i in range(len(self.both_list)):
                for j in self.both_list[i]:
                    with open(self.paths[i]+j, 'r') as f:
                        rows = list(csv.reader(f))
                        for k in range(len(rows)):
                            f = open(output_data_file,'a')
                            #print(str(rows[k][0]))
                            f.write(rows[k][0]+' ')
                            f.close()
                        f = open(output_data_file,'a')
                        f.write('\n'+str(i)+'.0'+'\n')
                        f.close()
            print('################################')
            print('# csv_write_splitted()         #')
            print('# status: finished             #')
            print('# output file:                 #')
            print('# * '+output_data_file+(32-5-len(output_data_file))*' '+'#')
            print('################################')
            print('')
        else:
            print('################################')
            print('# csv_write_splitted()         #')
            print('# status: aborted              #')
            print('# reason:                      #')
            print('#  *  No files in the input    #')
            print('#     directories. Try running #')
            print('#     csv_rows_split() first.  #')
            print('################################')
            print('')

    #   RUN function
    def run(self):
        print('')
        sth = self.update_dirs()
        print(sth)
        print('')
        '''
        if not os.path.exists(self.paths[0]):
            os.makedirs(self.paths[0])
            print(self.paths[0]+' empty directory created')
        if not os.path.exists(self.paths[1]):
            os.makedirs(self.paths[1])
            print(self.paths[1]+' empty directory created')
        print('')
        '''

    #   TEST function
    def test(self, output_data):
        print(self.output_data)
