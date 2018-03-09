#! /usr/bin/python

import sys

mapper_output = []
new_node = []

for line in sys.stdin:
    line = line.strip()
    
    # conditions pour visiter un node: qu'il ne soit pas encore visite et que son weight soit différent de inf
    if (line[2] == "unvisited") & (line[1] != math.inf):
        line[2] = "visited"
        
        # mise à jour du path:
        if line[0] not in line[3]:
            line[3].append(line[0])

        print '%s' % (line)
        
        for m in line[4:]:
            # nouvelles keys créées à partir des adjancy nodes du node visité
            new_node = m.copy() # on a ici node_name + node distance to last neighbor
            
            # 2nd key - mise à jour des poids associés à chaque adjency node (but = toujours avoir distance from start)
            new_node[1] = new_node[1] + line[1]
            
            # 3ème key - status
            new_node.append("unvisited")
            
            # 4ème key - path
            new_path = line[3].copy()
 
            if m[0] not in new_path:
                new_path.append(m[0])
            new_node.append(new_path)
            
            print '%s' % (line)
    else:
	print '%s' % (line)
