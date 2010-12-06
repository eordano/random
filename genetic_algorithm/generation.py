# -*- coding: utf-8 -*-
from random import random, choice
import config

class Generation:
	def __init__(self, kind, individuals=[]):
		self.kind = kind
		self.individuals = individuals
		if not self.individuals:
			self.individuals = self.spawn_random_individuals(config.gen_size)

	def spawn_new_gen(self, Debug = False):
		last_gen_fit = [(a.fitness(), a) for a in self.individuals]
		last_gen_fit.sort()
		new_gen = [a[1] for a in last_gen_fit[:config.elitism]]
		new_gen += self.spawn_weighted_babies(config.from_last_gen)
		new_gen += self.spawn_random_mutants(config.mutants)
		if Debug:
			print self.get_description()
		return Generation(self.kind, new_gen)

	def spawn_weighted_babies(self, amount):
		fitnesses = [[indiv.fitness(), indiv] for indiv in self.individuals]
		total_fitness = float(sum([pair[0] for pair in fitnesses]))
		acumm = -fitnesses[0][0]/total_fitness
		for trav in fitnesses:
			trav[0] = acumm = acumm + trav[0]/total_fitness

		def make_list(r, n):
			if not n: return []
			r += 1.0/amount
			r -= float(r >= 1)
			return [r] + make_list(r, n-1)

		chosen = make_list(random(), amount)
		mates = make_list(random(), amount)
		fitnesses.sort()

		def who(f):
			for t in fitnesses:
				if t[0] >= f:
					return t[1]
			return fitnesses[0][1]

		return [who(chosen[i]).mate(who(mates[i])) for i in xrange(amount)]

	def spawn_random_mutants(self, amount):
		return [choice(self.individuals).random_mutant() for i in xrange(amount)]

	def spawn_random_individuals(self, amount):
		return [self.kind.random_individual() for i in xrange(amount)]

	def get_description(self):
		ret = ""
		ret += '==============================================\n'
		ret += 'This generation is composed of:\n'
		for individual in self.individuals:
			ret += individual.get_description()
		ret += '==============================================\n'
		return ret

	def __str__(self):
		return "<Generation made of "+str(len(self.individuals))+" individuals of '"+self.kind.__name__+"'>"
