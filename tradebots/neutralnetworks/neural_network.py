"""
==========================================
TradeBots
Version: 0.0.1
Neural Network Module
==========================================

Authors: Connor Sanders
"""

import numpy as np
import tradebots.utils.math_utils as math_utils


class NeuralNetwork:

    def __init__(self, x, y):
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1], 2608)
        self.weights2 = np.random.rand(2608, 1)
        self.y = y
        self.output = np.zeros(y.shape)

    def feedforward(self):
        self.layer1 = math_utils.sigmoid(np.dot(self.input, self.weights1))
        self.output = math_utils.sigmoid(np.dot(self.layer1, self.weights2))

    def backprop(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) * math_utils.sigmoid_derivative(self.output)))
        d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * math_utils.sigmoid_derivative(self.output), self.weights2.T) * math_utils.sigmoid_derivative(self.layer1)))

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2


'''
if __name__ == "__main__":
    x = np.array([[0.2,0,1.2],
                  [0.2,1.1,1],
                  [1,0,1],
                  [1,1,1]])
    y = np.array([[0],[1],[1],[0]])
    nn = NeuralNetwork(x, y)

    print(nn.weights1)
    print(nn.weights2)
    for i in range(1500):
        nn.feedforward()
        nn.backprop()
    print(nn.output)
    print(nn.weights1)
    print(nn.weights2)
'''