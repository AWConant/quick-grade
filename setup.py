#!/usr/bin/env python

import os

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

if __name__ == '__main__':
    ensure_inputs_direc()
    ensure_digests_direc()
