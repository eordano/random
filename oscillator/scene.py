from __future__ import division

import pygame

import sys, os, math


class Scene:
    BLACK = (0,0,0)

    def __init__(self, screen, bgcolor=BLACK):
        self.handlers = []
        self.screen = screen
        self.bgcolor = bgcolor

        self.handlers = {}
        self.handlers['keyboard'] = []
        self.handlers['mouse'] = []

        self.objects = []

        self.pause = True
        self.clock = pygame.time.Clock()

        self.elapsed = 0

    def setPause(self, pause):
        self.clock.tick()
        self.pause = pause

    def getPause(self):
        return self.pause

    def loop(self):
        delta = self.clock.tick()
        self.elapsed += delta

        self.screen.fill(self.bgcolor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for handler in self.handlers['keyboard']:
                    handler.action(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for handler in self.handlers['mouse']:
                    handler.action(event)

        for object in self.objects:
            if not self.pause:
                object.update(delta)
            object.draw(self.screen)

        pygame.display.flip()

    def addHandler(self, type, handler):
        self.handlers[type] = self.handlers[type] or []
        self.handlers[type].append(handler)

    def addObject(self, object):
        self.objects.append(object)

