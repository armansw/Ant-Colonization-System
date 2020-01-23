import numpy as np
import time 
from ACS import ACS
from MatrixGraph import MatrixGraph

mtxgraph = MatrixGraph()
distances = mtxgraph.encode_to_array('example.tsp')
fd = open("exectime.txt", "w+")
acs = ACS(distances, 1, 1, 100, 0.95, alpha=1, beta=1)
start_time = time.time()
shortest_path = acs.master_run()
finish_time = time.time()
mtxgraph.normalize_answer(shortest_path)
print("The shortest path in the graph is {} with length {}".format(shortest_path[0], shortest_path[1]))
fd.close()