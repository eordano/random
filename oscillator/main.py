from __future__ import division

import sys, os, math

import pygame

from scene import *
from rkbar import *
from leyend import *
from handler import *
import config

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(
        (config.screenWidth, config.screenHeight)
    )

    myScene = Scene(screen)
    bar = RKBar(config.initialConditions)

    dispAngle = Leyend((10,5), lambda x: "Angulo: %f"%bar.X[0])
    dispSpeed = Leyend((10,25), lambda x: "Velocidad angular: %f"%bar.X[1])
    dispE = Leyend((10,45), lambda x: "E = %f"%(bar.X[1]**2-2*config.gravity/config.length*math.cos(bar.X[0])))
    dispFrames = Leyend((10,85), lambda x: "Cuadros por segundo = %f"%(1000/x))
    dispStep = Leyend((10,105), lambda x: "Paso de integracion = %f"%(x/1000))
    dispInitial = Leyend((10,65), lambda x: "Valores iniciales: %f, %f"%(
        config.initialConditions[0],
        config.initialConditions[1]
    ))

    def keyHandler(key):
        if key == pygame.K_q:
            sys.exit()
        elif key == pygame.K_SPACE:
            myScene.setPause(not myScene.getPause())
        elif key == pygame.K_r:
            bar.reset(config.initialConditions)
        elif key == pygame.K_a:
            config.initialConditions[0] += 0.1
            dispInitial.update(0)
        elif key == pygame.K_z:
            config.initialConditions[0] -= 0.1
            dispInitial.update(0)
        else:
            pass
    myScene.addHandler('keyboard', Handler(keyHandler))

    myScene.addObject(bar)

    myScene.addObject(dispAngle)
    myScene.addObject(dispSpeed)
    myScene.addObject(dispE)
    myScene.addObject(dispFrames)
    myScene.addObject(dispStep)
    myScene.addObject(dispInitial)

    while True:
        myScene.loop()

