import time
import random
import pygame
import math
import numpy
from pygame.locals import *
from random import randint
from network import neural_net, sigmoid
from Bird import *
import copy
from genetic import *

pygame.init()
display_width = 800
display_height = 600

# load all images
background = pygame.image.load('bg.png')
floor = pygame.image.load('base.png')
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('flappy game')
pipe = pygame.image.load('pipe.png')
flappy_model = pygame.image.load('bird-midflap.png')

gen = 0
maxScore = 0

def fitness(dist, birdMiddle, middle):
    x = (dist - abs(birdMiddle - middle))
    return int(x)

#collision detection
def collision(birdRightX,birdLeftX,birdBottomY,birdTopY,pipes,i,upperPipeLength):
    col = False

    if (birdRightX > pipes[i][0][0] and birdLeftX < pipes[i][1][0]+52 and (birdBottomY > pipes[i][0][1] or birdTopY < pipes[i][1][1]+upperPipeLength)) or (birdTopY <= 0 or birdTopY-24 >= 500):
        col = True
    return col


def main(birds):
    dist = 0
    score = 0
    pipes = []

    # physics
    gravity = 0.6
    upForce = 15
    velocity = 0

    # size of bird
    bird_width = 34
    bird_height = 24

    # pipe dimensions
    pipewidth = 52
    upperPipeLength = 320

    # create some start pipes
    x_pipe_pos = 550
    pipes.append(([x_pipe_pos,350],[x_pipe_pos,-100]))
    x_pipe_pos += 250

    for i in range(3):
        lowerPipeY = randint(200,400)
        upperPipeY = lowerPipeY - randint(410,450)

        pipes.append(([x_pipe_pos,lowerPipeY],[x_pipe_pos,upperPipeY]))
        x_pipe_pos += 250

    birdsCopy = copy.copy(birds)

    rotated = pygame.transform.rotate(pipe, 180)

    # game loop
    while True:
        dist += 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # if space is pressed down, fly up
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity -= upForce


        # draw background
        screen.blit(background,(0,0))

        for pippe in pipes:
            screen.blit(pipe, (pippe[0][0],pippe[0][1]))
            screen.blit(rotated, (pippe[1][0],pippe[1][1]))
            pippe[0][0] -= 4
            pippe[1][0] -= 4

        screen.blit(floor, (0,500))
        screen.blit(floor, (336, 500))
        screen.blit(floor, (336*2, 500))

        # spawning pipes
        if pipes[0][0][0] < -52:
            del pipes[0]
            lowerPipeY = randint(200,400)
            upperPipeY = lowerPipeY - randint(410,450)

            pipes.append(([pipes[len(pipes)-1][0][0]+250,lowerPipeY],[pipes[len(pipes)-1][0][0]+250,upperPipeY]))


        #collision detection and score handling for pipes
        if score > 0:

            if pipes[1][1][0]+40 > (birds[0].x-2) and pipes[1][1][0]+40 < (birds[0].x+3):
                score += 1

            middle = (pipes[1][0][1]+pipes[1][1][1]+320)/2

            for i, bird in enumerate(birds):
                distX = pipes[1][0][0]+(pipewidth/2)-bird.x+bird_width
                distY = middle-bird.y+(bird_height/2)
                bird.input = np.array([[distX],[distY],[bird.velocity]])

                bird.fitness = fitness(dist,bird.y+(bird_height/2),middle)
                screen.blit(flappy_model, (bird.x, bird.y))
                x = neural_net(bird.input, bird.w1, bird.w2,bird.b1,bird.b2)

                bird.velocity += gravity
                bird.y += bird.velocity

                if bird.velocity < -8:
                        bird.velocity = -8

                if bird.velocity > 10:
                    bird.velocity = 10

                if x > 0.5:
                    bird.velocity -= upForce
                col = collision(bird.x+bird_width,bird.x,bird.y+bird_height,bird.y,pipes,1,upperPipeLength)
                if col:
                    del birds[i]

        else:
            if pipes[0][1][0]+40 > (birds[0].x-2) and pipes[0][1][0]+40 < (birds[0].x+3):
                score += 1

            middle = (pipes[0][0][1]+pipes[0][1][1]+320)/2

            for i ,bird in enumerate(birds):
                distX = pipes[1][0][0]+(pipewidth/2)-bird.x+bird_width
                distY = middle-bird.y+(bird_height/2)
                bird.input = np.array([[distX],[distY],[bird.velocity]])

                bird.fitness = fitness(dist,bird.y+(bird_height/2),middle)
                screen.blit(flappy_model, (bird.x, bird.y))
                x = neural_net(bird.input, bird.w1, bird.w2,bird.b1,bird.b2)

                bird.velocity += gravity
                bird.y += bird.velocity

                if bird.velocity < -8:
                        bird.velocity = -8

                if bird.velocity > 10:
                    bird.velocity = 10

                if x > 0.5:
                    bird.velocity -= upForce
                col = collision(bird.x+bird_width,bird.x,bird.y+bird_height,bird.y,pipes,0,upperPipeLength)
                if col:
                    del birds[i]

        if not birds:
            # save top birds to file
            writeGen(birdsCopy)
            global maxScore

            if score > maxScore:
                maxScore = score

            global gen
            gen += 1

            newBirds = crossover(birdsCopy,gen)
            input_for_bird = np.array([[0],[0],[0]])
            for i in range(82):
                w1 = np.random.randn(hiddenLayer1size,len(input_for_bird)) * 0.01
                w2 = np.random.randn(outputLayer,hiddenLayer1size) * 0.01
                b1 = np.random.randn(hiddenLayer1size,1) * 0.01
                b2 = np.random.randn(1,1) * 0.01
                newBirds.append(Bird(input_for_bird,w1,w2,b1,b2,birdLeftX,birdTopY,velocity,0))

            main(newBirds)

        myFont = pygame.font.SysFont("Comic Sans MS", 40)
        # display generation
        genDisplay = myFont.render('generation:' + str(gen), 1, (255, 255, 255))
        screen.blit(genDisplay, (500, 530))

        fitDisplay = myFont.render('Nr Alive:' + str(len(birds)), 1, (255,255,255))
        screen.blit(fitDisplay, (20, 530))

        #display score
        myFont = pygame.font.SysFont("Comic Sans MS", 40)
        ### pass a string to myFont.render
        scoreDisplay = myFont.render("Score: "+str(score), 1, (255,255,255))
        maxScoreDisplay = myFont.render("Max score: "+str(maxScore), 1, (255,255,255))

        screen.blit(scoreDisplay, (30, 45))
        screen.blit(maxScoreDisplay, (30, 8))

        # update screen
        pygame.time.Clock().tick(144)
        pygame.display.update()


if __name__ == '__main__':

    # start position of bird
    birdTopY = 330
    birdLeftX = 250
    velocity = 0

    hiddenLayer1size = 16
    outputLayer = 1
    input_for_bird = np.array([[0],[0],[0]])

    birds = []
    for i in range(150):
        # randomized values for new birds
        w1 = np.random.randn(hiddenLayer1size,len(input_for_bird)) * 0.01
        w2 = np.random.randn(outputLayer,hiddenLayer1size) * 0.01
        b1 = np.random.randn(hiddenLayer1size,1) * 0.01
        b2 = np.random.randn(1,1) * 0.01
        birds.append(Bird(input_for_bird, w1, w2, b1 , b2,birdLeftX,birdTopY,velocity,0))

    main(birds)
