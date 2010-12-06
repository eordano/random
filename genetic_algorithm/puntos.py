# -*- coding: utf-8 -*-
import config

from individual import Individual
from random import randrange, random
from math import sqrt


def distance_sqrd(p1, p2):
	return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def average(p1, p2):
	return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

def inside_sqrd(pe, ce, radius_sqrd):
	return int(distance_sqrd(ce, pe) <= radius_sqrd)

def all_inside(pes, ce, radius_sqrd):
	return reduce(int.__mul__, [inside_sqrd(po, ce, radius_sqrd) for po in pes])


class Puntos(Individual):
	def __init__(self, conjunto=[]):
		self.conjunto = conjunto
	
	@classmethod
	def random_individual(cls):
		amount = config.points_per_individual
		randomly_generated = [(randrange(config.min_x, config.max_x),
			randrange(config.min_y, config.max_y)) for i in range(amount)]
		randomly_generated = list(set(randomly_generated))
		while len(randomly_generated) < amount:
			randomly_generated.append((randrange(config.min_x, config.max_x),
			randrange(config.min_y, config.max_y)))
			randomly_generated = list(set(randomly_generated))
		randomly_generated.sort()
		return Puntos(randomly_generated)
	
	def random_mutant(self):
		new_conj = []
		for i in self.conjunto:
			if random() > config.mutation_probability:
				if random() > config.mutation_mode_1:
					new_conj += [(randrange(config.min_x, config.max_x),
						randrange(config.min_y, config.max_y))]
				else:
					new_conj += [(i[0] + randrange(-2, 2), i[1] + randrange(-2, 2))]
			else:
				new_conj += [i]
		return Puntos(new_conj)
	
	def mate(self, friend):
		if len(friend.conjunto) != len(self.conjunto):
			raise RuntimeError
		new_conj = []
		for i in range(len(self.conjunto)):
			if random() > 0.5:
				new_conj += [self.conjunto[i]]
			else:
				new_conj += [friend.conjunto[i]]
		return Puntos(new_conj)

	def fitness(self):
		return (1+1/(self.get_circle()[0]/100)) ** (config.value_power/(1+self.get_choques()))

	def get_choques(self):
		choques = {}
		for a in self.conjunto:
			for b in self.conjunto:
				if b > a:
					try: choques[distance_sqrd(a, b)] += 1
					except KeyError: choques[distance_sqrd(a, b)] = 1
		return sum([choques[a] for a in choques if choques[a] > 1])

	def get_circle(self):
		record = (192379174, 0 , 0)
		d = self.conjunto
		for a in d:
			for b in d:
				if b == a:
					continue
				for c in d:
					if c == b or c == a:
						continue
					q = sqrt(distance_sqrd(a, b))
					w = sqrt(distance_sqrd(a, c))
					e = sqrt(distance_sqrd(b, c))
					div = ((q+w+e)*(-q+w+e)*(q-w+e)*(q+w-e))
					u = 2*(a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1]))
					if div == 0 or u == 0: # Aligned Points
						continue
					rad_sqrd = (q*w*e)**2/((q+w+e)*(-q+w+e)*(q-w+e)*(q+w-e))
					x = ((a[1]**2+a[0]**2)*(b[1]-c[1])+(b[1]**2+b[0]**2)*(c[1]-a[1])+(c[1]**2+c[0]**2)*(a[1]-b[1]))/u
					y = ((a[1]**2+a[0]**2)*(c[0]-b[0])+(b[1]**2+b[0]**2)*(a[0]-c[0])+(c[0]**2+c[1]**2)*(b[0]-a[0]))/u
					cond = True
					for t in d:
						if t != a and t != b and t != c:
							r = distance_sqrd(t, (x, y))
							if r > rad_sqrd:
								cond = False
					if cond:
						record = min(record, (sqrt(rad_sqrd), x, y))
		return record

	def get_description(self):
		return "\t"+str(self)+"\n"

	def __str__(self):
		return "<Puntos: "+str(self.conjunto)+">"
