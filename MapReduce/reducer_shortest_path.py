#!/usr/bin/python
  
import sys
  
current_point = None
current_distance = None
current_visit = None
current_path = None
neighbors = []
liste = []
  
for l in sys.stdin:
    l = l.strip()
    l = l.split()
    if current_point == str(l[0]) :
        if neighbors != l[4:]:
            neighbors = neighbors + l[4:]
        if float(l[1]) < current_distance :
            current_distance = float(l[1])
            if current_visit != 'visited':
                current_visit = str(l[2])
            current_path = l[3]
        elif float(l[1]) == current_distance:
            if current_visit != 'visited':
                current_visit = str(l[2])
            if len(l[3]) < len(current_path):
                current_path = l[3]
    else :
        liste = [current_point, current_distance, current_visit, current_path] + neighbors[0:]
        if len(liste) > 4:
            print '%s' % '\t'.join([str(x) for x in liste]) 
        liste = [] 
        current_point = str(l[0])
        current_distance = float(l[1])
        current_visit = str(l[2])
        current_path = l[3]
        neighbors = l[4:]
 
liste = [current_point, current_distance, current_visit, current_path] + neighbors[0:]
 
print '%s' % '\t'.join([str(x) for x in liste])
