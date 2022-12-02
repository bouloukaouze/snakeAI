import numpy as np
from numpy.random import uniform


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class NeuronalNetwork():

    def __init__(self):
        # données : distance tête-pomme (x,y)

         
        #  0 0 0 0 0 0 0 0 0
        #  0 0 0 0 0 0 0 0 0
        #  0 0 0 0 0 0 0 0 0
        #  0 0 0 0 0 0 0 0 0
        #  0 0 0 0 T 0 0 0 0 
        #  0 0 0 0 | 0 0 0 0
        #  0 0 0 0 | 0 0 0 0
        #  0 0 0 0 | 0 0 0 0
        #  0 0 0 0 | 0 0 0 0                

        # 82 inputs


        self.weights = []
        self.biases = []
        self.weights.append(uniform(-50,50,(56, 82)))
        self.biases.append(uniform(-50, 50, 56))
        self.weights.append(uniform(-50,50,(23, 56)))
        self.biases.append(uniform(-50, 50, 23))
        self.weights.append(uniform(-50, 50, (4, 23)))
        self.biases.append(uniform(-50, 50, 4))

        self.score = 0

    def choose(self, map):

        input_nn = [map.reward[0]-map.snake.head[0], map.reward[1]-map.snake.head[1]] 

        for i in range(-4,5):
            for j in range(-4,5):
                if (i!=0 or j!=0):
                    try:
                        if map.map[map.snake.head[0]+i][map.snake.head[1]+j] > 0:
                            input_nn.append(1)
                        elif map.map[map.snake.head[0]+i][map.snake.head[1]+j] < 0:
                            input_nn.append(-1)
                        else:
                            input_nn.append(0)
                    except:
                        input_nn.append(1)
        af = lambda x: np.tanh(x.astype(float))
        layer1 = af(np.dot(self.weights[0], input_nn) + self.biases[0])
        layer2 = af(np.dot(self.weights[1], layer1) + self.biases[1])
        output = (sigmoid(np.dot(self.weights[2], layer2) + self.biases[2])).tolist()
        return output.index(max(output))
    
    def save(self, name):
        np.save(name,  np.asarray([self.weights, self.biases], dtype=object))

