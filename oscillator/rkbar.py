from __future__ import division

import math

import pygame

import config


def averageVector(vector):
    weight = 0
    values = [0 for i in vector[0][1]]
    for element in vector:
        weight += element[0]
        for (i, value) in zip(xrange(len(element[1])), element[1]):
            values[i] += value*element[0]
    return [x/weight for x in values]

def vectorAdd(v1, v2):
    return [a+b for (a,b) in zip(v1,v2)]

def vectorScalarMultiply(v1, a):
    return [a*b for b in v1]

class RKBar:

    def __init__(self, initialConfig):
        self.reset(initialConfig)
        self.pivot = (config.screenWidth/2, config.screenHeight/2)

    def reset(self, configuration):
        self.X = [
            configuration[0],
            configuration[1],
        ]

    def update(self, t):
        def F(X):
            X1 = -config.gravity*math.sin(X[0]) / config.length
            X0 = X[1]
            return [X0, X1]
        t /= 1000
        K1 = vectorScalarMultiply(F(self.X), t)
        K2 = vectorScalarMultiply(
            F(vectorAdd(self.X, vectorScalarMultiply(K1, 0.5))), t)
        K3 = vectorScalarMultiply(
            F(vectorAdd(self.X, vectorScalarMultiply(K2, 0.5))), t)
        K4 = vectorScalarMultiply(F(
            vectorAdd(self.X, K3)), t)
        self.X = vectorAdd(self.X, averageVector(
            ((1, K1), (2, K2), (2, K3), (1, K4)))
        )

    def draw(self, screen):
        RED = (255, 0 , 0)
        endPoint = (
            self.pivot[0] + config.length * math.sin(self.X[0]),
            self.pivot[1] + config.length * math.cos(self.X[0]),
        )
        pygame.draw.line(screen, RED, self.pivot, endPoint, 3)


