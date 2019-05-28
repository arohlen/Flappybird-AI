import numpy as np

class Bird():

	def __init__(self, input,w1,w2,b1,b2, x, y, velocity,fitness):

		self.input = input*0.01
		self.w1 = w1
		self.w2 = w2
		self.b1 = b1
		self.b2 = b2
		self.x = x
		self.y = y
		self.velocity = velocity
		self.fitness = fitness
		self.probability = 0

	def __lt__(self,bird):

		return self.fitness > bird.fitness
