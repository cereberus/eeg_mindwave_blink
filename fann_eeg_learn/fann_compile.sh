#!/bin/bash

# gcc -lfann -l m *_create.c -o eeg_learn_prog_create
# ./*_prog_create
gcc -lfann -l m *_train.c -o eeg_learn_prog_train
./*_prog_train
