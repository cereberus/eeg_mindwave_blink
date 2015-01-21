#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui
from parser import Parser # mindwave eeg class
import random
import csv
import os
import multiprocessing
# import datetime

if os.path.isfile('baseline_raw.csv'):
    os.remove('baseline_raw.csv')
if os.path.isfile('blink_raw.csv'):
    os.remove('blink_raw.csv')
if os.path.isfile('norma_raw.csv'):
    os.remove('norma_raw.csv')
if os.path.isfile('esense_raw.csv'):
    os.remove('esense_raw.csv')
# if os.path.isfile('../csv_eeg_ann/raw_stimulus_mik_model.csv'):
#     os.remove('../csv_eeg_ann/raw_stimulus_mik_model.csv')

def start_recording(e):
    while not (exp_end.is_set()):
        if blink_present.is_set():
            p.stop_norma_recording()
            p.start_blink_recording('blink_raw.csv')
        else:
            p.stop_blink_recording()
        if norma_present.is_set():
            p.start_norma_recording('norma_raw.csv')
        if stimulus_shown.is_set():
            p.update(True)
        else:
            p.update(False)
        if p.sending_data:    
            pass
        else:
            print('Connection lost. Device not sending data')
            break

exp_end = multiprocessing.Event()
stimulus_shown = multiprocessing.Event()
blink_present = multiprocessing.Event()
norma_present = multiprocessing.Event()

mindwave_rec = multiprocessing.Process(name='block', 
                             target=start_recording,
                             args=(exp_end,))

################################################################
#                                                              #
#                  VARIABLES DECLARATION                       #
#                                                              #
################################################################

# sampling frequency (per second)
fs = 512

# calibration_size
cali_size = 40
# font size
font_size = 30

# experiment duration (in seconds)
exp_duration = 60

# clocks
time_control = core.Clock()
pause_init = 2.0
pause_stimulus = 0.5
stimulus_app_time = []
stimulus_expo_time = 5

################################
#                              #
# TEXT SECTION:                #
#     WELCOME, PREP, GOOD BYE  #
#                              #
################################
text_welcome=u"Witamy w eksperymencie! \
    Na środku ekranu pojawiać się będzie czerwony kwadrat. \
    Gdy pojawi się kwadrat mrugaj tak długo jak długo widzisz kwadrat. \
    Staraj się proszę by mrugnięcia były jak najbardziej spontaniczne. \
    Mrugaj raz za razem nie robiąc przerw. \
    Nie wolno Ci mrugać w przypadku innym niż pojawienie się kwadratu. \
    Naciśnij spację by przejść dalej."
text_preparation_begin=u"Pierwsze kilka kwadratów zostanie zaprezentowane \
        na próbę. Naciśnij spację by rozpocząć serię próbną."
text_preparation_end=u"Teraz możemy przejść do głównego badania. \
        Naciśnij spację by rozpocząć właściwą część eksperymentu."
text_goodbye=u"Dziękujemy za udział w badaniu. \
        Nacisnij escape by wyjść."

text_cali_pending=u'Kalibracja EEG'
text_cali_success=u'Kalibracja EEG zakończona pomyślnie'
text_cali_failure=u'Kalibracja EEG zakończona porażką'

text_cali_pending_color = 'Blue'
text_cali_success_color = 'Green'
text_cali_failure_color = 'Red'


################################
#                              #
# WINDOW AND STIMULUS CREATION #
#                              #
################################
mywin = visual.Window([2560, 1440],monitor="testMonitor", \
        winType='pyglet', units="pix", fullscr = True, )
mywin.setMouseVisible(False)

win_end = visual.Window([1500,800],monitor="testMonitor", \
        winType='pyglet', units="pix")

#fixation = visual.PatchStim(win=mywin, size=0.2, pos=[0,0], sf=0, rgb=-1)
#fixation = visual.PatchStim(win=mywin, color=-1, colorSpace='rgb', tex=None, mask='circle',size=0.2)

def cali_display(cali_status):
    if cali_status == 'pending':
        calibration = visual.TextStim(mywin, \
                                      text = text_cali_pending, \
                                      color= text_cali_pending_color, \
                                      height=cali_size)
        calibration.draw()
    if cali_status == 'success':
        calibration = visual.TextStim(mywin, \
                                      text = text_cali_success, \
                                      color= text_cali_success_color, \
                                      height=cali_size)
        calibration.draw()
    if cali_status == 'failure':
        calibration = visual.TextStim(mywin, \
                                      text = text_cali_failure, \
                                      color= text_cali_failure_color, \
                                      height=cali_size)
        calibration.draw()

rect = visual.Rect(mywin, width=100, height=100, \
       fillColor='Red', lineColor='Red')
# rect.setColor((0, 128, 255), 'rgb255')

################################################################
#                                                              #
#    EXPERIMENT CORE    EXPERIMENT CORE    EXPERIMENT CORE     #
#                                                              #
################################################################
exp_entire_time_beg = time_control.getTime()

cali_display('pending')
mywin.flip()
p = Parser()
p.start_raw_recording("baseline_raw.csv")
p.start_esense_recording("esense_raw.csv")
p.update(False)
if p.sending_data == 1:
    cali_display('success')
    mywin.flip()
    core.wait(1.5)
else:
    cali_display('failure')
    mywin.flip()
    core.wait(2)
    print('Could not connect to MindWave Mobile. Quiting core.')
    core.quit()

welcome=visual.TextStim(mywin, text = text_welcome, height=font_size)
# welcome=visual.TextStim(mywin, text = words_string, wrapWidth =5)
welcome.draw()
mywin.flip()

while not 'space' in event.getKeys():
    pass
    
mywin.flip()
print(str(time_control.getTime()) + ' instructions read')

mindwave_rec.start()

print(str(time_control.getTime()) + ' connection request')

print(str(time_control.getTime()) + ' exepriment starts')
exp_core_time_beg = time_control.getTime()
core.wait(pause_init)
print(str(time_control.getTime()) + ' fife second expired')
print('how many times?: ' + str(exp_duration/stimulus_expo_time/2))

for i in range(exp_duration/stimulus_expo_time/2):
    rect.draw()
    mywin.flip()
    norma_present.clear()
    stimulus_shown.set()
    blink_present.set()
    core.wait(stimulus_expo_time)
    mywin.flip()
    stimulus_shown.clear()
    blink_present.clear()
    core.wait(1.0)
    norma_present.set()
    core.wait(stimulus_expo_time-1.0)


    
exp_core_time_end = time_control.getTime()

exp_core_time_diff = exp_core_time_end -  exp_core_time_beg
print('core exp duration: ' + str(exp_core_time_diff))

mywin.flip()
goodbye=visual.TextStim(mywin, text = text_goodbye, height=font_size)
goodbye.draw()
mywin.flip()

exp_end.set()
goodbye_end_start = time_control.getTime()
while not 'escape' in event.getKeys():
    pass

goodbye_end_stop = time_control.getTime()
goodbye_time = goodbye_end_stop - goodbye_end_start

mywin.close()

# time of the entire experiment
exp_entire_end = time_control.getTime()
exp_entire_time = exp_entire_end - exp_entire_time_beg

win_end.flip()

with open('baseline_raw.csv', 'r') as f:
    rows = list(csv.reader(f))
#     exp_beg = len(rows) - (exp_duration+int(pause_init))*int(fs)
    exp_beg = len(rows) - (exp_duration)*int(fs)
    del(rows[0:exp_beg])
    with open('../csv_eeg_ann/eeg_train.csv','wb') as f:
        save=csv.writer(f)
        for i in range(len(rows)-1):
            save.writerow([rows[i][0],rows[i][1]])

# some cleanup
core.quit()
########
