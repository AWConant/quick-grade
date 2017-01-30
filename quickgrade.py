#!/usr/bin/env python

import os
import sys
import time
import glob
import itertools

from os import system

def get_roster(fname):
    '''
    Given a file of usernames that should be tested, read them into a list
    and return it.
    '''
    roster = []
    with open(fname, 'r') as f:
        for line in f:
            roster.append(line.strip())
    return roster

def fix_filenames(prog_names):
    '''
    Try to fix user's python filenames.
    '''
    for f in glob.glob('*.py'):
        # Rename files to lowercase
        system('mv -f %s.py %s.py 2>/dev/null; true' % (f, f.lower()))

        # If intended name is in the student's name for the file, change to
        # the intended name.
        for pname in prog_names:
            if pname in f:
                system('mv -f %s.py %s.py 2>/dev/null; true' % (f, pname))

def write_to_digest(username, digest):
    '''
    Write output to digest file for easy perusal
    '''
    system('echo "################################" >> %s' % digest)
    system('echo %s >> %s' % (username, digest))
    system('echo "################################" >> %s' % digest)
    system('cat autograde >> %s' % digest)

def test_user(prog_names, input_names):
    '''
    Run user's files against the input files. Write output to a file called
    'autograde' in that user's lab directory.
    '''
    # TODO: Solve halting problem
    # TODO: Improve pname/iname matching
    # Run test inputs against programs
    for pname in prog_names:
        for iname in input_names:
            if pname not in iname:
                continue

            system('echo "@@@@@@@@@@@@@@@@@@" >> autograde')
            if system('python %s.py < %s >> autograde' % (pname, iname)):
                # TODO: Maybe accumulate these in a file.
                system('echo "\nCHECK %s BY HAND!" >> autograde' % pname)

            system('echo "" >> autograde')
        system('echo "\n" >> autograde')

def ensure_inputs_direc():
    labs = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12']
    if not os.path.isdir('inputs'):
        os.mkdir('inputs')
        for lab in labs:
            os.mkdir('inputs/%s' % lab)

def ensure_digests_direc():
    if not os.path.isdir('digests'):
        os.mkdir('digests')

def main():
    if len(sys.argv) != 3:
        print('Usage: ./quickgrade.py <lab number (01 e.g.)> <ROSTER file>')
        sys.exit()

    lab_num = sys.argv[1]
    roster_file = sys.argv[2]

    ensure_inputs_direc()
    ensure_digests_direc()

    # Path to large file eventually containing all program output.
    digest = os.getcwd() + '/digests/digest' + lab_num

    system('rm -f %s' % digest)

    # The filenames for the input test files
    input_names = os.listdir('inputs/%s' % lab_num)

    # The names of the programs, without .py
    prog_names = set(name[:-1] for name in input_names)

    for username in get_roster(roster_file):
        print '##### %s #####' % username

        lab_dir = '%s/labs/%s' % (username, lab_num)
        system('cp -r inputs/%s/* %s' % (lab_num, lab_dir))

        # Enter user's directory.
        os.chdir(lab_dir)

        # Attempt to clean up user's filenames.
        fix_filenames(prog_names)

        system('rm -f autograde')

        # Run user's files on appropriate input files.
        test_user(prog_names, input_names)

        # Write output to long digest file.
        write_to_digest(username, digest)

        system('rm -f autograde')

        # Allow for ctrl+c to cancel script
        time.sleep(0.1)

        # Navigate back up to grading directory.
        os.chdir('../../..')

main()
