#!/usr/bin/env python3

# Copyright (c) 2018 Daniel Jakots
#
# Licensed under the MIT license. See the LICENSE file.

# Apply Pomodoro Technique and signal the user using the computer bell.

import subprocess
import time

SESSION = 25 * 60
SHORT_PAUSE = 5 * 60
LONG_PAUSE = 20 * 60
MUTE = ["xset", "b", "off"]
UNMUTE = ["xset", "b", "on"]


def beep():
    subprocess.run(UNMUTE)
    print('\a')
    subprocess.run(MUTE)


def session():
    for n in range(3):
        print("session begins", time.strftime("%H:%M:%S", time.localtime()))
        beep()
        time.sleep(SESSION)
        beep()
        if n != 2:
            print("spause begins", time.strftime("%H:%M:%S", time.localtime()))
            time.sleep(SHORT_PAUSE)
        else:
            print("lpause begins", time.strftime("%H:%M:%S", time.localtime()))
            time.sleep(LONG_PAUSE)
            beep()


session()
