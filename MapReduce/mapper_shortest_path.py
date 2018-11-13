#! /usr/bin/python

import sys

mapper_output = []
new_node = []
new_path = []
path = []

for line in sys.stdin:
    line = line.strip()
    line = line.split()
    

    if (line[2] == "unvisited") & (float(line[1]) < float('inf')):
        line[2] = "visited"
        
        path = line[3].split('/')
        if line[0] not in path:
            line[3]= "".join([str(car) + '/' for car in path]) + line[0]

        print '%s' % '\t'.join([str(x) for x in line])

        neighbor = line[4:]

        for i in range(0,len(neighbor),2):
            new_node.append(neighbor[0+i])
            new_node.append(float(neighbor[1+i]) + float(line[1]))
            new_node.append("unvisited")
            new_path = line[3].split('/')
 
            if new_node[0] not in new_path:
                new_path = "".join([str(car) + '/' for car in new_path]) + new_node[0]
                new_node.append(new_path)

            if len(new_node) >3:         
                print '%s' % '\t'.join([str(x) for x in new_node])

            new_node = []
            new_path = []

    else:
	print '%s' % '\t'.join([str(x) for x in line])
        

