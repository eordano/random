#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyglet.window import Window, mouse, key
from pyglet.app import run, exit
from pyglet.clock import schedule_interval, unschedule
from pyglet.image import load
from pyglet.gl import glColor3f, glRectf, gl

class World(Window):
    """ The World! """

    def __init__(self, x=20, y=20, speed=1, wrap=False):
        super(World, self).__init__(500, 500)
        self.speed = speed
        self.wrap = wrap
        self.x = range(x)
        self.y = range(y)
        self.x_size = x
        self.y_size = y
        self.grid = [[0 for v in xrange(x)] for i in xrange(y)]
        self.alive_matrix = [[(0, 0) for v in xrange(x)] for i in xrange(y)]
        self.__running = False

    def start(self):
        if self.__running:
            unschedule(self.update)
            self.__running = False
        else:
            schedule_interval(self.update, self.speed)
            self.__running = True

    def set_alive(self, x, y, state):
        if self.__running:
            raise Exception("The Game is running!")
        elif state:
            self.grid[y][x] = 1
        else:
            self.grid[y][x] = 0

    def __query_neighbours(self, x, y):
        alive = 0
        for v, w in [(a, b) for b in xrange(y - 1, y + 2) for a in \
                xrange(x - 1, x + 2) if (a, b) != (x, y)]:
            if self.wrap:
                w %= self.y_size
                v %= self.x_size
            elif w == self.y_size or v == self.x_size or w < 0 or v < 0:
                alive += 1
            if self.grid[w][v] == 1:
                alive += 1
        return alive

    def evolve(self):
#       Generate Alive Matrix
        for x, y in ((a, b) for b in self.y for a in self.x):
            alive_count = self.__query_neighbours(x, y)
            cell_status = self.grid[y][x]
            self.alive_matrix[y][x] = (cell_status, alive_count)

        for x, y in ((a, b) for b in self.y for a in self.x):
            cell, alive = self.alive_matrix[y][x]
            if (cell == 0 and alive == 3) or (cell == 1 and alive in (2, 3)):
                self.grid[y][x] = 1
            else:
                self.grid[y][x] = 0

    def update(self, dt):
        self.evolve()

    def on_key_press(self, k, modifiers):
        if key.SPACE == k:
            self.start()
        elif key.ESCAPE == k:
            exit()

    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT and self.__running == False:
            idx_x = int((self.x_size/500.0)*x)
            idx_y = int((self.y_size/500.0)*y)
            state = self.grid[idx_y][idx_x]
            if state:
                state = False
            else:
                state = True
            self.set_alive(idx_x, idx_y, state)

    def on_draw(self):
        self.clear()
        for x, y in ((a, b) for b in self.y for a in self.x):
            if self.grid[y][x] == 1:
                win_x_unit = 500/self.x_size
                win_y_unit = 500/self.y_size
                glColor3f(1, 1, 1)
                x1 = win_x_unit * x
                x2 = win_x_unit * (x + 1)
                y1 = win_y_unit * y
                y2 = win_y_unit * (y + 1)
                glRectf(x1, y1, x2, y2)

if __name__ == '__main__':
    world = World(15, 15, 1, True)
    run()
