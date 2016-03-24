#!/usr/bin/env python

import os
import os.path
import glob
import time
import sys

'''
Script to automatically grade cs21 assignments. Takes a lab number and a
username; dumps result of input files to a file called digest. 
'''

if len(sys.argv) != 3:
    print 'Usage: ./quickgrade.py <lab number (01 e.g.)> <your username>'
    exit(1)

lab_num = sys.argv[1]
username = sys.argv[2]
pathstring = '/home/'+username+'/gradingcs21-s16/'
digestnum = 'digest'+lab_num
directories = sorted(os.listdir('.'))

# Directories for instructors, ninjas, and program functionality.
ignore = ['my_labs', 'jk', 'lauri', 'inputs', 'dpike1', 'rmagier1', 'schen4']

# Add .appends here if you need to avoid a particular directory
#ignore.append()

# Clean up any leftover digest and dump files.
os.system('rm -f '+digestnum)
os.system('rm -f dump')

for entry in directories:
    if os.path.isdir(entry) and entry not in ignore:
        os.chdir(entry + '/labs/' + lab_num)
        print '-----Entering %s-----' % entry
        os.system('cp -r '+pathstring+'/inputs/lab'+lab_num+'/* .')
        os.system('rm -f autograde')
        
        # Assemble list of testfiles from the names of the inputfiles.
        # Assumes all testfiles have at least one associated inputfile.
        testfiles = set()
        inputfiles = os.listdir(pathstring+'inputs/lab'+lab_num)
        for inputfile in inputfiles:
            testfiles.add(inputfile[:-1] + '.py')

        # Fixes capitalization issues with filenames
        for f in glob.glob('*.py'):
            result = [fname for fname in testfiles if fname.lower() == f.lower()]
            if result:
                os.system('mv '+f+' '+result[0])
            else:
                os.system('echo '+entry+' >> '+pathstring+'dump')

        # Test all testfiles with their appropriate inputfiles
        for testfile in testfiles:
            for inputfile in inputfiles:
                if testfile[:-3] in inputfile[:-1]:
                    os.system('echo "@@@@@@@@@@@@@@@@@@@@" >> autograde')
                    try:
                        os.system('(python '+testfile+' < '+inputfile+') >> autograde')
                    except IOError:
                        os.system('echo '+entry+' >> '+pathstring+'dump')

                    os.system('echo $"\n" >> autograde')
            os.system('echo $"\n\n" >> autograde')

        # Write the contents of each autograde to a digest file
        # for easy perusal.
        os.system('echo "##########################################"'+' >> '+pathstring+digestnum)
        os.system('echo '+entry+' >> '+pathstring+digestnum) 
        os.system('echo "##########################################"'+' >> '+pathstring+digestnum)
        if os.path.exists('autograde'):
            os.system('cat autograde'+' >> '+pathstring+digestnum)
        else:
            os.system('echo "No output found."'+' << '+pathstring+digestnum)

        time.sleep(0.1)

        os.chdir('../../..')
        print '-----Finished with %s-----\n\n' % entry



