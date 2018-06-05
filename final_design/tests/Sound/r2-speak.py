#!/usr/bin/env python

from __future__ import print_function
from ttastromech import TTAstromech
import time


def play(r2, s):
    print(' ')
    print('String:', s)
    r2.speak(s)
    time.sleep(0.5)


r2 = TTAstromech()

msgs = [
    'error',
    'warning',
    'hello',
    'luke',
    'stop',
    'usafa',
    'kevin',
    'ok, this is the end now ... by!'
]

print('This runs through some different strings and plays r2 sounds ... enjoy!')
print(' ')
print('-'*30)

for msg in msgs:
    play(r2, msg)


print('done ...')
