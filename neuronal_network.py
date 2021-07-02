import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class NeuronalNetwork():

    def __init__(self):
        # entrée : map (20*20 cases)
        # 1ère couche : 5 neurones
        # 2e couche : 10 neurones
        # sortie : 4 neurones

        self.weights = []
        self.biases = []
        self.weights.append(np.random.rand(20 * 20, 5))
        self.biases.append(np.random.rand(5))
        self.weights.append(np.random.rand(5, 10))
        self.biases.append(np.random.rand(10))
        self.weights.append(np.random.rand(10, 4))
        self.biases.append(np.random.rand(4))

    def choose(self, a):

        layer1 = sigmoid(np.dot(a, self.weights[0]) + self.biases[0])
        layer2 = sigmoid(np.dot(layer1, self.weights[1]) + self.biases[1])
        output = sigmoid(np.dot(layer2, self.weights[2]) + self.biases[2])
        return output

