#!/usr/bin/env python

import csv
import matplotlib.pyplot as plt

fs=512
pause_init=2.0
experiment_time = sum(1 for line in open('../csv_eeg_ann/eeg_mik_raw.csv'))/512
print(experiment_time)

eeg_microvolts=[]
stimulus = []
blink_category = []
blink_time = []
blink_decision = []

################################################################
#     READING EEG BASELINE.CSV                                 #
################################################################
with open('../csv_eeg_ann/eeg_mik_raw.csv', 'r') as f:
    rows = list(csv.reader(f))
#     exp_beg = len(rows) - (experiment_time+4)*fs
#     del(rows[0:exp_beg])
    for i in range(len(rows)):
        eeg_microvolts.append(rows[i][0])


################################################################
#     READING BLINK OUT_PSYPY.CSV                              #
################################################################
with open('../csv_eeg_ann/out_psypy.csv', 'r') as f:
    rows = list(csv.reader(f))
#     del(rows[0:256])
#     for i in range(506):
#         stimulus.append(0)
    for i in range(len(rows)):
        stimulus.append(rows[i][0])


################################################################
#     READING CATEG EEG_BLINK_CATEGORIZED                      #
################################################################
with open('../csv_eeg_ann/categorized_blink') as f:
    lines = f.read().splitlines()

j = 0
for i in range(len(lines)):
    j+=1
    if j==3:
        blink_category.append([[int(lines[i-2]),int(lines[i-1])],float(lines[i])])
        j = 0 
            
blink_category = sorted(blink_category)

for i in range(len(blink_category)):
    blink_time.append(blink_category[i][0][0] + (blink_category[i][0][1] - blink_category[i][0][0]) / 2)
    blink_time.append(blink_category[i][0][0] + ((blink_category[i][0][1] - blink_category[i][0][0]) / 2) + 1)
    blink_decision.append(round(blink_category[i][1])*5)
    blink_decision.append(0)


################################################################
#     PRINTING FOR DEBUG                                       #
################################################################
# print(eeg_microvolts)
# print(stimulus)
print('length of eeg: ' + str(len(eeg_microvolts)))
print('length of stimulus: ' + str(len(stimulus)))
print('seconds of eeg: ' + str(len(eeg_microvolts)/float(512)))
print('seconds of stimulus: ' + str(len(stimulus)/float(512)))

################################################################
#     PLOTTING DATA                                            #
################################################################

plt.plot(eeg_microvolts, color='b')
plt.plot(stimulus, color='k',linewidth=10.0)
if len(blink_time) == len(blink_decision):
    plt.plot(blink_time,blink_decision, color='r',linewidth=5.0)
else:
    print("Wrong size of blink_time or blink_decision list")
plt.xlabel('sample number (512 samples per second)')
plt.ylabel('amplitude (micro Volts)')
plt.show()
