#!/usr/bin/python
  
import sys
import time

time_start = time.time()

current_point = None
current_distance = None
current_visit = None
current_path = None
neighbors = []
liste = []
unvis_count = 0
vis_count = 0
  
for l in sys.stdin:
    l = l.strip()
    l = l.split()
    if (str(l[0]) != 'time') & (str(l[0]) != 'count'):
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
            
            # count implemented to see how many points are visited so far
            if current_visit == "visited":
                vis_count += 1
            else:
                unvis_count += 1

            if len(liste) > 4:
                print '%s' % '\t'.join([str(x) for x in liste]) 
            liste = [] 
            current_point = str(l[0])
            current_distance = float(l[1])
            current_visit = str(l[2])
            current_path = l[3]
            neighbors = l[4:]

    elif str(l[0]) == 'time':
        former_time = float(l[1])
        
# last point:
liste = [current_point, current_distance, current_visit, current_path] + neighbors[0:]
print '%s' % '\t'.join([str(x) for x in liste])

if current_visit == "visited":
    vis_count += 1
else:
    unvis_count += 1
print '%s\t%s\t%s' % ('count',vis_count, unvis_count)

time_end = time.time()
runtime = former_time + time_end - time_start

print '%s\t%s' % ('time',runtime)
