#! /usr/bin/python

import sys
import time

time_start = time.time()
 
for line in sys.stdin:
    line = line.strip()
    line = line.replace(';',' ').replace(',',' ').replace('\t',' ').split()
    start = line[0]
    dest = line[1]
    dist = line[2]
    print '%s\t%s\t%s' % (start, dest, dist)

time_end = time.time()
runtime = float(time_end - time_start)

print '%s\t%s' % ('time',runtime)
