#!/usr/bin/env python

import csv
import matplotlib.pyplot as plt
import sys

file_name = str(sys.argv[1])
eeg_microvolts=[]

with open(file_name, 'r') as f:
# with open('norma_raw.csv', 'r') as f:
# with open('blink_raw.csv', 'r') as f:
    rows = list(csv.reader(f))
    for i in range(len(rows)):
        eeg_microvolts.append(rows[i][0])

print(eeg_microvolts)
print(len(eeg_microvolts))
print(len(eeg_microvolts)/512)

plt.plot(eeg_microvolts)
plt.ylabel('some numbers')
plt.show()
