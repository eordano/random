# -*- coding: utf-8 -*-
import pygame
import sys
from math import tan, sqrt, log, sin, cos, pi, atan

def getvel(x, y, angle, v0, l):
    w = v0/(l*sin(angle)) if angle else 0
    return (v0-w*y, w*(x-l*cos(angle))) 

def modulo(vector):
    return sqrt(vector[0]**2 + vector[1]**2)

def choose(vector):
    if modulo(vector) == 0:
        return (0,0,0)
    else:
        return (0, abs(int(255*vector[0]/modulo(vector))), abs(int(255*vector[1]/modulo(vector))))

def scale(modulo):
    return modulo

def p2s(point):
    ''' Point to Screen point '''
    return (30+point[0], 400-point[1])

def s2p(point):
    ''' Screen point to coordinate point '''
    return (point[0]-30, 400-point[1])

def closest(p1, p2, p3):
    if (p2[0]-p1[0])**2+(p2[1]-p1[1])**2 == 0:
        return (0,0) # This shouldn't happen: means that p1 == p2 (bar length = 0)
    u = ((p3[0]-p1[0])*(p2[0]-p1[0])+(p3[1]-p1[1])*(p2[1]-p1[1]))/((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
    return (p1[0]+u*(p2[0]-p1[0]), p1[1]+u*(p2[1]-p1[1]))

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 17)
    l = 400
    theta = pi/4
    v0 = 15
    play = False
    clock = pygame.time.Clock()
    sumticks = 0
    Qstate = True

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    play = True
                    clock.tick()
                    sumticks = 0
                if event.key == pygame.K_KP_PLUS or event.key == pygame.K_RIGHTBRACKET:
                    v0 += 1
                if event.key == pygame.K_KP_MINUS or event.key == pygame.K_LEFTBRACKET:
                    v0 -= 1
                if event.key == pygame.K_KP_MULTIPLY or event.key == pygame.K_COMMA:
                    theta += pi/24
                if event.key == pygame.K_KP_DIVIDE or event.key == pygame.K_PERIOD:
                    theta -= pi/24
                if event.key == pygame.K_r:
                    theta = pi/4
                    play = False
                if event.key == pygame.K_SPACE:
                    play = False if play else True
                if event.key == pygame.K_q:
                    Qstate = False if Qstate else True
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        if play:
            sumticks += clock.tick()
            if sumticks > 100:
                theta -= 0.01
                sumticks = 0
                if theta <= 0:
                    play = False
                    theta = 0

        screen.fill((0,0,0))

        # Axis
        pygame.draw.aaline(screen, (255,255,255), (30, 0), (30, 460))
        pygame.draw.aaline(screen, (255,255,255), (0, 400), (640, 400))

        # Some text
        text_vel = font.render('Velocidad = %d'%v0, True, (255,255,255), (0,0,0))
        text_theta = font.render('Angulo = %f'%theta, True, (255,255,255), (0,0,0))
        screen.blit(text_vel, (200, 0))
        screen.blit(text_theta, (200, 15))

        if Qstate:
            # In the "Q State", we draw speed lines for each value of x in the bar (cheap effect)
            # Q state is named after the key that activates this mode. Chosen by the Qwerty inventor
            x = int(l*cos(theta))
            for i in range(x):
                inicial = (i, l*sin(theta)-i*tan(theta))
                v = getvel(inicial[0], inicial[1], theta, v0, l)
                m = modulo(v)
                # Can also choose color = (0,255,i*255/x)
                color = choose(v)
                escala = scale(m)
                pygame.draw.aaline(screen, color, p2s(inicial), p2s((inicial[0]+v[0]*escala, inicial[1]+v[1]*escala)))
    
        punto = closest( (0, l*sin(theta)), (l*cos(theta), 0) , s2p(pygame.mouse.get_pos()) )
        v = getvel( punto[0], l*sin(theta)-punto[0]*tan(theta), theta, v0, l )
        m = modulo(v)
        color = (255,255,255)
        escala = scale(m)
        pygame.draw.line(screen, color, p2s(punto), p2s((punto[0]+v[0]*escala, punto[1]+v[1]*escala)), 3)
        text_current = font.render('Velocidad en el punto seleccionado = %f con un ángulo %f'%(m,atan(v[1]/v[0])), True, (255,255,255), (0,0,0))
        screen.blit(text_current, (200, 30))
        pygame.draw.aaline(screen, (255,0,0), p2s((0, l*sin(theta))), p2s((l*cos(theta), 0)), 10)

        pygame.display.flip()

