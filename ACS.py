import random as rn
import numpy as np
from numpy.random import choice as np_choice
import math
import time
import dispy as dp
import pycos

class ACS(object):

    def __init__(self, distances, ants_num, best_ant, iterations_num, pheromone_rate, alpha=1, beta=1):
        """
        Args:
            distance (2d np array) - square matrix of distances. Diagonal elements assumed to be np.inf
            ants_num (natural) - number of ants running each iteration
            best_ant (natural) - number of best ants who deposit pheromone
            iterations_num (natural) - number of iterations
            pheromone_rate (float) - Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        """
        self.distances = distances
        self.ants_num = ants_num
        self.best_ant = best_ant
        self.iterations_num = iterations_num
        self.all_inds = range(len(distances))
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.alpha = alpha
        self.beta = beta
        self.pheromone_rate = pheromone_rate

    def gen_path_dist(self, path):
        total_dist = 0
        for node in path:
            total_dist += self.distances[node]
        return total_dist

    def local_pheromone_update(self, all_paths, best_ant, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:best_ant]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]
        

    def global_pheromone_update(self, all_paths, best_ant, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for i in range(len(sorted_paths)):
            if(i == best_ant):
                self.pheromone = (1-self.pheromone_rate)*self.pheromone + self.alpha* 1.0 / sorted_paths[i][1] 
            else:
                self.pheromone *= (1-self.pheromone_rate)

    def bias_exploration(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone * ((1.0 / dist)**self.beta)
        norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move

    def exploitation(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone * ((1.0 / dist)**self.beta)
        move = np.argmax(row)
        return move

    
    def pick_move(self, pheromone, dist, visited, q_0 = 0.9):
        move = 0
        q = rn.uniform(0, 1)
        if(q < q_0):
            move = self.exploitation(pheromone, dist, visited)
        else:
            move = self.bias_exploration(pheromone, dist, visited)
        return move


    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(
                self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.ants_num):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths


    def master_run(self):
        all_paths = None
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.iterations_num):
            all_paths = self.gen_all_paths()
            self.local_pheromone_update(all_paths, self.best_ant, shortest_path = shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if(shortest_path[1] < all_time_shortest_path[1]):
                all_time_shortest_path = shortest_path
            self.pheromone *= self.pheromone_rate
        self.global_pheromone_update(all_paths, self.best_ant, shortest_path = shortest_path)
        shortest_path = min(all_paths, key=lambda x: x[1])
        if(shortest_path[1] < all_time_shortest_path[1]):
            all_time_shortest_path = shortest_path
        return all_time_shortest_path

#     def slave_run(self):
#         import dispy
#         import numpy as np
#         shortest_path = None
#         all_paths = self.gen_all_paths()
#         self.local_pheromone_update(all_paths, self.best_ant, shortest_path = shortest_path)
#         shortest_path = min(all_paths, key=lambda x: x[1])
#         self.pheromone *= self.pheromone_rate
#         self.global_pheromone_update(all_paths, self, shortest_path = shortest_path)
#         shortest_path = min(all_paths, key=lambda x: x[1])
#         return shortest_path

# def compute():
    

# def job_callback(job):
#      if job.status == dp.DispyJob.ProvisionalResult:


    