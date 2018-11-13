#! /usr/bin/python

import sys
import time

time_start = time.time()

if len(sys.argv) != 2:
    print 'Error, usage : reducerPP.py STARTER_NODE'
    exit(1)

current_point = None
start = sys.argv[1]
neighbor = []
flat_neighbor = []
time_list = []

for l in sys.stdin:
    l = l.strip()
    l = l.split('\t')
    if str(l[0]) != 'time':
		if current_point == None:
			current_point = str(l[0])
			neighbor.append([str(l[1]), int(l[2])])
            	    flat_neighbor = [item for sublist in neighbor for item in sublist]
		elif current_point == str(l[0]) :
			neighbor.append([str(l[1]), int(l[2])])
            	    flat_neighbor = [item for sublist in neighbor for item in sublist]
		else :
			if current_point == start:
				liste = [current_point, 0, 'unvisited', start]
			else :
				liste = [current_point, float('inf'), 'unvisited', start]
			liste = liste + flat_neighbor
			print '%s' % '\t'.join([str(x) for x in liste])
			current_point = str(l[0])
			neighbor = []
			neighbor.append([str(l[1]), int(l[2])])
            	    flat_neighbor = [item for sublist in neighbor for item in sublist]
    else:
        time_list.append(float(l[1]))

if current_point == start:
    liste = [current_point, 0, 'unvisited', start]
else : 
    liste = [current_point, float('inf'), 'unvisited', start]
liste = liste + flat_neighbor
print '%s' % '\t'.join([str(x) for x in liste])

former_time = max(time_list)
time_end = time.time()
runtime = former_time + float(time_end - time_start)

print '%s\t%s' % ('time',runtime)


