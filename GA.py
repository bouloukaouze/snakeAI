import operator
import uuid
from neuronal_network import *
from game import *
from numpy.random import randint,uniform,rand
import matplotlib.pyplot as plt
import os
import multiprocessing
from time import time
import json

class GA():

    def __init__(self, pop_size, num_select, rate, num_play, id=None):
        self.pop_size = pop_size
        if id == None:
            self.id = uuid.uuid4().hex
            os.mkdir(f"snakes_{self.pop_size}_{self.id}")
        else:
            self.id = id
        self.num_select = num_select
        self.rate = rate
        self.num_play = num_play
        self.pop = [NeuronalNetwork() for _ in range(pop_size)]
        self.processes = multiprocessing.cpu_count()

    def setProcesses(self, processes):
        self.processes = max(processes, multiprocessing.cpu_count())


    def play_pop(self, i):
        score_final = 0
        for _ in range(self.num_play):
            run = Game().run_AI(self.pop[i])
            score_final += run[0]/self.num_play
        print(f"NN {i}  ", end="\r")
        self.pop[i].score = score_final
        return self.pop[i]

    def play(self):

        pool = multiprocessing.Pool(processes=self.processes)
        self.pop = pool.map(self.play_pop, range(self.pop_size))
        pool.close()
        pool.join()

        """for i in range(self.pop_size):
            score_final = 0
            print(f"NN {i}", end="\r")
            for _ in range(self.num_play):
                run = Game().run_AI(self.pop[i])
                score_final += run[0]/self.num_play
            self.pop[i].score = score_final"""

    def run_once(self):
        run = Game().run_AI_dis(self.pop[0])
        print(f"SCORE : {run[1]}")

    def mutate(self, child):
        for i in range(len(child.weights)):
            for j in range(len(child.weights[i])):
                for k in range(len(child.weights[i][j])):
                    child.weights[i][j][k] = uniform(1-self.rate, 1+self.rate)*child.weights[i][j][k]
        for i in range(len(child.biases)):
            for j in range(len(child.biases[i])):
                child.biases[i][j] = uniform(1-self.rate, 1+self.rate)*child.biases[i][j]

    def create_child(self, _):
        couple = randint(0, self.num_select, 2)
        parent1 = self.pop[couple[0]]
        parent2 = self.pop[couple[1]]
        weight = uniform(0,1)
        child = NeuronalNetwork()
        child.weights[0] = (weight*parent1.weights[0] + (1-weight)*parent2.weights[0])
        child.biases[0] = (weight*parent1.biases[0] + (1-weight)*parent2.biases[0])
        child.weights[1] = (weight*parent1.weights[1] + (1-weight)*parent2.weights[1])
        child.biases[1] = (weight*parent1.biases[1] + (1-weight)*parent2.biases[1])
        child.weights[2] = (weight*parent1.weights[2] + (1-weight)*parent2.weights[2])
        child.biases[2] = (weight*parent1.biases[2] + (1-weight)*parent2.biases[2])
        self.mutate(child)
        return child
    
    def crossover(self):
        self.pop = sorted(self.pop, key=operator.attrgetter('score'), reverse=True)
        self.pop = self.pop[:self.num_select]

        pool = multiprocessing.Pool(processes=self.processes)
        self.pop = self.pop + pool.map(self.create_child, range(self.pop_size-self.num_select))
        pool.close()
        pool.join()

        """for _ in range(self.pop_size - self.num_select):
            couple = randint(0, self.num_select, 2)
            parent1 = self.pop[couple[0]]
            parent2 = self.pop[couple[1]]
            weight = uniform(0,1)
            child = NeuronalNetwork()
            child.weights[0] = (weight*parent1.weights[0] + (1-weight)*parent2.weights[0])
            child.biases[0] = (weight*parent1.biases[0] + (1-weight)*parent2.biases[0])
            child.weights[1] = (weight*parent1.weights[1] + (1-weight)*parent2.weights[1])
            child.biases[1] = (weight*parent1.biases[1] + (1-weight)*parent2.biases[1])
            child.weights[2] = (weight*parent1.weights[2] + (1-weight)*parent2.weights[2])
            child.biases[2] = (weight*parent1.biases[2] + (1-weight)*parent2.biases[2])
            self.mutate(child)
            self.pop.append(child)"""

    def avg(self):
        total = 0
        for NN in self.pop:
            total += NN.score
        return total/len(self.pop)

    def secondsToHoursAndMinutes(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return hours, minutes, seconds

    def save_session(self, graph_avg, graph_best, gen_num, plot=False):
        with open(f"session.txt", "w") as file:
            file.write(str(graph_avg)+"\n")
            file.write(str(graph_best)+"\n")
            file.write(str(gen_num)+"\n")
            file.write(str(int(plot))+"\n")
            file.write(str(self.pop_size)+"\n")
            file.write(str(self.num_select)+"\n")
            file.write(str(self.num_play)+"\n")
            file.write(str(self.rate)+"\n")
            file.write(str(self.id)+"\n")

    def restore_session(self):
        with open(f"session.txt", "r") as file:
            graph_avg = json.loads(file.readline())
            graph_best = json.loads(file.readline())
            gen_num = int(file.readline())
            plot = bool(int(file.readline()))

        self.pop = [NeuronalNetwork() for _ in range(self.num_select)]
        for i in range(self.num_select):
            data = np.load(f"snakes_{self.pop_size}_{self.id}/gen_{gen_num}/snake_{i}.npy", allow_pickle=True)
            self.pop[i].weights = data[0]
            self.pop[i].biases = data[1]
        self.crossover()

        return graph_avg, graph_best, gen_num + 1, plot


    def run(self, gen_num, plot=False, session=False):
        start = 0
        graph_avg = []
        graph_best = []
        if session:
            graph_avg, graph_best, start, plot = self.restore_session()
        times = []
        for i in range(start, gen_num):
            begin = time()
            self.play()
            average = self.avg()
            os.mkdir(f"snakes_{self.pop_size}_{self.id}/gen_{i}")
            for k in range(len(self.pop[:self.num_select])):
                self.pop[k].save(f"snakes_{self.pop_size}_{self.id}/gen_{i}/snake_{k}.npy")
            self.crossover()
            graph_avg.append(average)
            graph_best.append(self.pop[0].score)
            self.save_session(str(graph_avg), str(graph_best), str(i), plot)
            print(f"GENERATION {i} : avg = {average:.2f} ; best = {self.pop[0].score:.2f}")
            #self.run_once()
            end = time()
            print(f"Time : {int(end-begin)}s")
            times.append(int(end-begin))
            mean_time = sum(times)/len(times)
            print(f"Mean time : {int(mean_time)}s")
            hours, minutes, seconds = self.secondsToHoursAndMinutes(mean_time*(gen_num-i))
            print(f"Estimated time : {int(hours)}h {int(minutes)}m {int(seconds)}s")
        if plot:
            del self.pop
            X = np.linspace(0,len(graph_avg),len(graph_avg))
            plt.plot(X,graph_avg,'b')
            plt.plot(X,graph_best,'r')
            plt.savefig(f"./snakes_{self.pop_size}_{self.id}/graph.png")
