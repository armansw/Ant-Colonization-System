import math
import numpy as np

class MatrixGraph(object):
    
    def parse_input(self, file_name):
        infile = open(file_name, 'r')
        Name = infile.readline().strip().split()[1]
        Comment = infile.readline().strip().split()[1] # COMMENT
        FileType = infile.readline().strip().split()[1] # TYPE
        Dimension = infile.readline().strip().split()[2] # DIMENSION
        EdgeWeightType = infile.readline().strip().split()[1] # EDGE_WEIGHT_TYPE
        infile.readline()

        nodelist = []
        N = int(Dimension)
        for i in range(N):
            x, y = infile.readline().strip().split()[1:]
            nodelist.append([float(x), float(y)])
        infile.close()
        return nodelist

    def euclidean(self, x, y):
        return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)


    def make_distances_array(self, array):
        distances = np.zeros(shape=(len(array), len(array)))
        for i in range(len(array)):
            for j in range(len(array)):
                if(i == j):
                    distances[i][j] = np.inf
                else:
                    distances[i][j] = self.euclidean(array[i], array[j])
        return distances

    def encode_to_array(self, file_name):
        return self.make_distances_array(self.parse_input(file_name))

    def normalize_answer(self, path):
        for i in range(len(path[0])):
            path[0][i] = list(path[0][i])
            path[0][i][0] += 1
            path[0][i][1] += 1
            path[0][i] = tuple(path[0][i])