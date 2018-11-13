#! /usr/bin/python

import sys

if len(sys.argv) != 2:
	print("Error, usage: name.py source_node")
	exit(1)

current_point = None	
start = sys.argv[1]
neighbor = []
flat_neighbor = []

for l in sys.stdin:
	l = l.strip()
	l = l.split('\t')
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
if current_point == start:
	liste = [current_point, 0, 'unvisited', start]
else : liste = [current_point, float('inf'), 'unvisited', start]
flat_neighbor = [item for sublist in neighbor for item in sublist]
liste = liste + flat_neighbor
print '%s' % '\t'.join([str(x) for x in liste])