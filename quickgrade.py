#!/usr/bin/env python

import os
import sys
import time
import glob
import traceback

from os import system

if len(sys.argv) != 2:
    print 'Usage: ./quickgrade.py <lab number (01 e.g.)>'
    sys.exit()

lab_num = sys.argv[1]
digest = os.getcwd() + '/digest' + lab_num
direcs = next(os.walk('.'))[1]

# Directories for instructors, ninjas, and script functionality
ignore = ['my_labs', 'jk', 'lauri', 'inputs']

system('rm -f %s' % digest)

for username in direcs:
    if username in ignore:
        continue

    print '-----Beginning %s-----' % username

    lab_dir = '%s/labs/%s' % (username, lab_num)
    system('cp -r inputs/%s/* %s' % (lab_num, lab_dir))

    prog_files = set()
    input_files = os.listdir('inputs/%s' % lab_num)
    for f in input_files:
        prog_files.add(f[:-1] + '.py')

    os.chdir(lab_dir)

    # Try to fix filenames by doing the following:
    # - Rename files to lowercase
    # - If intended name is in the student's name for the file, change to the
    #   intended name.
    for f in glob.glob('*.py'):
        system('mv -f %s %s 2>/dev/null; true' % (f, f.lower()))
        for pfile in prog_files:
            if pfile[:-3] in f:
                system('mv -f %s %s 2>/dev/null; true' % (f, pfile))

    system('rm -f autograde')

    # Run test inputs against programs
    for pfile in prog_files:
        for ifile in input_files:
            if pfile[:-3] not in ifile[:-1]:
                continue
            system('echo "@@@@@@@@@@@@@@@@@@" >> autograde')
            if system('python %s < %s >> autograde' % (pfile, ifile)):
                system('echo "!!!Check %s by hand!!!" >> autograde' % pfile)

            system('echo "\n" >> autograde')

        system('echo "\n\n\n" >> autograde')

    # Write autograded output to digest file for easy perusal
    system('echo "################################" >> %s' %  digest)
    system('echo %s >> %s' % (username, digest))
    system('echo "################################" >> %s' % digest)
    if os.path.exists('autograde'):
        system('cat autograde >> %s' % digest)
    else:
        system('echo "No autograde found." >> %s' % digest)

    time.sleep(0.1)

    os.chdir('../../..')
    print '-----Done with %s-----\n' % username
