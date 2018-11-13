import pyspark
import time
import sys
from copy import deepcopy

if len(sys.argv) != 2:
    print('Error, usage : Spark-script.py SOURCE_NODE')
    exit(1)

sc= pyspark.SparkContext()
time_start = time.time()
start = sc.broadcast(str(sys.argv[1]))

#### PREPROCESSING

# mapper preprocessing
def map_pp(x):    
    if x[0] == start.value:
        return (x[0], [0, "unvisited", [start.value]])
    else:
        return (x[0], [float('inf'), "unvisited", [start.value]])


# standard mapping to always have the same format
def map_sd(x):
    return (x[0], [x[1][0][0], x[1][0][1], x[1][0][2], x[1][1]])


#### PROCESSING

# emission des prochains nodes a parcourir
def next_nodes(x):
    new_nodes= []
    neigh = x[1][-1]
    for i in range(0,len(neigh),2):
        path = deepcopy(x[1][2])
        if str(neigh[i]) not in path:
            path.append(str(neigh[i]))
        new_nodes.append((neigh[i], (neigh[i+1] + x[1][0], 'unvisited', path)))
    return new_nodes


# mise a jour du statut pour nodes parcourus
def visited(x): 
    if (x[1][1] == 'unvisited') & (x[1][0] < float('inf')):
        path = deepcopy(x[1][2])
        if x[0] not in path:
            path.append(x[0])
        try:
            return (x[0], [x[1][0], 'visited', path, x[1][3]])
        except IndexError:
            return (x[0], [x[1][0], 'visited', path])
    else:
        return x


# choice of the shortest node - reduceByKey
def shortest(x,y):
    if x[0] < y[0]:
        return x
    elif x[0] == y[0]:
        if len(x[2]) < len(y[2]):
            return x
        else:
            return y
    else:
        return y
#input path below
document = sc.textFile('hdfs:///user/hadoop/medium/input/TABLE2_x300.csv')
document.collect()

lines = document.map(lambda x: x.strip().encode('utf-8').replace('\t',',').replace(' ',',').replace(';',',').split(','))

if start.value not in lines.map(lambda x : x[0]).collect():
    print('Error, this SOURCE_NODE is not in the graph (sink node)')
    exit(1)


neighbor = lines.map(lambda x : (x[0],[x[1],float(x[2])])).reduceByKey(lambda x,y : [item for sublist in [x,y] for item in sublist])

keys = lines.map(lambda x : map_pp(x)).reduceByKey(lambda x, y : x)

iterat = keys.join(neighbor).map(lambda x: map_sd(x)).sortBy(lambda x : x[0])

current_count = -1
count_visited = [item[1][1] for item in iterat.collect()].count('visited')
nb_it = 0


# While the number of visited nodes keeps increasing at each step:
while count_visited > current_count:
    current_count = [item[1][1] for item in iterat.collect()].count('visited')
    var = iterat.filter(lambda x : (x[1][1] == 'unvisited') & (x[1][0] < float('inf')) & (len(x[1]) == 4)).map(next_nodes).flatMap(lambda xs: [x for x in xs])
    if var.collect() != []:
        next_neighbors = var.join(neighbor).map(map_sd)
        next_neighbors = next_neighbors.union(var.subtractByKey(neighbor))
        iterat = iterat.map(visited).union(next_neighbors).reduceByKey(shortest).sortBy(lambda x : x[0])
    count_visited = [item[1][1] for item in iterat.collect()].count('visited')
    nb_it += 1

result = iterat.map(visited)

nodes_visited = result.filter(lambda x :x[1][1] == 'visited').map(lambda x: (x[0], x[1][0], x[1][2]))
separated_nodes = result.filter(lambda x :x[1][1] == 'unvisited').map(lambda x: x[0])
        
time_end = time.time()
runtime = time_end - time_start

with open('meta_output.txt','w+') as fichier:
    fichier.write('runtile: {0}'.format(runtime))
    fichier.write('\nnumber of iterations: {0}'.format(nb_it))

with open('spark_result.txt','w+') as fichier:
    fichier.write('Visited Nodes: {0}'.format(nodes_visited.collect()))
    fichier.write('\nSeparated Nodes: {0}'.format(separated_nodes.collect()))


   


