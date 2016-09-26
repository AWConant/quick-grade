#!/usr/bin/env python

import os
import sys

labnum = sys.argv[1]
progname = sys.argv[2]

os.chdir('inputs/{}'.format(labnum))

ind = 0
while True:
    case = raw_input('Enter a test case: ')

    if case == '':
        break

    with open('{}{}'.format(progname, ind), 'w') as f:
        f.write(case + '\n')

    ind += 1
