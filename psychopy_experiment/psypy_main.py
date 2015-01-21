#!/usr/bin/env python2
# -*- coding: utf-8 -*-

################################################################
#                                                              #
# psypy_main.py                                                # 
#     the script with experiment for acquiring                 #
#     the signal for later categorization                      #
#                                                              #
################################################################

# TODO experiment time. It categorizes only to 20th second.

from psychopy import visual, core, event, gui
from parser import Parser # mindwave eeg class
import random
import csv
import os
import multiprocessing
# import datetime

if os.path.isfile('baseline_raw.csv'):
    os.remove('baseline_raw.csv')
if os.path.isfile('esense_raw.csv'):
    os.remove('esense_raw.csv')

def start_recording(e):
    while not (exp_end.is_set()):
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

# number of stimuli
stimuli_number = 14

# stimulus experiment ratio
stimulus_expertment_ratio = exp_duration/stimuli_number

# clocks
time_control = core.Clock()
pause_init = 2.0
pause_stimulus = 0.5
stimulus_app_time = []

################################
#                              #
# TEXT SECTION:                #
#     WELCOME, PREP, GOOD BYE  #
#                              #
################################
text_welcome=u"Witamy w eksperymencie! \
    Na środku ekranu pojawiać się będzie czerwony kwadrat. \
    Gdy pojawi się kwadrat mrugnij proszę jeden raz. \
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


################################
#                              #
# STIMULUS APPEARANCE          #
# TIME RANDOMIZING             #
#                              #
################################

exp_duration_seconds = [i for i in range(3,exp_duration-2)]

for n_th_stimulus in range(stimuli_number):
    second_randomed = random.choice(exp_duration_seconds)
    stimulus_app_time.append(second_randomed)
    exp_duration_seconds.remove(second_randomed)
    if second_randomed-2 in exp_duration_seconds:
        exp_duration_seconds.remove(second_randomed-2)
    if second_randomed-1 in exp_duration_seconds:
        exp_duration_seconds.remove(second_randomed-1)
    if second_randomed+1 in exp_duration_seconds:
        exp_duration_seconds.remove(second_randomed+1)
    if second_randomed+2 in exp_duration_seconds:
        exp_duration_seconds.remove(second_randomed+2)
stimulus_app_time = sorted(stimulus_app_time)
print(stimulus_app_time)
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

for i in range(len(stimulus_app_time)):
    if i == 0:
        core.wait(stimulus_app_time[i]-0.5)
        print('\ns_a_t for '+ str(i+1) + '-th:\n' +\
              str(stimulus_app_time[i]))
        rect.draw()
        mywin.flip()
        stimulus_shown.set()
        core.wait(0.5)
        mywin.flip()
        stimulus_shown.clear()
    if i != 0:
        core.wait(stimulus_app_time[i]-stimulus_app_time[i-1]-0.5)
        print('\ns_a_t for '+ str(i+1) + '-th:\n' + \
              str(stimulus_app_time[i]-stimulus_app_time[i-1]))
        rect.draw()
        mywin.flip()
        stimulus_shown.set()
        core.wait(0.5)
        mywin.flip()
        stimulus_shown.clear()
    if i+1 == len(stimulus_app_time):
        time_left = (exp_duration - stimulus_app_time[i] - 0.5 + 1)
        print('time left: '+ str(time_left))
        core.wait(time_left)
    
exp_end.set()

exp_core_time_end = time_control.getTime()

exp_core_time_diff = exp_core_time_end -  exp_core_time_beg
print(exp_core_time_diff)


mywin.flip()
goodbye=visual.TextStim(mywin, text = text_goodbye, height=font_size)
goodbye.draw()
mywin.flip()

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
    with open ('../csv_eeg_ann/eeg_categ.csv','wb') as f:
        save=csv.writer(f)
        for i in range(len(rows)-1):
            save.writerow([rows[i][0],rows[i][1]])



# some cleanup
core.quit()
########
