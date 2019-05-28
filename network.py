import math
import random
import numpy as np


saved_data = []

# neural network
def neural_net(input,w1,w2,b1,b2):

    z1 = sigmoid(np.add(np.matmul(w1,input),b1))

    z2 = sigmoid(np.add(np.matmul(w2,z1),b2))
    return z2[0,0]

# sigmoid function
def sigmoid(x):
    return  1/(1 + math.e**(-x))
