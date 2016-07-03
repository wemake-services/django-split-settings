#!/bin/env/python

""" This script runs `coveralls` on travis and creates report locally.

Credit goes to https://github.com/brechtm/citeproc-py/blob/master/coveralls.py
"""

import os

from subprocess import call


if __name__ == '__main__':
    # create a report from the coverage data
    if 'TRAVIS' in os.environ:
        rc = call('coveralls')
        raise SystemExit(rc)
    else:
        rc = call(['coverage', 'report'])
        raise SystemExit(rc)
