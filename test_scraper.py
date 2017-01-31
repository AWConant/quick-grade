#!/usr/bin/env python

'''
Scrapes Swarthmore CS21 labs for their input test cases; useful for grading
purposes. Relies on the assumption that input lines are in blue text wrapped
by "code" class pre tags.

Meant to be used with quick-grade.py.

Andrew Conant
Spring 2017

'''

import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print('Usage: python3 test_scraper.py <lab number e.g. 03>')
    sys.exit()

lab_num = sys.argv[1]
url = 'https://www.cs.swarthmore.edu/courses/CS21Labs/s17/lab%s.php' % lab_num

# Try to open the url. If it isn't successful, exit.
page = requests.get(url)
if page.status_code != 200:
    print('Bad response; did you supply a valid lab number?')
    sys.exit()

# Parse the html for all 'pre' tags with 'code' classes.
soup = BeautifulSoup(page.text, 'lxml')
code_tags = soup.find_all('pre', class_='code')

# Only include code blocks whose first line begins with 'python'.
programs = [tag for tag in code_tags if tag.text.split()[1] == 'python']

current_name = None
current_file = None
for program in programs:
    blue_lines = program.find_all(attrs={'color': 'blue'})
    blue_lines.extend(program.find_all(attrs={'class': 'blue'}))

    for line in blue_lines:
        words = line.text.split()

        # If the first word of the line is 'python', it begins a new test case.
        if words[0] == 'python':
            # Assuming this isn't the first file, we need to close the previous
            # one.
            if current_file is not None:
                current_file.close()

            program_name = words[1][:-3]
            # If this is the name of a new program, then restart the counter at
            # 0 and it becomes the new current name.
            if current_name != program_name:
                idx = 0
                current_name = program_name
            # Otherwise, it's a new test case for the current program.
            else:
                idx += 1

            # Begin writing to a new file.
            path = 'inputs/%s/%s%d' % (lab_num, current_name, idx)
            current_file = open(path, 'w')

            print(path)
        # Otherwise, it's a continuation of the previous test case and we writt
        # it to the file that we have open.
        else:
            current_file.write(line.text + '\n')
