import random
import numpy as np
from Bird import *

def writeGen(birds):

	birds.sort()

	with open ('birds.txt','w') as file:
		for bird in birds:
			file.write(str(bird.w1)+'@')
			file.write(str(bird.w2)+'%')
			file.write(str(bird.b1)+'&')
			file.write(str(bird.b2)+'$')
			file.write(str(bird.fitness))
			file.write('#\n')

def mutation(newBirds):

	chance = 0.98

	for bird in newBirds:
		for i in range(len(bird.w1)):
			rand = random.random()
			if rand >= chance:
				bird.w1[i] = np.random.randn(1,3)*0.01

		for i in range(len(bird.w2)):
			rand = random.random()
			if rand >= chance:
				bird.w2[i] = np.random.randn()*0.01

		for i in range(len(bird.b1)):
			rand = random.random()
			if rand >= chance:
				bird.b1[i] = np.random.randn(1,1)*0.01

		rand = random.random()
		if rand >= chance:
			bird.b2 = np.random.randn(1,1)*0.01


def crossover(birds,generation):

	birdTopY = 330
	birdLeftX = 250
	velocity = 0

	birds.sort()
	newBirds = []
	nrBirds = 20

	totalFitness = 0

	geneBirds = []


	birds = birds[:nrBirds]
	newBirds += birds

	mutation(newBirds)

	for bird in birds:
		totalFitness += bird.fitness

	for bird in birds:
		chance = bird.fitness/totalFitness
		nrBird = round(chance*100)
		for i in range(nrBird):
			geneBirds.append(bird)


	# crossover magic
	for i in range(60):
		bird1 = random.randint(0,len(geneBirds)-1)
		bird2 = random.randint(0,len(birds)-1)
		bird1w1 = np.split(geneBirds[bird1].w1,2)[0]
		bird2w1 = np.split(birds[bird2].w1,2)[1]

		bird1 = random.randint(0,len(geneBirds)-1)
		bird2 = random.randint(0,len(birds)-1)
		split = int(len(geneBirds[bird1].w2[0])/2)
		bird1w2 = geneBirds[bird1].w2[0][:split]
		bird2w2 = birds[bird2].w2[0][split:]


		bird1 = random.randint(0,len(geneBirds)-1)
		bird2 = random.randint(0,len(birds)-1)
		bird1b1 = np.split(geneBirds[bird1].b1,2)[0]
		bird2b1 = np.split(birds[bird2].b1,2)[1]

		indexes = random.sample(range(nrBirds), 2)
		randomBird = random.randint(0,1)

		b2 = birds[indexes[randomBird]].b2
		w1 = np.concatenate((bird1w1,bird2w1), axis=0)
		w2 = np.concatenate(([bird1w2],[bird2w2]), axis = 1)
		b1 = np.concatenate((bird1w1,bird2w1), axis=0)
		input = np.array([[0],[0],[0]])

		newBirds.append(Bird(input,w1,w2,b1,b2,birdLeftX,birdTopY,velocity,0))

	return newBirds
