#! /usr/bin/python

import sys
import time

time_start = time.time()

mapper_output = []
new_node = []
new_path = []
path = []

for l in sys.stdin:
    l = l.strip()
    l = l.split()
    if (str(l[0]) != 'time') & (str(l[0]) != 'count'):
   
        # mise a jour du statut pour nodes parcourus
        if (l[2] == "unvisited") & (float(l[1]) < float('inf')):
            l[2] = "visited"

            path = l[3].split('/')
            if l[0] not in path:
                l[3]= "".join([str(car) + '/' for car in path]) + str(l[0])

            print '%s' % '\t'.join([str(x) for x in l])
        
            # emission de nouveaux parcours possibles a partir du node parcouru 
            neighbor = l[4:]

            for i in range(0,len(neighbor),2):
                new_node.append(str(neighbor[0+i]))
                new_node.append(float(neighbor[1+i]) + float(l[1]))
                new_node.append("unvisited")
                new_path = l[3].split('/')
 
                if new_node[0] not in new_path:
                    new_path = "".join([str(car) + '/' for car in new_path]) + str(new_node[0])
                    new_node.append(new_path)

                if len(new_node) >3:         
                    print '%s' % '\t'.join([str(x) for x in new_node])

                new_node = []
                new_path = []
        else:
	    print '%s' % '\t'.join([str(x) for x in l])
        
    elif str(l[0]) == 'time':
        former_time = float(l[1])


time_end = time.time()
runtime = former_time + time_end - time_start

print '%s\t%s' % ('time',runtime)
