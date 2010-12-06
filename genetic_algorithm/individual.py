# -*- coding: utf-8 -*-
class Individual:
	def __init__(self):
		raise NotImplementedError
	
	@classmethod
	def random_individual(cls):
		raise NotImplementedError
	
	def random_mutant(self):
		raise NotImplementedError
	
	def mate(self, friend):
		raise NotImplementedError
	
	def fitness(self):
		raise NotImplementedError
	
	def get_description(self):
		raise NotImplementedError